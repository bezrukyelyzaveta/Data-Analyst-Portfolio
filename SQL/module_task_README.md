SQL Query Requirements

The query result should include a set of grouping fields — categorical values that are not subjected to any calculations.
Metrics should be calculated in these breakdowns:
- date — date (for accounts: account creation date; for emails: email sent date)
- country — country
- send_interval — sending interval set by the account
- is_verified — whether the account is verified
- is_unsubscribed — whether the subscriber has unsubscribed


Note: These breakdowns apply to both account and email metrics. All necessary information is in the account table.

Metrics to calculate per grouping:

Primary metrics:
- account_cnt — number of created accounts
- sent_msg — number of emails sent
- open_msg — number of emails opened
- visit_msg — number of email clicks

Additional metrics (derived from primary metrics):
- total_country_account_cnt — total number of accounts created per country
- total_country_sent_cnt — total number of emails sent per country
- rank_total_country_account_cnt — country rank by total accounts
- rank_total_country_sent_cnt — country rank by total emails sent

  
Important notes:
Account and email metrics should be calculated separately to preserve unique breakdowns and avoid conflicts due to different logic for the date field. Use UNION to combine the results.
In the final result, include only rows where rank_total_country_account_cnt or rank_total_country_sent_cnt is less than or equal to 10.
Use at least one CTE for logical parts of the query.
Use window functions for ranking.

Output columns:
- date
- country
- send_interval
- is_verified
- is_unsubscribed
- account_cnt
- sent_msg
- open_msg
- visit_msg
- total_country_account_cnt
- total_country_sent_cnt
- rank_total_country_account_cnt
- rank_total_country_sent_cnt

  
Visualization:
In Looker Studio, create visualizations showing totals by country for:
- account_cnt
- total_country_sent_cnt
- rank_total_country_account_cnt
- rank_total_country_sent_cnt

Show a trend over time for the sent_msg metric.
