# districts with the highest wastage rate linked to temparature breaches 
# vaccines with highest wastage rate linked to temparature breaches
# districts with the highest wastage rate linked to non-temparature breaches(expiry)

import pandas as pd

# load the data into a df
deliveries = pd.read_csv("deliveries.csv")
temp_logs = pd.read_csv("temparature_logs.csv")
wastages = pd.read_csv("wastage.csv")

# check for null values per column
deliveries.isnull().sum()

# convert delivery_date from str to date time inorder to standardize data formats and for easier filtering
deliveries['delivery_date'] = pd.to_datetime(deliveries['delivery_date'], errors='coerce')

# check for duplicates (repeating rows) in the entire df
# return true if any exists and false if none exists.
deliveries.duplicated().any()
deliveries.duplicated().sum()

# check for duplicate rows for specific columns
deliveries.duplicated(subset=['district', 'vaccine_type']).sum()

# transformations
# count the total_number of breach counts equals to true for each delivery.
# merge to deliveries
# calculate the wastage rate for each delivery of each vaccine made linked to temparature breach.
# group by district and vaccine type
# sort from the highest to the lowest

breach_counts = temp_logs[temp_logs['is_breach'] == True].groupby('delivery_id').size().reset_index(name="breach_counts")
merged = deliveries.merge(breach_counts, how='left', on='delivery_id')
merged = merged.merge(wastages, on='delivery_id', how='left')

# fill in NaN values with 0 for easy filtering
merged['breach_counts'] = merged['breach_counts'].fillna(0)
merged['doses_wasted'] = merged['doses_wasted'].fillna(0)

# filter the entire df by breach counts
filtered_merged = merged[merged['breach_counts'] > 0]

# calculate the wastage rate for each delivery
filtered_merged['wastage_rate'] = ((filtered_merged['doses_wasted'] / filtered_merged['doses_received']) * 100).round(1)

# sort breach counts by descending order - largest to the smallest
# set in place to true instead of creating another dataframe
filtered_merged.sort_values('wastage_rate', ascending=False, inplace=True)

# create a csv file from the above information
filtered_merged.to_csv("script_summary", index=False)

# print the final filtered dataframe
print(filtered_merged.to_string())




