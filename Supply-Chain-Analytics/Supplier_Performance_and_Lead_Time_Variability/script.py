import pandas as pd

# load the data
df = pd.read_csv("supplier_performance.csv")

# clean the data
# convert the dates from str to datetime format
df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce') 
df['delivery_date'] = pd.to_datetime(df['delivery_date'], errors='coerce')

# check for duplicate supplier records
df.duplicated(subset=['order_id']).sum() 

# transform the data
# evaluate the performance of the suppliers using three metrics, lead_time, order_rate and deviation from the set delivery lead time
# lead_time in days
df['lead_time'] = (df['delivery_date'] - df['order_date']).dt.days

# order-fill_rate
df['order_fill_rate'] = ((df['quantity_delivered'] / df['quantity_ordered']) * 100).round(1)

# filter by order_fill rate
# filtered_df = df[df['order_fill_rate'] >= 100]

# filter by supplier to get the supplier with the highest number of order fill rates across all medicines
# dfx = filtered_df.groupby('supplier')['order_fill_rate'].count().reset_index()

# perform aggregations
# average lead time in days for each supplier across all medicines
# avrage order fill rate for each supplier accross diffrent medicines
# standard deviation of lead time - checks for variability or consistency(how spreac are the values from the average)
# total orders made, total value delivered

supplier_stats = df.groupby('supplier').agg(
    avg_lead_time = ("lead_time", "mean"),
    avg_fill_rate = ("order_fill_rate", "mean"),
    lead_time_deviation = ("lead_time", "std")
).reset_index()

print(supplier_stats.to_string())