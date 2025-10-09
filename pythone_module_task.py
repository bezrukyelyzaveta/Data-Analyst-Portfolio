#https://colab.research.google.com/drive/1Iz8eRSMXRlONKO8K_KEYVOKRp_0w56ha?usp=sharing

# Importing data and modules:

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

from google.colab import drive
drive.mount("/content/drive")

%cd /content/drive/MyDrive/python

events = pd.read_csv("events.csv")
countries = pd.read_csv("countries.csv")
products = pd.read_csv("products.csv")

#Display basic info about main tables:

print(events.info())
print(countries.info())
print(products.info())

#Assign appropriate data type to columns:

events["Order Date"] = pd.to_datetime(events["Order Date"])
events["Ship Date"] = pd.to_datetime(events["Ship Date"])

#Looking for NaNs:

print(events.isna().sum())
print(countries.isna().sum())
print(products.isna().sum())

#Merge tables into one:

join = pd.merge(events, countries, left_on="Country Code", right_on="alpha-3", how="left")
df = pd.merge(join, products, left_on="Product ID", right_on = "id", how="inner")

#Display info about NaNs, since they contain a big part of total revenue, I leave them:

nans = df[df["Country Code"].isna()]
nans.describe()

#Looking for duplicates, standartize data:

df.duplicated().sum()
df = df.apply(lambda col: col.str.strip().str.capitalize() if col.dtype == "object" else col)


#Working with final look of the table:


df= df.drop(columns=["Order Priority", "Country Code", "Product ID", "alpha-2", "alpha-3", "id"])
df.rename(columns={"name": "Country", "item_type": "Product Type"}, inplace=True)
df["Year"] = df["Order Date"].dt.year
df["Month_year"] = df["Order Date"].dt.strftime("%m.%Y")
df["Month name"] = df["Order Date"].dt.strftime("%B")
df["Weekday"] = df["Order Date"].dt.day_name()
df["Delivery"] = df["Ship Date"] - df["Order Date"]
df["Profit"] = (df["Unit Price"] - df["Unit Cost"])*df["Units Sold"]
df["Country"] = df["Country"].fillna("Not Defined")
df["Revenue"] = df["Unit Price"] * df["Units Sold"]
df["Cost"] = df["Unit Cost"] * df["Units Sold"]

from pandas.api.types import CategoricalDtype
month_order = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
month_type = CategoricalDtype(categories=month_order, ordered=True)
df["Month name"] = df["Month name"].astype(month_type)

df["Month_year"] = pd.to_datetime(df["Month_year"], format="%m.%Y")

#Calculate main metrics:

total_sales = (df["Revenue"]).sum()
total_profit = df["Profit"].sum()
orders_count = df["Order ID"].count()
units_sold = df["Units Sold"].sum()
avg_price =  df["Unit Price"].mean()
countries = df.loc[df["Country"] != "Not Defined", "Country"].nunique()
profit_by_years = df.groupby("Year")[["Profit"]].sum()
sales_by_month = df.groupby("Month name")[["Revenue"]].sum()
profit_dynamics = df.groupby("Month_year")[["Profit"]].sum()


#Change number fornat:

pd.set_option('display.float_format', '{:,.2f}'.format)

#Analyze sales and profit breakdowns, display top product categories by sales in top 10 countries:

categories_sales = df.groupby("Product Type")[["Revenue"]].sum()
categories_sales = categories_sales.sort_values(by="Revenue", ascending=False)

categories_profit = df.groupby("Product Type")[["Profit"]].sum()
categories_profit = categories_profit.sort_values(by="Profit", ascending=False)

countries_profit = df.groupby("Country")[["Profit"]].sum()
countries_profit = countries_profit.sort_values(by="Profit", ascending=False)

region_profit = df.groupby("region")[["Profit"]].sum()
region_profit = region_profit.sort_values(by="Profit", ascending = False)

top_countries = df.groupby("Country")[["Revenue"]].sum()
top_countries = top_countries.sort_values(by="Revenue", ascending = False).head(10).index
top_df = df[df["Country"].isin(top_countries)]
top_category_per_country = (top_df.groupby(["Country", "Product Type"])["Revenue"].sum().reset_index())
top_category_per_country = top_category_per_country.sort_values("Revenue", ascending=False)
top_category_per_country = top_category_per_country.drop_duplicates(subset=["Country"])

channel = df.groupby("Sales Channel")[["Revenue"]].sum()


#Calculate average delivery time:

countries_ship = df.groupby("Country")[["Delivery"]].mean()

subregion_ship = df.groupby("sub-region")[["Delivery"]].mean()

category_ship = df.groupby("Product Type")[["Delivery"]].mean()

df["Delivery Days"] = (df["Ship Date"] - df["Order Date"]).dt.days
df["Delivery Group"] = pd.cut(df["Delivery Days"],bins=[-1, 10, 20, float("inf")],labels=["0-10 days", "11-20 days", "21+ days"])
delivery_stats = (df.groupby("Delivery Group")["Revenue"].mean().reset_index().rename(columns={"Revenue": "Average Revenue"}))

#Calculate profir by years, months, and total profit dynamics:

profit_by_years = df.groupby("Year")[["Profit"]].sum()
sales_by_month = df.groupby("Month name")[["Revenue"]].sum()
profit_dynamics = df.groupby("Month_year")[["Profit"]].sum()

#Calculate monthly profit by categories:

cereal = df[df["Product Type"] == "Cereal"].groupby("Month name")["Revenue"].sum()
household = df[df["Product Type"] == "Household"].groupby("Month name")["Revenue"].sum()
clothes = df[df["Product Type"] == "Clothes"].groupby("Month name")["Revenue"].sum()
beverages = df[df["Product Type"] == "Beverages"].groupby("Month name")["Revenue"].sum()
office_supplies = df[df["Product Type"] == "Office supplies"].groupby("Month name")["Revenue"].sum()
fruits = df[df["Product Type"] == "Fruits"].groupby("Month name")["Revenue"].sum()
vegetables = df[df["Product Type"] == "Vegetables"].groupby("Month name")["Revenue"].sum()
baby_food = df[df["Product Type"] == "Baby Food"].groupby("Month name")["Revenue"].sum()
meat = df[df["Product Type"] == "Meat"].groupby("Month name")["Revenue"].sum()
cosmetics = df[df["Product Type"] == "Cosmetics"].groupby("Month name")["Revenue"].sum()
snacks = df[df["Product Type"] == "Snacks"].groupby("Month name")["Revenue"].sum()
personal_care = df[df["Product Type"] == "Personal care"].groupby("Month name")["Revenue"].sum()

#Dynamics for regions:

regions = df.groupby(["region", "Month name"])[["Revenue"]].sum()

#Number of orders by weekday:

weekday = df.groupby("Weekday")["Order ID"].count()
week_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
week_type = CategoricalDtype(categories=week_order, ordered=True)
df["Weekday"] = df["Weekday"].astype(week_type)


#Summary metrics visualization:

metrics = {
    "Total Sales": total_sales,
    "Total Profit": total_profit,
    "Orders Count": orders_count,
    "Units Sold": units_sold,
    "Avg. Unit Price": avg_price,
    "Countries": countries
}

fig, ax = plt.subplots(figsize=(12, 6))
ax.axis("off")

x_start = 0.05
width = 0.25
gap = 0.06

for i, (key, value) in enumerate(metrics.items()):
    x_pos = x_start + (i % 3) * (width + gap)
    y_pos = 0.6 if i < 3 else 0.1
    ax.add_patch(plt.Rectangle((x_pos, y_pos), width, 0.3, color="#414286", lw=2))
    ax.text(x_pos + width / 2, y_pos + 0.25, key, ha="center", va="center", fontsize=14, color="white")
    ax.text(x_pos + width / 2, y_pos + 0.15, f"{value:,.0f}", ha="center", va="center", fontsize=14, color="white", weight="bold")

plt.tight_layout()
plt.show()


#Visualizations: profit by years, revenue by month, profit dynamics by months: 

fig = plt.figure(figsize=(14, 8))
gs = fig.add_gridspec(2, 2, height_ratios=[1, 1])

ax1 = fig.add_subplot(gs[0, 0])
ax1.bar(profit_by_years.index, profit_by_years["Profit"], color='#440154')
ax1.set_title("Profit by Years")
ax1.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
ax1.set_ylim(top=max(profit_by_years["Profit"].max(), 100000000))


ax2 = fig.add_subplot(gs[0, 1])
ax2.plot(sales_by_month.index, sales_by_month["Revenue"], marker='o', color='#482374')
ax2.set_title("Revenue by Month")
ax2.tick_params(axis='x', rotation=45)
ax2.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))


ax3 = fig.add_subplot(gs[1, :])
ax3.plot(profit_dynamics.index, profit_dynamics["Profit"], marker='o', color='#3dbb74')
ax3.set_title("Profit Dynamics by Months")
ax3.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
ax3.set_ylim(top=max(profit_dynamics["Profit"].max(), 2000000))


ax3.set_xlim(left=profit_dynamics.index.min(), right=profit_dynamics.index.max())
ax3.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
ax3.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
ax3.tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.show()

#Visualization: total revenue, total profit, monthly revenue by product type:

category_sales = category_sales.sort_values(by="%", ascending=False).reset_index(drop=True)
category_profit = category_profit.sort_values(by="%", ascending=False).reset_index(drop=True)
category_sales["%"] = (category_sales["Revenue"] / category_sales["Revenue"].sum() * 100).round(1)
category_profit["%"] = (category_profit["Profit"] / category_profit["Profit"].sum() * 100).round(1)

fig = plt.figure(figsize=(14, 10))
gs = fig.add_gridspec(2, 2, height_ratios=[1, 1])

ax1 = fig.add_subplot(gs[0, 0])
sns.barplot(data=category_sales, x="Product Type", y="Revenue", palette="viridis", ax=ax1)
ax1.set_title("Total Revenue by Product Type")
ax1.set_xlabel("")
ax1.set_ylabel("Revenue")
ax1.tick_params(axis='x', rotation=45)
ax1.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))


ax2 = fig.add_subplot(gs[0, 1])
sns.barplot(data=category_profit, x="Product Type", y="Profit", palette="viridis", ax=ax2)
ax2.set_title("Total Profit by Product Type")
ax2.set_xlabel("")
ax2.set_ylabel("Profit")
ax2.tick_params(axis='x', rotation=45)
ax2.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
ax2.set_ylim(top=max(category_profit["Profit"].max(), 100000000))


ax3 = fig.add_subplot(gs[1, :])
monthly_revenue = df.groupby(["Month name", "Product Type"])["Revenue"].sum().reset_index()
months_order = ["January", "February", "March", "April", "May", "June",
                "July", "August", "September", "October", "November", "December"]
monthly_revenue["Month name"] = pd.Categorical(monthly_revenue["Month name"], categories=months_order, ordered=True)
monthly_revenue = monthly_revenue.sort_values("Month name")
product_types = monthly_revenue["Product Type"].unique()
palette = sns.color_palette("viridis", len(product_types))
color_map = dict(zip(product_types, palette))

for product_type, group_data in monthly_revenue.groupby("Product Type"):
    ax3.plot(
        group_data["Month name"],
        group_data["Revenue"],
        label=product_type,
        color=color_map[product_type]
    )

ax3.set_title("Monthly Revenue by Product Type")
ax3.set_xlabel("Month")
ax3.set_ylabel("Revenue")
ax3.legend(title="Product Type")
ax3.tick_params(axis='x', rotation=45)
ax3.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
ax3.set_ylim(top=max(monthly_revenue["Revenue"].max(), 60000000))

plt.tight_layout()
plt.show();


#Visualization: TOP 10 countries by profit, Europe sales, Asia sales:

fig = plt.figure(figsize=(14, 12))
gs = fig.add_gridspec(3, 1, height_ratios=[1, 1, 1])

top_countries = countries_profit.sort_values("Profit", ascending=False).head(10)
colors = sns.color_palette("viridis", len(top_countries))
ax1 = fig.add_subplot(gs[0, 0])
ax1.bar(top_countries.index, top_countries["Profit"], color=colors)
ax1.set_title("Top 10 Countries by Profit")
ax1.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
ax1.set_ylim(top=max(top_countries["Profit"].max(), 30000000))


europe_sales = (df[df["region"] == "Europe"].groupby("Month name")[["Revenue"]].sum().reset_index())
europe_sales["Month name"] = pd.Categorical(europe_sales["Month name"], categories=months_order, ordered=True)
europe_sales = europe_sales.sort_values("Month name")
ax2 = fig.add_subplot(gs[1, 0])
ax2.plot(europe_sales["Month name"], europe_sales["Revenue"], marker='o', color='#482374')
ax2.set_title("Europe Sales")
ax2.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))

asia_sales = (df[df["region"] == "Asia"].groupby("Month name")[["Revenue"]].sum().reset_index())
asia_sales["Month name"] = pd.Categorical(asia_sales["Month name"], categories=months_order, ordered=True)
asia_sales = asia_sales.sort_values("Month name")
ax3 = fig.add_subplot(gs[2, 0])
ax3.plot(asia_sales["Month name"], asia_sales["Revenue"], marker='o', color='#afdc2e')
ax3.set_title("Asia Sales")
ax3.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))

#Visualization: number of orders by weekday, orders by sales channel: 

weekday = weekday.reindex(week_order)
channels =df.groupby("Sales Channel")[["Order ID"]].count()
channel_percent = (channels / channels.sum() * 100).round(1)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

sns.barplot(x=weekday.index, y=weekday.values, palette="viridis", ax=ax1)
ax1.set_title("Number of Orders by Weekday")
ax1.set_ylabel("Number of Orders")
ax1.set_xlabel("")
ax1.tick_params(axis='x', rotation=45)
ax1.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))

colors = sns.color_palette("viridis", len(channels))
ax2.pie(channels["Order ID"], labels=[
    f"{name} ({percent}%)" for name, percent in zip(channel.index, channel_percent["Order ID"])
], autopct='%1.1f%%', colors=colors, startangle=90)
ax2.set_title("Orders by Sales Channel")

plt.tight_layout()
plt.show()


