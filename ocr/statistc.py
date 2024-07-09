# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
# from get_dat import get_data_as_dataframe



# df = get_data_as_dataframe() 

# def perform_statistical_analysis(df):
#     # Drop 'Customer ID' column
#     df = df.drop(columns=['Customer ID'])

#     # Descriptive Statistics
#     print("\nDescriptive Statistics:")
#     print(df.describe())

#     # Correlation Analysis
#     print("\nCorrelation Analysis:")
#     # Exclude non-numeric columns from correlation analysis
#     numeric_columns = df.select_dtypes(include=['number']).columns
#     correlation_matrix = df[numeric_columns].corr()
#     print(correlation_matrix)
#     # Plot correlation matrix
#     plt.figure(figsize=(10, 8))
#     sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
#     plt.title("Correlation Matrix")
#     plt.show()

#     # Customer Analysis
#     print("\nCustomer Analysis:")
#     customer_analysis = df.groupby('Customer Name')['Total'].agg(['sum', 'count'])
#     customer_analysis = customer_analysis.nlargest(10, 'sum')  # Select top 10 customers by total sales
#     print(customer_analysis)
#     # Plot customer analysis
#     plt.figure(figsize=(10, 6))
#     sns.barplot(x=customer_analysis.index, y='sum', data=customer_analysis, palette='viridis')
#     plt.title("Top 10 Customers by Total Sales")
#     plt.xlabel("Customer Name")
#     plt.ylabel("Total Sales")
#     plt.xticks(rotation=45, ha='right')
#     plt.tight_layout()
#     plt.show()

#     # Category Analysis
#     print("\nCategory Analysis:")
#     category_analysis = df.groupby('Category')['Total'].agg(['sum', 'mean', 'count'])
#     category_analysis = category_analysis.nlargest(10, 'sum')  # Select top 10 categories by total sales
#     print(category_analysis)
#     # Plot category analysis
#     category_analysis.plot(kind='bar', figsize=(10, 6))
#     plt.title("Top 10 Categories by Total Sales")
#     plt.xlabel("Category")
#     plt.ylabel("Values")
#     plt.xticks(rotation=45, ha='right')
#     plt.tight_layout()
#     plt.show()
    
    
    
#     category_sales = df.groupby('Category')['Total'].sum()
#     print(category_sales)
     
    
#     plt.figure(figsize=(8, 6))
#     ax = category_sales.plot(kind='pie', autopct='%1.1f%%', colors=sns.color_palette('pastel'), startangle=140)
#     ax.set_title('Total Sales by Category', fontsize=16, fontweight='bold')
#     plt.ylabel('')
#     plt.axis('equal')
#     plt.tight_layout()
#     plt.show()

    

#     # Item Analysis
#     print("\nItem Analysis:")
#     item_analysis = df.groupby('Description')[['Quantity', 'Total']].agg(['sum'])
#     item_analysis = item_analysis.nlargest(10, ('Total', 'sum'))  # Select top 10 items by total sales
#     print(item_analysis)
#     # Plot item analysis
#     item_analysis.plot(kind='bar', figsize=(12, 6), stacked=True)
#     plt.title("Top 10 Items by Total Sales")
#     plt.xlabel("Description")
#     plt.ylabel("Values")
#     plt.xticks(rotation=45, ha='right')
#     plt.tight_layout()
#     plt.show()
    
    
    
# perform_statistical_analysis(df)


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import base64
import io

def perform_statistical_analysis(df):
    # Drop 'Customer ID' column
    df = df.drop(columns=['Customer ID'])

    descriptive_stats = df.describe()

    numeric_columns = df.select_dtypes(include=['number']).columns
    correlation_matrix = df[numeric_columns].corr()

    customer_analysis = df.groupby('Customer Name')['Total'].agg(['sum', 'count'])
    customer_analysis = customer_analysis.nlargest(10, 'sum')

    category_analysis = df.groupby('Category')['Total'].agg(['sum', 'mean', 'count'])
    category_analysis = category_analysis.nlargest(10, 'sum')

    category_sales = df.groupby('Category')['Total'].sum()

       # Calculate yearly sales
    df['Year'] = pd.to_datetime(df['Date']).dt.year
    yearly_sales = df.groupby('Year')['Total'].sum()
    
    # Category Sales Pie Chart
    category_sales = df.groupby('Category')['Total'].sum()
    category_sales_fig = plt.figure(figsize=(8, 6))
    ax = category_sales.plot(kind='pie', autopct='%1.1f%%', colors=sns.color_palette('pastel'), startangle=140)
    ax.set_title('Total Sales by Category', fontsize=16, fontweight='bold')
    plt.ylabel('')
    plt.axis('equal')
    plt.tight_layout()

    # Item Analysis
    item_analysis = df.groupby('Description')[['Quantity', 'Total']].agg(['sum'])
    item_analysis = item_analysis.nlargest(10, ('Total', 'sum'))

    # Convert plots to base64 encoded strings
    descriptive_stats_buf = io.BytesIO()
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
    plt.title("Correlation Matrix")
    plt.savefig(descriptive_stats_buf, format='png')
    descriptive_stats_buf.seek(0)
    descriptive_stats_encoded = base64.b64encode(descriptive_stats_buf.read()).decode()

    correlation_matrix_buf = io.BytesIO()
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
    plt.title("Correlation Matrix")
    plt.savefig(correlation_matrix_buf, format='png')
    correlation_matrix_buf.seek(0)
    correlation_matrix_encoded = base64.b64encode(correlation_matrix_buf.read()).decode()

    customer_analysis_buf = io.BytesIO()
    plt.figure(figsize=(10, 6))
    sns.barplot(x=customer_analysis.index, y='sum', data=customer_analysis, palette='viridis')
    plt.title("Top 10 Customers by Total Sales")
    plt.xlabel("Customer Name")
    plt.ylabel("Total Sales")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(customer_analysis_buf, format='png')
    customer_analysis_buf.seek(0)
    customer_analysis_encoded = base64.b64encode(customer_analysis_buf.read()).decode()

    category_analysis_buf = io.BytesIO()
    category_analysis.plot(kind='bar', figsize=(10, 6))
    plt.title("Categories by Total Sales")
    plt.xlabel("Category")
    plt.ylabel("Values")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(category_analysis_buf, format='png')
    category_analysis_buf.seek(0)
    category_analysis_encoded = base64.b64encode(category_analysis_buf.read()).decode()

    category_sales_buf = io.BytesIO()
    plt.figure(figsize=(8, 6))
    ax = category_sales.plot(kind='pie', autopct='%1.1f%%', colors=sns.color_palette('pastel'), startangle=140)
    ax.set_title('Total Sales by Category', fontsize=16, fontweight='bold')
    plt.ylabel('')
    plt.axis('equal')
    plt.tight_layout()
    plt.savefig(category_sales_buf, format='png')
    category_sales_buf.seek(0)
    category_sales_encoded = base64.b64encode(category_sales_buf.read()).decode()

    item_analysis_buf = io.BytesIO()
    item_analysis.plot(kind='bar', figsize=(12, 6), stacked=True)
    plt.title("Top 10 Items by Total Sales")
    plt.xlabel("Description")
    plt.ylabel("Values")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(item_analysis_buf, format='png')
    item_analysis_buf.seek(0)
    item_analysis_encoded = base64.b64encode(item_analysis_buf.read()).decode()

     
    yearly_sales_buf = io.BytesIO()
    plt.figure(figsize=(10, 6))
    yearly_sales.plot(kind='bar', color='orange',  figsize=(12, 6), stacked=True)
    plt.title('Yearly Sales')
    plt.xlabel('Year')
    plt.ylabel('Total Sales')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(yearly_sales_buf, format='png')
    yearly_sales_buf.seek(0)
    yearly_sales_encoded = base64.b64encode(yearly_sales_buf.read()).decode()

    # Return encoded strings
    return descriptive_stats_encoded, correlation_matrix_encoded, customer_analysis_encoded, category_analysis_encoded, category_sales_encoded, item_analysis_encoded , yearly_sales_encoded
 
 
 
 
 
 
 
 # monotoring 
import base64
from io import BytesIO
import matplotlib.pyplot as plt

def create_status_codes_plot(status_counts):
    """Generates a plot for request status codes and returns a base64-encoded image string."""
    status_codes = [str(status_code) for status_code, _ in status_counts]
    counts = [count for _, count in status_counts]
    
    fig, ax = plt.subplots()
    ax.bar(status_codes, counts)
    ax.set_xlabel('Status Codes')
    ax.set_ylabel('Counts')
    ax.set_title('Requests by Status Code')

    # Convert plot to PNG image
    img = BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    plt.close()
    img.seek(0)  # Go to the beginning of the BytesIO buffer

    # Encode the PNG image to base64
    img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')

    return img_base64
