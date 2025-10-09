--https://lookerstudio.google.com/reporting/0a111f2d-d826-4f2c-ac23-2401ba706607


WITH account AS(SELECT date,
     country,
     send_interval,
     CASE WHEN is_verified = 0 THEN 'unverified' WHEN is_verified = 1 THEN 'verified' END AS is_verified,
     CASE WHEN is_unsubscribed = 0 THEN 'subscribed' WHEN is_unsubscribed = 1 THEN 'unsubscribed' END AS is_unsubscribed,
     COUNT(DISTINCT account.id) AS account_cnt,
     0 AS sent_msg,
     0 AS open_msg,
     0 AS visit_msg
FROM DA.account AS account
JOIN `DA.account_session`AS acc_session
ON account.id = acc_session.account_id
JOIN DA.session AS session
ON acc_session.ga_session_id = session.ga_session_id
JOIN data-analytics-mate.DA.session_params AS params
ON session.ga_session_id = params.ga_session_id
GROUP BY date, country, send_interval, is_verified, is_unsubscribed),




emails AS(SELECT DATE_ADD(session.date, INTERVAL sent.sent_date DAY) AS date,
     country,
     send_interval,
     CASE WHEN is_verified = 0 THEN 'unverified' WHEN is_verified = 1 THEN 'verified' END AS is_verified,
     CASE WHEN is_unsubscribed = 0 THEN 'subscribed' WHEN is_unsubscribed = 1 THEN 'unsubscribed' END AS is_unsubscribed,
     0 AS account_cnt,
     COUNT(DISTINCT sent.id_message) AS sent_msg,
     COUNT(DISTINCT open.id_message) AS open_msg,
     COUNT(DISTINCT visit.id_message) AS visit_msg
FROM DA.email_sent AS sent
LEFT JOIN DA.email_open AS open
ON sent.id_message = open.id_message
LEFT JOIN DA.email_visit AS visit
ON sent.id_message = visit.id_message
JOIN DA.account_session AS acc_session
ON sent.id_account = acc_session.account_id
JOIN DA.session AS session
ON acc_session.ga_session_id = session.ga_session_id
JOIN DA.session_params AS params
ON session.ga_session_id = params.ga_session_id
FULL JOIN `DA.account` AS account
ON sent.id_account = account.id
GROUP BY date, country, send_interval, is_verified, is_unsubscribed),




union1 AS(SELECT *
FROM account
UNION ALL
SELECT *
FROM emails),




emails_acc AS (SELECT date,
                    country,
                    send_interval,
                    is_verified,
                    is_unsubscribed,
                    SUM(account_cnt) AS account_cnt,
                    SUM(sent_msg) AS sent_msg,
                    SUM(open_msg) AS open_msg,
                    SUM(visit_msg) AS visit_msg,
                   


FROM union1
GROUP BY date, country, send_interval, is_verified, is_unsubscribed),


final AS(SELECT date, country, send_interval, is_verified, is_unsubscribed, account_cnt, sent_msg, open_msg, visit_msg,
      total_country_acc_cnt, total_country_sent_cnt,
      rank_total_country_account_cnt,
      rank_total_country_sent_cnt
FROM(
SELECT date, country, send_interval, is_verified, is_unsubscribed, account_cnt, sent_msg, open_msg, visit_msg,
      total_country_acc_cnt, total_country_sent_cnt,
      DENSE_RANK() OVER (ORDER BY total_country_acc_cnt DESC) AS rank_total_country_account_cnt,
      DENSE_RANK() OVER (ORDER BY total_country_sent_cnt DESC) AS rank_total_country_sent_cnt
FROM(
SELECT date, country, send_interval, is_verified, is_unsubscribed, account_cnt, sent_msg, open_msg, visit_msg,
      SUM(sent_msg) OVER(PARTITION BY country) AS total_country_sent_cnt,
      SUM(account_cnt) OVER(PARTITION BY country) AS total_country_acc_cnt,
FROM emails_acc) AS abc) AS bca )


SELECT *
FROM final
WHERE rank_total_country_account_cnt <=10 OR rank_total_country_sent_cnt <=10


