# Financial Crime Intelligence & Risk Analytics

**Financial Crime Analytics Portfolio Project**

An end-to-end financial-crime intelligence project using **Python, SQL,
Tableau, and Streamlit** to combine AML, fraud, sanctions,
KYC/customer-risk, transaction, geographic, product, and counterparty
signals into an explainable customer-level risk and
investigation-prioritization view.

> **Portfolio scope:** All data is synthetic and created for educational
> and portfolio demonstration. Risk scores, prioritization rules,
> alerts, cases, and investigation outcomes are illustrative.

------------------------------------------------------------------------

## Project Overview

Financial-crime teams often investigate risk across separate alert types
and systems. This project brings those signals together into a broader
intelligence layer so an analyst can identify repeat activity, multiple
risk categories, elevated geographic exposure, counterparty
concentration, and customers requiring focused investigation.

The project contains:

-   **1,200 synthetic customers**
-   **30,000 transactions**
-   **1,800 financial-crime alerts**
-   **420 investigation cases**
-   **6,440 counterparties in the derived network summary**
-   Product and regional risk summary layers
-   A customer-level financial-crime intelligence dataset with
    engineered risk features

The analytical workflow moves from operational records to enriched
alerts, customer intelligence, risk prioritization, and executive
reporting.

------------------------------------------------------------------------

## Business & Investigation Questions

This project answers questions such as:

-   Which customers have multiple financial-crime indicators?
-   Which customers repeatedly generate alerts?
-   Which High/Critical customers should be prioritized?
-   Which risk categories and drivers generate the most alerts?
-   Where is financial-crime activity geographically concentrated?
-   Which products or channels carry the greatest high-risk exposure?
-   Which counterparties connect multiple customers?
-   Which counterparties warrant network review?
-   How do alerts progress into escalations and investigations?
-   How can customer, alert, transaction, counterparty, product, and
    regional signals be combined into an investigation queue?

------------------------------------------------------------------------

## Data Model

  --------------------------------------------------------------------------
  Dataset                                       Rows Purpose
  --------------------- ---------------------------- -----------------------
  Customer reference                           1,200 Customer profile and
                                                     KYC-risk context

  Transactions                                30,000 Customer/counterparty
                                                     transaction activity

  Financial-crime                              1,800 Alert-level risk and
  alerts                                             investigation signals

  Investigation cases                            420 Case-level
                                                     financial-crime review

  Counterparty network                         6,440 Relationship and
  summary                                            concentration analysis

  Customer                                     1,200 Analytics-ready
  financial-crime                                    customer risk layer
  intelligence                                       

  Product exposure                                 6 Product/channel
  summary                                            exposure

  Regional risk summary                           10 Geographic risk
                                                     concentration
  --------------------------------------------------------------------------

See [`docs/data_dictionary.md`](docs/data_dictionary.md) for the
field-level definitions and dataset relationships.

------------------------------------------------------------------------

## Exploratory Data Analysis

The notebook preserves the original project analysis and adds a
straightforward, recruiter-friendly EDA workflow:

-   Dataset and schema review
-   Missing-value analysis
-   Duplicate validation
-   Datatype and range review
-   Summary statistics
-   IQR-based outlier review
-   Business-rule validation
-   KPI validation
-   Final analytical-dataset validation

Unusual financial activity is reviewed as a potential investigation
signal rather than automatically deleted as an outlier.

------------------------------------------------------------------------

## Feature Engineering

The customer intelligence layer contains explainable analytical features
including:

-   `total_alerts`
-   `escalated_alerts`
-   `total_alerted_amount`
-   `avg_alert_risk`
-   `unique_risk_categories`
-   `unique_risk_drivers`
-   `total_transactions`
-   `total_transaction_amount`
-   `high_risk_geo_transactions`
-   `unique_counterparties`
-   `high_risk_geo_ratio`
-   `financial_crime_risk_score`
-   `financial_crime_risk_level`

The notebook explicitly demonstrates three simple engineered features:

-   **`multi_risk_flag`** --- identifies customers associated with
    multiple financial-crime risk categories.
-   **`repeat_alert_flag`** --- identifies customers with repeated alert
    activity.
-   **`risk_score_band`** --- converts the existing financial-crime risk
    score into explainable Lower, Medium, and Higher analytical bands.

These features are intentionally simple and interpretable for
investigation prioritization.

------------------------------------------------------------------------

## SQL Analysis

The project contains **12 focused SQL analyses**, including:

1.  Multi-risk customers
2.  Repeat-alert customers
3.  High-risk customer queue
4.  Alerts by financial-crime category
5.  Top risk drivers
6.  Escalation rate by category
7.  High-risk geographic exposure
8.  Common counterparties
9.  Network-review candidates
10. Customers with repeated alert behavior
11. Monthly financial-crime trends
12. Customer-segment risk concentration

See [`sql/`](sql/) for the complete queries.

------------------------------------------------------------------------

## Verified Portfolio KPIs

The following results were recalculated from the current processed CSVs:

  KPI                                  Current Result
  ---------------------------------- ----------------
  Total Customers                           **1,200**
  Financial Crime Alerts                    **1,800**
  Investigation Cases                         **420**
  Alert-Level Escalations                     **648**
  High/Critical Customers                     **159**
  Repeat-Alert Customers                      **230**
  Multi-Risk Customers                        **420**
  Total Alerted Amount                    **\$82.0M**
  Product-Level High-Risk Exposure       **\$210.2M**
  Network Review Candidates                 **2,457**

------------------------------------------------------------------------

## Key Findings

-   **230 customers** are flagged for repeat-alert behavior, helping
    investigators focus on recurring activity.
-   **420 customers** show multiple financial-crime risk signals and are
    candidates for cross-risk review.
-   The largest alert category is **Transaction Monitoring (763
    alerts)**.
-   The leading alert driver is **Unusual Volume (202 alerts)**.
-   The regional summary identifies **United States** as the largest
    alert concentration with **895 alerts**.
-   **2,457 counterparties** are flagged as network-review candidates in
    the derived network layer.
-   Product-level high-risk exposure totals approximately **$210.2M**
    across the six summarized product/channel groups.

These findings are designed to support investigation prioritization and
cross-risk intelligence rather than automatic customer disposition.

------------------------------------------------------------------------

## Streamlit Decision-Support Application

The Streamlit application applies portfolio filters across the customer
and alert populations.

### Filters

-   Date / Month
-   Customer Segment
-   Product Type
-   Risk Rating
-   Region

The Product Type logic normalizes activity into:

-   Wire Transfer
-   ACH
-   ATM
-   P2P
-   Cash
-   Trade Finance

### Portfolio Decision Support

The application summarizes the selected population as:

-   **Generally Stable**
-   **Targeted Review Recommended**
-   **Heightened Financial Crime Risk**

The assessment considers High/Critical concentration, repeat-alert
activity, multi-risk customers, and escalations.

### Customer Investigation Summary

At customer level, the application provides:

-   Risk level
-   Risk score
-   Total alerts
-   Alerted exposure
-   Escalated alerts
-   Repeat-alert behavior
-   Multi-risk behavior
-   Main risk category
-   Leading risk driver

It then produces an explainable portfolio decision:

-   **Priority Investigation**
-   **Enhanced Review**
-   **Targeted Review**
-   **Routine Monitoring**

### Interactive Analysis

The application includes:

-   Risk Queue
-   Multi-Risk Analysis
-   Counterparty Intelligence
-   Tableau Gallery
-   Interactive Story Walkthrough

The **Tableau Gallery intentionally displays only the Executive
Dashboard**. The Story Walkthrough uses filtered Streamlit analysis
rather than repeating static dashboard images.

------------------------------------------------------------------------

## Tableau Executive Dashboard

The executive dashboard brings the portfolio into one visual
decision-support view.

### Dashboard Components

1.  Financial Crime Activity Trend
2.  Alerts by Risk Category
3.  Alerts by Region
4.  Customer Risk Activity Heatmap
5.  Investigation Funnel
6.  Crime Exposure by Product Type

### Dashboard Preview

![Financial Crime Intelligence & Risk Analytics Dashboard](images/02_executive_dashboard.png)

> **Dashboard status:** The Executive Dashboard is synchronized to the current processed-data KPIs used throughout this README and the Streamlit application.

------------------------------------------------------------------------

## Financial Crime Intelligence Workflow

``` text
Customer Profile
       ↓
Transactions
       ↓
Financial Crime Alerts
       ↓
Investigation Cases
       ↓
EDA + Feature Engineering
       ↓
Customer Risk Intelligence
       ↓
Counterparty / Product / Regional Analysis
       ↓
Risk & Investigation Prioritization
       ↓
Tableau + Streamlit Decision Support
```

------------------------------------------------------------------------

## Tools & Technologies

  -----------------------------------------------------------------------
  Tool                                Application
  ----------------------------------- -----------------------------------
  **Python / Pandas**                 EDA, feature engineering,
                                      validation and intelligence
                                      analysis

  **SQL**                             Risk queues, trends, exposure,
                                      counterparties and alert analysis

  **Tableau**                         Executive financial-crime dashboard

  **Streamlit**                       Interactive investigation and
                                      portfolio decision support

  **Jupyter Notebook**                Reproducible analytical workflow

  **Git / GitHub**                    Version control and portfolio
                                      presentation
  -----------------------------------------------------------------------

------------------------------------------------------------------------

## Repository Structure

``` text
Financial-Crime/
├── app/             # Streamlit application
├── data/            # Synthetic source and processed datasets
├── docs/            # Data dictionary / supporting documentation
├── images/          # Executive dashboard
├── notebooks/       # EDA, feature engineering and intelligence analysis
├── sql/             # Financial-crime analytical queries
├── src/             # Supporting project logic
├── tableau/         # Tableau workbook / assets
├── .gitignore
├── .python-version
├── main.py
├── pyproject.toml
├── requirements.txt
├── uv.lock
└── README.md
```

------------------------------------------------------------------------

## How to Run

``` bash
git clone https://github.com/Denis0242/Financial-Crime.git
cd Financial-Crime
pip install -r requirements.txt
streamlit run app/streamlit_app.py
```

------------------------------------------------------------------------

## Skills Demonstrated

### Financial Crime / AML

-   Financial Crime Intelligence
-   AML Investigation Analytics
-   Transaction Monitoring Analytics
-   Fraud Risk Analysis
-   Sanctions Risk Analysis
-   KYC / Customer Risk
-   Alert & Case Analysis
-   Repeat-Alert Analysis
-   Multi-Risk Analysis
-   Counterparty / Network Intelligence
-   Geographic Risk Analysis
-   Product / Channel Exposure
-   Investigation Prioritization

### Data & Analytics

-   Exploratory Data Analysis
-   Feature Engineering
-   Data Quality Validation
-   SQL
-   Python / Pandas
-   Risk Scoring
-   KPI Development
-   Trend Analysis
-   Segmentation
-   Business-Rule Validation

### Visualization & Decision Support

-   Tableau
-   Streamlit
-   Executive Dashboards
-   Interactive Filtering
-   Customer-Level Investigation Views
-   Risk Queues
-   Data Storytelling

------------------------------------------------------------------------

## Disclaimer

This project uses **synthetic data** created for educational and
portfolio purposes. No real customer, account, transaction, alert, case,
counterparty, SAR, or confidential financial-institution data is
included.

Financial-crime risk scores, alert categories, engineered features,
prioritization logic, investigation outcomes, exposure measures, and
decision-support labels are illustrative and should not be interpreted
as actual financial-institution policies, regulatory determinations, or
production monitoring rules.
