from sqlalchemy.orm import Session
from database import Invoice, Item, Customer

def get_latest_invoice_data(db_session: Session):
    """Fetch the latest invoice data based on the invoice date."""
    latest_invoice = db_session.query(Invoice).order_by(Invoice.date.desc()).first()
    if latest_invoice:
        # Assuming you want to return a dictionary of the relevant invoice details
        invoice_data = {
            "id": latest_invoice.id,
            "invoice_number": latest_invoice.invoice_number,
            "date": latest_invoice.date,
            "total": latest_invoice.total,
            # Assuming customer relationship exists and is a single object (modify as needed)
            "customer_name": latest_invoice.customer.customer_name if latest_invoice.customer else None,
            "items": [
                {
                    "description": item.description,
                    "amount": item.amount,
                    "quantity": item.quantity,
                } for item in latest_invoice.items
            ] if latest_invoice.items else []
        }
        return invoice_data
    else:
        return None   
