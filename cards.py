import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="🛍️",
    layout="wide",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #1e3a5f 0%, #2d6a9f 100%);
        border-radius: 12px;
        padding: 24px 28px;
        color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.15);
    }
    .metric-label {
        font-size: 13px;
        font-weight: 600;
        letter-spacing: 1px;
        text-transform: uppercase;
        opacity: 0.8;
        margin-bottom: 8px;
    }
    .metric-value {
        font-size: 30px;
        font-weight: 700;
        line-height: 1.2;
    }
    .metric-sub {
        font-size: 13px;
        opacity: 0.75;
        margin-top: 6px;
    }
    .section-title {
        font-size: 18px;
        font-weight: 600;
        color: #1e3a5f;
        margin-bottom: 4px;
    }
</style>
""", unsafe_allow_html=True)

# ── Load Data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["DOC_DT"] = pd.to_datetime(df["DOC_DT"], errors="coerce")
    return df

uploaded = st.file_uploader("📂 Upload Sales CSV", type=["csv"])

if uploaded:
    df_raw = pd.read_csv(uploaded)
    df_raw["DOC_DT"] = pd.to_datetime(df_raw["DOC_DT"], errors="coerce")
else:
    # Default: use the bundled file if available
    try:
        df_raw = load_data("Sales_SalesRtn.csv")
    except FileNotFoundError:
        st.warning("Please upload the Sales CSV file.")
        st.stop()

# ── Sidebar Filters ───────────────────────────────────────────────────────────
st.sidebar.header("🔽 Filters")

trj_options = df_raw["Trj_Type"].dropna().unique().tolist()
selected_trj = st.sidebar.multiselect("Transaction Type", trj_options, default=["Sales"])

brand_options = sorted(df_raw["BRAND"].dropna().unique().tolist())
selected_brands = st.sidebar.multiselect("Brand", brand_options, default=[])

item_options = sorted(df_raw["ITEM"].dropna().unique().tolist())
selected_items = st.sidebar.multiselect("Product (Item)", item_options, default=[])

min_date = df_raw["DOC_DT"].min()
max_date = df_raw["DOC_DT"].max()
date_range = st.sidebar.date_input("Date Range", value=(min_date, max_date))

# ── Apply Filters ─────────────────────────────────────────────────────────────
df = df_raw.copy()

if selected_trj:
    df = df[df["Trj_Type"].isin(selected_trj)]
if selected_brands:
    df = df[df["BRAND"].isin(selected_brands)]
if selected_items:
    df = df[df["ITEM"].isin(selected_items)]
if len(date_range) == 2:
    df = df[(df["DOC_DT"] >= pd.Timestamp(date_range[0])) &
            (df["DOC_DT"] <= pd.Timestamp(date_range[1]))]

# ── KPI Calculations ──────────────────────────────────────────────────────────
total_revenue = df["NET_AMT"].sum()

brand_rev = df.groupby("BRAND")["NET_AMT"].sum().sort_values(ascending=False)
top_brand = brand_rev.index[0] if not brand_rev.empty else "N/A"
top_brand_rev = brand_rev.iloc[0] if not brand_rev.empty else 0

item_rev = df.groupby("ITEM")["NET_AMT"].sum().sort_values(ascending=False)
top_item = item_rev.index[0] if not item_rev.empty else "N/A"
top_item_rev = item_rev.iloc[0] if not item_rev.empty else 0

# ── Header ────────────────────────────────────────────────────────────────────
st.title("🛍️ Sales Dashboard")
st.caption(f"Showing **{len(df):,}** transactions · Revenue in ₹")
st.markdown("---")

# ── KPI Cards ─────────────────────────────────────────────────────────────────
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">💰 Total Revenue</div>
        <div class="metric-value">₹{total_revenue:,.0f}</div>
        <div class="metric-sub">{len(df):,} transactions</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">🏆 Top Brand by Revenue</div>
        <div class="metric-value">{top_brand}</div>
        <div class="metric-sub">₹{top_brand_rev:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">🥇 Top Product by Revenue</div>
        <div class="metric-value">{top_item}</div>
        <div class="metric-sub">₹{top_item_rev:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")

# ── Charts ────────────────────────────────────────────────────────────────────
col_left, col_right = st.columns(2)

# Top 10 Brands bar chart
with col_left:
    st.markdown('<div class="section-title">Top 10 Brands by Revenue</div>', unsafe_allow_html=True)
    top10_brands = brand_rev.head(10).reset_index()
    top10_brands.columns = ["Brand", "Revenue"]
    fig_brand = px.bar(
        top10_brands,
        x="Revenue",
        y="Brand",
        orientation="h",
        color="Revenue",
        color_continuous_scale="Blues",
        text=top10_brands["Revenue"].apply(lambda x: f"₹{x:,.0f}"),
    )
    fig_brand.update_traces(textposition="outside")
    fig_brand.update_layout(
        coloraxis_showscale=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(autorange="reversed"),
        margin=dict(l=10, r=10, t=10, b=10),
        height=360,
    )
    st.plotly_chart(fig_brand, use_container_width=True)

# Top 10 Products bar chart
with col_right:
    st.markdown('<div class="section-title">Top 10 Products by Revenue</div>', unsafe_allow_html=True)
    top10_items = item_rev.head(10).reset_index()
    top10_items.columns = ["Product", "Revenue"]
    fig_item = px.bar(
        top10_items,
        x="Revenue",
        y="Product",
        orientation="h",
        color="Revenue",
        color_continuous_scale="Teal",
        text=top10_items["Revenue"].apply(lambda x: f"₹{x:,.0f}"),
    )
    fig_item.update_traces(textposition="outside")
    fig_item.update_layout(
        coloraxis_showscale=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(autorange="reversed"),
        margin=dict(l=10, r=10, t=10, b=10),
        height=360,
    )
    st.plotly_chart(fig_item, use_container_width=True)

# Revenue trend over time
st.markdown("---")
st.markdown('<div class="section-title">Revenue Trend Over Time</div>', unsafe_allow_html=True)

daily_rev = df.groupby(df["DOC_DT"].dt.date)["NET_AMT"].sum().reset_index()
daily_rev.columns = ["Date", "Revenue"]

fig_trend = px.area(
    daily_rev,
    x="Date",
    y="Revenue",
    color_discrete_sequence=["#2d6a9f"],
)
fig_trend.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=10, r=10, t=10, b=10),
    height=300,
    yaxis_title="Revenue (₹)",
    xaxis_title="",
)
fig_trend.update_traces(line_width=2, fillcolor="rgba(45,106,159,0.15)")
st.plotly_chart(fig_trend, use_container_width=True)

# ── Raw Data Table ────────────────────────────────────────────────────────────
st.markdown("---")
with st.expander("📋 View Raw Data", expanded=False):
    display_cols = ["DOC_DT", "PDOC_NO", "ITEM", "BRAND", "QTY", "SALERATE", "NET_AMT", "LOCATION", "Trj_Type"]
    st.dataframe(df[display_cols].reset_index(drop=True), use_container_width=True, height=350)
