import pandas as pd
from tabulate import tabulate
import os
import matplotlib.pyplot as plt
from itertools import combinations
from collections import Counter

### PREPARING DATA ###

# read test data and print using tabulate
df = pd.read_csv("./Sales_Data/Sales_April_2019.csv")
# print(tabulate(df, headers='keys', tablefmt='psql'))

# we have sales of each month in separate file. We must merge all files in one
files = [file for file in os.listdir("./Sales_Data")]
all_df = pd.DataFrame()
for f in files:
    df = pd.read_csv("./Sales_Data/"+f)
    all_df = pd.concat([all_df, df])

# now we can save all_df to new csv file
all_df.to_csv("all_sales_data.csv")


### ANALYSIS ###

# [1] Find best month for sales

# first we need add 'Month' column
all_df['Month'] = all_df['Order Date'].str[:2]

# now we can find and drop 'NaN' rows
nan_df = all_df[all_df.isna().any(axis=1)]
all_df = all_df.dropna(how='all') # dropna() remove missing values

# now we can find and drop 'Or' rows
all_df = all_df[all_df['Order Date'].str[:2] != 'Or']

# converting 'Month' column to int
all_df['Month'] = all_df['Month'].astype('int32')

# we need add Sales column. Firstly we should convert required columns to int
all_df['Quantity Ordered'] = all_df['Quantity Ordered'].astype('float')
all_df['Price Each'] = all_df['Price Each'].astype('float')

# now we can compute 'Sales' column
all_df['Sales'] = all_df['Quantity Ordered'] * all_df['Price Each']

# we can use groupby() and sum() to find sales of each month and matplotlib to represent this on bar plot
months_numbers = range(1, 13)
plt.bar(months_numbers, all_df.groupby('Month').sum()['Sales'])
plt.title('Find best month for sales')
plt.xticks(months_numbers)
plt.ylabel('$')
plt.xlabel('Month number')
plt.show()

# [2] Which city had the best sales?

# firstly we need add 'City' column
all_df['City'] = all_df['Purchase Address'].apply(lambda x: x.split(',')[1] + ' ' + x.split(',')[2].split(' ')[1])

# now we can check which city has a best sales

cities = [city for city, df in all_df.groupby('City')]
plt.bar(cities, all_df.groupby('City').sum()['Sales'])
plt.title('Which city had the best sales?')
plt.xticks(cities, rotation='vertical')
plt.ylabel('$')
plt.xlabel('City')
plt.show()

# [3] What time is the best to display advertise?

# firstly we need convert 'Order Date' column to DateTime
all_df['Order Date'] = pd.to_datetime(all_df['Order Date'])

# now we can add 'Hour' and 'Minute' columns that will be represent hour and minutes of orders
all_df['Hour'] = all_df['Order Date'].dt.hour
all_df['Minute'] = all_df['Order Date'].dt.minute

# finally we can represent on the plot, what time is the best for display advertise
hours = [hour for hour, df in all_df.groupby('Hour')]
plt.plot(hours, all_df.groupby(['Hour']).count())
plt.title('What time is the best to display advertise?')
plt.xticks(hours)
plt.xlabel('Hour')
plt.ylabel('Orders')
plt.show()

# [4] What products are mostly often sold together?

# firstly we need check rows with duplicated 'Order ID'
items_sold_together = all_df[all_df['Order ID'].duplicated(keep=False)]
items_sold_together['Grouped'] = items_sold_together.groupby('Order ID')['Product'].transform(lambda x: ','.join(x))
items_sold_together = items_sold_together[['Order ID', 'Grouped']].drop_duplicates()

# now we can find mostly often sold together products
count = Counter()

for row in items_sold_together['Grouped']:
    row_list = row.split(',')
    count.update(Counter(combinations(row_list, 2)))

# and print them
for key, value in count.most_common(10):
    print(key, value)

# [5] Find product which is sold the most
products = all_df.groupby('Product')
quantity_orders = products.sum()['Quantity Ordered']

products_names = [product for product, df in products]
plt.bar(products_names, quantity_orders)
plt.title('Find product which is sold the most')
plt.xticks(products_names, rotation='vertical')
plt.show()