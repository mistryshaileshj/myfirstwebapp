import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Sales Performance Dashboard",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .stApp { background-color: #0f0f1a; }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
        border-right: 1px solid #2d2d4e;
    }
    [data-testid="stSidebar"] * { color: #e0e0ff !important; }
    .kpi-card {
        background: linear-gradient(135deg, #1e1e3a 0%, #2d2d5e 100%);
        border: 1px solid #3d3d7e;
        border-radius: 16px;
        padding: 20px 24px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.4);
        transition: transform 0.2s;
    }
    .kpi-card:hover { transform: translateY(-3px); }
    .kpi-label {
        font-size: 12px; font-weight: 600; letter-spacing: 1.2px;
        text-transform: uppercase; color: #9090cc; margin-bottom: 8px;
    }
    .kpi-value { font-size: 28px; font-weight: 800; color: #ffffff; line-height: 1.1; }
    .kpi-sub   { font-size: 12px; color: #7070aa; margin-top: 6px; }
    .accent-1 .kpi-value { color: #00d4aa; } .accent-1 { border-top: 3px solid #00d4aa; }
    .accent-2 .kpi-value { color: #ff6b6b; } .accent-2 { border-top: 3px solid #ff6b6b; }
    .accent-3 .kpi-value { color: #ffd93d; } .accent-3 { border-top: 3px solid #ffd93d; }
    .accent-4 .kpi-value { color: #6bcb77; } .accent-4 { border-top: 3px solid #6bcb77; }
    .accent-5 .kpi-value { color: #4d96ff; } .accent-5 { border-top: 3px solid #4d96ff; }
    .section-title {
        font-size: 18px; font-weight: 700; color: #c0c0ff;
        letter-spacing: 0.5px; margin: 28px 0 12px 0;
        padding-left: 4px; border-left: 4px solid #5555ff;
    }
    .filter-pill {
        display: inline-block;
        background: #2a1a4e; border: 1px solid #7755ff;
        border-radius: 20px; padding: 4px 14px;
        font-size: 12px; color: #c0a0ff; margin: 2px 4px;
    }
    div[data-testid="metric-container"] { display: none; }
    h1, h2, h3 { color: #ffffff !important; }
    p, li { color: #c0c0d0; }
</style>
""", unsafe_allow_html=True)

# ── Load data ──────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("Sales_SalesRtn_OG.csv")
    df["DOC_DT"] = pd.to_datetime(df["DOC_DT"])
    sales = df[df["ISSALE"] == "S"].copy()
    sales["MARGIN_PCT"] = (
        (sales["SALERATE"] - sales["PURRATE"]) / sales["SALERATE"] * 100
    ).round(2)
    return sales

sales = load_data()

# ── Session state — cross-filter selections ────────────────────────────────────
for key in ["sel_brand", "sel_item", "sel_size"]:
    if key not in st.session_state:
        st.session_state[key] = None

# ── Sidebar — global filters ───────────────────────────────────────────────────
st.sidebar.markdown("## 🛍️ Sales Dashboard")
st.sidebar.markdown("---")

min_date = sales["DOC_DT"].min().date()
max_date = sales["DOC_DT"].max().date()

st.sidebar.markdown("### 📅 Date Range")
date_from = st.sidebar.date_input("From", value=min_date, min_value=min_date, max_value=max_date)
date_to   = st.sidebar.date_input("To",   value=max_date, min_value=min_date, max_value=max_date)

st.sidebar.markdown("### 📂 Sub-Group")
subgrps = ["All"] + sorted(sales["SUBGRP"].dropna().unique().tolist())
sel_subgrp = st.sidebar.selectbox("Sub-Group", subgrps)

st.sidebar.markdown("---")

# Clear cross-filters button
if st.sidebar.button("🔄 Clear Chart Selections", use_container_width=True):
    st.session_state.sel_brand = None
    st.session_state.sel_item  = None
    st.session_state.sel_size  = None
    st.rerun()

# Active selection pills in sidebar
active = {
    "Brand": st.session_state.sel_brand,
    "Item":  st.session_state.sel_item,
    "Size":  st.session_state.sel_size,
}
pills = [f"<span class='filter-pill'>🔍 {k}: <b>{v}</b></span>"
         for k, v in active.items() if v]
if pills:
    st.sidebar.markdown("**Active selections:**", unsafe_allow_html=True)
    st.sidebar.markdown(" ".join(pills), unsafe_allow_html=True)

# ── Build the main filtered dataframe (global filters only) ───────────────────
mask = (
    (sales["DOC_DT"].dt.date >= date_from) &
    (sales["DOC_DT"].dt.date <= date_to)
)
if sel_subgrp != "All":
    mask &= (sales["SUBGRP"] == sel_subgrp)
base_df = sales[mask].copy()

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Base records:** {len(base_df):,}")

# ── Cross-filter helper ────────────────────────────────────────────────────────
def cross_filter(df, exclude=None):
    """Apply all active cross-filters except the one named in `exclude`."""
    m = pd.Series(True, index=df.index)
    if exclude != "brand" and st.session_state.sel_brand:
        m &= (df["BRAND"] == st.session_state.sel_brand)
    if exclude != "item" and st.session_state.sel_item:
        m &= (df["ITEM"] == st.session_state.sel_item)
    if exclude != "size" and st.session_state.sel_size:
        m &= (df["SIZE_NAME"] == st.session_state.sel_size)
    return df[m]

# ── KPI block — uses fully cross-filtered data ─────────────────────────────────
kpi_df = cross_filter(base_df)

def fmt_inr(v):
    if v >= 1_00_00_000: return f"₹{v/1_00_00_000:.1f} Cr"
    elif v >= 1_00_000:  return f"₹{v/1_00_000:.1f} L"
    else:                return f"₹{v:,.0f}"

def kpi_card(label, value, sub, accent):
    return f"""<div class="kpi-card accent-{accent}">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-sub">{sub}</div>
    </div>"""

total_revenue = kpi_df["NET_AMT"].sum()
avg_margin    = kpi_df["MARGIN_PCT"].mean()
avg_discount  = kpi_df["Disc_Perc"].mean()
item_rev  = kpi_df.groupby("ITEM")["NET_AMT"].sum()
brand_rev = kpi_df.groupby("BRAND")["NET_AMT"].sum()
top_item  = item_rev.idxmax()  if not item_rev.empty  else "—"
top_brand = brand_rev.idxmax() if not brand_rev.empty else "—"

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown(
    "<h1 style='text-align:center;color:#ffffff;font-size:32px;margin-bottom:4px;'>"
    "🛍️ Sales Performance Dashboard</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    f"<p style='text-align:center;color:#7070aa;font-size:13px;'>"
    f"{date_from.strftime('%d %b %Y')} → {date_to.strftime('%d %b %Y')} "
    f"· <i>Click any bar to cross-filter all charts</i></p>",
    unsafe_allow_html=True,
)

# ── KPI Cards ──────────────────────────────────────────────────────────────────
st.markdown("<div class='section-title'>📊 Key Metrics</div>", unsafe_allow_html=True)
c1, c2, c3, c4, c5 = st.columns(5)
with c1: st.markdown(kpi_card("Total Revenue",   fmt_inr(total_revenue), f"{len(kpi_df):,} transactions", 1), unsafe_allow_html=True)
with c2: st.markdown(kpi_card("Avg Margin %",    f"{avg_margin:.1f}%",   "(Sale − Purch) / Sale", 2), unsafe_allow_html=True)
with c3: st.markdown(kpi_card("Avg Discount %",  f"{avg_discount:.1f}%", "Disc_Perc avg", 3), unsafe_allow_html=True)
with c4: st.markdown(kpi_card("Top Item",        top_item,               f"{fmt_inr(item_rev.max() if not item_rev.empty else 0)} in sales", 4), unsafe_allow_html=True)
with c5: st.markdown(kpi_card("Top Brand",       top_brand,              f"{fmt_inr(brand_rev.max() if not brand_rev.empty else 0)} in sales", 5), unsafe_allow_html=True)

# ── Chart theme helpers ────────────────────────────────────────────────────────
CHART_BG = "#1a1a2e"
GRID_COL = "#2d2d4e"
FONT_COL = "#c0c0d0"
TICK_COL = "#7070aa"

BASE_LAYOUT = dict(
    paper_bgcolor=CHART_BG, plot_bgcolor=CHART_BG,
    font=dict(color=FONT_COL, family="Inter, sans-serif"),
    margin=dict(l=16, r=16, t=48, b=16),
    showlegend=False,
    dragmode=False,
)

def ax(title=None, ticksuffix=None, tickformat=None, tickangle=None, categoryorder=None):
    d = dict(gridcolor=GRID_COL, tickfont=dict(color=TICK_COL, size=11))
    if title:         d["title"] = title
    if ticksuffix:    d["ticksuffix"] = ticksuffix
    if tickformat:    d["tickformat"] = tickformat
    if tickangle is not None: d["tickangle"] = tickangle
    if categoryorder: d["categoryorder"] = categoryorder
    return d

def bar_colors(values, labels, selected, hi="#00d4aa", lo="rgba(80,80,140,0.35)"):
    """Return per-bar color: highlight selected bar, dim the rest."""
    if selected is None:
        # No selection — use continuous gradient
        mn, mx = min(values), max(values) if max(values) != min(values) else min(values) + 1
        scale = px.colors.sample_colorscale(
            [[0, "#2d2d7e"], [0.5, "#6655ff"], [1, hi]],
            [(v - mn) / (mx - mn) for v in values]
        )
        return scale
    return [hi if lbl == selected else lo for lbl in labels]

# ── Charts section ─────────────────────────────────────────────────────────────
st.markdown("<div class='section-title'>📈 KPI Charts</div>", unsafe_allow_html=True)
top_n = st.slider("Top N brands / items to show", 5, 20, 10)

# ════════════════════════════════════════════════════════════════════════════════
# CHART 1 — Top Brands by Sales
# cross-filtered by: item, size  (not brand — that's what this chart drives)
# ════════════════════════════════════════════════════════════════════════════════
col1, col2 = st.columns(2)

with col1:
    df1 = cross_filter(base_df, exclude="brand")
    brand_df = (
        df1.groupby("BRAND")["NET_AMT"].sum()
        .nlargest(top_n).reset_index()
        .sort_values("NET_AMT")
    )
    cols1 = bar_colors(
        brand_df["NET_AMT"].tolist(),
        brand_df["BRAND"].tolist(),
        st.session_state.sel_brand,
        hi="#00d4aa",
    )
    fig1 = go.Figure(go.Bar(
        x=brand_df["BRAND"], y=brand_df["NET_AMT"],
        marker_color=cols1,
        text=[fmt_inr(v) for v in brand_df["NET_AMT"]],
        textposition="outside", textfont=dict(size=10, color="#c0c0d0"),
        customdata=brand_df["BRAND"],
        hovertemplate="<b>%{x}</b><br>Revenue: ₹%{y:,.0f}<extra></extra>",
    ))
    fig1.update_layout(
        **BASE_LAYOUT,
        title=dict(text=f"1. Top {top_n} Brands by Sales  {'· 🔍 '+st.session_state.sel_brand if st.session_state.sel_brand else '— click bar to filter'}",
                   font=dict(size=13, color="#ffffff"), x=0.02),
        yaxis=ax(title="Revenue (₹)", tickformat=",.0f"),
        xaxis=ax(tickangle=-35),
        height=380,
    )
    ev1 = st.plotly_chart(fig1, use_container_width=True,
                          on_select="rerun", key="chart_brand")
    # Handle click
    pts1 = (ev1.selection or {}).get("points", [])
    if pts1:
        clicked = pts1[0].get("x")
        st.session_state.sel_brand = None if clicked == st.session_state.sel_brand else clicked
        st.rerun()

# ════════════════════════════════════════════════════════════════════════════════
# CHART 2 — Daily Revenue Trend  (responds to brand + item + size)
# ════════════════════════════════════════════════════════════════════════════════
with col2:
    df2 = cross_filter(base_df)
    daily = (
        df2.groupby(df2["DOC_DT"].dt.date)["NET_AMT"].sum().reset_index()
    )
    daily.columns = ["Date", "Revenue"]

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=daily["Date"], y=daily["Revenue"],
        mode="lines",
        line=dict(color="#4d96ff", width=2.5),
        fill="tozeroy", fillcolor="rgba(77,150,255,0.12)",
        hovertemplate="<b>%{x}</b><br>Revenue: ₹%{y:,.0f}<extra></extra>",
    ))
    fig2.update_layout(
        **BASE_LAYOUT,
        title=dict(text="2. Daily Revenue Trend", font=dict(size=13, color="#ffffff"), x=0.02),
        yaxis=ax(title="Revenue (₹)", tickformat=",.0f"),
        xaxis=ax(title="Date"),
        height=380,
    )
    st.plotly_chart(fig2, use_container_width=True, key="chart_trend")

# ════════════════════════════════════════════════════════════════════════════════
# CHART 3 — Avg Margin % by Item
# cross-filtered by: brand, size  (not item — this chart drives item)
# ════════════════════════════════════════════════════════════════════════════════
col3, col4 = st.columns(2)

with col3:
    df3 = cross_filter(base_df, exclude="item")
    margin_df = (
        df3.groupby("ITEM")["MARGIN_PCT"].mean()
        .reset_index()
        .sort_values("MARGIN_PCT", ascending=False)
        .head(top_n)
        .sort_values("MARGIN_PCT")
    )
    margin_df.columns = ["Item", "Avg Margin %"]

    n = len(margin_df)
    if st.session_state.sel_item is None:
        grad_colors = px.colors.sample_colorscale(
            [[0, "#ff6b6b"], [0.5, "#ffd93d"], [1, "#6bcb77"]],
            [i / max(n - 1, 1) for i in range(n)]
        )
        cols3 = grad_colors
    else:
        cols3 = ["#6bcb77" if lbl == st.session_state.sel_item
                 else "rgba(80,80,140,0.35)"
                 for lbl in margin_df["Item"]]

    fig3 = go.Figure(go.Bar(
        x=margin_df["Item"], y=margin_df["Avg Margin %"],
        marker_color=cols3,
        text=[f"{v:.1f}%" for v in margin_df["Avg Margin %"]],
        textposition="outside", textfont=dict(size=10, color="#c0c0d0"),
        hovertemplate="<b>%{x}</b><br>Margin: %{y:.1f}%<extra></extra>",
    ))
    fig3.update_layout(
        **BASE_LAYOUT,
        title=dict(text=f"3. Avg Margin % by Item  {'· 🔍 '+st.session_state.sel_item if st.session_state.sel_item else '— click bar to filter'}",
                   font=dict(size=13, color="#ffffff"), x=0.02),
        yaxis=ax(title="Avg Margin %", ticksuffix="%"),
        xaxis=ax(tickangle=-35),
        height=380,
    )
    ev3 = st.plotly_chart(fig3, use_container_width=True,
                          on_select="rerun", key="chart_item")
    pts3 = (ev3.selection or {}).get("points", [])
    if pts3:
        clicked = pts3[0].get("x")
        st.session_state.sel_item = None if clicked == st.session_state.sel_item else clicked
        st.rerun()

# ════════════════════════════════════════════════════════════════════════════════
# CHART 4 — Units Sold by Size
# cross-filtered by: brand, item  (not size — this chart drives size)
# ════════════════════════════════════════════════════════════════════════════════
with col4:
    df4 = cross_filter(base_df, exclude="size")
    size_df = (
        df4.groupby("SIZE_NAME")["QTY"].sum()
        .reset_index()
        .sort_values("QTY", ascending=False)
        .dropna(subset=["SIZE_NAME"])
    )
    size_df.columns = ["Size", "Units Sold"]

    n2 = len(size_df)
    if st.session_state.sel_size is None:
        grad_colors2 = px.colors.sample_colorscale(
            [[0, "#2d2d9e"], [0.5, "#c77dff"], [1, "#ff9f1c"]],
            [i / max(n2 - 1, 1) for i in range(n2)]
        )
        cols4 = grad_colors2
    else:
        cols4 = ["#ff9f1c" if lbl == st.session_state.sel_size
                 else "rgba(80,80,140,0.35)"
                 for lbl in size_df["Size"]]

    fig4 = go.Figure(go.Bar(
        x=size_df["Size"], y=size_df["Units Sold"],
        marker_color=cols4,
        text=[f"{int(v):,}" for v in size_df["Units Sold"]],
        textposition="outside", textfont=dict(size=10, color="#c0c0d0"),
        hovertemplate="<b>%{x}</b><br>Units: %{y:,.0f}<extra></extra>",
    ))
    fig4.update_layout(
        **BASE_LAYOUT,
        title=dict(text=f"4. Units Sold by Size  {'· 🔍 '+st.session_state.sel_size if st.session_state.sel_size else '— click bar to filter'}",
                   font=dict(size=13, color="#ffffff"), x=0.02),
        yaxis=ax(title="Units Sold"),
        xaxis=ax(categoryorder="total descending"),
        height=380,
    )
    ev4 = st.plotly_chart(fig4, use_container_width=True,
                          on_select="rerun", key="chart_size")
    pts4 = (ev4.selection or {}).get("points", [])
    if pts4:
        clicked = pts4[0].get("x")
        st.session_state.sel_size = None if clicked == st.session_state.sel_size else clicked
        st.rerun()

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center;color:#3d3d5e;font-size:11px;'>"
    "Sales Performance Dashboard · Data: Sales_SalesRtn_OG.csv · "
    "Click any bar to cross-filter · Click same bar again to deselect"
    "</p>",
    unsafe_allow_html=True,
)
