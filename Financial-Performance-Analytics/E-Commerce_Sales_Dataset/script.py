import pandas as pd

# load the csv data into the dataframe for manipulation purposes
customers = pd.read_csv('customers.csv')
order_items = pd.read_csv("order_items.csv")
orders = pd.read_csv("orders.csv")
payments = pd.read_csv("payments.csv")
products = pd.read_csv("products.csv")

# change the str to datetimes
# Remove leading/trailing whitespace
customers['signup_date'] = customers['signup_date'].str.strip()
customers['signup_date'] = pd.to_datetime(customers['signup_date'], format='%Y-%m-%d', errors='coerce')

orders['order_date'] = orders['order_date'].str.strip()
orders['order_date'] = pd.to_datetime(orders['order_date'], format='%Y-%m-%d', errors='coerce')

payments['payment_date'] = payments['payment_date'].str.strip()
payments['payment_date'] = pd.to_datetime(payments['payment_date'], format='%Y-%m-%d',  errors='coerce')

# get the summary info about the data in the dataframe
# data type, null values present, total rows, total columns etc
print(payments.info())

