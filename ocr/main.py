from fastapi import FastAPI, HTTPException, Form, Request , Depends , Query
from sqlalchemy import or_ , func
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse , RedirectResponse 
from pydantic import BaseModel
from sqlalchemy.orm import Session
from con import SessionLocal, engine , get_db
from dotenv import load_dotenv
import os
from datetime import datetime
from qr import fetch_and_decode_qr_cv2
from last_invo import get_latest_invoice_data
from add_database import add_invoice_data 
from statistc import perform_statistical_analysis , create_status_codes_plot
from fin import extract_invoice_data_from_image
from get_dat import get_data_as_dataframe
import plotly.graph_objs as go
from database import Invoice, Item, Customer , RequestLog
from sqlalchemy.orm import selectinload 
from search import search_invoices ,get_invoice_details , search_by_date
from double import azure_form_recognizer_invoice_url




load_dotenv()

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


class ImageURL(BaseModel):
    url: str

@app.get("/")
async def form_post(request: Request):
    return templates.TemplateResponse('form.html', context={'request': request})

@app.post("/")
async def form_post(request: Request, query: str = Form()):
    # Redirect to the search results page
    return RedirectResponse(url=f"/search/?query={query}")

@app.get("/search/", response_class=HTMLResponse)
async def search(request: Request, query: str, db: Session = Depends(get_db)):
    try:
        # Perform search logic
        invoices = search_invoices(db, query)
        
        # Render template with search results
        return templates.TemplateResponse("search_results.html", {"request": request, "invoices": invoices})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
@app.get("/invoice/{invoice_id}", response_class=HTMLResponse)
async def invoice_details(request: Request, invoice_id: int, db: Session = Depends(get_db)):
    try:
        # Retrieve invoice details from the database
        invoice = get_invoice_details(db, invoice_id)

        # Render template with invoice details
        return templates.TemplateResponse("invoice_details.html", {"request": request, "invoice": invoice})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/search/by-date/")
async def search_by_date_route(request: Request,start_date: str = Query(None), end_date: str = Query(None), db: Session = Depends(get_db)):
    try:
        
        invoices = search_by_date(db, start_date, end_date)
        return templates.TemplateResponse("search_results.html", {"request": request, "invoices": invoices})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

import logging

@app.post("/submit-image/")
async def submit_image(request: Request, image_url: str = Form()):
    try:
        fr_endpoint = os.getenv("fr_endpoint")
        fr_key = os.getenv("fr_key")
        subscription_key = os.getenv("VISION_KEY")
        endpoint = os.getenv("VISION_ENDPOINT")
        if not fr_endpoint or not fr_key:
            raise HTTPException(status_code=500, detail="Azure Form Recognizer credentials are not set.")

        # Process the image and store results
        invoice_data = azure_form_recognizer_invoice_url(image_url, fr_endpoint, fr_key, endpoint, subscription_key)
        qr_data = fetch_and_decode_qr_cv2(image_url)
        if qr_data is not None:
            customer_number = qr_data.get('CUST', 'N/A')
            category = qr_data.get('CAT', 'N/A')
        else:
             print("No QR code data was found.")
             customer_number = 'N/A' 
             category =  'N/A'
        
        # Assuming add_invoice_data is a function you have for storing the results
        # add_invoice_data(invoice_data, image_url)
        return templates.TemplateResponse("results_page.html", {"request": request, "image_url":image_url , "customer_number": customer_number , "category" : category , "invoice_data": invoice_data})
    except Exception as e:
        logging.error(f"Error processing image: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing image: {e}")



@app.get("/statistics/", response_class=HTMLResponse)
async def get_statistics(request: Request):
    try:
        df = get_data_as_dataframe()
        descriptive_stats, correlation_matrix, customer_analysis, category_analysis, category_sales, item_analysis , yearly_sales_encoded = perform_statistical_analysis(df)
        
        return templates.TemplateResponse("statistics.html", {
            "request": request,
            "descriptive_stats": descriptive_stats,
            "correlation_matrix": correlation_matrix,
            "customer_analysis": customer_analysis,
            "category_analysis": category_analysis,
            "category_sales": category_sales,
            "yearly_sales_encoded": yearly_sales_encoded,
            "item_analysis": item_analysis
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.middleware("http")
async def log_requests(request, call_next):
    start_time = datetime.utcnow()
    response = await call_next(request)
    end_time = datetime.utcnow()

    # Log request to database
    db = SessionLocal()
    request_log = RequestLog(
        timestamp=start_time,
        method=request.method,
        path=request.url.path,
        status_code=response.status_code
    )
    db.add(request_log)
    db.commit()
    db.close()

    return response



@app.get("/status_codes")
async def get_requests_by_status_code(request: Request, db: Session = Depends(get_db)):
    status_counts = db.query(RequestLog.status_code, func.count(RequestLog.status_code)).group_by(RequestLog.status_code).all()
    
    img_base64 = create_status_codes_plot(status_counts)

    return templates.TemplateResponse("status_codes.html", {"request": request, "img_base64": img_base64})