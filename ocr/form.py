
import os
import requests
from dotenv import load_dotenv
from forma import azure_form_recognizer_invoice_url
from add_database import add_invoice_data
from fin import extract_invoice_data_from_image


load_dotenv()

# Authenticate
subscription_key = os.getenv("VISION_KEY")
endpoint = os.getenv("VISION_ENDPOINT")

image_url = "https://invoiceocrp3.azurewebsites.net/static/FAC_2019_0996-2430974.png"

# Call the function and get the data
invoice_data = extract_invoice_data_from_image(image_url, endpoint, subscription_key)

# add information to data base 
add_invoice_data(invoice_data , image_url)



# print (invoice)


# print(f"Vendor Name: {invoice['Vendor Name']}")
# print(f"Customer Name: {invoice['Customer Name']}")
# print(f"Billing Address: {invoice['Billing Address']}")
# print(f"Invoice ID: {invoice['Invoice ID']}")
# print(f"Invoice Date: {invoice['Invoice Date']}")
# print(f"Invoice Total: {invoice['Invoice Total']}")
# print("\nItems:")
# for item in invoice['Items']:
#         print(f"  Description: {item['Description']}")
#         print(f"  Amount: {item['Amount']}")
#         print(f"  Quantity: {item['Quantity']}\n")
        
        
# qr_data = fetch_and_decode_qr_cv2(image_url)
# customer_number = qr_data.get('CUST', 'N/A')
# category = qr_data.get('CAT', 'N/A')
# print(f"Customer Number: {customer_number}")
# print(f"Category: {category}")




# def add_invoice_data(invoice_data):
#     session = Session()
#     # Check for existing customer by number (assuming customer_number is a unique identifier for each customer)
#     qr_data = fetch_and_decode_qr_cv2(image_url)
#     customer = session.query(Customer).filter_by(customer_number=qr_data.get('CUST', 'N/A')).first()
#     if not customer:
#         customer = Customer(
#             customer_number=qr_data.get('CUST', 'N/A'),
#             customer_name=invoice_data['Customer Name'],
#             address=invoice_data['Billing Address'],
#             category=qr_data.get('CAT', 'N/A')
#         )
#         session.add(customer)
#     else:
#         # Update existing customer info if necessary
#         customer.customer_name = invoice_data['Customer Name']
#         customer.address = invoice_data['Billing Address']
#         customer.category = qr_data.get('CAT', 'N/A')
    
#     # Add or update invoice
#     invoice = session.query(Invoice).filter_by(invoice_number=invoice_data['Invoice ID']).first()
#     if not invoice:
#         invoice = Invoice(
#             invoice_number=invoice_data['Invoice ID'],
#             date=invoice_data['Invoice Date'],
#             total=invoice_data['Invoice Total'],
#             customer=customer
#         )
#         session.add(invoice)
#     else:
#         # Assuming you want to update existing invoices
#         invoice.date = invoice_data['Invoice Date']
#         invoice.total = invoice_data['Invoice Total']
    
#     # Add items
#     for item_data in invoice_data['Items']:
#         # Here you might want to consider how to handle duplicate items. For simplicity, we're adding new items each time.
#         item = Item(
#             description=item_data['Description'],
#             amount=item_data['Amount'],
#             quantity=item_data['Quantity'],
#             invoice=invoice
#         )
#         session.add(item)

#     session.commit()
#     print("Invoice and items added successfully.")







