import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import date
import numpy as np

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="Retail Intelligence", layout="wide", initial_sidebar_state="expanded")

# ── Theme colours (dark navy palette used everywhere) ─────────────────────────
BG_DEEP   = "#0f1628"
BG_MID    = "#1a2340"
BG_CARD   = "#1e2a42"
BG_CARD2  = "#243150"
ACCENT    = "#4f8ef7"
ACCENT2   = "#38d9a9"
ACCENT3   = "#f6ad55"
ACCENT4   = "#fc8181"
ACCENT5   = "#b794f4"
TEXT_PRI  = "#e8edf5"
TEXT_SEC  = "#8fa3c7"
GRID_COL  = "rgba(255,255,255,0.06)"
BORDER    = "rgba(255,255,255,0.08)"

PALETTE = [ACCENT, ACCENT2, ACCENT3, ACCENT4, ACCENT5,
           "#63b3ed","#68d391","#fbd38d","#feb2b2","#d6bcfa",
           "#4299e1","#48bb78","#ed8936","#f56565","#9f7aea"]

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
html, body, [class*="css"] {{ font-family: 'Inter', sans-serif; }}

/* ── App background — same dark navy as sidebar ── */
.stApp {{ background: {BG_DEEP}; }}
.main .block-container {{ padding-top: 14px; padding-bottom: 10px; }}

/* ── Sidebar ── */
[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, {BG_DEEP} 0%, {BG_MID} 100%);
    border-right: 1px solid {BORDER};
}}
[data-testid="stSidebar"] * {{ color: {TEXT_PRI} !important; }}

/* sidebar date inputs */
[data-testid="stSidebar"] .stDateInput input {{
    background: {BG_CARD} !important; border: 1px solid {BORDER} !important;
    border-radius: 7px !important; color: {TEXT_PRI} !important; font-size: 12px !important;
    padding: 5px 9px !important;
}}
/* tighten sidebar vertical gaps */
[data-testid="stSidebar"] .stDateInput  {{ margin-bottom: 4px !important; }}
[data-testid="stSidebar"] .stSlider     {{ margin-bottom: 0px !important; padding-top: 0px !important;}}
[data-testid="stSidebar"] [data-testid="stVerticalBlock"] > div {{ gap: 2px !important; }}
[data-testid="stSidebar"] hr {{ margin: 8px 0 !important; border-color: {BORDER}; }}

/* sidebar buttons */
[data-testid="stSidebar"] .stButton button {{
    background: {BG_CARD}; border: 1px solid {BORDER}; color: {TEXT_SEC} !important;
    border-radius: 7px; font-size: 12px; font-weight: 500; padding: 5px 4px;
    transition: all 0.18s;
}}
[data-testid="stSidebar"] .stButton button:hover {{
    background: {BG_CARD2}; color: {TEXT_PRI} !important; border-color: {ACCENT};
}}
[data-testid="stSidebar"] .stButton button[kind="primary"] {{
    background: {ACCENT} !important; border-color: {ACCENT} !important;
    color: #fff !important; font-weight: 600;
}}

/* ── Section label ── */
.sec-label {{
    font-size: 10px; font-weight: 600; color: {TEXT_SEC};
    text-transform: uppercase; letter-spacing: 0.09em; margin-bottom: 3px; margin-top: 6px;
}}

/* ── Main header ── */
.main-header {{
    background: linear-gradient(135deg, {BG_MID} 0%, {BG_CARD} 100%);
    border: 1px solid {BORDER}; border-radius: 14px;
    padding: 16px 24px; margin-bottom: 12px;
    display: flex; align-items: center; justify-content: space-between;
}}
.main-header h1 {{ color: {TEXT_PRI}; font-size: 20px; font-weight: 700; margin: 0; }}
.main-header .sub {{ color: {TEXT_SEC}; font-size: 12px; margin-top: 2px; }}
.main-header .rev-val {{ color: {TEXT_PRI}; font-size: 26px; font-weight: 700; }}
.main-header .rev-lbl {{ color: {TEXT_SEC}; font-size: 11px; }}

/* ── Dark chart card ── */
.chart-card {{
    background: {BG_CARD}; border: 1px solid {BORDER}; border-radius: 13px;
    padding: 14px 16px 6px; margin-bottom: 10px;
}}
.chart-title {{
    font-size: 11px; font-weight: 600; color: {TEXT_SEC};
    text-transform: uppercase; letter-spacing: 0.07em; margin-bottom: 4px;
}}

/* ── Story header ── */
.story-header {{
    background: linear-gradient(135deg, {BG_MID} 0%, {BG_CARD2} 100%);
    border: 1px solid {BORDER}; border-radius: 13px;
    padding: 13px 20px; margin: 10px 0 10px;
    display: flex; align-items: center; gap: 12px;
}}
.story-header .item-name {{ font-size: 19px; font-weight: 700; color: {TEXT_PRI}; }}
.story-header .dim-badge {{
    font-size: 10px; font-weight: 600; color: {ACCENT};
    background: rgba(79,142,247,0.18); padding: 3px 10px; border-radius: 20px;
    text-transform: uppercase; letter-spacing: 0.06em; border: 1px solid rgba(79,142,247,0.3);
}}

/* ── KPI cards ── */
.kpi-card {{
    background: {BG_CARD}; border: 1px solid {BORDER}; border-radius: 12px;
    padding: 13px 15px; border-top: 3px solid transparent; transition: transform 0.15s;
}}
.kpi-card:hover {{ transform: translateY(-2px); }}
.kpi-card.c1 {{ border-top-color: {ACCENT}; }}
.kpi-card.c2 {{ border-top-color: {ACCENT2}; }}
.kpi-card.c3 {{ border-top-color: {ACCENT3}; }}
.kpi-card.c4 {{ border-top-color: {ACCENT4}; }}
.kpi-card.c5 {{ border-top-color: {ACCENT5}; }}
.kpi-label  {{ font-size: 10px; font-weight: 600; color: {TEXT_SEC}; text-transform: uppercase; letter-spacing: 0.07em; }}
.kpi-value  {{ font-size: 21px; font-weight: 700; color: {TEXT_PRI}; margin: 4px 0 2px; }}
.kpi-delta  {{ font-size: 11px; font-weight: 500; }}
.kpi-delta.up      {{ color: {ACCENT2}; }}
.kpi-delta.down    {{ color: {ACCENT4}; }}
.kpi-delta.neutral {{ color: {TEXT_SEC}; }}

/* ── Story chart card ── */
.story-chart-card {{
    background: {BG_CARD}; border: 1px solid {BORDER}; border-radius: 13px;
    padding: 13px 15px 6px; margin-bottom: 10px;
}}
.story-chart-title {{
    font-size: 11px; font-weight: 600; color: {TEXT_SEC};
    text-transform: uppercase; letter-spacing: 0.07em; margin-bottom: 2px;
}}

/* ── No-selection placeholder ── */
.no-sel {{
    background: {BG_CARD}; border: 1px solid {BORDER}; border-radius: 13px;
    padding: 44px; text-align: center; color: {TEXT_SEC}; font-size: 14px;
}}

/* plotly tooltip override already handled via hoverlabel */
</style>
""", unsafe_allow_html=True)

# ── Load & cache data ─────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("Sales_SalesRtn_OG.csv")
    df['DOC_DT'] = pd.to_datetime(df['DOC_DT'], errors='coerce')
    df['IS_SALE']   = df['ISSALE'] == 'S'
    df['IS_RETURN'] = df['ISSALE'] == 'E'
    df['REVENUE']    = df.apply(lambda r: r['NET_AMT']        if r['IS_SALE']   else 0, axis=1)
    df['RETURN_AMT'] = df.apply(lambda r: abs(r['NET_AMT'])   if r['IS_RETURN'] else 0, axis=1)
    df['MARGIN']     = df['SALERATE'] - df['PURRATE']
    df['MARGIN_PCT'] = df.apply(lambda r: (r['MARGIN'] / r['SALERATE'] * 100) if r['SALERATE'] > 0 else 0, axis=1)
    df['MONTH'] = df['DOC_DT'].dt.to_period('M').astype(str)
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

    min_date = df['DOC_DT'].min().date()
    max_date = df['DOC_DT'].max().date()

    st.markdown('<div class="sec-label">From Date</div>', unsafe_allow_html=True)
    date_from = st.date_input("_fd", value=min_date, min_value=min_date,
                               max_value=max_date, format="DD/MM/YYYY",
                               label_visibility="collapsed")
    st.markdown('<div class="sec-label">To Date</div>', unsafe_allow_html=True)
    date_to = st.date_input("_td", value=max_date, min_value=min_date,
                             max_value=max_date, format="DD/MM/YYYY",
                             label_visibility="collapsed")

    st.markdown("---")

    # View By buttons
    st.markdown('<div class="sec-label">View By</div>', unsafe_allow_html=True)
    dim_map = {"Product": "ITEM", "Brand": "BRAND", "Style": "STYLE"}
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

    # Top N
    st.markdown('<div class="sec-label">Top N</div>', unsafe_allow_html=True)
    top_n = st.slider("_tn", 5, 20, 10, label_visibility="collapsed")

    st.markdown("---")

    # Rank By — button style: Quantity / Value
    st.markdown('<div class="sec-label">Rank By</div>', unsafe_allow_html=True)
    rb = st.columns(2)
    for lbl in ["Value", "Quantity"]:
        with rb[0 if lbl == "Value" else 1]:
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
    <div style='margin-top:16px;text-align:center;color:#4a5568;font-size:10px;line-height:1.6'>
        {min_date.strftime('%d/%m/%Y')} – {max_date.strftime('%d/%m/%Y')}<br>
        {len(df):,} records
    </div>""", unsafe_allow_html=True)

# ── Filter ────────────────────────────────────────────────────────────────────
mask = (df['DOC_DT'].dt.date >= date_from) & (df['DOC_DT'].dt.date <= date_to)
fdf  = df[mask].copy()

dim_col   = st.session_state.dimension
dim_label = {v: k for k, v in dim_map.items()}[dim_col]
rank_by   = st.session_state.rank_by          # "Value" or "Quantity"
sort_col  = "Revenue" if rank_by == "Value" else "Units"

# ── Aggregate for ranking ─────────────────────────────────────────────────────
def get_ranked(df_in, dim, sc, n):
    g = df_in.groupby(dim).agg(
        Revenue=('REVENUE', 'sum'),
        Units=('QTY', 'sum'),
        Transactions=('PDOC_NO', 'nunique'),
        Return_Qty=('RTN_QTY', 'sum'),
    ).reset_index()
    g['Return_Rate'] = (g['Return_Qty'] / g['Units'].replace(0, np.nan) * 100).fillna(0)
    return g.sort_values(sc, ascending=False).head(n)

ranked = get_ranked(fdf, dim_col, sort_col, top_n)

# ── Plotly dark theme helper ──────────────────────────────────────────────────
def dark_fig(fig, height=300, showlegend=True):
    # Snapshot any axis titles already set so the bulk update below does not erase them
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
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=60, r=20, t=36, b=52),
        height=height,
        font=dict(family="Inter", color=TEXT_SEC, size=11),
        showlegend=showlegend,
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02,
            xanchor="right", x=1,
            font=dict(size=10, color=TEXT_PRI),
            bgcolor="rgba(0,0,0,0)", borderwidth=0,
        ),
        hoverlabel=dict(bgcolor=BG_DEEP, font_color=TEXT_PRI, font_size=11, bordercolor=BORDER),
    )
    fig.update_xaxes(
        gridcolor=GRID_COL, zerolinecolor=GRID_COL,
        tickfont=dict(color=TEXT_SEC, size=10),
        title_font=dict(color=TEXT_PRI, size=11),
        title_standoff=10,
    )
    fig.update_yaxes(
        gridcolor=GRID_COL, zerolinecolor=GRID_COL,
        tickfont=dict(color=TEXT_SEC, size=10),
        title_font=dict(color=TEXT_PRI, size=11),
        title_standoff=10,
    )
    # Restore axis titles that were set before this call
    for key, txt in saved_x.items():
        getattr(fig.layout, key).title.text = txt
    for key, txt in saved_y.items():
        getattr(fig.layout, key).title.text = txt

    return fig

# ── Main header ───────────────────────────────────────────────────────────────
total_rev = fdf['REVENUE'].sum()
total_rtn = fdf['RETURN_AMT'].sum()
st.markdown(f"""
<div class="main-header">
  <div>
    <h1>🏪 Retail Intelligence</h1>
    <div class="sub">Top {top_n} {dim_label}s · Ranked by {rank_by} · {date_from.strftime('%d/%m/%Y')} – {date_to.strftime('%d/%m/%Y')}</div>
  </div>
  <div style='display:flex;gap:32px;align-items:center'>
    <div style='text-align:center'>
      <div class="rev-val">₹{total_rev:,.0f}</div>
      <div class="rev-lbl">Gross Revenue</div>
    </div>
    <div style='text-align:center'>
      <div class="rev-val" style='color:{ACCENT4}'>₹{total_rtn:,.0f}</div>
      <div class="rev-lbl">Returns</div>
    </div>
    <div style='text-align:center'>
      <div class="rev-val" style='color:{ACCENT2}'>₹{total_rev - total_rtn:,.0f}</div>
      <div class="rev-lbl">Net Revenue</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Primary Chart — full width horizontal bar ─────────────────────────────────
colors = [PALETTE[i % len(PALETTE)] for i in range(len(ranked))]
if st.session_state.selected_item:
    colors = [
        ACCENT if row[dim_col] == st.session_state.selected_item else "rgba(255,255,255,0.12)"
        for _, row in ranked.iterrows()
    ]

bar_vals  = ranked[sort_col]
fmt       = "₹{:,.0f}" if rank_by == "Value" else "{:,.0f} units"
bar_texts = [fmt.format(v) for v in bar_vals]
x_title   = "Revenue (₹)" if rank_by == "Value" else "Units Sold"

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
fig1.update_xaxes(showgrid=True, zeroline=False, showticklabels=True,
                  title_text=x_title, tickformat=",")
fig1 = dark_fig(fig1, height=max(300, top_n * 32), showlegend=False)

st.markdown(f'<div class="chart-card"><div class="chart-title">🏆 Top {top_n} {dim_label}s · Ranked by {rank_by}</div>', unsafe_allow_html=True)
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
    item = st.session_state.selected_item
    idf         = fdf[fdf[dim_col] == item].copy()
    idf_sales   = idf[idf['IS_SALE']]
    idf_returns = idf[idf['IS_RETURN']]

    revenue      = idf_sales['REVENUE'].sum()
    units        = idf_sales['QTY'].sum()
    transactions = idf_sales['PDOC_NO'].nunique()
    avg_price    = idf_sales['SALERATE'].mean()   if len(idf_sales) else 0
    return_qty   = idf_returns['RTN_QTY'].sum()
    return_rate  = (return_qty / units * 100)     if units > 0 else 0
    gross_margin = idf_sales['MARGIN_PCT'].mean() if len(idf_sales) else 0
    avg_disc     = idf_sales['Disc_Perc'].mean()  if len(idf_sales) else 0
    total_disc   = idf_sales['ITEMDISC_AMT'].sum()
    return_amt   = idf_returns['RETURN_AMT'].sum()
    share_pct    = (revenue / fdf['REVENUE'].sum() * 100) if fdf['REVENUE'].sum() > 0 else 0

    st.markdown(f"""
    <div class="story-header">
      <div style='font-size:26px'>📖</div>
      <div>
        <div class="dim-badge">{dim_label}</div>
        <div class="item-name">{item}</div>
      </div>
      <div style='margin-left:auto;text-align:right'>
        <div style='font-size:20px;font-weight:700;color:{TEXT_PRI}'>{share_pct:.1f}%</div>
        <div style='font-size:11px;color:{TEXT_SEC}'>Revenue Share</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── 5 KPI cards ───────────────────────────────────────────────────────────
    def kpi(col, label, value, delta, direction, cls, icon):
        arrow = "▲" if direction == "up" else ("▼" if direction == "down" else "●")
        col.markdown(f"""
        <div class="kpi-card {cls}">
          <div class="kpi-label">{icon} {label}</div>
          <div class="kpi-value">{value}</div>
          <div class="kpi-delta {direction}">{arrow} {delta}</div>
        </div>""", unsafe_allow_html=True)

    k1, k2, k3, k4, k5 = st.columns(5)
    kpi(k1, "Revenue",         f"₹{revenue:,.0f}",       f"{share_pct:.1f}% of total",     "up",      "c1", "💰")
    kpi(k2, "Units Sold",      f"{units:,.0f}",           f"{transactions} transactions",    "neutral", "c2", "📦")
    kpi(k3, "Avg Sell Price",  f"₹{avg_price:,.0f}",     f"Avg disc: {avg_disc:.1f}%",      "neutral", "c3", "🏷️")
    kpi(k4, "Return Rate",     f"{return_rate:.1f}%",     f"₹{return_amt:,.0f} returned",   "down" if return_rate > 10 else "up", "c4", "↩️")
    kpi(k5, "Gross Margin",    f"{gross_margin:.1f}%",    f"₹{total_disc:,.0f} discounted", "up" if gross_margin > 30 else "neutral", "c5", "📊")

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

    # ── Story row 1: 3 charts ─────────────────────────────────────────────────
    sc1, sc2, sc3 = st.columns(3)

    # A — Monthly Revenue & Units (dual axis)
    with sc1:
        mt = idf_sales.groupby('MONTH').agg(Revenue=('REVENUE','sum'), Units=('QTY','sum')).reset_index().sort_values('MONTH')
        figA = go.Figure()
        figA.add_trace(go.Bar(
            x=mt['MONTH'], y=mt['Revenue'], name='Revenue',
            marker_color='rgba(79,142,247,0.80)',
            hovertemplate="<b>%{x}</b><br>Revenue: ₹%{y:,.0f}<extra></extra>",
        ))
        figA.add_trace(go.Scatter(
            x=mt['MONTH'], y=mt['Units'], name='Units', yaxis='y2',
            line=dict(color=ACCENT2, width=2), marker=dict(size=4),
            hovertemplate="<b>%{x}</b><br>Units: %{y:,.0f}<extra></extra>",
        ))
        figA.update_layout(
            yaxis=dict(title='Revenue (₹)', showgrid=True, gridcolor=GRID_COL,
                       tickformat=',', tickfont=dict(color=TEXT_SEC, size=9),
                       title_font=dict(color=TEXT_SEC, size=10)),
            yaxis2=dict(title='Units', overlaying='y', side='right', showgrid=False,
                        tickfont=dict(color=TEXT_SEC, size=9),
                        title_font=dict(color=TEXT_SEC, size=10)),
            xaxis=dict(title='Month', tickangle=-35, tickfont=dict(size=8, color=TEXT_SEC),
                       title_font=dict(color=TEXT_SEC, size=10)),
            barmode='overlay',
        )
        figA = dark_fig(figA, height=230)
        st.markdown('<div class="story-chart-card"><div class="story-chart-title">📅 Monthly Revenue & Units</div>', unsafe_allow_html=True)
        st.plotly_chart(figA, use_container_width=True, key="sA")
        st.markdown("</div>", unsafe_allow_html=True)

    # B — Sub-dimension breakdown
    with sc2:
        sub_dim = 'BRAND' if dim_col == 'ITEM' else 'ITEM'
        sub_lbl = 'Brand'  if dim_col == 'ITEM' else 'Product'
        sub = idf_sales.groupby(sub_dim)['REVENUE'].sum().reset_index().sort_values('REVENUE', ascending=False).head(8)
        figB = go.Figure(go.Bar(
            x=sub[sub_dim], y=sub['REVENUE'],
            marker_color=[PALETTE[i % len(PALETTE)] for i in range(len(sub))],
            text=[f"₹{v:,.0f}" for v in sub['REVENUE']],
            textposition='outside', textfont=dict(size=9, color=TEXT_SEC),
            hovertemplate=f"<b>%{{x}}</b><br>Revenue: ₹%{{y:,.0f}}<extra></extra>",
            name='Revenue',
        ))
        figB.update_xaxes(title_text=sub_lbl, tickangle=-30, tickfont=dict(size=8))
        figB.update_yaxes(title_text='Revenue (₹)', showgrid=True, tickformat=',')
        figB = dark_fig(figB, height=230, showlegend=False)
        st.markdown(f'<div class="story-chart-card"><div class="story-chart-title">🔎 Revenue by {sub_lbl}</div>', unsafe_allow_html=True)
        st.plotly_chart(figB, use_container_width=True, key="sB")
        st.markdown("</div>", unsafe_allow_html=True)

    # C — Sales vs Returns by month
    with sc3:
        sr = pd.merge(
            idf_sales.groupby('MONTH')['REVENUE'].sum().reset_index(),
            idf_returns.groupby('MONTH')['RETURN_AMT'].sum().reset_index(),
            on='MONTH', how='outer'
        ).fillna(0).sort_values('MONTH')
        figC = go.Figure()
        figC.add_trace(go.Bar(x=sr['MONTH'], y=sr['REVENUE'],    name='Sales',   marker_color='rgba(79,142,247,0.82)', hovertemplate="Sales: ₹%{y:,.0f}<extra></extra>"))
        figC.add_trace(go.Bar(x=sr['MONTH'], y=sr['RETURN_AMT'], name='Returns', marker_color='rgba(252,129,129,0.82)', hovertemplate="Returns: ₹%{y:,.0f}<extra></extra>"))
        figC.update_layout(barmode='group')
        figC.update_xaxes(title_text='Month', tickangle=-35, tickfont=dict(size=8))
        figC.update_yaxes(title_text='Amount (₹)', showgrid=True, tickformat=',')
        figC = dark_fig(figC, height=230)
        st.markdown('<div class="story-chart-card"><div class="story-chart-title">↩️ Sales vs Returns</div>', unsafe_allow_html=True)
        st.plotly_chart(figC, use_container_width=True, key="sC")
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Story row 2: 2 charts ─────────────────────────────────────────────────
    sd1, sd2 = st.columns([3, 2])

    with sd1:
        sz = idf_sales.groupby('SIZE_NAME')['QTY'].sum().reset_index()
        sz = sz[sz['SIZE_NAME'].notna()].sort_values('QTY', ascending=False)
        figD = go.Figure(go.Bar(
            y=sz['SIZE_NAME'], x=sz['QTY'], orientation='h',
            marker_color=[PALETTE[i % len(PALETTE)] for i in range(len(sz))],
            text=[f"{v:.0f}" for v in sz['QTY']],
            textposition='outside', textfont=dict(size=9, color=TEXT_SEC),
            hovertemplate="<b>Size %{y}</b><br>Units: %{x:,.0f}<extra></extra>",
            name='Units',
        ))
        figD.update_yaxes(autorange='reversed', title_text='Size', tickfont=dict(size=9))
        figD.update_xaxes(title_text='Units Sold', showgrid=True, tickformat=',')
        figD = dark_fig(figD, height=210, showlegend=False)
        st.markdown('<div class="story-chart-card"><div class="story-chart-title">📐 Units by Size</div>', unsafe_allow_html=True)
        st.plotly_chart(figD, use_container_width=True, key="sD")
        st.markdown("</div>", unsafe_allow_html=True)

    with sd2:
        dm = idf_sales.groupby('MONTH')['Disc_Perc'].mean().reset_index().sort_values('MONTH')
        figE = go.Figure(go.Scatter(
            x=dm['MONTH'], y=dm['Disc_Perc'], name='Avg Discount %',
            mode='lines+markers',
            line=dict(color=ACCENT3, width=2.5, shape='spline'),
            marker=dict(size=5, color=ACCENT3),
            fill='tozeroy', fillcolor='rgba(246,173,85,0.10)',
            hovertemplate="<b>%{x}</b><br>Avg Disc: %{y:.1f}%<extra></extra>",
        ))
        figE.update_xaxes(title_text='Month', tickangle=-35, tickfont=dict(size=8))
        figE.update_yaxes(title_text='Discount %', showgrid=True, ticksuffix='%')
        figE = dark_fig(figE, height=210, showlegend=False)
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
