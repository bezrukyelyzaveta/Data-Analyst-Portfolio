The dataset contains information about the company's product sales. The company operates globally, selling products both in physical stores and online. 
The dataset consists of three tables:

- events.csv — sales data spanning multiple years;
- products.csv — product categories and their codes;
- countries.csv — countries, regions, and their codes.


Project goal: Data cleaning and analysis to extract actionable business insights.

Project stages:

1. Data Overview
Load the dataset and examine the columns. Provide a description of each column.
Identify key fields that link the three tables.

3. Data Cleaning
Handle missing, incorrect, or anomalous values.
Check each table for missing values, assess their proportion, and try to understand the reasons for missing data.
Fill in or remove missing values, justifying your approach.
Investigate the dataset for duplicates.

5. Data Analysis and Visualization
Join the three tables into a single DataFrame. Remove unnecessary columns and rename columns if needed.
Start with key business metrics: total number of orders, total profit, number of countries covered, and other relevant KPIs.
Analyze sales (revenue, costs, profits, product popularity) and create visualizations by:
- Product categories
- Geography (countries, regions)
- Sales channels (online vs offline)
Analyze the time interval between order placement and shipment, visualizing by:
- Product categories
- Countries
- Regions

Explore whether profit depends on the time required for shipment. Perform necessary aggregations and visualizations.
Visualize sales dynamics over time by product category, country, and region to identify key trends.
Analyze sales by day of the week to identify potentially seasonal products.
