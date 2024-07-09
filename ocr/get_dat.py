
import pandas as pd
from con import engine , Session
from database import Customer, Invoice, Item  # Import your SQLAlchemy models
import re

# Function to extract numeric value from string
def extract_numeric_value(s):
    numeric_part = re.search(r'\d+\.\d+', s)
    if numeric_part:
        return float(numeric_part.group())
    else:
        return None

# Function to get data from the database and convert it into a DataFrame
def get_data_as_dataframe():
    session = Session()
    try:
        # Querying data from the database using ORM with relationships
        query_result = session.query(Customer, Invoice, Item).\
            join(Invoice, Customer.invoices).\
            join(Item, Invoice.items).all()

        # Extracting data into lists
        data = []
        for customer, invoice, item in query_result:
            # Extract numeric value from the total
            total = extract_numeric_value(invoice.total)

            data.append({
                'Customer ID': customer.id,
                'Customer Name': customer.customer_name,
                'Address': customer.address,
                'Category': customer.category,
                'Invoice Number': invoice.invoice_number,
                'Date': invoice.date,
                'Total': total,
                'Description': item.description,
                'Amount': item.amount,
                'Quantity': item.quantity
            })

        # Converting data into DataFrame
        df = pd.DataFrame(data)
        return df
    finally:
        session.close()
df = get_data_as_dataframe()
print(df)