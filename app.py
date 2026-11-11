import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(
    page_title="Financial Performance Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Styling ----------
st.markdown("""
<style>
    .stApp { background: #F3F6FA; }
    [data-testid="stSidebar"] { background: #14243D; }
    [data-testid="stSidebar"] * { color: #F5F7FB !important; }
    [data-testid="stSidebar"] [data-baseweb="tag"] {
        background-color: #176B87 !important;
        border: 0 !important;
    }
    [data-testid="stSidebar"] [data-baseweb="tag"] * { color: white !important; }
    .main-title { font-size: 2.15rem; font-weight: 780; color: #14243D; letter-spacing: -.6px; }
    .subtitle { color: #66758A; margin-top: .15rem; margin-bottom: 1.1rem; font-size: 1rem; }
    [data-testid="stMetric"] {
        background: #FFFFFF; padding: 17px 18px; border-radius: 13px;
        border: 1px solid #E1E8F0; box-shadow: 0 3px 10px rgba(20,36,61,.045);
        min-height: 116px;
    }
    [data-testid="stMetricLabel"] { color: #64748B; font-weight: 600; }
    [data-testid="stMetricValue"] { color: #14243D; }
    [data-testid="stMetricDelta"] { font-size: .82rem; }
    h2, h3 { color: #14243D; }
    div[data-testid="stDataFrame"] { background: white; border-radius: 12px; }
    .note {
        background: #E8F0F8; border-left: 4px solid #176B87;
        padding: 12px 15px; border-radius: 8px; color: #334155; font-size: .9rem;
    }
    .section-caption { color: #64748B; font-size: .88rem; margin-top: -8px; }
    hr { border-color: #DCE4EE; }
</style>
""", unsafe_allow_html=True)

DATA_FILE = Path(__file__).parent / "Financial_Data_English.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_FILE)
    df["Month"] = pd.to_datetime(df["Month"], errors="coerce")
    numeric_cols = [c for c in df.columns if c not in ["Month", "Region", "Establishment"]]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df.dropna(subset=["Month"])

df = load_data()

# ---------- Sidebar filters ----------
st.sidebar.title("FINANCE | PERFORMANCE")
st.sidebar.caption("Management reporting • FY2025")
st.sidebar.markdown("---")

regions = sorted(df["Region"].dropna().unique().tolist())
selected_regions = st.sidebar.multiselect("Region", regions, default=regions)

establishments = sorted(
    df.loc[df["Region"].isin(selected_regions), "Establishment"].dropna().unique().tolist()
)
selected_establishments = st.sidebar.multiselect(
    "Establishment", establishments, default=establishments
)

months = sorted(df["Month"].dt.to_period("M").unique().tolist())
month_labels = [m.strftime("%b %Y") for m in months]
selected_month_labels = st.sidebar.multiselect(
    "Month", month_labels, default=month_labels
)
selected_months = [months[i] for i, label in enumerate(month_labels) if label in selected_month_labels]

filtered = df[
    df["Region"].isin(selected_regions)
    & df["Establishment"].isin(selected_establishments)
    & df["Month"].dt.to_period("M").isin(selected_months)
].copy()

if filtered.empty:
    st.title("Financial Performance Dashboard")
    st.warning("No data matches the selected filters. Please update your selections.")
    st.stop()

# ---------- KPI calculations ----------
revenue_actual = filtered["Revenue_Actual"].sum()
revenue_budget = filtered["Revenue_Budget"].sum()
revenue_py = filtered["Revenue_PY"].sum()
revenue_var = revenue_actual - revenue_budget
revenue_var_pct = revenue_var / revenue_budget if revenue_budget else 0

cost_actual = filtered["Cost_of_Sales_Actual"].sum()
opex_actual = filtered["Operating_Expenses_Actual"].sum()
gross_profit = revenue_actual - cost_actual
gross_margin = gross_profit / revenue_actual if revenue_actual else 0
simplified_result = gross_profit - opex_actual
opex_budget = filtered["Operating_Expenses_Budget"].sum()
opex_var = opex_actual - opex_budget

def eur(value):
    return f"€{value:,.0f}"

def pct(value):
    return f"{value:.1%}"

st.markdown('<div class="main-title">Financial Performance Dashboard</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Management reporting | Actual vs Budget vs Prior Year</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="note">Portfolio case study based on a simulated multi-site distribution business. '
    'All figures are fictional and do not represent an actual employer.</div>',
    unsafe_allow_html=True,
)

st.markdown("### Executive overview")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Revenue actual", eur(revenue_actual), f"{revenue_var:+,.0f} € vs budget")
c2.metric("Revenue vs budget", pct(revenue_var_pct), f"{revenue_var:+,.0f} €")
c3.metric("Gross margin", pct(gross_margin), f"{eur(gross_profit)} gross profit")
c4.metric("Simplified operating result", eur(simplified_result), f"{pct(simplified_result/revenue_actual if revenue_actual else 0)} of revenue")

c5, c6, c7, c8 = st.columns(4)
c5.metric("Revenue prior year", eur(revenue_py))
c6.metric("Operating expenses", eur(opex_actual), f"{opex_var:+,.0f} € vs budget", delta_color="inverse")
c7.metric("Cost of sales", eur(cost_actual))
c8.metric("Operating expenses / revenue", pct(opex_actual/revenue_actual if revenue_actual else 0))

st.caption("Variance convention: positive revenue variance is favourable; positive expense variance is unfavourable.")

# ---------- Monthly performance ----------
st.markdown("---")
st.markdown("### 1. Revenue performance")
monthly = (
    filtered.groupby(filtered["Month"].dt.to_period("M"), as_index=False)
    .agg(
        Revenue_Actual=("Revenue_Actual", "sum"),
        Revenue_Budget=("Revenue_Budget", "sum"),
        Revenue_PY=("Revenue_PY", "sum"),
    )
)
monthly["Month"] = monthly["Month"].dt.to_timestamp()
monthly_long = monthly.melt(
    id_vars="Month",
    value_vars=["Revenue_Actual", "Revenue_Budget", "Revenue_PY"],
    var_name="Scenario",
    value_name="Revenue",
)
monthly_long["Scenario"] = monthly_long["Scenario"].map({
    "Revenue_Actual": "Actual", "Revenue_Budget": "Budget", "Revenue_PY": "Prior year"
})
fig_month = px.line(
    monthly_long, x="Month", y="Revenue", color="Scenario", markers=True,
    labels={"Revenue": "Revenue (€)", "Month": "", "Scenario": ""},
    color_discrete_map={"Actual": "#176B87", "Budget": "#E09F3E", "Prior year": "#8A94A6"},
)
fig_month.update_layout(
    template="plotly_white", height=370, margin=dict(l=10, r=10, t=20, b=10),
    legend=dict(orientation="h", y=1.12, x=0),
    yaxis=dict(tickprefix="€", separatethousands=True),
)
st.plotly_chart(fig_month, use_container_width=True)

# ---------- Regional analysis ----------
st.markdown("### 2. Regional performance")
regional = (
    filtered.groupby("Region", as_index=False)
    .agg(
        Revenue_Actual=("Revenue_Actual", "sum"),
        Revenue_Budget=("Revenue_Budget", "sum"),
        Cost_of_Sales_Actual=("Cost_of_Sales_Actual", "sum"),
        Operating_Expenses_Actual=("Operating_Expenses_Actual", "sum"),
    )
)
regional["Revenue variance"] = regional["Revenue_Actual"] - regional["Revenue_Budget"]
regional["Gross margin %"] = (
    regional["Revenue_Actual"] - regional["Cost_of_Sales_Actual"]
) / regional["Revenue_Actual"].replace(0, pd.NA)

left, right = st.columns([1.25, 1])
with left:
    reg_long = regional.melt(
        id_vars="Region", value_vars=["Revenue_Actual", "Revenue_Budget"],
        var_name="Scenario", value_name="Revenue"
    )
    reg_long["Scenario"] = reg_long["Scenario"].map(
        {"Revenue_Actual": "Actual", "Revenue_Budget": "Budget"}
    )
    fig_region = px.bar(
        reg_long, x="Region", y="Revenue", color="Scenario", barmode="group",
        labels={"Revenue": "Revenue (€)", "Region": "", "Scenario": ""},
        color_discrete_map={"Actual": "#176B87", "Budget": "#E09F3E"},
    )
    fig_region.update_layout(template="plotly_white", height=340, margin=dict(l=5,r=5,t=15,b=5),
                             yaxis=dict(tickprefix="€", separatethousands=True),
                             legend=dict(orientation="h", y=1.12, x=0))
    st.plotly_chart(fig_region, use_container_width=True)
with right:
    fig_mix = px.pie(
        regional, names="Region", values="Revenue_Actual", hole=.58,
        color_discrete_sequence=["#176B87", "#2A9D8F", "#E09F3E", "#8A94A6"],
    )
    fig_mix.update_layout(template="plotly_white", height=340, margin=dict(l=5,r=5,t=15,b=5),
                          legend=dict(orientation="h", y=-.05))
    fig_mix.update_traces(textposition="inside", textinfo="percent")
    st.plotly_chart(fig_mix, use_container_width=True)

# ---------- Cost structure ----------
st.markdown("### 3. Cost structure")
costs = pd.DataFrame({
    "Cost category": ["Cost of sales", "Operating expenses"],
    "Actual": [cost_actual, opex_actual],
    "Budget": [filtered["Cost_of_Sales_Budget"].sum(), opex_budget],
})
cost_long = costs.melt(id_vars="Cost category", var_name="Scenario", value_name="Amount")
fig_cost = px.bar(
    cost_long, x="Cost category", y="Amount", color="Scenario", barmode="group",
    labels={"Amount": "Amount (€)", "Cost category": "", "Scenario": ""},
    color_discrete_map={"Actual": "#176B87", "Budget": "#E09F3E"},
)
fig_cost.update_layout(template="plotly_white", height=320, margin=dict(l=5,r=5,t=15,b=5),
                       yaxis=dict(tickprefix="€", separatethousands=True),
                       legend=dict(orientation="h", y=1.12, x=0))
st.plotly_chart(fig_cost, use_container_width=True)

# ---------- Establishment drilldown ----------
st.markdown("### 4. Establishment performance")
est = (
    filtered.groupby(["Region", "Establishment"], as_index=False)
    .agg(
        Revenue_Actual=("Revenue_Actual", "sum"),
        Revenue_Budget=("Revenue_Budget", "sum"),
        Cost_of_Sales_Actual=("Cost_of_Sales_Actual", "sum"),
        Operating_Expenses_Actual=("Operating_Expenses_Actual", "sum"),
    )
)
est["Revenue variance"] = est["Revenue_Actual"] - est["Revenue_Budget"]
est["Revenue variance %"] = est["Revenue variance"] / est["Revenue_Budget"].replace(0, pd.NA)
est["Gross margin %"] = (
    est["Revenue_Actual"] - est["Cost_of_Sales_Actual"]
) / est["Revenue_Actual"].replace(0, pd.NA)
est["Simplified operating result"] = (
    est["Revenue_Actual"] - est["Cost_of_Sales_Actual"] - est["Operating_Expenses_Actual"]
)
display = est.rename(columns={
    "Revenue_Actual": "Revenue actual",
    "Revenue_Budget": "Revenue budget",
    "Revenue variance": "Revenue variance",
    "Revenue variance %": "Revenue variance %",
    "Gross margin %": "Gross margin %",
})
formatters = {
    "Revenue actual": "€{:,.0f}",
    "Revenue budget": "€{:,.0f}",
    "Revenue variance": "€{:,.0f}",
    "Revenue variance %": "{:.1%}",
    "Gross margin %": "{:.1%}",
    "Simplified operating result": "€{:,.0f}",
}
st.dataframe(
    display[["Region", "Establishment", "Revenue actual", "Revenue budget",
             "Revenue variance", "Revenue variance %", "Gross margin %",
             "Simplified operating result"]].style.format(formatters),
    use_container_width=True, hide_index=True
)

# ---------- Management insights ----------
st.markdown("### 5. Management takeaways")
if revenue_var > 0:
    st.write(f"• Revenue is **{eur(revenue_var)} above budget** ({pct(revenue_var_pct)}). Identify the regions and establishments contributing most to this favourable variance.")
else:
    st.write(f"• Revenue is **{eur(abs(revenue_var))} below budget** ({pct(abs(revenue_var_pct))}). Review volume, pricing and sales mix by region.")
if gross_margin < 0.35:
    st.write(f"• Gross margin is **{pct(gross_margin)}**. Review purchasing costs, selling prices and product mix.")
else:
    st.write(f"• Gross margin stands at **{pct(gross_margin)}**. Monitor whether this level is sustainable across regions and months.")
if opex_var > 0:
    st.write(f"• Operating expenses are **{eur(opex_var)} above budget (unfavourable)**; investigate the main cost drivers.")
else:
    st.write(f"• Operating expenses are **{eur(abs(opex_var))} below budget (favourable)**, indicating cost discipline.")

with st.expander("KPI definitions and methodology"):
    st.markdown("""
    - **Revenue variance (€):** Actual revenue − Budget revenue.
    - **Revenue variance (%):** Revenue variance ÷ Budget revenue.
    - **Gross profit:** Revenue actual − Cost of sales actual.
    - **Gross margin (%):** Gross profit ÷ Revenue actual.
    - **Simplified operating result:** Gross profit − Operating expenses actual.
    - **Operating expense variance (€):** Actual operating expenses − Budget operating expenses. A positive value is unfavourable.

    The simplified operating result is a portfolio KPI, not statutory operating profit (EBIT).
    """)

st.caption("Financial KPI Portfolio | Simulated dataset | FY2025")
