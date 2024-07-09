import os
import time
import re
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials
from qr import fetch_and_decode_qr_cv2 
from dotenv import load_dotenv
load_dotenv() 

# Authenticate
subscription_key = os.getenv("VISION_KEY")
endpoint = os.getenv("VISION_ENDPOINT")

# Ensure subscription_key and endpoint are present
if not subscription_key or not endpoint:
    raise ValueError("Missing VISION_KEY or VISION_ENDPOINT in environment variables.")



def perform_ocr_and_extract_text(computervision_client, image_url):
    ocr_output = []
    read_response = computervision_client.read(url=image_url, raw=True)
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
                line_text = line.text
                if not re.match(r"^\*+$|X+$", line_text.replace(" ", "")):  # Skip lines with only 'XXXX' or '****'
                    ocr_output.append((line.text, line.bounding_box))
    return ocr_output


def extract_field(pattern, text):
    match = re.search(pattern, text, re.IGNORECASE)  # Using re.IGNORECASE to make the search case-insensitive
    if match:
        return match.group(1)  # Return the first captured group
    return None
def are_aligned_horizontally(box1, box2, tolerance=10):
    """Check if two boxes are aligned horizontally based on y-axis overlap."""
    _, y1_top, _, _, _, y1_bottom, _, _ = box1
    _, y2_top, _, _, _, y2_bottom, _, _ = box2
    return not (y1_bottom < y2_top - tolerance or y1_top > y2_bottom + tolerance)

def find_total_amount(ocr_data, total_label_box):
    """Find the total amount based on its proximity to the 'TOTAL' label."""
    for text, box in ocr_data:
        if 'Euro' in text and are_aligned_horizontally(box, total_label_box):
            return text
    return "Unknown"

def extract_address(lines):
    for line in lines:
        
          if line[0].lower().startswith("address"):
            address_index = lines.index(line)
            break
    if address_index is not None:
      
        address = lines[address_index][0] + ", " + lines[address_index + 1][0]
        return address.replace("Address ", "")
    return "Address not found"

def extract_price(text):
    """
    Extracts the price from a given text, supporting various formats.
    """
    match = re.search(r'\d{1,3}(?:,\d{3})*(?:\.\d{2})?', text.replace(' ', ''))
    print (match)
    return float(match.group(0).replace(',', '')) if match else None


def are_aligned_horizontally(box1, box2, threshold=5):
    """
    Checks if two boxes are aligned horizontally based on a threshold.
    Assumes boxes are in the format [x1, y1, x2, y2, x3, y3, x4, y4].
    """
    top1, bottom1 = min(box1[1], box1[3], box1[5], box1[7]), max(box1[1], box1[3], box1[5], box1[7])
    top2, bottom2 = min(box2[1], box2[3], box2[5], box2[7]), max(box2[1], box2[3], box2[5], box2[7])
    return abs((top1 + bottom1) / 2 - (top2 + bottom2) / 2) <= threshold



def is_separator_line(text):
    no_space_text = text.replace(" ", "")
    if len(set(no_space_text)) == 1 and len(no_space_text) > 1:
        return True
    return False 

def extract_price(text):
    match = re.search(r'(\d+\.\d{2}) Euro', text)
    if match:
        return float(match.group(1))
    return None

def parse_items(ocr_data):
    items = []
    for i, (text, box) in enumerate(ocr_data):
        # Skip if line contains only 'XXXX' or '****'
        if re.match(r"^\*+$|X+$|x+$", text.replace(" ", "")):
            continue # Skip this iteration and move to the next line
        if ' x' in text:
            # Extracting quantity
            quantity_match = re.search(r'(\d+) x', text)
            if quantity_match:
                quantity = int(quantity_match.group(1))
                # Find the price in the same line or in the next lines
                price = extract_price(text)
                if not price:  # If price is not in the same line, look ahead for the price
                    for j in range(i + 1, len(ocr_data)):
                        next_text, next_box = ocr_data[j]
                        price = extract_price(next_text)
                        if price:
                            break
                
                # Assuming description is in the previous line if not found in the current line with quantity
                if i > 0 and not ' x' in ocr_data[i-1][0]:  # Ensuring not picking another quantity line as description
                    description = ocr_data[i-1][0]
                else:
                    description = "Description not found"

                if price and quantity:
                    items.append({'Description': description, 'Quantity': quantity, 'Amount': price})
        elif 'Euro' in text:  # This case is for when only the price is on the line, handled above, but included for clarity
            continue

    return items

#image_url = "https://invoiceocrp3.azurewebsites.net/static/FAC_2024_0165-90804.png"
def extract_invoice_data_from_image(image_url, endpoint, subscription_key):
    computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))
    # Perform OCR to get the data
    ocr_data = perform_ocr_and_extract_text(computervision_client, image_url)
    print( ocr_data)
    # Extracting fields using your defined functions
    invoice_number = extract_field(r'INVOICE (\S+)', ocr_data[0][0])
    issue_date = extract_field(r'Issue date (.+)', ocr_data[1][0])
    bill_to = extract_field(r'Bill to (.+)', ocr_data[2][0])
    address = extract_address(ocr_data)

    # Finding the "TOTAL" amount
    total_label_box = None
    for text, box in ocr_data:
        if 'TOTAL' in text:
            total_label_box = box
            break
    total_amount = find_total_amount(ocr_data, total_label_box) if total_label_box else "Unknown"
    
    # Parsing items
    items = parse_items(ocr_data)

    # Organizing everything into a dictionary
    invoice_data = {
        "Invoice ID": invoice_number,
        "Invoice Date": issue_date,
        "Customer Name": bill_to,
        "Billing Address": address,
        "Invoice Total": total_amount,
        'Items': items
    }

    return invoice_data

#extracted_invoice_data = extract_invoice_data_from_image(image_url, endpoint, subscription_key)#
#print(extracted_invoice_data)