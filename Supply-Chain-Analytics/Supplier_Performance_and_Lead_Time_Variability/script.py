import pandas as pd

# load the data
df = pd.read_csv("supplier_performance.csv")

# clean the data
# convert the dates from str to datetime format
df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce') 
df['delivery_date'] = pd.to_datetime(df['delivery_date'], errors='coerce')

# check for duplicate supplier records
df.duplicated(subset=['order_id']).sum() 

# ensure consistent category names or other column lables
print(df.to_string())


