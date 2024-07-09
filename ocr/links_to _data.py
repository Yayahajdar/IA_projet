import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
from dotenv import load_dotenv
from add_database import add_invoice_data  
from fin import extract_invoice_data_from_image

# Load environment variables
load_dotenv()

# Azure Form Recognizer credentials
subscription_key = os.getenv("VISION_KEY")
endpoint = os.getenv("VISION_ENDPOINT")


# Fetch all invoice image links from the webpage
main_url = "https://invoiceocrp3.azurewebsites.net/invoices?start_date=2023-04-07"
response = requests.get(main_url)
soup = BeautifulSoup(response.text, 'html.parser')
links = soup.find_all('a')

def process_invoice_image(image_url):
    """Process an invoice image URL through Azure Form Recognizer and add data to the database."""
    invoice_data = extract_invoice_data_from_image(image_url, endpoint, subscription_key)
    add_invoice_data(invoice_data, image_url)

for link in links:
    href = link.get('href')
    if href:        
        absolute_url = urljoin(main_url, href)
        # Assuming that the absolute_url is the direct link to the image
        # Validate or filter URLs if necessary
        process_invoice_image(absolute_url)


# import requests
# from bs4 import BeautifulSoup
# from database import Base, Customer, Invoice, Item  # Assuming your SQLAlchemy setup is in a separate module
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy import create_engine
# from con import engine
# from urllib.parse import urljoin
# import requests
# from bs4 import BeautifulSoup
# from urllib.parse import urljoin
# import os
# from dotenv import load_dotenv
# from add_database import add_invoice_data  
# from fin import extract_invoice_data_from_image
# load_dotenv()

# # Azure Form Recognizer credentials
# subscription_key = os.getenv("VISION_KEY")
# endpoint = os.getenv("VISION_ENDPOINT") 

# # Create the engine and session
# Base.metadata.create_all(engine)
# Session = sessionmaker(bind=engine)
# session = Session()

# # Fetch all invoice image links from the webpage
# main_url = "https://invoiceocrp3.azurewebsites.net/invoices?start_date=2019-01-01"
# response = requests.get(main_url)
# soup = BeautifulSoup(response.text, 'html.parser')
# lines = soup.find_all('a')

# # Loop through the lines and extract the invoice number and image link
# for line in lines:
#     line_text = line.get_text().strip()
#     invoice_number = line_text.split()[0]  # Extract the invoice number from the beginning of each line
#     # Check if the line contains an <a> tag
#     for link in lines:
#         href = link.get('href')
#     if href:        
#         absolute_url = urljoin(main_url, href)
#         invoice = session.query(Invoice).filter_by(invoice_number=invoice_number).first()
#         if invoice:
#           print(f"Invoice number {invoice_number} not found in the database. Skipping...")  
#         else:
#           image_link = absolute_url 
#           invoice_data = extract_invoice_data_from_image(absolute_url, endpoint, subscription_key)
#           add_invoice_data(invoice_data, absolute_url)
#           session.commit()
#     else:
#         print("No link found in the line. Skipping...")



# import requests
# from bs4 import BeautifulSoup
# from database import Base, Customer, Invoice, Item  # Assuming your SQLAlchemy setup is in a separate module
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy import create_engine
# from con import engine
# from urllib.parse import urljoin

# # Create the engine and session
# Base.metadata.create_all(engine)
# Session = sessionmaker(bind=engine)
# session = Session()

# # Fetch all invoice image links from the webpage
# main_url = "https://invoiceocrp3.azurewebsites.net/invoices?start_date=2023-01-01"
# response = requests.get(main_url)
# soup = BeautifulSoup(response.text, 'html.parser')
# lines = soup.find_all('a')

# # Loop through the lines and extract the invoice number and image link
# for line in lines:
#     line_text = line.get_text().strip()
#     invoice_number = line_text.split()[0]  # Extract the invoice number from the beginning of each line
#     # Check if the line contains an <a> tag
#     for link in lines:
#         href = link.get('href')
#     if href:        
#         absolute_url = urljoin(main_url, href)
#         invoice = session.query(Invoice).filter_by(invoice_number=invoice_number).first()
#         if invoice:
#             # Update the invoice with the image link
#             invoice.image_link = absolute_url
#             session.commit()
#         else:
#             print(f"Invoice number {invoice_number} not found in the database. Skipping...")
#     else:
#         print("No link found in the line. Skipping...")






