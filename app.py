"""
app.py — Main Streamlit Dashboard Application
SMS Spam Collection — Data Visualization Dashboard
Course: Exploratory Data Analysis | Instructor: Ali Hassan Sherazi
Submission Date: 05-June-2026
"""

import streamlit as st
import pandas as pd

from filters import load_data, clean_and_engineer, apply_filters, reset_filters, get_kpis
from charts  import (
    chart_pie, chart_histogram, chart_line,  chart_bar,
    chart_scatter, chart_box,   chart_heatmap, chart_area,
    chart_count,   chart_violin
)

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title='SMS Spam Dashboard',
    page_icon='📩',
    layout='wide',
    initial_sidebar_state='expanded'
)

# ─────────────────────────────────────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main-title  { font-size:2.2rem; font-weight:700; color:#1A237E; margin-bottom:0; }
    .sub-title   { font-size:1rem;   color:#555;      margin-top:0;   }
    .kpi-card    { background:#F5F7FA; border-radius:10px; padding:16px 20px;
                   border-left:5px solid #1A237E; }
    .kpi-label   { font-size:.85rem; color:#888; margin:0; }
    .kpi-value   { font-size:1.6rem; font-weight:700; color:#1A237E; margin:0; }
    .section-hdr { font-size:1.15rem; font-weight:600;
                   border-bottom:2px solid #E0E0E0; padding-bottom:4px;
                   margin-top:1.5rem; color:#333; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# LOAD DATA (cached)
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data
def get_data():
    raw = load_data()
    return clean_and_engineer(raw)

df_full = get_data()

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR — FILTERS
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('## 🔍 Dashboard Filters')
    st.markdown('All filters update every chart simultaneously.')
    st.divider()

    # Category Filter
    label_opts  = ['All', 'Ham', 'Spam']
    label_sel   = st.selectbox('📂 Category Filter (Label)', label_opts, index=0)

    st.divider()

    # Numerical Range Sliders
    len_min, len_max = int(df_full['msg_length'].min()), int(df_full['msg_length'].max())
    len_range = st.slider('📏 Message Length Range (chars)',
                          len_min, len_max, (len_min, len_max))

    wc_min, wc_max = int(df_full['word_count'].min()), int(df_full['word_count'].max())
    wc_range  = st.slider('📝 Word Count Range',
                          wc_min, wc_max, (wc_min, wc_max))

    st.divider()

    # Multi-Select Filter
    url_opts = ['All', 'No URL', 'Has URL']
    url_sel  = st.selectbox('🔗 Multi-Select: URL Filter', url_opts, index=0)

    st.divider()

    # Text / Keyword Search
    keyword = st.text_input('🔎 Search / Text Filter (keyword in message)', '')

    st.divider()

    # Reset Button
    if st.button('🔄 Reset All Filters', use_container_width=True):
        st.rerun()

    st.caption('SMS Spam Collection Dashboard\nEDA Course — Ali Hassan Sherazi')

# ─────────────────────────────────────────────────────────────────────────────
# APPLY FILTERS
# ─────────────────────────────────────────────────────────────────────────────
df = apply_filters(
    df_full,
    label_filter     = None if label_sel == 'All' else label_sel,
    msg_len_range    = len_range,
    word_count_range = wc_range,
    url_filter       = None if url_sel == 'All' else url_sel,
    keyword          = keyword
)

# ─────────────────────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<p class="main-title">📩 SMS Spam Collection — Data Dashboard</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Exploratory Data Analysis | Instructor: Ali Hassan Sherazi | Submission: 05-June-2026</p>', unsafe_allow_html=True)
st.caption(f'Showing **{len(df):,}** of **{len(df_full):,}** messages after filters.')
st.divider()

# Guard: stop gracefully if filters removed everything
if len(df) == 0:
    st.warning('⚠️ No messages match the current filters. Adjust the filters or click "Reset All Filters" in the sidebar.')
    st.stop()

# ─────────────────────────────────────────────────────────────────────────────
# KPI CARDS
# ─────────────────────────────────────────────────────────────────────────────
kpis = get_kpis(df)
st.markdown('<p class="section-hdr">📌 KPI Summary</p>', unsafe_allow_html=True)

c1, c2, c3, c4, c5, c6 = st.columns(6)
for col, label, value in [
    (c1, 'Total Messages',   f"{kpis['total']:,}"),
    (c2, '🚫 Spam Count',    f"{kpis['spam_count']:,}  ({kpis['spam_pct']}%)"),
    (c3, '✅ Ham Count',     f"{kpis['ham_count']:,}"),
    (c4, 'Avg Msg Length',   f"{kpis['avg_length']} chars"),
    (c5, 'Max Msg Length',   f"{kpis['max_length']} chars"),
    (c6, 'Messages w/ URL',  f"{kpis['url_pct']}%"),
]:
    col.markdown(
        f'<div class="kpi-card"><p class="kpi-label">{label}</p>'
        f'<p class="kpi-value">{value}</p></div>',
        unsafe_allow_html=True
    )

st.divider()

# ─────────────────────────────────────────────────────────────────────────────
# ROW 1 — Pie + Histogram
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<p class="section-hdr">📊 Distribution Overview</p>', unsafe_allow_html=True)
col1, col2 = st.columns([1, 2])
with col1:
    st.pyplot(chart_pie(df), use_container_width=True)
with col2:
    st.pyplot(chart_histogram(df), use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# ROW 2 — Bar + Scatter
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<p class="section-hdr">📈 Feature Comparisons</p>', unsafe_allow_html=True)
col3, col4 = st.columns(2)
with col3:
    st.pyplot(chart_bar(df), use_container_width=True)
with col4:
    st.pyplot(chart_scatter(df), use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# ROW 3 — Line + Count
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<p class="section-hdr">📉 Trends & Counts</p>', unsafe_allow_html=True)
col5, col6 = st.columns(2)
with col5:
    st.pyplot(chart_line(df), use_container_width=True)
with col6:
    st.pyplot(chart_count(df), use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# ROW 4 — Box + Violin
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<p class="section-hdr">🎻 Statistical Distributions</p>', unsafe_allow_html=True)
st.pyplot(chart_box(df),    use_container_width=True)
st.pyplot(chart_violin(df), use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# ROW 5 — Heatmap + Area
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<p class="section-hdr">🔥 Correlations & Cumulative Trends</p>', unsafe_allow_html=True)
col7, col8 = st.columns([1, 1])
with col7:
    st.pyplot(chart_heatmap(df), use_container_width=True)
with col8:
    st.pyplot(chart_area(df),    use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# FOOTER — Raw Data Table
# ─────────────────────────────────────────────────────────────────────────────
st.divider()
st.markdown('<p class="section-hdr">🗂️ Filtered Data Preview</p>', unsafe_allow_html=True)
show_cols = ['label', 'message', 'msg_length', 'word_count',
             'upper_count', 'digit_count', 'url_label']
st.dataframe(df[show_cols].head(100), use_container_width=True, height=300)
st.caption(f'Displaying first 100 of {len(df):,} filtered rows.')
