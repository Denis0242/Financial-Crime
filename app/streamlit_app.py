from pathlib import Path
import streamlit as st
import pandas as pd

# =========================================================
# DATA
# =========================================================
ROOT = Path(__file__).resolve().parents[1]

C = pd.read_csv(ROOT / "data/processed/customer_financial_crime_intelligence.csv")
A = pd.read_csv(ROOT / "data/processed/financial_crime_alerts_enriched.csv")
N = pd.read_csv(ROOT / "data/processed/counterparty_network_summary.csv")

st.set_page_config(
    page_title="Financial Crime Intelligence & Risk Analytics",
    layout="wide"
)

# =========================================================
# HELPERS
# =========================================================
def find_col(df, candidates):
    """Return the first matching column, case-insensitive."""
    if df is None or df.empty and len(df.columns) == 0:
        return None

    lookup = {str(c).lower(): c for c in df.columns}

    for candidate in candidates:
        if candidate.lower() in lookup:
            return lookup[candidate.lower()]

    return None


def clean_options(series):
    values = (
        series.dropna()
        .astype(str)
        .str.strip()
    )
    values = values[values.ne("")]
    return sorted(values.unique().tolist())


PRODUCT_TYPES = [
    "Wire Transfer",
    "ACH",
    "ATM",
    "P2P",
    "Cash",
    "Trade Finance",
]


def classify_product_value(value):
    """Map raw product/transaction text into the six portfolio product groups."""
    if pd.isna(value):
        return None

    s = str(value).strip().lower()

    # Order matters: specific categories first.
    if any(k in s for k in [
        "trade finance", "letter of credit", "letters of credit",
        "documentary collection", "trade-based", "trade based",
        "invoice", "shipment"
    ]):
        return "Trade Finance"

    if any(k in s for k in [
        "wire", "swift", "international transfer",
        "domestic transfer", "bank transfer"
    ]):
        return "Wire Transfer"

    if any(k in s for k in [
        "ach", "automated clearing house"
    ]):
        return "ACH"

    if any(k in s for k in [
        "atm", "cash machine"
    ]):
        return "ATM"

    if any(k in s for k in [
        "p2p", "peer-to-peer", "peer to peer",
        "zelle", "venmo", "cash app"
    ]):
        return "P2P"

    if any(k in s for k in [
        "cash", "currency", "teller deposit",
        "teller withdrawal", "cash deposit", "cash withdrawal"
    ]):
        return "Cash"

    return None


def build_product_classification(df):
    """
    Build one normalized product category per alert by checking likely transaction,
    product, channel, scenario, and risk-description fields.
    """
    candidate_names = [
        "product_type", "product", "primary_product", "product_name",
        "transaction_type", "transaction_channel", "payment_type", "channel",
        "alert_type", "scenario", "scenario_name", "risk_driver",
        "risk_category", "description"
    ]

    cols = []
    lookup = {str(c).lower(): c for c in df.columns}

    for name in candidate_names:
        if name.lower() in lookup:
            cols.append(lookup[name.lower()])

    # Also include any column whose name strongly suggests product/transaction/channel.
    for c in df.columns:
        lc = str(c).lower()
        if any(token in lc for token in ["product", "transaction", "payment", "channel", "scenario"]):
            if c not in cols:
                cols.append(c)

    if not cols:
        return pd.Series([None] * len(df), index=df.index, dtype="object")

    def classify_row(row):
        for c in cols:
            category = classify_product_value(row.get(c))
            if category:
                return category
        return None

    return df.apply(classify_row, axis=1)


def safe_sum(df, candidates):
    col = find_col(df, candidates)
    if not col:
        return None
    return pd.to_numeric(df[col], errors="coerce").fillna(0).sum()


def safe_count_true(df, candidates):
    col = find_col(df, candidates)
    if not col:
        return None

    s = df[col]

    if pd.api.types.is_numeric_dtype(s):
        return int(pd.to_numeric(s, errors="coerce").fillna(0).gt(0).sum())

    normalized = s.astype(str).str.strip().str.lower()
    truthy = {
        "1", "true", "yes", "y",
        "escalated", "investigated", "filed",
        "sar filed", "sar_filed"
    }
    return int(normalized.isin(truthy).sum())


def first_existing_image(*relative_paths):
    for rel in relative_paths:
        p = ROOT / rel
        if p.exists():
            return p
    return None


def render_story_image(title, caption, *paths):
    p = first_existing_image(*paths)
    if p:
        st.markdown(f"#### {title}")
        st.image(str(p), use_container_width=True)
        if caption:
            st.caption(caption)


# Candidate columns — allows the app to work even if Region/Product
# are stored in the alert-level file rather than the customer file.
REGION_CANDIDATES = [
    "region", "customer_region", "alert_region", "transaction_region",
    "geographic_region", "geography", "country", "state"
]

PRODUCT_CANDIDATES = [
    "product_type", "product", "primary_product", "transaction_type",
    "payment_type", "channel", "product_name"
]

AMOUNT_CANDIDATES = [
    "alerted_amount", "transaction_amount", "amount",
    "total_alerted_amount", "alert_amount", "usd_amount"
]

COUNTERPARTY_CANDIDATES = [
    "counterparty_id", "counterparty", "beneficiary_id",
    "recipient_id", "connected_counterparty"
]

ALERT_ID_CANDIDATES = ["alert_id", "case_id", "event_id"]
DATE_CANDIDATES = ["alert_date", "transaction_date", "date", "created_date"]

# Prefer alert-level dimensions where available because those are normally
# the correct source for transaction/product/geographic filtering.
region_a = find_col(A, REGION_CANDIDATES)
region_c = find_col(C, REGION_CANDIDATES)
region_source = "A" if region_a else ("C" if region_c else None)
region_col = region_a or region_c

# Build a normalized product category directly from the alert-level data.
# This keeps the Product Type filter active even when the raw data uses
# different field names or labels such as SWIFT, peer-to-peer, or cash deposit.
A["_product_group"] = build_product_classification(A)
product_source = "A"
product_col = "_product_group"

date_col = find_col(A, DATE_CANDIDATES)
customer_id_c = find_col(C, ["customer_id"])
customer_id_a = find_col(A, ["customer_id"])

# =========================================================
# PAGE HEADER
# =========================================================
st.title("Financial Crime Intelligence & Risk Analytics")
st.caption(
    "Synthetic portfolio project | Detect. Investigate. Prioritize. Prevent. "
    "A recruiter-friendly view of portfolio risk, alerts, exposure, escalation, "
    "investigation flow, and repeat-risk behavior."
)

# =========================================================
# VERTICAL SIDEBAR FILTERS
# =========================================================
with st.sidebar:
    st.header("Dashboard Filters")
    st.caption("Use the dropdowns below to filter the entire application.")

    segment_col = find_col(C, ["customer_segment", "segment"])
    risk_col = find_col(C, ["financial_crime_risk_level", "risk_level", "risk_rating"])

    segment_options = ["All"]
    if segment_col:
        segment_options += clean_options(C[segment_col])

    risk_options = ["All"]
    if risk_col:
        risk_options += clean_options(C[risk_col])

    region_df = A if region_source == "A" else C
    region_options = ["All"]
    if region_col:
        region_options += clean_options(region_df[region_col])

    product_df = A
    detected_products = set(
        A["_product_group"].dropna().astype(str).unique().tolist()
    )
    # Keep the requested six product categories visible in the dropdown.
    # Categories with no matching alerts will simply return no records.
    product_options = ["All"] + PRODUCT_TYPES

    month_options = ["All"]
    if date_col:
        parsed_dates = pd.to_datetime(A[date_col], errors="coerce").dropna()
        periods = sorted(parsed_dates.dt.to_period("M").unique(), reverse=True)
        month_options += [p.strftime("%m/%y") for p in periods]

    selected_segment = st.selectbox(
        "Customer Segment",
        segment_options,
        index=0
    )

    selected_risk = st.selectbox(
        "Risk Rating",
        risk_options,
        index=0
    )

    selected_region = st.selectbox(
        "Region",
        region_options,
        index=0,
        disabled=(region_col is None)
    )

    selected_product = st.selectbox(
        "Product Type",
        product_options,
        index=0
    )

    selected_month = st.selectbox(
        "Date (Month/Year)",
        month_options,
        index=0,
        disabled=(date_col is None)
    )

    st.divider()

    # Helpful transparency for development/debugging.
    if region_col:
        st.caption(f"Region source: `{region_source}.{region_col}`")
    else:
        st.caption("Region field not detected.")

    st.caption("Product groups: Wire Transfer, ACH, ATM, P2P, Cash, Trade Finance")

# =========================================================
# APPLY FILTERS TO THE ENTIRE APP
# =========================================================
F = C.copy()
AF = A.copy()

# Customer-level filters
if segment_col and selected_segment != "All":
    F = F[F[segment_col].astype(str).eq(selected_segment)]

if risk_col and selected_risk != "All":
    F = F[F[risk_col].astype(str).eq(selected_risk)]

if region_source == "C" and selected_region != "All":
    F = F[F[region_col].astype(str).eq(selected_region)]

if product_source == "C" and selected_product != "All":
    F = F[F[product_col].astype(str).eq(selected_product)]

# Alert-level filters
if region_source == "A" and selected_region != "All":
    AF = AF[AF[region_col].astype(str).eq(selected_region)]

if product_source == "A" and selected_product != "All":
    AF = AF[AF[product_col].astype(str).eq(selected_product)]

if date_col and selected_month != "All":
    alert_month = pd.to_datetime(AF[date_col], errors="coerce").dt.strftime("%m/%y")
    AF = AF[alert_month.eq(selected_month)]

# First restrict alerts to customer-level selections.
if customer_id_a and customer_id_c:
    customer_ids = set(F[customer_id_c].dropna())
    AF = AF[AF[customer_id_a].isin(customer_ids)]

    # If an alert-level filter was selected, reduce the customer population
    # to customers that actually have matching alerts.
    alert_dimension_filter_active = (
        (region_source == "A" and selected_region != "All")
        or (product_source == "A" and selected_product != "All")
        or (selected_month != "All")
    )

    if alert_dimension_filter_active:
        matching_ids = set(AF[customer_id_a].dropna())
        F = F[F[customer_id_c].isin(matching_ids)]

    # Final synchronization so every section uses the same filtered population.
    final_ids = set(F[customer_id_c].dropna())
    AF = AF[AF[customer_id_a].isin(final_ids)]

# =========================================================
# FILTERED KPI CALCULATIONS
# =========================================================
customers = F[customer_id_c].nunique() if customer_id_c else len(F)

alert_id_col = find_col(AF, ALERT_ID_CANDIDATES)
alerts = AF[alert_id_col].nunique() if alert_id_col else len(AF)

if risk_col:
    high_critical = int(
        F[risk_col].astype(str).str.lower().isin(["high", "critical"]).sum()
    )
else:
    high_critical = 0

# Prefer alert-level escalation fields when available.
escalations = safe_count_true(
    AF,
    ["escalated_flag", "is_escalated", "escalation_flag", "escalated"]
)

if escalations is None:
    escalation_customer_col = find_col(F, ["escalated_alerts"])
    escalations = (
        int(pd.to_numeric(F[escalation_customer_col], errors="coerce").fillna(0).sum())
        if escalation_customer_col else 0
    )

repeat_col = find_col(F, ["repeat_alert_flag"])
repeat_alerts = (
    int(pd.to_numeric(F[repeat_col], errors="coerce").fillna(0).gt(0).sum())
    if repeat_col else 0
)

multi_col = find_col(F, ["multi_risk_flag"])
multi_risk_customers = (
    int(pd.to_numeric(F[multi_col], errors="coerce").fillna(0).gt(0).sum())
    if multi_col else 0
)

alert_amount_col = find_col(AF, AMOUNT_CANDIDATES)
if alert_amount_col:
    alerted_exposure = float(
        pd.to_numeric(AF[alert_amount_col], errors="coerce").fillna(0).sum()
    )
else:
    customer_amount_col = find_col(F, ["total_alerted_amount"])
    alerted_exposure = (
        float(pd.to_numeric(F[customer_amount_col], errors="coerce").fillna(0).sum())
        if customer_amount_col else 0.0
    )

high_critical_pct = (high_critical / customers * 100) if customers else 0.0
repeat_pct = (repeat_alerts / customers * 100) if customers else 0.0
multi_risk_pct = (multi_risk_customers / customers * 100) if customers else 0.0

# =========================================================
# OVERALL ASSESSMENT
# =========================================================
def portfolio_status():
    signals = 0

    if high_critical_pct >= 25:
        signals += 1
    if repeat_pct >= 20:
        signals += 1
    if multi_risk_pct >= 15:
        signals += 1
    if escalations > 0:
        signals += 1

    if signals >= 3:
        return (
            "Heightened Financial Crime Risk",
            "Multiple risk signals are present in the filtered portfolio and warrant focused investigation."
        )

    if signals >= 1:
        return (
            "Targeted Review Recommended",
            "The filtered population contains specific customers or alert patterns that warrant closer review."
        )

    return (
        "Generally Stable",
        "The current filtered population does not show broad concentration of elevated risk signals."
    )


status, status_message = portfolio_status()

# =========================================================
# EXECUTIVE SUMMARY
# =========================================================
st.subheader("Executive Summary")

active_filters = []
if selected_segment != "All":
    active_filters.append(f"Segment: {selected_segment}")
if selected_risk != "All":
    active_filters.append(f"Risk: {selected_risk}")
if selected_region != "All":
    active_filters.append(f"Region: {selected_region}")
if selected_product != "All":
    active_filters.append(f"Product: {selected_product}")
if selected_month != "All":
    active_filters.append(f"Date: {selected_month}")

if active_filters:
    st.caption("Active filters — " + " | ".join(active_filters))
else:
    st.caption("Active filters — All portfolio records")

if customers == 0:
    st.warning("No customers match the selected filters.")
else:
    s1, s2, s3 = st.columns([1.3, 1.0, 2.7])

    with s1:
        st.metric("Portfolio Status", status)

    with s2:
        st.metric("High/Critical Customers", f"{high_critical:,}")

    with s3:
        st.info(status_message)

    st.markdown(
        f"""
        **Filtered portfolio summary:** **{customers:,} customer(s)** and **{alerts:,} alert(s)**
        are currently in scope. **{high_critical_pct:.1f}%** of customers are High/Critical risk,
        **{repeat_alerts:,}** have repeat-alert activity, and **{multi_risk_customers:,}**
        show multiple financial-crime risk signals. Filtered alerted exposure is approximately
        **${alerted_exposure/1e6:.1f}M**.
        """
    )

    st.markdown("#### What this means")

    if high_critical_pct >= 25:
        st.write("• High/Critical-risk customers are materially concentrated in the filtered population.")
    else:
        st.write("• High/Critical risk is not broadly concentrated in the filtered population.")

    if repeat_alerts > 0:
        st.write(f"• {repeat_alerts:,} customer(s) show repeat-alert behavior and deserve recurrence review.")

    if multi_risk_customers > 0:
        st.write(f"• {multi_risk_customers:,} customer(s) show multiple risk signals and merit cross-risk review.")

    if escalations > 0:
        st.write(f"• {escalations:,} escalation(s) indicate existing investigator attention.")

    st.markdown("#### Final Portfolio Decision")

    if status == "Heightened Financial Crime Risk":
        st.error(
            "Prioritize High/Critical, repeat-alert, multi-risk, and escalated activity. "
            "Use geography, product, risk-driver, and counterparty context to determine investigative priority."
        )
    elif status == "Targeted Review Recommended":
        st.warning(
            "Maintain routine monitoring across the broader filtered population, "
            "but investigate the identified elevated-risk signals first."
        )
    else:
        st.success(
            "Maintain routine monitoring. The current filtered population does not indicate broad portfolio-level escalation."
        )

st.divider()

# =========================================================
# KPI SCORECARD
# =========================================================
c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("Customers", f"{customers:,}")
c2.metric("Alerts", f"{alerts:,}")
c3.metric("High/Critical", f"{high_critical:,}")
c4.metric("Escalations", f"{escalations:,}")
c5.metric("Repeat Alerts", f"{repeat_alerts:,}")
c6.metric("Alerted Exposure", f"${alerted_exposure/1e6:.1f}M")

# =========================================================
# CUSTOMER INVESTIGATION SUMMARY
# =========================================================
st.subheader("Customer Investigation Summary")

if customers == 0 or not customer_id_c:
    st.info("No customer is available under the current filter selection.")
else:
    available_customers = sorted(F[customer_id_c].dropna().astype(str).unique().tolist())

    selected_customer = st.selectbox(
        "Select a customer to understand the risk",
        available_customers
    )

    customer_row = F[F[customer_id_c].astype(str).eq(selected_customer)]

    if len(customer_row):
        r = customer_row.iloc[0]

        x1, x2, x3, x4 = st.columns(4)

        with x1:
            st.metric("Customer", str(r.get(customer_id_c, "")))

        with x2:
            st.metric("Risk Level", str(r.get(risk_col, "N/A")) if risk_col else "N/A")

        with x3:
            score_col = find_col(F, ["financial_crime_risk_score", "risk_score"])
            st.metric("Risk Score", str(r.get(score_col, "N/A")) if score_col else "N/A")

        with x4:
            total_alerts_col = find_col(F, ["total_alerts"])
            customer_total_alerts = (
                int(pd.to_numeric(r.get(total_alerts_col, 0), errors="coerce"))
                if total_alerts_col else len(AF[AF[customer_id_a].astype(str).eq(selected_customer)])
            )
            st.metric("Total Alerts", f"{customer_total_alerts:,}")

        st.markdown("#### Why this customer matters")

        risk_level = str(r.get(risk_col, "N/A")) if risk_col else "N/A"
        escalated_customer_col = find_col(F, ["escalated_alerts"])
        customer_escalated = (
            int(pd.to_numeric(r.get(escalated_customer_col, 0), errors="coerce"))
            if escalated_customer_col else 0
        )
        repeat_flag = (
            int(pd.to_numeric(r.get(repeat_col, 0), errors="coerce"))
            if repeat_col else 0
        )
        multi_flag = (
            int(pd.to_numeric(r.get(multi_col, 0), errors="coerce"))
            if multi_col else 0
        )

        customer_exposure_col = find_col(F, ["total_alerted_amount"])
        exposure = (
            float(pd.to_numeric(r.get(customer_exposure_col, 0), errors="coerce"))
            if customer_exposure_col else 0.0
        )

        reasons = [
            f"This customer is rated **{risk_level} risk** with **{customer_total_alerts} alert(s)**.",
            f"Alerted exposure totals approximately **${exposure:,.0f}**."
        ]

        if customer_escalated > 0:
            reasons.append(f"**{customer_escalated} alert(s)** have been escalated.")
        if repeat_flag > 0:
            reasons.append("The customer has **repeat-alert activity**.")
        if multi_flag > 0:
            reasons.append("The customer shows **multiple financial-crime risk signals**.")

        st.write(" ".join(reasons))

        customer_alerts = (
            AF[AF[customer_id_a].astype(str).eq(selected_customer)].copy()
            if customer_id_a else pd.DataFrame()
        )

        risk_category_col = find_col(customer_alerts, ["risk_category"])
        risk_driver_col = find_col(customer_alerts, ["risk_driver"])

        if not customer_alerts.empty and (risk_category_col or risk_driver_col):
            st.markdown("#### Main Risk Signal")

            signal_text = ""

            if risk_category_col and not customer_alerts[risk_category_col].dropna().empty:
                top_category = customer_alerts[risk_category_col].value_counts().index[0]
                signal_text += f"The most common risk category is **{top_category}**. "

            if risk_driver_col and not customer_alerts[risk_driver_col].dropna().empty:
                top_driver = customer_alerts[risk_driver_col].value_counts().index[0]
                signal_text += f"The leading risk driver is **{top_driver}**."

            if signal_text:
                st.info(signal_text)

        st.markdown("#### Final Customer Decision")

        if risk_level.lower() in ["critical", "high"] and (
            repeat_flag > 0 or multi_flag > 0 or customer_escalated > 0
        ):
            st.error(
                "Decision: **PRIORITY INVESTIGATION**. Elevated risk combined with recurring, "
                "multi-risk, or escalated activity supports immediate investigator review."
            )
        elif risk_level.lower() in ["critical", "high"]:
            st.warning(
                "Decision: **ENHANCED REVIEW**. Elevated customer risk supports deeper review."
            )
        elif repeat_flag > 0 or multi_flag > 0 or customer_escalated > 0:
            st.warning(
                "Decision: **TARGETED REVIEW**. Repeat, multi-risk, or escalated activity warrants investigation."
            )
        else:
            st.success(
                "Decision: **ROUTINE MONITORING**. No strong combination of elevated indicators is visible."
            )

st.divider()

# =========================================================
# TABS
# =========================================================
tabs = st.tabs([
    "Risk Queue",
    "Multi-Risk Analysis",
    "Counterparty Intelligence",
    "Tableau Gallery",
    "Story Walkthrough"
])

# ---------------------------------------------------------
# TAB 1 — RISK QUEUE
# ---------------------------------------------------------
with tabs[0]:
    st.subheader("Risk Queue")
    st.caption(
        "The queue reflects the same sidebar filters applied to the entire application."
    )

    score_col = find_col(F, ["financial_crime_risk_score", "risk_score"])

    if F.empty:
        st.info("No customers match the current filters.")
    elif score_col:
        st.dataframe(
            F.sort_values(score_col, ascending=False),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.dataframe(
            F,
            use_container_width=True,
            hide_index=True
        )

# ---------------------------------------------------------
# TAB 2 — MULTI-RISK
# ---------------------------------------------------------
with tabs[1]:
    st.subheader("Multi-Risk Analysis")
    st.caption(
        "Highlights customers with repeat alerts and/or multiple risk categories in the filtered population."
    )

    if F.empty:
        st.info("No customers match the current filters.")
    else:
        mask = pd.Series(False, index=F.index)

        if repeat_col:
            mask = mask | pd.to_numeric(F[repeat_col], errors="coerce").fillna(0).gt(0)

        if multi_col:
            mask = mask | pd.to_numeric(F[multi_col], errors="coerce").fillna(0).gt(0)

        multi = F[mask].copy()

        score_col = find_col(multi, ["financial_crime_risk_score", "risk_score"])
        if score_col:
            multi = multi.sort_values(score_col, ascending=False)

        if multi.empty:
            st.success("No repeat-alert or multi-risk customers are present under the current filters.")
        else:
            st.dataframe(
                multi,
                use_container_width=True,
                hide_index=True
            )

# ---------------------------------------------------------
# TAB 3 — COUNTERPARTY INTELLIGENCE
# ---------------------------------------------------------
with tabs[2]:
    st.subheader("Counterparty Intelligence")
    st.caption(
        "Counterparty results are rebuilt from the filtered alert population whenever a counterparty field is available."
    )

    counterparty_col_a = find_col(AF, COUNTERPARTY_CANDIDATES)

    if counterparty_col_a and not AF.empty:
        amount_col = find_col(AF, AMOUNT_CANDIDATES)

        agg_dict = {
            "Alert Count": (counterparty_col_a, "size")
        }

        if customer_id_a:
            agg_dict["Connected Customers"] = (customer_id_a, "nunique")

        if amount_col:
            AF["_amount_numeric"] = pd.to_numeric(AF[amount_col], errors="coerce").fillna(0)
            agg_dict["Alerted Amount"] = ("_amount_numeric", "sum")

        counterparty_summary = (
            AF.groupby(counterparty_col_a)
            .agg(**agg_dict)
            .reset_index()
            .rename(columns={counterparty_col_a: "Counterparty"})
            .sort_values(
                "Connected Customers" if "Connected Customers" in agg_dict else "Alert Count",
                ascending=False
            )
        )

        st.dataframe(
            counterparty_summary.head(50),
            use_container_width=True,
            hide_index=True
        )

    else:
        network_flag_col = find_col(N, ["network_review_flag"])

        if network_flag_col:
            network = N[
                pd.to_numeric(N[network_flag_col], errors="coerce").fillna(0).gt(0)
            ].copy()
        else:
            network = N.copy()

        connected_col = find_col(network, ["connected_customers"])
        total_amount_col = find_col(network, ["total_amount"])

        sort_cols = [c for c in [connected_col, total_amount_col] if c]
        if sort_cols:
            network = network.sort_values(sort_cols, ascending=False)

        st.info(
            "The alert dataset does not expose a counterparty identifier, so this section uses the project-level network summary."
        )

        st.dataframe(
            network,
            use_container_width=True,
            hide_index=True
        )

# ---------------------------------------------------------
# TAB 4 — TABLEAU GALLERY
# ---------------------------------------------------------
with tabs[3]:
    st.subheader("Tableau Gallery")
    st.caption(
        "Final Executive Dashboard synchronized with the current processed datasets and verified KPI results."
    )

    dashboard = first_existing_image("images/02_executive_dashboard.png")

    if dashboard:
        st.image(
            str(dashboard),
            caption="Financial Crime Intelligence & Risk Analytics — Executive Dashboard",
            use_container_width=True
        )
    else:
        st.warning(
            "Executive dashboard image not found. Add `02_executive_dashboard.png` to the images folder."
        )

# ---------------------------------------------------------
# TAB 5 — STORY WALKTHROUGH (HYBRID)
# ---------------------------------------------------------
with tabs[4]:
    st.subheader("Story Walkthrough")
    st.caption(
        "Interactive analyst story driven by the same sidebar filters as the rest of the application."
    )

    # =====================================================
    # STORY 1 — PORTFOLIO OVERVIEW
    # =====================================================
    st.markdown("## 1. Portfolio Overview")
    st.write(
        "Start with the size and overall risk posture of the filtered population before drilling into the drivers."
    )

    o1, o2, o3, o4 = st.columns(4)
    o1.metric("Customers", f"{customers:,}")
    o2.metric("Alerts", f"{alerts:,}")
    o3.metric("Escalations", f"{escalations:,}")
    o4.metric("Exposure", f"${alerted_exposure/1e6:.1f}M")

    st.info(
        f"Analyst takeaway: The current filter selection is assessed as **{status}**."
    )
    st.divider()

    # =====================================================
    # STORY 2 — RISK / ALERT DRIVERS
    # =====================================================
    st.markdown("## 2. Risk & Alert Drivers")
    st.write(
        "Identify which risk categories and underlying behaviors are generating the filtered alerts."
    )

    risk_category_col = find_col(AF, ["risk_category"])
    risk_driver_col = find_col(AF, ["risk_driver"])

    r1, r2 = st.columns(2)

    with r1:
        st.markdown("#### Alert Categories")
        if risk_category_col and not AF.empty:
            category_counts = (
                AF[risk_category_col]
                .dropna()
                .astype(str)
                .value_counts()
                .head(10)
                .rename("Alerts")
            )
            if not category_counts.empty:
                st.bar_chart(category_counts)
            else:
                st.info("No category data is available under the current filters.")
        else:
            st.info("Risk-category field not detected in the filtered alert data.")

    with r2:
        st.markdown("#### Top Risk Drivers")
        if risk_driver_col and not AF.empty:
            driver_counts = (
                AF[risk_driver_col]
                .dropna()
                .astype(str)
                .value_counts()
                .head(10)
                .rename("Alerts")
            )
            if not driver_counts.empty:
                st.bar_chart(driver_counts)
            else:
                st.info("No risk-driver data is available under the current filters.")
        else:
            st.info("Risk-driver field not detected in the filtered alert data.")

    if risk_driver_col and not AF[risk_driver_col].dropna().empty:
        top_driver = AF[risk_driver_col].astype(str).value_counts().index[0]
        st.info(
            f"Analyst takeaway: **{top_driver}** is the leading risk driver in the current filtered population."
        )

    st.divider()

    # =====================================================
    # STORY 3 — GEOGRAPHIC RISK
    # =====================================================
    st.markdown("## 3. Geographic / Regional Risk")
    st.write(
        "Assess where alert activity and financial-crime exposure are concentrated."
    )

    if region_source == "A" and region_col and not AF.empty:
        geo_counts = (
            AF[region_col]
            .dropna()
            .astype(str)
            .value_counts()
            .head(10)
            .rename("Alerts")
        )

        if not geo_counts.empty:
            st.bar_chart(geo_counts)

            top_geo = geo_counts.index[0]
            st.info(
                f"Analyst takeaway: **{top_geo}** has the highest alert concentration under the current filters."
            )

    elif region_source == "C" and region_col and not F.empty:
        geo_counts = (
            F[region_col]
            .dropna()
            .astype(str)
            .value_counts()
            .head(10)
            .rename("Customers")
        )

        if not geo_counts.empty:
            st.bar_chart(geo_counts)

            top_geo = geo_counts.index[0]
            st.info(
                f"Analyst takeaway: **{top_geo}** has the largest customer concentration under the current filters."
            )
    else:
        st.info("No regional field is available for interactive geographic analysis.")
    st.divider()

    # =====================================================
    # STORY 4 — PRODUCT EXPOSURE
    # =====================================================
    st.markdown("## 4. Product & Channel Exposure")
    st.write(
        "Identify which products or transaction channels carry the greatest alert pressure or exposure."
    )

    if product_source == "A" and product_col and not AF.empty:
        if alert_amount_col:
            temp = AF[[product_col, alert_amount_col]].copy()
            temp["_amount"] = pd.to_numeric(temp[alert_amount_col], errors="coerce").fillna(0)

            product_exposure = (
                temp.groupby(product_col)["_amount"]
                .sum()
                .sort_values(ascending=False)
                .head(10)
            )

            st.bar_chart(product_exposure)

            if not product_exposure.empty:
                st.info(
                    f"Analyst takeaway: **{product_exposure.index[0]}** has the highest alerted exposure under the current filters."
                )
        else:
            product_counts = (
                AF[product_col]
                .dropna()
                .astype(str)
                .value_counts()
                .head(10)
            )

            st.bar_chart(product_counts)

            if not product_counts.empty:
                st.info(
                    f"Analyst takeaway: **{product_counts.index[0]}** generates the highest alert volume under the current filters."
                )

    elif product_source == "C" and product_col and not F.empty:
        product_counts = (
            F[product_col]
            .dropna()
            .astype(str)
            .value_counts()
            .head(10)
        )

        st.bar_chart(product_counts)

        if not product_counts.empty:
            st.info(
                f"Analyst takeaway: **{product_counts.index[0]}** is the largest product group under the current filters."
            )
    else:
        st.info("No product field is available for interactive product analysis.")
    st.divider()

    # =====================================================
    # STORY 5 — INVESTIGATION FUNNEL
    # =====================================================
    st.markdown("## 5. Investigation Funnel")
    st.write(
        "Follow how alert volume narrows through escalation, investigation, and SAR filing. "
        "This section is fully interactive and responds to the sidebar filters."
    )

    total_alert_stage = int(alerts)

    escalated_stage = int(escalations)

    investigated_stage = safe_count_true(
        AF,
        ["investigated_flag", "is_investigated", "investigation_flag", "investigated"]
    )

    if investigated_stage is None:
        investigated_stage = safe_sum(
            F,
            ["investigated_cases", "investigated_alerts"]
        )

    sar_stage = safe_count_true(
        AF,
        ["sar_filed_flag", "is_sar_filed", "sar_flag", "sar_filed"]
    )

    if sar_stage is None:
        sar_stage = safe_sum(
            F,
            ["sar_filed", "sars_filed", "sar_count"]
        )

    funnel_rows = [
        ("Total Alerts", total_alert_stage),
        ("Escalated", escalated_stage)
    ]

    if investigated_stage is not None:
        funnel_rows.append(("Investigated", int(investigated_stage)))

    if sar_stage is not None:
        funnel_rows.append(("SAR Filed", int(sar_stage)))

    funnel_df = pd.DataFrame(funnel_rows, columns=["Stage", "Count"]).set_index("Stage")
    st.bar_chart(funnel_df)

    if total_alert_stage:
        escalation_rate = escalated_stage / total_alert_stage * 100
        st.info(
            f"Analyst takeaway: **{escalation_rate:.1f}%** of filtered alerts are escalated for deeper review."
        )


    st.divider()

    # =====================================================
    # STORY 6 — REPEAT ALERT & COUNTERPARTY INTELLIGENCE
    # =====================================================
    st.markdown("## 6. Repeat-Alert & Counterparty Intelligence")
    st.write(
        "Focus investigator attention on customers and counterparties that repeatedly appear across the workflow."
    )

    total_alerts_col = find_col(F, ["total_alerts"])

    if total_alerts_col and not F.empty:
        repeat_customer_view = (
            F[[customer_id_c, total_alerts_col]]
            .copy()
        )
        repeat_customer_view[total_alerts_col] = pd.to_numeric(
            repeat_customer_view[total_alerts_col],
            errors="coerce"
        ).fillna(0)

        repeat_customer_view = (
            repeat_customer_view
            .sort_values(total_alerts_col, ascending=False)
            .head(10)
            .set_index(customer_id_c)
        )

        st.markdown("#### Top Repeat-Alert Customers")
        st.bar_chart(repeat_customer_view)

    counterparty_col_a = find_col(AF, COUNTERPARTY_CANDIDATES)

    if counterparty_col_a and not AF.empty:
        st.markdown("#### Common Counterparties")

        cp_counts = (
            AF[counterparty_col_a]
            .dropna()
            .astype(str)
            .value_counts()
            .head(10)
        )

        st.bar_chart(cp_counts)

        if not cp_counts.empty:
            st.info(
                f"Analyst takeaway: **{cp_counts.index[0]}** is the most frequently observed counterparty in the current filter selection."
            )
    elif repeat_alerts > 0:
        st.info(
            f"Analyst takeaway: **{repeat_alerts:,}** customer(s) in the current filtered population have repeat-alert activity."
        )
    st.divider()

    # =====================================================
    # STORY 7 — FINDINGS & RECOMMENDED ACTIONS
    # =====================================================
    st.markdown("## 7. Key Findings & Recommended Actions")

    findings = []

    if customers == 0:
        findings.append("No customers match the current filter selection.")
    else:
        findings.append(
            f"The filtered population contains {customers:,} customer(s) and {alerts:,} alert(s)."
        )

        if high_critical > 0:
            findings.append(
                f"{high_critical:,} customer(s) are High/Critical risk."
            )

        if repeat_alerts > 0:
            findings.append(
                f"{repeat_alerts:,} customer(s) show repeat-alert activity."
            )

        if multi_risk_customers > 0:
            findings.append(
                f"{multi_risk_customers:,} customer(s) show multiple financial-crime risk signals."
            )

        if selected_region != "All":
            findings.append(
                f"Regional analysis is currently focused on {selected_region}."
            )

        if selected_product != "All":
            findings.append(
                f"Product analysis is currently focused on {selected_product}."
            )

    for finding in findings:
        st.write(f"• {finding}")

    st.markdown("#### Recommended Analyst Action")

    if status == "Heightened Financial Crime Risk":
        st.error(
            "Prioritize the highest-risk customers first, validate repeat-alert patterns, "
            "review product/geographic concentration, examine connected counterparties, "
            "and escalate cases where the combined evidence supports deeper investigation."
        )
    elif status == "Targeted Review Recommended":
        st.warning(
            "Prioritize customers with the strongest combination of risk rating, repeat alerts, "
            "multi-risk signals, product/geographic concentration, and escalation history."
        )
    else:
        st.success(
            "Maintain routine monitoring while continuing to watch for repeat-alert, "
            "counterparty-network, product, and geographic concentration signals."
        )

# =========================================================
# FOOTER
# =========================================================
st.caption(
    "Synthetic educational portfolio project. No real customer, bank, alert, sanctions, fraud, or case data."
)
