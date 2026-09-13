# Financial Crime Intelligence & Risk Analytics

**Project 7 — Financial Crime Analyst Portfolio**

This project connects AML, fraud, sanctions and KYC/EDD risk signals into a broader customer-level financial-crime view. It complements Projects 1–6 rather than rebuilding their individual workflows.

## Scale
- 1,200 synthetic customers
- 30,000 synthetic transactions
- 1,800 financial-crime alerts
- 420 escalated cases
- 6,440 counterparties analyzed

## Business Questions
- Which customers have multiple financial-crime indicators?
- Which customers repeatedly generate alerts?
- Which risk categories and drivers create the greatest exposure?
- Which customers combine high transaction exposure with elevated financial-crime risk?
- Which counterparties connect multiple customers and deserve analyst review?
- Where is risk concentrated by segment and time?

## Tools
SQL, Python, Tableau, Streamlit.

## KPI Scorecard
1. Total Customers
2. Financial Crime Alerts
3. High-Risk Customers
4. Escalated Cases
5. Repeat-Alert Customers
6. High-Risk Exposure

## Executive Dashboard — 6 Visualizations
1. Financial Crime Risk Trend
2. Financial Crime Risk Categories
3. Top 5 Financial Crime Risk Drivers
4. Risk Activity Heatmap
5. Customer Risk vs Transaction Exposure
6. Repeat-Alert & Multi-Risk Customers

Dashboard colors: blue + orange. Dates use MM/YY such as 07/26.

## Dashboard Preview

The visuals below come directly from the approved executive dashboard and summarize the project's main financial-crime intelligence findings.

### KPI Scorecard

![Financial Crime Intelligence KPI Scorecard](images/01_kpi_scorecard.png)

**What it represents:** Provides a quick view of total customers, financial-crime alerts, escalated cases, SAR filings, repeat-alert customers, and high-risk exposure.

### Executive Dashboard

![Financial Crime Intelligence Executive Dashboard](images/02_executive_dashboard.png)

**What it represents:** Combines financial-crime trends, risk categories, geographic exposure, customer-risk activity, investigation outcomes, and product exposure in one executive view.

### Financial Crime Activity Trend

![Financial Crime Activity Trend](images/03_financial_crime_activity_trend.png)

**What it represents:** Tracks monthly alerts, escalated cases, and SAR filings to show how financial-crime activity and investigative outcomes change over time.

### Alerts by Risk Category

![Alerts by Risk Category](images/04_alerts_by_risk_category.png)

**What it represents:** Shows how alerts are distributed across Transaction Monitoring, Fraud, Sanctions, KYC/Customer Risk, P2P/Account Takeover, and other risk categories.

### Alerts by Region

![Alerts by Region](images/05_alerts_by_region.png)

**What it represents:** Highlights where financial-crime alerts are concentrated geographically and identifies the regions generating the highest alert volumes.

### Investigation Funnel

![Investigation Funnel](images/06_investigation_funnel.png)

**What it represents:** Shows how alerts move from initial detection through review, escalation, investigation, and SAR filing.


## Disclaimer
All customers, transactions, alerts and cases are synthetic and created for educational portfolio use only.


# Tableau Story Expansion

Project 7 now includes an **8-point Tableau Story** in addition to the executive dashboard:

1. Executive Overview
2. Financial Crime Risk Trends
3. Customer Risk Segmentation
4. Geographic / Regional Risk
5. Product & Channel Exposure
6. Investigation Funnel
7. Repeat-Alert & Counterparty Intelligence
8. Key Findings & Recommended Actions


The story is designed to show how a Financial Crime Analyst moves from broad portfolio signals to investigation priorities and actionable recommendations.
