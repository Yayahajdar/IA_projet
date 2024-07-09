import os
import time
import requests
from azure.ai.formrecognizer import FormRecognizerClient
from azure.core.credentials import AzureKeyCredential
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials

# Helper function to perform OCR and extract text lines and their bounding boxes
def perform_ocr_and_extract_text(computervision_client, image_url):
    ocr_output = []
    read_response = computervision_client.read(image_url, raw=True)
    read_operation_location = read_response.headers["Operation-Location"]
    operation_id = read_operation_location.split("/")[-1]

    # Polling for the result
    while True:
        read_result = computervision_client.get_read_result(operation_id)
        if read_result.status not in ['notStarted', 'running']:
            break
        time.sleep(1)
    
    if read_result.status == OperationStatusCodes.succeeded:
        for text_result in read_result.analyze_result.read_results:
            for line in text_result.lines:
                ocr_output.append((line.text, line.bounding_box))
    return ocr_output

# Function to extract invoice number from OCR data
def extract_invoice_number(ocr_data):
    for text, _ in ocr_data:
        if "invoice" in text.lower():
            parts = text.split()
            if parts:
                return parts[-1]
    return None

# Function to extract issue date from OCR data
def extract_issue_date(ocr_data):
    for text, _ in ocr_data:
        if "issue date" in text.lower():
            return text.split(' ', 2)[-1]
    return None

# Function to extract billing address from OCR data
def extract_bill_to(ocr_data):
    for text, _ in ocr_data:
        if "bill to" in text.lower():
            return text.split(' ', 2)[-1]
    return None

def extract_address(lines):
    for line in lines:
        
          if line[0].lower().startswith("address"):
            address_index = lines.index(line)
            break
    if address_index is not None:
      
        address = lines[address_index][0] + ", " + lines[address_index + 1][0]
        return address.replace("Address ", "")
    return "Address not found"

import re

def parse_combined_quantity_and_price(text):
    match = re.search(r'(\d+)\s*[×x]\s*(\d+(\.\d+)?)( Euro)?', text)
    if match:
        quantity = int(match.group(1))
        unit_price = float(match.group(2))
        return quantity, unit_price
    return None, None

# Function to extract total amount from OCR data
def extract_total(ocr_data):
    total_index = None
    for index, (text, _) in enumerate(ocr_data):
        if "TOTAL" in text:
            total_index = index + 1   
            break
    if total_index and total_index < len(ocr_data):
        return ocr_data[total_index][0]
    return None

# Main function to process the invoice using Azure Form Recognizer and OCR
def azure_form_recognizer_invoice_url(image_url, fr_endpoint, fr_key, endpoint, subscription_key):
    form_recognizer_client = FormRecognizerClient(fr_endpoint, AzureKeyCredential(fr_key))
    computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

    # Step 1: Use Azure Form Recognizer to analyze the invoice
    invoice_poller = form_recognizer_client.begin_recognize_invoices_from_url(image_url)
    invoices = invoice_poller.result()

    # Step 2: Use OCR as a fallback to extract additional details
    ocr_output = perform_ocr_and_extract_text(computervision_client, image_url)
    # barcode_data = fetch_and_decode_qr_cv2(image_url)
    
    
    # Prepare the consolidated invoice details dictionary
    invoice_details = {
        "Customer Name" : extract_bill_to(ocr_output),
        "Invoice ID": extract_invoice_number(ocr_output),
        "Invoice Date": extract_issue_date(ocr_output),
        "Billing Address": extract_address(ocr_output),
        "Invoice Total": extract_total(ocr_output),
        # "Customer Number": barcode_data.get('CUST', 'N/A'),
        # "category" : barcode_data.get('CAT', 'N/A'),
        "Items": []  # Populating items would require parsing item lines specifically, which is not covered here
    }
    for invoice in invoices:
     if "Items" in invoice.fields and invoice.fields["Items"].value:
        for item in invoice.fields["Items"].value:
            # Assume 'Amount' field contains combined quantity and unit price
            combined_value = item.value.get("Amount").value_data.text if item.value.get("Amount") else ""
            quantity, unit_price = parse_combined_quantity_and_price(combined_value)

            if quantity is not None and unit_price is not None:
                item_details = {
                    "Description": item.value.get("Description").value if item.value.get("Description") else "No Description",
                    "Unit Price": unit_price,
                    "Quantity": quantity,
                }
            else:
                # If parsing fails or 'Amount' does not contain combined quantity and price
                item_details = {
                    "Description": item.value.get("Description").value if item.value.get("Description") else "No Description",
                    "Amount": item.value.get("Amount").value if item.value.get("Amount") else "Failed to parse",
                    "Quantity": item.value.get("Quantity").value if item.value.get("Quantity") else 0,  # Or consider setting to None or "Failed to parse"
                }
            invoice_details["Items"].append(item_details)
    
    return invoice_details
   
import os
import requests
from dotenv import load_dotenv
# Authenticate
fr_endpoint = os.getenv("fr_endpoint")
fr_key = os.getenv("fr_key")
subscription_key = os.getenv("VISION_KEY")
endpoint = os.getenv("VISION_ENDPOINT")

# load_dotenv()   
# INVOICE_URL = "https://invoiceocrp3.azurewebsites.net/static/FAC_2019_0001-112650.png"
# extracted_data = azure_form_recognizer_invoice_url(INVOICE_URL, fr_endpoint, fr_key, endpoint, subscription_key)
# print(extracted_data)
