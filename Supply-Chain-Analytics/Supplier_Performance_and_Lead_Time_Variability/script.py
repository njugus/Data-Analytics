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

# calculate the order_value_shortfall - the dffrence between the quantity ordered and quantity delivered to help
# understand the supplier effectiveness in terms of delivering what is needed
# order_fill_rate * order_value_usd = value for what is delivered
# order_value - delivered_value = order_value_shortfall
df['value_delivered'] = (df['quantity_delivered'] / df['quantity_ordered']) * df['order_value_usd']
order_value_shortfall = df['order_value_usd'] - df['value_delivered']
df['order_value_shortfall'] = order_value_shortfall


# perform aggregations
# average lead time in days for each supplier across all medicines
# avrage order fill rate for each supplier accross diffrent medicines
# standard deviation of lead time - checks for variability or consistency(how spreac are the values from the average)
# total orders made, total value delivered

supplier_stats = df.groupby('supplier').agg(
    avg_lead_time = ("lead_time", "mean"),
    avg_fill_rate = ("order_fill_rate", "mean"),
    lead_time_deviation = ("lead_time", "std"),
    total_orders_made = ("quantity_delivered", "count"),
    total_value_shortfall = ("order_value_shortfall", 'sum')

).reset_index()


# lets create the supplier scoring model
# normalization method used - min-max method
# normalize the supplier metrics to a 0 - 100 scale
order_fill_rate = supplier_stats['avg_fill_rate']
# the longest time it took to fulfill an order 

# lead time score
max_lead_time = supplier_stats['avg_lead_time'].max()
min_lead_time = supplier_stats['avg_lead_time'].min()
lead_time_score = 100 * (max_lead_time - supplier_stats['avg_lead_time']) / (max_lead_time - min_lead_time)
supplier_stats['lead_time_score'] = lead_time_score

# standard deviation score
max_std = supplier_stats['lead_time_deviation'].max()
min_std = supplier_stats['lead_time_deviation'].min()
std_score = 100 * (max_std - supplier_stats['lead_time_deviation']) / (max_std - min_std)
supplier_stats['std_score'] = std_score


# value_shortfall score normalization
shortfall_score = (
    (supplier_stats['total_value_shortfall'].max() - supplier_stats['total_value_shortfall']) /
    (supplier_stats['total_value_shortfall'].max() - supplier_stats['total_value_shortfall'].min())
)* 100


# define the weighted score model for evaluating the supplier performance using the three metrics based on importance
weighted_score = {
    "fill_rate" : 0.35,
    "lead_time" : 0.35,
    "std_dev" : 0.15,
    "shortfall_value" : 0.15
}

# calculate the scores for each supplier
supplier_stats['supplier_reliability_score'] = (
    (lead_time_score * weighted_score['lead_time']) + 
    (order_fill_rate  * weighted_score['fill_rate']) + 
    (std_score * weighted_score['std_dev']) +
    (shortfall_score * weighted_score['shortfall_value'])
)

print(supplier_stats.to_string())