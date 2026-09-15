# Data Dictionary

## Financial Crime Analytics & Intelligence

This data dictionary documents the customer, transaction, alert, investigation-case, counterparty-network, product-exposure, regional-risk, and financial-crime intelligence datasets used in this portfolio project. It distinguishes operational fields from enriched and engineered analytical features so the project's EDA, feature engineering, and financial-crime analytics work is visible to reviewers.

> **Portfolio note:** These datasets are structured for analytical demonstration. Definitions reflect their use within this project and do not represent any specific financial institution's production data standards.

## Dataset Overview

| Dataset | Rows | Columns | Purpose |
|---|---:|---:|---|
| `cases.csv` | 420 | 7 | Investigation-case dataset containing case-level financial-crime review information. |
| `customers(20260914-025211).csv` | 1,200 | 7 | Customer reference dataset providing profile and risk context. |
| `financial_crime_alerts.csv` | 1,800 | 10 | Alert-level dataset containing financial-crime alerts generated for investigation. |
| `transactions(20260914-025211).csv` | 30,000 | 9 | Transaction-level dataset used to analyze customer and counterparty activity. |
| `cases(1).csv` | 420 | 8 | Additional case-level dataset used in the project's investigation and analytical workflow. |
| `counterparty_network_summary.csv` | 6,440 | 6 | Derived counterparty/network summary used to identify concentration and relationship patterns. |
| `customer_financial_crime_intelligence.csv` | 1,200 | 22 | Analytics-ready customer intelligence layer combining financial-crime indicators and derived risk measures. |
| `financial_crime_alerts_enriched.csv` | 1,800 | 10 | Enriched alert dataset combining alert information with additional analytical context. |
| `product_exposure_summary.csv` | 6 | 7 | Aggregated dataset used to analyze financial-crime exposure across products or channels. |
| `regional_risk_summary.csv` | 10 | 5 | Aggregated dataset used to analyze geographic concentration and regional financial-crime risk. |

## `cases.csv`

Investigation-case dataset containing case-level financial-crime review information.

| Column | Data Type | Classification | Description | Example |
|---|---|---|---|---|
| `case_id` | String | Source / Operational | Unique identifier assigned to the investigation case. | `CASE0001` |
| `alert_id` | String | Source / Operational | Unique identifier assigned to the financial-crime alert. | `FCA00736` |
| `customer_id` | String | Source / Operational | Unique identifier assigned to the customer. | `CUST10449` |
| `risk_category` | String | Source / Operational | Attribute used to assess risk category. | `Transaction Monitoring` |
| `case_risk_score` | Float | Derived / Analytical | Numeric analytical score representing case risk. | `40` |
| `case_age_days` | Integer | Source / Operational | Field representing case age days within the financial-crime analytics workflow. | `12` |
| `case_status` | String | Source / Operational | Current or final status of the investigation case. | `In Review` |

## `customers(20260914-025211).csv`

Customer reference dataset providing profile and risk context.

| Column | Data Type | Classification | Description | Example |
|---|---|---|---|---|
| `customer_id` | String | Source / Operational | Unique identifier assigned to the customer. | `CUST10000` |
| `customer_name` | String | Source / Operational | Customer or legal-entity name. | `Customer 0001` |
| `customer_segment` | String | Source / Operational | Field representing customer segment within the financial-crime analytics workflow. | `Commercial` |
| `country` | String | Derived / Analytical | Country associated with the customer, counterparty, or activity. | `United States` |
| `kyc_risk` | String | Source / Operational | Attribute used to assess kyc risk. | `Low` |
| `pep_flag` | Integer | Source / Operational | Indicator identifying whether pep applies. | `0` |
| `expected_monthly_volume` | Float | Source / Operational | Field representing expected monthly volume within the financial-crime analytics workflow. | `21083.82` |

## `financial_crime_alerts.csv`

Alert-level dataset containing financial-crime alerts generated for investigation.

| Column | Data Type | Classification | Description | Example |
|---|---|---|---|---|
| `alert_id` | String | Source / Operational | Unique identifier assigned to the financial-crime alert. | `FCA00001` |
| `customer_id` | String | Source / Operational | Unique identifier assigned to the customer. | `CUST10827` |
| `alert_date` | String | Source / Operational | Date on which the financial-crime alert was generated. | `2026-01-03` |
| `risk_category` | String | Source / Operational | Attribute used to assess risk category. | `Transaction Monitoring` |
| `risk_driver` | String | Source / Operational | Attribute used to assess risk driver. | `Unusual Volume` |
| `risk_score` | Float | Derived / Analytical | Numeric score representing assessed financial-crime risk. | `44` |
| `alert_amount` | Float | Source / Operational | Field representing alert amount within the financial-crime analytics workflow. | `8968.47` |
| `disposition` | String | Source / Operational | Final review or investigation outcome. | `Closed - Explained` |
| `escalated_flag` | Integer | Source / Operational | Indicator identifying whether escalated applies. | `0` |
| `month` | String | Source / Operational | Field representing month within the financial-crime analytics workflow. | `2026-01` |

## `transactions(20260914-025211).csv`

Transaction-level dataset used to analyze customer and counterparty activity.

| Column | Data Type | Classification | Description | Example |
|---|---|---|---|---|
| `transaction_id` | String | Source / Operational | Unique identifier assigned to the transaction. | `TX500000` |
| `customer_id` | String | Source / Operational | Unique identifier assigned to the customer. | `CUST10629` |
| `transaction_date` | String | Source / Operational | Date on which the transaction occurred. | `2026-01-12` |
| `channel` | String | Source / Operational | Field representing channel within the financial-crime analytics workflow. | `Card` |
| `direction` | String | Source / Operational | Field representing direction within the financial-crime analytics workflow. | `Debit` |
| `amount` | Float | Source / Operational | Monetary value associated with the transaction or activity. | `11174.09` |
| `counterparty_id` | String | Derived / Analytical | Unique identifier assigned to a transaction counterparty. | `CP04321` |
| `counterparty_country` | String | Derived / Analytical | Country associated with the counterparty. | `Russia` |
| `high_risk_geo_flag` | Integer | Source / Operational | Indicator identifying whether high risk geo applies. | `1` |

## `cases(1).csv`

Additional case-level dataset used in the project's investigation and analytical workflow.

| Column | Data Type | Classification | Description | Example |
|---|---|---|---|---|
| `case_id` | String | Source / Operational | Unique identifier assigned to the investigation case. | `CASE0001` |
| `alert_id` | String | Source / Operational | Unique identifier assigned to the financial-crime alert. | `FCA00736` |
| `customer_id` | String | Source / Operational | Unique identifier assigned to the customer. | `CUST10449` |
| `risk_category` | String | Source / Operational | Attribute used to assess risk category. | `Transaction Monitoring` |
| `case_risk_score` | Float | Derived / Analytical | Numeric analytical score representing case risk. | `40` |
| `case_age_days` | Integer | Source / Operational | Field representing case age days within the financial-crime analytics workflow. | `12` |
| `case_status` | String | Source / Operational | Current or final status of the investigation case. | `In Review` |
| `investigation_outcome` | String | Source / Operational | Field representing investigation outcome within the financial-crime analytics workflow. | `Further Investigation` |

## `counterparty_network_summary.csv`

Derived counterparty/network summary used to identify concentration and relationship patterns.

| Column | Data Type | Classification | Description | Example |
|---|---|---|---|---|
| `counterparty_id` | String | Derived / Analytical | Unique identifier assigned to a transaction counterparty. | `CP00001` |
| `connected_customers` | Integer | Derived / Analytical | Field representing connected customers within the financial-crime analytics workflow. | `4` |
| `transaction_count` | Integer | Derived / Analytical | Count used to measure transaction count. | `4` |
| `total_amount` | Float | Derived / Analytical | Aggregated total representing amount. | `10806.46` |
| `high_risk_geo_transactions` | Integer | Derived / Analytical | Attribute used to assess high risk geo transactions. | `0` |
| `network_review_flag` | Integer | Derived / Analytical | Indicator identifying whether network review applies. | `0` |

## `customer_financial_crime_intelligence.csv`

Analytics-ready customer intelligence layer combining financial-crime indicators and derived risk measures.

| Column | Data Type | Classification | Description | Example |
|---|---|---|---|---|
| `customer_id` | String | Derived / Analytical | Unique identifier assigned to the customer. | `CUST10000` |
| `customer_name` | String | Derived / Analytical | Customer or legal-entity name. | `Customer 0001` |
| `customer_segment` | String | Derived / Analytical | Field representing customer segment within the financial-crime analytics workflow. | `Commercial` |
| `country` | String | Derived / Analytical | Country associated with the customer, counterparty, or activity. | `United States` |
| `kyc_risk` | String | Derived / Analytical | Attribute used to assess kyc risk. | `Low` |
| `pep_flag` | Integer | Derived / Analytical | Indicator identifying whether pep applies. | `0` |
| `expected_monthly_volume` | Float | Derived / Analytical | Field representing expected monthly volume within the financial-crime analytics workflow. | `21083.82` |
| `total_alerts` | Float | Derived / Analytical | Aggregated total representing alerts. | `1` |
| `escalated_alerts` | Float | Derived / Analytical | Field representing escalated alerts within the financial-crime analytics workflow. | `0` |
| `total_alerted_amount` | Float | Derived / Analytical | Aggregated total representing alerted amount. | `4984.85` |
| `avg_alert_risk` | Float | Derived / Analytical | Average measure representing alert risk. | `72` |
| `unique_risk_categories` | Float | Derived / Analytical | Attribute used to assess unique risk categories. | `1` |
| `unique_risk_drivers` | Float | Derived / Analytical | Attribute used to assess unique risk drivers. | `1` |
| `total_transactions` | Integer | Derived / Analytical | Aggregated total representing transactions. | `31` |
| `total_transaction_amount` | Float | Derived / Analytical | Aggregated total representing transaction amount. | `446249.67` |
| `high_risk_geo_transactions` | Integer | Derived / Analytical | Attribute used to assess high risk geo transactions. | `12` |
| `unique_counterparties` | Integer | Derived / Analytical | Count used to measure unique counterparties. | `31` |
| `repeat_alert_flag` | Integer | Derived / Analytical | Indicator identifying whether repeat alert applies. | `0` |
| `multi_risk_flag` | Integer | Derived / Analytical | Indicator identifying whether multi risk applies. | `0` |
| `high_risk_geo_ratio` | Float | Derived / Analytical | Derived measure representing high risk geo ratio. | `0.3871` |
| `financial_crime_risk_score` | Float | Derived / Analytical | Numeric analytical score representing financial crime risk. | `21` |
| `financial_crime_risk_level` | String | Derived / Analytical | Attribute used to assess financial crime risk level. | `Low` |

## `financial_crime_alerts_enriched.csv`

Enriched alert dataset combining alert information with additional analytical context.

| Column | Data Type | Classification | Description | Example |
|---|---|---|---|---|
| `alert_id` | String | Source / Operational | Unique identifier assigned to the financial-crime alert. | `FCA00001` |
| `customer_id` | String | Source / Operational | Unique identifier assigned to the customer. | `CUST10827` |
| `alert_date` | String | Enriched / Analytical | Date on which the financial-crime alert was generated. | `2026-01-03` |
| `risk_category` | String | Enriched / Analytical | Attribute used to assess risk category. | `Transaction Monitoring` |
| `risk_driver` | String | Enriched / Analytical | Attribute used to assess risk driver. | `Unusual Volume` |
| `risk_score` | Float | Enriched / Analytical | Numeric score representing assessed financial-crime risk. | `44` |
| `alert_amount` | Float | Enriched / Analytical | Field representing alert amount within the financial-crime analytics workflow. | `8968.47` |
| `disposition` | String | Enriched / Analytical | Final review or investigation outcome. | `Closed - Explained` |
| `escalated_flag` | Integer | Enriched / Analytical | Indicator identifying whether escalated applies. | `0` |
| `month` | String | Enriched / Analytical | Field representing month within the financial-crime analytics workflow. | `2026-01` |

## `product_exposure_summary.csv`

Aggregated dataset used to analyze financial-crime exposure across products or channels.

| Column | Data Type | Classification | Description | Example |
|---|---|---|---|---|
| `product_type` | String | Derived / Analytical | Financial product or transaction-channel classification. | `ACH Transfer` |
| `transaction_count` | Integer | Derived / Analytical | Count used to measure transaction count. | `6591` |
| `transaction_amount` | Float | Derived / Analytical | Monetary value associated with the transaction. | `74991555.76` |
| `high_risk_geo_transactions` | Integer | Derived / Analytical | Attribute used to assess high risk geo transactions. | `2604` |
| `avg_customer_alert_risk` | Float | Derived / Analytical | Average measure representing customer alert risk. | `45.3382` |
| `escalations` | Float | Derived / Analytical | Field representing escalations within the financial-crime analytics workflow. | `3510` |
| `high_risk_exposure` | Float | Derived / Analytical | Attribute used to assess high risk exposure. | `45248537.83` |

## `regional_risk_summary.csv`

Aggregated dataset used to analyze geographic concentration and regional financial-crime risk.

| Column | Data Type | Classification | Description | Example |
|---|---|---|---|---|
| `country` | String | Derived / Analytical | Country associated with the customer, counterparty, or activity. | `United States` |
| `alerts` | Integer | Derived / Analytical | Field representing alerts within the financial-crime analytics workflow. | `895` |
| `escalations` | Integer | Derived / Analytical | Field representing escalations within the financial-crime analytics workflow. | `318` |
| `alerted_amount` | Float | Derived / Analytical | Field representing alerted amount within the financial-crime analytics workflow. | `39163449.48` |
| `avg_risk` | Float | Derived / Analytical | Average measure representing risk. | `58.1732` |

## Dataset Relationships

- `cases.csv.customer_id` ↔ `customers(20260914-025211).csv.customer_id` provides a shared identifier for analysis and joins.
- `cases.csv.alert_id` ↔ `financial_crime_alerts.csv.alert_id` provides a shared identifier for analysis and joins.
- `cases.csv.customer_id` ↔ `financial_crime_alerts.csv.customer_id` provides a shared identifier for analysis and joins.
- `cases.csv.customer_id` ↔ `transactions(20260914-025211).csv.customer_id` provides a shared identifier for analysis and joins.
- `cases.csv.case_id` ↔ `cases(1).csv.case_id` provides a shared identifier for analysis and joins.
- `cases.csv.alert_id` ↔ `cases(1).csv.alert_id` provides a shared identifier for analysis and joins.
- `cases.csv.customer_id` ↔ `cases(1).csv.customer_id` provides a shared identifier for analysis and joins.
- `cases.csv.customer_id` ↔ `customer_financial_crime_intelligence.csv.customer_id` provides a shared identifier for analysis and joins.
- `cases.csv.alert_id` ↔ `financial_crime_alerts_enriched.csv.alert_id` provides a shared identifier for analysis and joins.
- `cases.csv.customer_id` ↔ `financial_crime_alerts_enriched.csv.customer_id` provides a shared identifier for analysis and joins.
- `customers(20260914-025211).csv.customer_id` ↔ `financial_crime_alerts.csv.customer_id` provides a shared identifier for analysis and joins.
- `customers(20260914-025211).csv.customer_id` ↔ `transactions(20260914-025211).csv.customer_id` provides a shared identifier for analysis and joins.
- `customers(20260914-025211).csv.customer_id` ↔ `cases(1).csv.customer_id` provides a shared identifier for analysis and joins.
- `customers(20260914-025211).csv.customer_id` ↔ `customer_financial_crime_intelligence.csv.customer_id` provides a shared identifier for analysis and joins.
- `customers(20260914-025211).csv.customer_id` ↔ `financial_crime_alerts_enriched.csv.customer_id` provides a shared identifier for analysis and joins.
- `financial_crime_alerts.csv.customer_id` ↔ `transactions(20260914-025211).csv.customer_id` provides a shared identifier for analysis and joins.
- `financial_crime_alerts.csv.alert_id` ↔ `cases(1).csv.alert_id` provides a shared identifier for analysis and joins.
- `financial_crime_alerts.csv.customer_id` ↔ `cases(1).csv.customer_id` provides a shared identifier for analysis and joins.
- `financial_crime_alerts.csv.customer_id` ↔ `customer_financial_crime_intelligence.csv.customer_id` provides a shared identifier for analysis and joins.
- `financial_crime_alerts.csv.alert_id` ↔ `financial_crime_alerts_enriched.csv.alert_id` provides a shared identifier for analysis and joins.
- `financial_crime_alerts.csv.customer_id` ↔ `financial_crime_alerts_enriched.csv.customer_id` provides a shared identifier for analysis and joins.
- `transactions(20260914-025211).csv.customer_id` ↔ `cases(1).csv.customer_id` provides a shared identifier for analysis and joins.
- `transactions(20260914-025211).csv.counterparty_id` ↔ `counterparty_network_summary.csv.counterparty_id` provides a shared identifier for analysis and joins.
- `transactions(20260914-025211).csv.customer_id` ↔ `customer_financial_crime_intelligence.csv.customer_id` provides a shared identifier for analysis and joins.
- `transactions(20260914-025211).csv.customer_id` ↔ `financial_crime_alerts_enriched.csv.customer_id` provides a shared identifier for analysis and joins.
- `cases(1).csv.customer_id` ↔ `customer_financial_crime_intelligence.csv.customer_id` provides a shared identifier for analysis and joins.
- `cases(1).csv.alert_id` ↔ `financial_crime_alerts_enriched.csv.alert_id` provides a shared identifier for analysis and joins.
- `cases(1).csv.customer_id` ↔ `financial_crime_alerts_enriched.csv.customer_id` provides a shared identifier for analysis and joins.
- `customer_financial_crime_intelligence.csv.customer_id` ↔ `financial_crime_alerts_enriched.csv.customer_id` provides a shared identifier for analysis and joins.

## Financial Crime Analytics Workflow

**Customer Profile → Transactions → Financial Crime Alerts → Case Investigation → Enrichment → Counterparty / Product / Regional Analysis → Financial Crime Intelligence**

This layered structure supports both investigation analytics and broader financial-crime intelligence. Operational records provide the foundation, enriched alert data adds investigative context, and summary/intelligence tables convert detailed records into features and KPIs suitable for pattern detection, trend analysis, risk prioritization, and dashboards.

## EDA & Feature Engineering Context

The project supports exploratory analysis across transaction behavior, alerts, cases, counterparties, products, and geography. Fields classified as **Derived / Analytical** or **Enriched / Analytical** make the feature-engineering layer explicit. These features support identification of unusual activity, customer-risk prioritization, network exposure analysis, product/channel concentration, and regional-risk patterns.

## Data Quality Conventions

- Validate entity identifiers for uniqueness within their natural source tables before joining datasets.
- Check transaction amounts and derived monetary metrics for missing, negative, duplicate, or implausible values.
- Standardize dates before time-series and investigation-lifecycle analysis.
- Standardize categorical fields such as product, region, status, disposition, and risk classification before aggregation.
- Validate enriched and aggregated metrics against their underlying source records.
- Treat missing values according to business meaning; not every null necessarily represents a data-quality failure.
- Review derived risk features for consistency with documented project business rules.

---

*Prepared for the Financial Crime Analytics & Intelligence GitHub portfolio project.*