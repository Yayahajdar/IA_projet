
import os
import requests
from dotenv import load_dotenv
from qr import fetch_and_decode_qr_cv2
from con import Session , engine
from database import Invoice, Item, Customer


def add_invoice_data( invoice_data , image_url):
    # Check for existing customer by number (assuming customer_number is a unique identifier for each customer)
    session = Session()
    qr_data = fetch_and_decode_qr_cv2(image_url)
    if qr_data is not None:
        customer_number = qr_data.get('CUST', 'N/A')
        category = qr_data.get('CAT', 'N/A')
    else:
        print("No QR code data was found.")
        customer_number = 'N/A' 
        category =  'N/A'
    
    

    customer = session.query(Customer).filter_by(customer_number=customer_number).first()
    if not customer:
        customer = Customer(
            customer_number=customer_number,
            customer_name=invoice_data['Customer Name'],  # Assuming the model has a 'name' field
            address=invoice_data['Billing Address'],
            category=category
        )
        session.add(customer)
    else:
        # Update existing customer info if necessary
        customer.name = invoice_data['Customer Name']
        customer.address = invoice_data['Billing Address']
        customer.category = category

    # Check if the invoice already exists
    invoice = session.query(Invoice).filter_by(invoice_number=invoice_data['Invoice ID']).first()
    if invoice:
        # If the invoice already exists, raise an error or handle as needed
        raise ValueError(f"Invoice with ID {invoice_data['Invoice ID']} already exists.")
    
    # Since invoice does not exist, create a new one
    invoice = Invoice(
        invoice_number=invoice_data['Invoice ID'],
        date=invoice_data['Invoice Date'],
        total=invoice_data['Invoice Total'],
        customer=customer
    )
    session.add(invoice)

    # Add items
    for item_data in invoice_data['Items']:
        # Consider how to handle potential duplicate items. For now, adding new items each time.
        item = Item(
            description=item_data['Description'],
            amount=item_data['Amount'],
            quantity=item_data['Quantity'],
            invoice=invoice
        )
        session.add(item)

    # Commit all changes to the database
    session.commit()
    print("Invoice and items added successfully.")