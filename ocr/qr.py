import cv2
import numpy as np
import requests

def fetch_and_decode_qr_cv2(image_url):
    # Fetch the image from the URL
    response = requests.get(image_url)
    if response.status_code == 200:
        # Convert response content to a numpy array, then decode to an image
        image_array = np.array(bytearray(response.content), dtype=np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

        # Initialize QR Code detector
        detector = cv2.QRCodeDetector()

        # Detect and decode the QR Code
        data, points, _ = detector.detectAndDecode(image)

        if data:
            print(f"Decoded QR data: {data}")
            # Parse the QR code data string into a dictionary and return it
            qr_data_dict = {}
            for line in data.strip().split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    qr_data_dict[key.strip()] = value.strip()
            return qr_data_dict
        else:
            print("QR Code not found.")
            return None
    else:
        print(f"Failed to fetch the image from URL. Status code: {response.status_code}")
        return None