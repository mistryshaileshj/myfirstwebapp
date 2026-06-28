import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import date
import numpy as np

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="Retail Intelligence", layout="wide", initial_sidebar_state="expanded")

# ── Palette ───────────────────────────────────────────────────────────────────
BG_DEEP  = "#0f1628"
BG_MID   = "#1a2340"
BG_CARD  = "#1e2a42"
BG_CARD2 = "#243150"
ACCENT   = "#4f8ef7"
ACCENT2  = "#38d9a9"
ACCENT3  = "#f6ad55"
ACCENT4  = "#fc8181"
ACCENT5  = "#b794f4"
TEXT_PRI = "#e8edf5"
TEXT_SEC = "#8fa3c7"
GRID_COL = "rgba(255,255,255,0.06)"
BORDER   = "rgba(255,255,255,0.08)"
PALETTE  = [ACCENT,ACCENT2,ACCENT3,ACCENT4,ACCENT5,
            "#63b3ed","#68d391","#fbd38d","#feb2b2","#d6bcfa",
            "#4299e1","#48bb78","#ed8936","#f56565","#9f7aea"]

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
html,body,[class*="css"]{{font-family:'Inter',sans-serif;}}
.stApp{{background:{BG_DEEP};}}
.main .block-container{{padding-top:14px;padding-bottom:10px;}}

[data-testid="stSidebar"]{{
    background:linear-gradient(180deg,{BG_DEEP} 0%,{BG_MID} 100%);
    border-right:1px solid {BORDER};
}}
[data-testid="stSidebar"] *{{color:{TEXT_PRI} !important;}}
[data-testid="stSidebar"] .stDateInput input{{
    background:{BG_CARD} !important;border:1px solid {BORDER} !important;
    border-radius:7px !important;color:{TEXT_PRI} !important;
    font-size:12px !important;padding:5px 9px !important;
}}
[data-testid="stSidebar"] .stDateInput{{margin-bottom:2px !important;}}
[data-testid="stSidebar"] .stSlider{{margin-bottom:0px !important;padding-top:0px !important;}}
[data-testid="stSidebar"] [data-testid="stVerticalBlock"]>div{{gap:2px !important;}}
[data-testid="stSidebar"] hr{{margin:6px 0 !important;border-color:{BORDER};}}
[data-testid="stSidebar"] .stButton button{{
    background:{BG_CARD};border:1px solid {BORDER};color:{TEXT_SEC} !important;
    border-radius:7px;font-size:12px;font-weight:500;padding:5px 4px;transition:all 0.18s;
}}
[data-testid="stSidebar"] .stButton button:hover{{
    background:{BG_CARD2};color:{TEXT_PRI} !important;border-color:{ACCENT};
}}
[data-testid="stSidebar"] .stButton button[kind="primary"]{{
    background:{ACCENT} !important;border-color:{ACCENT} !important;
    color:#fff !important;font-weight:600;
}}

.sec-label{{
    font-size:10px;font-weight:600;color:{TEXT_SEC};
    text-transform:uppercase;letter-spacing:0.09em;
    margin-bottom:3px;margin-top:5px;
}}
.main-header{{
    background:linear-gradient(135deg,{BG_MID} 0%,{BG_CARD} 100%);
    border:1px solid {BORDER};border-radius:14px;
    padding:16px 24px;margin-bottom:12px;
    display:flex;align-items:center;justify-content:space-between;
}}
.main-header h1{{color:{TEXT_PRI};font-size:20px;font-weight:700;margin:0;}}
.main-header .sub{{color:{TEXT_SEC};font-size:12px;margin-top:2px;}}
.hdr-val{{color:{TEXT_PRI};font-size:24px;font-weight:700;}}
.hdr-lbl{{color:{TEXT_SEC};font-size:10px;margin-top:1px;}}

.chart-card{{
    background:{BG_CARD};border:1px solid {BORDER};border-radius:13px;
    padding:14px 16px 6px;margin-bottom:10px;
}}
.chart-title{{
    font-size:11px;font-weight:600;color:{TEXT_SEC};
    text-transform:uppercase;letter-spacing:0.07em;margin-bottom:4px;
}}
.story-header{{
    background:linear-gradient(135deg,{BG_MID} 0%,{BG_CARD2} 100%);
    border:1px solid {BORDER};border-radius:13px;
    padding:13px 20px;margin:10px 0;
    display:flex;align-items:center;gap:12px;
}}
.story-header .item-name{{font-size:19px;font-weight:700;color:{TEXT_PRI};}}
.dim-badge{{
    font-size:10px;font-weight:600;color:{ACCENT};
    background:rgba(79,142,247,0.18);padding:3px 10px;
    border-radius:20px;text-transform:uppercase;letter-spacing:0.06em;
    border:1px solid rgba(79,142,247,0.3);display:inline-block;margin-bottom:3px;
}}
.kpi-card{{
    background:{BG_CARD};border:1px solid {BORDER};border-radius:12px;
    padding:13px 15px;border-top:3px solid transparent;transition:transform 0.15s;
}}
.kpi-card:hover{{transform:translateY(-2px);}}
.kpi-card.c1{{border-top-color:{ACCENT};}}
.kpi-card.c2{{border-top-color:{ACCENT2};}}
.kpi-card.c3{{border-top-color:{ACCENT3};}}
.kpi-card.c4{{border-top-color:{ACCENT4};}}
.kpi-card.c5{{border-top-color:{ACCENT5};}}
.kpi-label{{font-size:10px;font-weight:600;color:{TEXT_SEC};text-transform:uppercase;letter-spacing:0.07em;}}
.kpi-value{{font-size:21px;font-weight:700;color:{TEXT_PRI};margin:4px 0 2px;}}
.kpi-delta{{font-size:11px;font-weight:500;}}
.kpi-delta.up{{color:{ACCENT2};}}
.kpi-delta.down{{color:{ACCENT4};}}
.kpi-delta.neutral{{color:{TEXT_SEC};}}
.story-chart-card{{
    background:{BG_CARD};border:1px solid {BORDER};border-radius:13px;
    padding:13px 15px 6px;margin-bottom:10px;
}}
.story-chart-title{{
    font-size:11px;font-weight:600;color:{TEXT_SEC};
    text-transform:uppercase;letter-spacing:0.07em;margin-bottom:2px;
}}
.no-sel{{
    background:{BG_CARD};border:1px solid {BORDER};border-radius:13px;
    padding:44px;text-align:center;color:{TEXT_SEC};font-size:14px;
}}
</style>
""", unsafe_allow_html=True)

# ── Load & cache ──────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("Sales_SalesRtn_New.csv", low_memory=False)
    df['DOC_DT']   = pd.to_datetime(df['DOC_DT'], errors='coerce')
    df['MONTH']    = df['DOC_DT'].dt.to_period('M').astype(str)
    df['MONTH_DT'] = pd.to_datetime(df['MONTH'], format='%Y-%m')   # for sorting

    df['IS_SALE'] = df['Trj_Type'] == 'Sales'
    df['IS_RTN']  = df['Trj_Type'] == 'Sales Rtn'

    # Revenue  = NET_AMT for Sales rows
    # Rtn_Amt  = NET_AMT for Sales Rtn rows (always treated as positive)
    df['REVENUE']   = df['NET_AMT'].where(df['IS_SALE'], 0)
    df['RTN_AMT']   = df['NET_AMT'].abs().where(df['IS_RTN'], 0)
    df['SALE_QTY']  = df['QTY'].where(df['IS_SALE'], 0)
    df['RTN_QTY2']  = df['RTN_QTY'].where(df['IS_RTN'], 0)

    df['MARGIN']    = df['SALERATE'] - df['PURRATE']
    df['MARGIN_PCT']= (df['MARGIN'] / df['SALERATE'].replace(0, np.nan) * 100).fillna(0)

    return df

df = load_data()

# ── Session state ─────────────────────────────────────────────────────────────
for k, v in [('selected_item', None), ('dimension', 'ITEM'), ('rank_by', 'Value')]:
    if k not in st.session_state:
        st.session_state[k] = v

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🔍 Filters")
    st.markdown("---")

    abs_min = df['DOC_DT'].min().date()
    abs_max = df['DOC_DT'].max().date()

    st.markdown('<div class="sec-label">From Date</div>', unsafe_allow_html=True)
    date_from = st.date_input("_fd", value=abs_min, min_value=abs_min,
                               max_value=abs_max, format="DD/MM/YYYY",
                               label_visibility="collapsed")
    st.markdown('<div class="sec-label">To Date</div>', unsafe_allow_html=True)
    date_to = st.date_input("_td", value=abs_max, min_value=abs_min,
                             max_value=abs_max, format="DD/MM/YYYY",
                             label_visibility="collapsed")

    st.markdown("---")

    dim_map = {"Product": "ITEM", "Brand": "BRAND", "Style": "STYLE"}
    st.markdown('<div class="sec-label">View By</div>', unsafe_allow_html=True)
    dc = st.columns(3)
    for i, (lbl, val) in enumerate(dim_map.items()):
        with dc[i]:
            active = st.session_state.dimension == val
            if st.button(lbl, key=f"dim_{val}",
                         type="primary" if active else "secondary",
                         use_container_width=True):
                st.session_state.dimension = val
                st.session_state.selected_item = None
                st.rerun()

    st.markdown("---")

    st.markdown('<div class="sec-label">Top N</div>', unsafe_allow_html=True)
    top_n = st.slider("_tn", 5, 20, 10, label_visibility="collapsed")

    st.markdown("---")

    st.markdown('<div class="sec-label">Rank By</div>', unsafe_allow_html=True)
    rb_cols = st.columns(2)
    for lbl in ["Value", "Quantity"]:
        with rb_cols[0 if lbl == "Value" else 1]:
            active = st.session_state.rank_by == lbl
            if st.button(lbl, key=f"rb_{lbl}",
                         type="primary" if active else "secondary",
                         use_container_width=True):
                st.session_state.rank_by = lbl
                st.rerun()

    st.markdown("---")

    if st.session_state.selected_item:
        if st.button("✕  Clear Selection", use_container_width=True):
            st.session_state.selected_item = None
            st.rerun()

    st.markdown(f"""
    <div style='margin-top:10px;color:#4a5568;font-size:10px;line-height:1.7;'>
        📅 Data: {abs_min.strftime('%d/%m/%Y')} – {abs_max.strftime('%d/%m/%Y')}<br>
        📋 {len(df):,} records &nbsp;|&nbsp; Sales: {(df['IS_SALE']).sum():,} &nbsp;|&nbsp; Rtns: {(df['IS_RTN']).sum():,}
    </div>""", unsafe_allow_html=True)

# ── Date filter — both Sales and Returns share same date range, filter uniformly ─
mask = (df['DOC_DT'].dt.date >= date_from) & (df['DOC_DT'].dt.date <= date_to)
fdf  = df[mask].copy()

fdf_sales = fdf[fdf['IS_SALE']].copy()
fdf_rtn   = fdf[fdf['IS_RTN']].copy()

dim_col   = st.session_state.dimension
dim_label = {v: k for k, v in dim_map.items()}[dim_col]
rank_by   = st.session_state.rank_by
sort_col  = "Net_Sales" if rank_by == "Value" else "Sale_Qty"

# ── Aggregate for ranking ─────────────────────────────────────────────────────
def get_ranked(s_df, r_df, dim, sc, n):
    sg = s_df.groupby(dim).agg(
        Gross_Sales=('REVENUE',   'sum'),
        Sale_Qty   =('SALE_QTY', 'sum'),
        Transactions=('PDOC_NO', 'nunique'),
        Avg_Price  =('SALERATE',  'mean'),
        Margin_Pct =('MARGIN_PCT','mean'),
        Disc_Pct   =('Disc_Perc', 'mean'),
        Total_Disc =('ITEMDISC_AMT','sum'),
    ).reset_index()

    rg = r_df.groupby(dim).agg(
        Rtn_Amt=('RTN_AMT', 'sum'),
        Rtn_Qty=('RTN_QTY2','sum'),
    ).reset_index()

    g = sg.merge(rg, on=dim, how='left').fillna(0)
    g['Net_Sales']   = g['Gross_Sales'] - g['Rtn_Amt']
    g['Return_Rate'] = (g['Rtn_Qty'] / g['Sale_Qty'].replace(0, np.nan) * 100).fillna(0)

    asc = (sc == 'Return_Rate')
    return g.sort_values(sc, ascending=asc).head(n)

ranked = get_ranked(fdf_sales, fdf_rtn, dim_col, sort_col, top_n)

# ── Plotly dark theme helper ──────────────────────────────────────────────────
def dark_fig(fig, height=300, showlegend=True):
    # Snapshot axis titles before bulk update erases them
    saved_x, saved_y = {}, {}
    for key in fig.layout:
        if key.startswith('xaxis'):
            t = getattr(getattr(fig.layout, key, None), 'title', None)
            if t and getattr(t, 'text', None):
                saved_x[key] = t.text
        if key.startswith('yaxis'):
            t = getattr(getattr(fig.layout, key, None), 'title', None)
            if t and getattr(t, 'text', None):
                saved_y[key] = t.text

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=60, r=20, t=36, b=52),
        height=height,
        font=dict(family="Inter", color=TEXT_SEC, size=11),
        showlegend=showlegend,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                    font=dict(size=10, color=TEXT_PRI), bgcolor="rgba(0,0,0,0)", borderwidth=0),
        hoverlabel=dict(bgcolor=BG_DEEP, font_color=TEXT_PRI, font_size=11, bordercolor=BORDER),
    )
    fig.update_xaxes(gridcolor=GRID_COL, zerolinecolor=GRID_COL,
                     tickfont=dict(color=TEXT_SEC, size=10),
                     title_font=dict(color=TEXT_PRI, size=11), title_standoff=10)
    fig.update_yaxes(gridcolor=GRID_COL, zerolinecolor=GRID_COL,
                     tickfont=dict(color=TEXT_SEC, size=10),
                     title_font=dict(color=TEXT_PRI, size=11), title_standoff=10)
    for key, txt in saved_x.items():
        getattr(fig.layout, key).title.text = txt
    for key, txt in saved_y.items():
        getattr(fig.layout, key).title.text = txt
    return fig

# ── Header KPIs ──────────────────────────────────────────────────────────────
gross_sales = fdf_sales['REVENUE'].sum()
total_rtn   = fdf_rtn['RTN_AMT'].sum()
net_sales   = gross_sales - total_rtn
rtn_rate_overall = (fdf_rtn['RTN_QTY2'].sum() / fdf_sales['SALE_QTY'].sum() * 100) if fdf_sales['SALE_QTY'].sum() > 0 else 0

st.markdown(f"""
<div class="main-header">
  <div>
    <h1>🏪 Retail Intelligence</h1>
    <div class="sub">Top {top_n} {dim_label}s · Ranked by {rank_by} · {date_from.strftime('%d/%m/%Y')} – {date_to.strftime('%d/%m/%Y')}</div>
  </div>
  <div style='display:flex;gap:28px;align-items:center'>
    <div style='text-align:center'>
      <div class="hdr-val">₹{gross_sales:,.0f}</div>
      <div class="hdr-lbl">Gross Sales</div>
    </div>
    <div style='text-align:center;color:{ACCENT4}'>
      <div class="hdr-val" style='color:{ACCENT4}'>₹{total_rtn:,.0f}</div>
      <div class="hdr-lbl">Sales Returns</div>
    </div>
    <div style='text-align:center'>
      <div class="hdr-val" style='color:{ACCENT2}'>₹{net_sales:,.0f}</div>
      <div class="hdr-lbl">Net Sales</div>
    </div>
    <div style='text-align:center'>
      <div class="hdr-val" style='color:{ACCENT3}'>{rtn_rate_overall:.1f}%</div>
      <div class="hdr-lbl">Return Rate</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Primary chart: Top N horizontal bar ──────────────────────────────────────
colors = [PALETTE[i % len(PALETTE)] for i in range(len(ranked))]
if st.session_state.selected_item:
    colors = [ACCENT if row[dim_col] == st.session_state.selected_item
              else "rgba(255,255,255,0.10)" for _, row in ranked.iterrows()]

bar_vals  = ranked[sort_col]
x_title   = "Net Sales (₹)" if rank_by == "Value" else "Units Sold"
bar_texts = [f"₹{v:,.0f}" if rank_by == "Value" else f"{v:,.0f}" for v in bar_vals]

fig1 = go.Figure(go.Bar(
    y=ranked[dim_col], x=bar_vals, orientation='h',
    marker_color=colors,
    text=bar_texts, textposition='outside',
    textfont=dict(size=10, color=TEXT_PRI),
    hovertemplate=f"<b>%{{y}}</b><br>{x_title}: %{{x:,.0f}}<extra></extra>",
    name=rank_by,
))
fig1.update_yaxes(autorange='reversed', tickfont=dict(size=11, color=TEXT_PRI),
                  title_text=dim_label, title_standoff=8)
fig1.update_xaxes(showgrid=True, zeroline=False, title_text=x_title, tickformat=",")
fig1 = dark_fig(fig1, height=max(300, top_n * 34), showlegend=False)

st.markdown(f'<div class="chart-card"><div class="chart-title">🏆 Top {top_n} {dim_label}s · Net Sales = Gross Sales − Returns</div>', unsafe_allow_html=True)
sel = st.plotly_chart(fig1, use_container_width=True, key="bar_chart",
                       on_select="rerun", selection_mode="points")
st.markdown("</div>", unsafe_allow_html=True)

if sel and sel.selection and sel.selection.get("points"):
    clicked = sel.selection["points"][0].get("y")
    if clicked and clicked != st.session_state.selected_item:
        st.session_state.selected_item = clicked
        st.rerun()

# ── Story section ─────────────────────────────────────────────────────────────
if st.session_state.selected_item:
    item  = st.session_state.selected_item
    is_df = fdf_sales[fdf_sales[dim_col] == item].copy()
    ir_df = fdf_rtn[fdf_rtn[dim_col] == item].copy()

    gross    = is_df['REVENUE'].sum()
    rtn_amt  = ir_df['RTN_AMT'].sum()
    net      = gross - rtn_amt
    units    = is_df['SALE_QTY'].sum()
    rtn_qty  = ir_df['RTN_QTY2'].sum()
    txns     = is_df['PDOC_NO'].nunique()
    avg_pr   = is_df['SALERATE'].mean()   if len(is_df) else 0
    margin   = is_df['MARGIN_PCT'].mean() if len(is_df) else 0
    avg_disc = is_df['Disc_Perc'].mean()  if len(is_df) else 0
    tot_disc = is_df['ITEMDISC_AMT'].sum()
    rtn_rate = (rtn_qty / units * 100)    if units > 0 else 0
    share    = (net / net_sales * 100)    if net_sales > 0 else 0

    st.markdown(f"""
    <div class="story-header">
      <div style='font-size:26px'>📖</div>
      <div>
        <div class="dim-badge">{dim_label}</div>
        <div class="item-name">{item}</div>
      </div>
      <div style='margin-left:auto;display:flex;gap:28px;align-items:center;text-align:center'>
        <div>
          <div style='font-size:18px;font-weight:700;color:{TEXT_PRI}'>₹{net:,.0f}</div>
          <div style='font-size:10px;color:{TEXT_SEC}'>Net Sales</div>
        </div>
        <div>
          <div style='font-size:18px;font-weight:700;color:{ACCENT2}'>{share:.1f}%</div>
          <div style='font-size:10px;color:{TEXT_SEC}'>Net Sales Share</div>
        </div>
      </div>
    </div>""", unsafe_allow_html=True)

    # ── KPI cards ──────────────────────────────────────────────────────────────
    def kpi(col, label, value, delta, direction, cls, icon):
        arrow = "▲" if direction == "up" else ("▼" if direction == "down" else "●")
        col.markdown(f"""
        <div class="kpi-card {cls}">
          <div class="kpi-label">{icon} {label}</div>
          <div class="kpi-value">{value}</div>
          <div class="kpi-delta {direction}">{arrow} {delta}</div>
        </div>""", unsafe_allow_html=True)

    k1,k2,k3,k4,k5 = st.columns(5)
    kpi(k1, "Net Sales",      f"₹{net:,.0f}",       f"Gross ₹{gross:,.0f}",           "up",      "c1","💰")
    kpi(k2, "Units Sold",     f"{units:,.0f}",       f"{txns} transactions",            "neutral", "c2","📦")
    kpi(k3, "Avg Sell Price", f"₹{avg_pr:,.0f}",    f"Disc: {avg_disc:.1f}%",          "neutral", "c3","🏷️")
    kpi(k4, "Return Rate",    f"{rtn_rate:.1f}%",    f"₹{rtn_amt:,.0f} | {rtn_qty:.0f} units", "down" if rtn_rate>10 else "up","c4","↩️")
    kpi(k5, "Gross Margin",   f"{margin:.1f}%",      f"₹{tot_disc:,.0f} discounted",   "up" if margin>30 else "neutral","c5","📊")

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

    # ── Story row 1: 3 charts ─────────────────────────────────────────────────
    sc1, sc2, sc3 = st.columns(3)

    # A — Monthly Gross Sales, Returns, Net Sales
    with sc1:
        ms = is_df.groupby('MONTH').agg(Gross=('REVENUE','sum'), Qty=('SALE_QTY','sum')).reset_index()
        mr = ir_df.groupby('MONTH').agg(Rtn=('RTN_AMT','sum')).reset_index()
        mt = ms.merge(mr, on='MONTH', how='outer').fillna(0).sort_values('MONTH')
        mt['Net'] = mt['Gross'] - mt['Rtn']

        figA = go.Figure()
        figA.add_trace(go.Bar(x=mt['MONTH'], y=mt['Gross'], name='Gross Sales',
                              marker_color='rgba(79,142,247,0.75)',
                              hovertemplate="<b>%{x}</b><br>Gross: ₹%{y:,.0f}<extra></extra>"))
        figA.add_trace(go.Bar(x=mt['MONTH'], y=mt['Rtn'], name='Returns',
                              marker_color='rgba(252,129,129,0.75)',
                              hovertemplate="<b>%{x}</b><br>Returns: ₹%{y:,.0f}<extra></extra>"))
        figA.add_trace(go.Scatter(x=mt['MONTH'], y=mt['Net'], name='Net Sales',
                                  line=dict(color=ACCENT2, width=2.5), marker=dict(size=5),
                                  hovertemplate="<b>%{x}</b><br>Net: ₹%{y:,.0f}<extra></extra>"))
        figA.update_layout(barmode='overlay')
        figA.update_xaxes(title_text='Month', tickangle=-35, tickfont=dict(size=8))
        figA.update_yaxes(title_text='Amount (₹)', showgrid=True, tickformat=',')
        figA = dark_fig(figA, height=230)
        st.markdown('<div class="story-chart-card"><div class="story-chart-title">📅 Gross Sales · Returns · Net Sales</div>', unsafe_allow_html=True)
        st.plotly_chart(figA, use_container_width=True, key="sA")
        st.markdown("</div>", unsafe_allow_html=True)

    # B — Sub-dimension revenue breakdown
    with sc2:
        sub_dim = 'BRAND' if dim_col=='ITEM' else ('ITEM' if dim_col=='BRAND' else 'ITEM')
        sub_lbl = 'Brand'  if dim_col=='ITEM' else ('Product' if dim_col=='BRAND' else 'Product')
        sub_s = is_df.groupby(sub_dim)['REVENUE'].sum().reset_index().rename(columns={'REVENUE':'Gross'})
        sub_r = ir_df.groupby(sub_dim)['RTN_AMT'].sum().reset_index()
        sub   = sub_s.merge(sub_r, on=sub_dim, how='left').fillna(0)
        sub['Net'] = sub['Gross'] - sub['RTN_AMT']
        sub = sub.sort_values('Net', ascending=False).head(8)

        figB = go.Figure()
        figB.add_trace(go.Bar(x=sub[sub_dim], y=sub['Gross'], name='Gross Sales',
                              marker_color='rgba(79,142,247,0.75)',
                              hovertemplate="<b>%{x}</b><br>Gross: ₹%{y:,.0f}<extra></extra>"))
        figB.add_trace(go.Bar(x=sub[sub_dim], y=sub['RTN_AMT'], name='Returns',
                              marker_color='rgba(252,129,129,0.75)',
                              hovertemplate="<b>%{x}</b><br>Returns: ₹%{y:,.0f}<extra></extra>"))
        figB.update_layout(barmode='group')
        figB.update_xaxes(title_text=sub_lbl, tickangle=-30, tickfont=dict(size=8))
        figB.update_yaxes(title_text='Amount (₹)', showgrid=True, tickformat=',')
        figB = dark_fig(figB, height=230)
        st.markdown(f'<div class="story-chart-card"><div class="story-chart-title">🔎 Net Sales by {sub_lbl}</div>', unsafe_allow_html=True)
        st.plotly_chart(figB, use_container_width=True, key="sB")
        st.markdown("</div>", unsafe_allow_html=True)

    # C — Monthly units sold vs returned
    with sc3:
        mu = is_df.groupby('MONTH')['SALE_QTY'].sum().reset_index()
        mr2= ir_df.groupby('MONTH')['RTN_QTY2'].sum().reset_index()
        mu2= mu.merge(mr2, on='MONTH', how='outer').fillna(0).sort_values('MONTH')

        figC = go.Figure()
        figC.add_trace(go.Bar(x=mu2['MONTH'], y=mu2['SALE_QTY'], name='Units Sold',
                              marker_color='rgba(56,217,169,0.75)',
                              hovertemplate="<b>%{x}</b><br>Units Sold: %{y:,.0f}<extra></extra>"))
        figC.add_trace(go.Bar(x=mu2['MONTH'], y=mu2['RTN_QTY2'], name='Units Returned',
                              marker_color='rgba(252,129,129,0.75)',
                              hovertemplate="<b>%{x}</b><br>Units Returned: %{y:,.0f}<extra></extra>"))
        figC.update_layout(barmode='group')
        figC.update_xaxes(title_text='Month', tickangle=-35, tickfont=dict(size=8))
        figC.update_yaxes(title_text='Quantity', showgrid=True)
        figC = dark_fig(figC, height=230)
        st.markdown('<div class="story-chart-card"><div class="story-chart-title">📦 Units Sold vs Returned</div>', unsafe_allow_html=True)
        st.plotly_chart(figC, use_container_width=True, key="sC")
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Story row 2: 2 charts ─────────────────────────────────────────────────
    sd1, sd2 = st.columns([3, 2])

    with sd1:
        sz_s = is_df.groupby('SIZE_NAME')['SALE_QTY'].sum().reset_index()
        sz_r = ir_df.groupby('SIZE_NAME')['RTN_QTY2'].sum().reset_index()
        sz   = sz_s.merge(sz_r, on='SIZE_NAME', how='left').fillna(0)
        sz   = sz[sz['SIZE_NAME'].notna() & (sz['SIZE_NAME'] != '')].sort_values('SALE_QTY', ascending=False)

        figD = go.Figure()
        figD.add_trace(go.Bar(y=sz['SIZE_NAME'], x=sz['SALE_QTY'], orientation='h',
                              name='Units Sold',
                              marker_color='rgba(56,217,169,0.80)',
                              hovertemplate="<b>Size %{y}</b><br>Sold: %{x:,.0f}<extra></extra>"))
        figD.add_trace(go.Bar(y=sz['SIZE_NAME'], x=sz['RTN_QTY2'], orientation='h',
                              name='Units Returned',
                              marker_color='rgba(252,129,129,0.80)',
                              hovertemplate="<b>Size %{y}</b><br>Returned: %{x:,.0f}<extra></extra>"))
        figD.update_layout(barmode='group')
        figD.update_yaxes(autorange='reversed', title_text='Size', tickfont=dict(size=9))
        figD.update_xaxes(title_text='Quantity', showgrid=True)
        figD = dark_fig(figD, height=220)
        st.markdown('<div class="story-chart-card"><div class="story-chart-title">📐 Units Sold vs Returned by Size</div>', unsafe_allow_html=True)
        st.plotly_chart(figD, use_container_width=True, key="sD")
        st.markdown("</div>", unsafe_allow_html=True)

    with sd2:
        dm = is_df.groupby('MONTH')['Disc_Perc'].mean().reset_index().sort_values('MONTH')
        figE = go.Figure(go.Scatter(
            x=dm['MONTH'], y=dm['Disc_Perc'], name='Avg Discount %',
            mode='lines+markers',
            line=dict(color=ACCENT3, width=2.5, shape='spline'),
            marker=dict(size=5, color=ACCENT3),
            fill='tozeroy', fillcolor='rgba(246,173,85,0.10)',
            hovertemplate="<b>%{x}</b><br>Disc: %{y:.1f}%<extra></extra>",
        ))
        figE.update_xaxes(title_text='Month', tickangle=-35, tickfont=dict(size=8))
        figE.update_yaxes(title_text='Discount %', showgrid=True, ticksuffix='%')
        figE = dark_fig(figE, height=220, showlegend=False)
        st.markdown('<div class="story-chart-card"><div class="story-chart-title">🏷️ Avg Discount % Trend</div>', unsafe_allow_html=True)
        st.plotly_chart(figE, use_container_width=True, key="sE")
        st.markdown("</div>", unsafe_allow_html=True)

else:
    st.markdown("""
    <div class="no-sel">
      <div style='font-size:38px;margin-bottom:10px'>👆</div>
      <div style='font-weight:600;font-size:15px;color:#e8edf5;margin-bottom:6px'>Click any bar to explore its story</div>
      <div>Select a product, brand or style from the chart above to see KPIs, trends and insights.</div>
    </div>""", unsafe_allow_html=True)
