--1. What is the average, minimum, and maximum price of an item for each category?

SELECT category, AVG(price) AS avg_price, MIN(price) AS min_price, MAX(price) AS max_price
FROM `DA.product`
GROUP BY category
ORDER BY AVG(price) DESC

--2. What are the most profitable categories and their % of total_revenue? 

SELECT category, SUM(price) AS revenue, SUM(price)/SUM(SUM(price)) OVER()*100 AS percent_of_total_revenue
FROM `DA.order` AS orders
JOIN `DA.product` AS products
ON orders.item_id = products.item_id
GROUP BY category
ORDER BY SUM(price) DESC


--3. What is the most purchased item and how many times all items were purchased? 

SELECT short_description, COUNT(ga_session_id) AS number_od_orders
FROM `DA.order` AS orders
JOIN `DA.product` AS products
ON orders.item_id = products.item_id
GROUP BY short_description
ORDER BY COUNT(ga_session_id) DESC


--4. How many emails were opened and visited by each device? 

SELECT device, COUNT(DISTINCT open.id_message) AS emails_opened, COUNT(DISTINCT visit.id_message) AS emails_visited
FROM `DA.email_open` AS open
LEFT JOIN `DA.email_visit` AS visit
ON open.id_account = visit.id_account
LEFT JOIN `DA.account_session` AS acs
ON open.id_account = acs.account_id
LEFT JOIN `DA.session_params` AS params
ON acs.ga_session_id = params.ga_session_id
GROUP BY device
ORDER BY emails_opened DESC

--5. Revenue (total, desktop, mobile) and number of accounts (total and verified) by continent

WITH profit AS(
SELECT
  continent,
  SUM(price) AS revenue,
  SUM(CASE WHEN device = 'mobile' THEN price END) AS revenue_from_mobile,
  SUM(CASE WHEN device = 'desktop' THEN price END) AS revenue_from_desktop,
FROM data-analytics-mate.DA.order AS orders
JOIN data-analytics-mate.DA.product AS products
ON orders.item_id = products.item_id
JOIN data-analytics-mate.DA.session_params AS params
ON orders.ga_session_id = params.ga_session_id
GROUP BY continent),
account AS(
SELECT continent, COUNT(account.id) AS account_count,
COUNT(CASE WHEN is_verified = 1 THEN id END) AS verified_account
FROM data-analytics-mate.DA.account AS account
FULL JOIN data-analytics-mate.DA.account_session AS acc_session
ON account.id = acc_session.account_id
FULL JOIN data-analytics-mate.DA.session_params AS params
ON acc_session.ga_session_id = params.ga_session_id
GROUP BY continent
)


SELECT account.continent, revenue, revenue_from_mobile, revenue_from_desktop, account_count, verified_account
FROM profit
JOIN account
ON profit.continent = account.continent
ORDER BY revenue DESC



--6. What is monthly revenue and it’s % of total revenue? 

SELECT month, month_revenue, SUM(month_revenue) OVER() AS total_revenue, month_revenue/SUM(month_revenue) OVER()*100 AS percent
FROM(SELECT DATE(EXTRACT(YEAR FROM date), EXTRACT(MONTH FROM date), 1) AS month, SUM(cost) AS month_revenue
FROM data-analytics-mate.DA.paid_search_cost
GROUP BY month) AS unions
ORDER BY month

















