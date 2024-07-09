# search_logic.py

from sqlalchemy.orm import Session
from  database import Customer, Invoice
from fastapi import HTTPException , Query
from sqlalchemy import or_ , and_
 

def search_invoices(db: Session, query: str):
    # Split the query into separate first name and last name components
    query_parts = query.split()

    # Search for invoices based on customer number, first name, last name, or invoice number
    return (
        db.query(Invoice)
        .join(Customer)
        .filter(
            or_(
                Customer.customer_number == query,
                Customer.customer_name.ilike(f"%{query}%"),
                Invoice.invoice_number.ilike(f"%{query}%"),
                # Check if first name or last name matches any part of the query
                or_(
                    Customer.customer_name.ilike(f"%{query_part}%")
                    for query_part in query_parts
                )
            )
        )
        .all()
    )
 
 
 
 
 
 
def search_by_date(db: Session, start_date: str = Query(None), end_date: str = Query(None)):
    try:
        if start_date and end_date:
            # Search by date range
            invoices = db.query(Invoice).filter(
                and_(Invoice.date >= start_date, Invoice.date <= end_date)
            ).all()
        elif start_date:
            # Search by start date only
            invoices = db.query(Invoice).filter(Invoice.date >= start_date).all()
        else:
            raise HTTPException(status_code=400, detail="At least one date parameter is required.")
        
        return invoices
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
 
 
 
 
 
 
def get_invoice_details(db: Session, invoice_id: int):
    # Retrieve invoice details from the database
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice