import pandas as pd

# load the csv data into the dataframe for manipulation purposes

# change the str to date type
customers = pd.read_csv('customers.csv')

order_items = pd.read_csv("order_items.csv")
# change the order date from str to datetime
orders = pd.read_csv("orders.csv")

# change the str date to datetime
payments = pd.read_csv("payments.csv")

products = pd.read_csv("products.csv")

# get the summary info about the data in the dataframe
# data type, null values present, total rows, total columns etc
print(products.info())
