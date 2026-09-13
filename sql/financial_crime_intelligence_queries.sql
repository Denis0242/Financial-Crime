-- Financial Crime Intelligence & Risk Analytics

-- 1. Multi-risk customers
SELECT * FROM customer_financial_crime_intelligence
WHERE unique_risk_categories >= 2
ORDER BY financial_crime_risk_score DESC;

-- 2. Repeat-alert customers
SELECT * FROM customer_financial_crime_intelligence
WHERE total_alerts >= 3
ORDER BY total_alerts DESC;

-- 3. High-risk customer queue
SELECT * FROM customer_financial_crime_intelligence
WHERE financial_crime_risk_level IN ('High','Critical')
ORDER BY financial_crime_risk_score DESC;

-- 4. Financial-crime alerts by category
SELECT risk_category, COUNT(*) AS alerts, SUM(alert_amount) AS alerted_amount
FROM financial_crime_alerts_enriched
GROUP BY risk_category ORDER BY alerts DESC;

-- 5. Top risk drivers
SELECT risk_driver, COUNT(*) AS alerts
FROM financial_crime_alerts_enriched
GROUP BY risk_driver ORDER BY alerts DESC;

-- 6. Escalation rate by category
SELECT risk_category, COUNT(*) AS alerts,
       AVG(escalated_flag * 1.0) AS escalation_rate
FROM financial_crime_alerts_enriched
GROUP BY risk_category ORDER BY escalation_rate DESC;

-- 7. High-risk geographic exposure
SELECT customer_id, high_risk_geo_transactions, total_transactions,
       high_risk_geo_ratio
FROM customer_financial_crime_intelligence
ORDER BY high_risk_geo_ratio DESC;

-- 8. Common counterparties
SELECT * FROM counterparty_network_summary
WHERE connected_customers >= 5
ORDER BY connected_customers DESC, total_amount DESC;

-- 9. Network review candidates
SELECT * FROM counterparty_network_summary
WHERE network_review_flag = 1
ORDER BY connected_customers DESC;

-- 10. Closed customers with repeated alert behavior
SELECT customer_id, total_alerts, escalated_alerts, unique_risk_categories,
       financial_crime_risk_score
FROM customer_financial_crime_intelligence
WHERE total_alerts >= 3
ORDER BY escalated_alerts DESC;

-- 11. Monthly financial-crime trend
SELECT DATE_TRUNC('month', alert_date) AS month,
       COUNT(*) AS alerts,
       SUM(escalated_flag) AS escalations
FROM financial_crime_alerts_enriched
GROUP BY DATE_TRUNC('month', alert_date)
ORDER BY month;

-- 12. Customer segment risk concentration
SELECT customer_segment, COUNT(*) AS customers,
       AVG(financial_crime_risk_score) AS avg_risk_score,
       SUM(total_alerted_amount) AS alerted_amount
FROM customer_financial_crime_intelligence
GROUP BY customer_segment;
