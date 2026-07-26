import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="E-Commerce Dashboard",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# GLOBAL CSS  -  fonts, gradients, glassmorphism, animations
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&family=Inter:wght@400;500;600&display=swap');

html, body, [class*="css"]  {
    font-family: 'Inter', sans-serif;
}

/* ---------- Animated gradient background ---------- */
.stApp {
    background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #1a1a3c);
    background-size: 400% 400%;
    animation: gradientShift 18s ease infinite;
}
@keyframes gradientShift {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* ---------- Fade-in for main block ---------- */
.block-container {
    animation: fadeInUp 0.8s ease-out;
    padding-top: 2rem;
}
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(25px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* ---------- Title ---------- */
.dashboard-title {
    font-family: 'Poppins', sans-serif;
    font-weight: 800;
    font-size: 2.6rem;
    background: linear-gradient(90deg, #00d4ff, #7b2ff7, #ff6ec4, #00d4ff);
    background-size: 300% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: shine 6s linear infinite;
    margin-bottom: 0;
}
@keyframes shine {
    to { background-position: 300% center; }
}
.dashboard-subtitle {
    color: #b5b5d1;
    font-size: 1rem;
    font-weight: 400;
    margin-top: -5px;
    letter-spacing: 0.3px;
}

/* ---------- Glass KPI cards ---------- */
.kpi-card {
    background: rgba(255, 255, 255, 0.06);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 18px;
    padding: 22px 20px;
    text-align: left;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.25);
    transition: transform 0.35s ease, box-shadow 0.35s ease, border 0.35s ease;
    animation: fadeInUp 0.9s ease-out;
    position: relative;
    overflow: hidden;
}
.kpi-card:hover {
    transform: translateY(-6px) scale(1.02);
    box-shadow: 0 14px 40px rgba(123, 47, 247, 0.35);
    border: 1px solid rgba(0, 212, 255, 0.5);
}
.kpi-card::before {
    content: "";
    position: absolute;
    top: -50%; left: -50%;
    width: 200%; height: 200%;
    background: radial-gradient(circle, rgba(0,212,255,0.08) 0%, transparent 60%);
    animation: rotateGlow 12s linear infinite;
}
@keyframes rotateGlow {
    from { transform: rotate(0deg); }
    to   { transform: rotate(360deg); }
}
.kpi-icon {
    font-size: 1.8rem;
    margin-bottom: 6px;
}
.kpi-label {
    color: #a9a9c8;
    font-size: 0.85rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.6px;
}
.kpi-value {
    font-family: 'Poppins', sans-serif;
    font-size: 1.9rem;
    font-weight: 700;
    color: #ffffff;
    margin-top: 2px;
}
.kpi-delta {
    font-size: 0.8rem;
    color: #6be3a7;
    margin-top: 4px;
}

/* ---------- Tabs styling ---------- */
button[data-baseweb="tab"] {
    font-family: 'Poppins', sans-serif;
    font-weight: 600;
    font-size: 1rem;
    color: #b5b5d1;
    transition: color 0.3s ease;
}
button[data-baseweb="tab"]:hover {
    color: #00d4ff;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: #00d4ff !important;
}
div[data-baseweb="tab-highlight"] {
    background: linear-gradient(90deg, #00d4ff, #7b2ff7) !important;
    height: 3px !important;
    border-radius: 3px;
}

/* ---------- Section headers ---------- */
.section-header {
    font-family: 'Poppins', sans-serif;
    font-weight: 600;
    font-size: 1.25rem;
    color: #f0f0ff;
    border-left: 4px solid #00d4ff;
    padding-left: 12px;
    margin: 24px 0 12px 0;
    animation: fadeInUp 0.6s ease-out;
}

/* ---------- Chart container card ---------- */
.chart-card {
    background: rgba(255, 255, 255, 0.04);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 10px 14px 4px 14px;
    margin-bottom: 18px;
    transition: box-shadow 0.3s ease;
}
.chart-card:hover {
    box-shadow: 0 10px 30px rgba(0, 212, 255, 0.15);
}

/* ---------- Sidebar ---------- */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #14142b 0%, #1f1f3d 100%);
    border-right: 1px solid rgba(255,255,255,0.08);
}
section[data-testid="stSidebar"] * {
    color: #e4e4f5 !important;
}
.sidebar-footer {
    margin-top: 30px;
    padding-top: 14px;
    border-top: 1px solid rgba(255,255,255,0.15);
    font-size: 0.8rem;
    color: #8f8fb3 !important;
    animation: fadeInUp 1s ease-out;
}

/* ---------- Scrollbar ---------- */
::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #00d4ff, #7b2ff7);
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# Consistent Plotly template for every chart
PLOTLY_TEMPLATE = "plotly_dark"
COLOR_SEQUENCE = px.colors.sequential.Plasma_r
COLOR_SEQUENCE_DISCRETE = ["#00d4ff", "#7b2ff7", "#ff6ec4", "#6be3a7", "#ffd166", "#ff8fab"]

def style_fig(fig, height=420):
    """Apply a shared modern look + subtle entrance animation to every figure."""
    fig.update_layout(
        template=PLOTLY_TEMPLATE,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color="#e8e8f5", size=13),
        title_font=dict(family="Poppins, sans-serif", size=17, color="#ffffff"),
        margin=dict(l=10, r=10, t=55, b=10),
        height=height,
        hoverlabel=dict(bgcolor="#1f1f3d", font_size=13, font_family="Inter"),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
        transition=dict(duration=600, easing="cubic-in-out"),
    )
    fig.update_xaxes(showgrid=True, gridcolor="rgba(255,255,255,0.06)", zeroline=False)
    fig.update_yaxes(showgrid=True, gridcolor="rgba(255,255,255,0.06)", zeroline=False)
    return fig

# =========================================================
# LOAD DATA
# =========================================================
@st.cache_data
def load_data():
    df = pd.read_csv("data/cleaned_data.csv")
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    return df

df = load_data()

# =========================================================
# SIDEBAR
# =========================================================
st.sidebar.markdown("## 🎛️ Filters")

locations = sorted(df['Country'].dropna().unique())
location_option = st.sidebar.selectbox(
    "📍 Select Location",
    ["Global"] + list(locations)
)

min_date = df['InvoiceDate'].min()
max_date = df['InvoiceDate'].max()

date_range = st.sidebar.date_input(
    "📅 Select Date Range",
    [min_date, max_date]
)

# =========================================================
# APPLY FILTERS
# =========================================================
filtered_df = df.copy()

if location_option != "Global":
    filtered_df = filtered_df[filtered_df['Country'] == location_option]

if len(date_range) == 2:
    filtered_df = filtered_df[
        (filtered_df['InvoiceDate'] >= pd.to_datetime(date_range[0])) &
        (filtered_df['InvoiceDate'] <= pd.to_datetime(date_range[1]))
    ]

st.sidebar.markdown(
    """<div class="sidebar-footer">
    ✨ <b>Pritthish Lal Chattaraj</b><br>
    Internship Project Dashboard
    </div>""",
    unsafe_allow_html=True
)

# =========================================================
# MAIN TITLE
# =========================================================
st.markdown('<div class="dashboard-title">🛍️ E-Commerce Interactive Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="dashboard-subtitle">Real-time customer, product & country intelligence</div>', unsafe_allow_html=True)
st.write("")

# =========================================================
# TOP-LEVEL KPI ROW
# =========================================================
total_revenue = filtered_df['TotalPrice'].sum() if 'TotalPrice' in filtered_df else 0
total_customers = filtered_df['CustomerID'].nunique() if 'CustomerID' in filtered_df else 0
total_orders = filtered_df['InvoiceNo'].nunique() if 'InvoiceNo' in filtered_df else len(filtered_df)
avg_order_value = (total_revenue / total_orders) if total_orders else 0

kpi_cols = st.columns(4)
kpi_data = [
    ("💰", "Total Revenue", f"£{total_revenue:,.0f}"),
    ("👥", "Unique Customers", f"{total_customers:,}"),
    ("🧾", "Total Orders", f"{total_orders:,}"),
    ("📈", "Avg Order Value", f"£{avg_order_value:,.2f}"),
]
for col, (icon, label, value) in zip(kpi_cols, kpi_data):
    with col:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">{icon}</div>
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
        </div>
        """, unsafe_allow_html=True)

st.write("")

# =========================================================
# TABS
# =========================================================
tab1, tab2, tab3 = st.tabs(["👤 Customer", "📦 Product", "🌍 Country"])

# =========================================================
# CUSTOMER TAB
# =========================================================
with tab1:
    st.markdown('<div class="section-header">Customer Analysis</div>', unsafe_allow_html=True)

    rfm = pd.read_csv("data/rfm_data.csv")

    rfm['R_score'] = pd.qcut(rfm['Recency'], q=4, labels=[4, 3, 2, 1], duplicates='drop')
    rfm['F_score'] = pd.qcut(rfm['Frequency'].rank(method='first'), q=4, labels=[1, 2, 3, 4], duplicates='drop')
    rfm['M_score'] = pd.qcut(rfm['Monetary'], q=4, labels=[1, 2, 3, 4], duplicates='drop')

    rfm['R_score'] = rfm['R_score'].astype(int)
    rfm['F_score'] = rfm['F_score'].astype(int)
    rfm['M_score'] = rfm['M_score'].astype(int)

    rfm['RFM_Score'] = (
        rfm['R_score'].astype(str) +
        rfm['F_score'].astype(str) +
        rfm['M_score'].astype(str)
    )

    def segment_customer(row):
        if row['R_score'] == 4 and row['F_score'] == 4:
            return 'VIP'
        elif row['F_score'] >= 3:
            return 'Loyal'
        elif row['R_score'] == 1:
            return 'At Risk'
        else:
            return 'Regular'

    rfm['Segment'] = rfm.apply(segment_customer, axis=1)

    if location_option != "Global":
        customers_in_location = filtered_df['CustomerID'].unique()
        rfm = rfm[rfm['CustomerID'].isin(customers_in_location)]

    c1, c2 = st.columns([1, 1.2])

    with c1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        segment_counts = rfm['Segment'].value_counts().reset_index()
        segment_counts.columns = ['Segment', 'Count']

        fig1 = px.pie(
            segment_counts,
            names='Segment',
            values='Count',
            title="Customer Segment Distribution",
            hole=0.55,
            color_discrete_sequence=COLOR_SEQUENCE_DISCRETE
        )
        fig1.update_traces(
            textinfo="percent+label",
            pull=[0.06] * len(segment_counts),
            marker=dict(line=dict(color="#0f0c29", width=2))
        )
        st.plotly_chart(style_fig(fig1), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        seg_selected = rfm[rfm['Segment'].isin(['VIP', 'Loyal', 'At Risk'])]
        seg_count = seg_selected['Segment'].value_counts().reset_index()
        seg_count.columns = ['Segment', 'Count']

        fig3 = px.bar(
            seg_count,
            x='Segment',
            y='Count',
            title="VIP vs Loyal vs At Risk",
            color='Segment',
            color_discrete_sequence=COLOR_SEQUENCE_DISCRETE,
            text='Count'
        )
        fig3.update_traces(marker_line_width=0, textposition="outside")
        st.plotly_chart(style_fig(fig3), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    top_customers = rfm.sort_values(by='Monetary', ascending=False).head(10)
    fig2 = px.bar(
        top_customers,
        x='Monetary',
        y='CustomerID',
        orientation='h',
        title="Top 10 Customers by Spending",
        color='Monetary',
        color_continuous_scale=COLOR_SEQUENCE,
        text='Monetary'
    )
    fig2.update_traces(texttemplate='£%{text:,.0f}', textposition='outside', marker_line_width=0)
    fig2.update_layout(yaxis=dict(categoryorder="total ascending"))
    st.plotly_chart(style_fig(fig2, height=460), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# PRODUCT TAB
# =========================================================
with tab2:
    st.markdown('<div class="section-header">Product Analysis</div>', unsafe_allow_html=True)

    p1, p2 = st.columns(2)

    with p1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        product_df = filtered_df.groupby('Description')['Quantity'].sum().reset_index()
        product_df = product_df.sort_values(by='Quantity', ascending=False).head(10)

        fig3 = px.bar(
            product_df,
            x='Quantity',
            y='Description',
            orientation='h',
            title="Top 10 Products by Quantity Sold",
            color='Quantity',
            color_continuous_scale=COLOR_SEQUENCE,
            text='Quantity'
        )
        fig3.update_traces(textposition='outside', marker_line_width=0)
        fig3.update_layout(yaxis=dict(categoryorder="total ascending"))
        st.plotly_chart(style_fig(fig3, height=460), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with p2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        sales_product = filtered_df.groupby('Description')['TotalPrice'].sum().reset_index()
        sales_product = sales_product.sort_values(by='TotalPrice', ascending=False).head(10)

        fig4 = px.bar(
            sales_product,
            x='TotalPrice',
            y='Description',
            orientation='h',
            title="Top 10 Products by Revenue",
            color='TotalPrice',
            color_continuous_scale=COLOR_SEQUENCE,
            text='TotalPrice'
        )
        fig4.update_traces(texttemplate='£%{text:,.0f}', textposition='outside', marker_line_width=0)
        fig4.update_layout(yaxis=dict(categoryorder="total ascending"))
        st.plotly_chart(style_fig(fig4, height=460), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    treemap_df = filtered_df.groupby('Description')['TotalPrice'].sum().reset_index()
    treemap_df = treemap_df.sort_values(by='TotalPrice', ascending=False).head(25)
    fig_tree = px.treemap(
        treemap_df,
        path=['Description'],
        values='TotalPrice',
        title="Product Revenue Treemap (Top 25)",
        color='TotalPrice',
        color_continuous_scale=COLOR_SEQUENCE
    )
    fig_tree.update_traces(marker_line_width=1, marker_line_color="#0f0c29")
    st.plotly_chart(style_fig(fig_tree, height=480), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# COUNTRY TAB
# =========================================================
with tab3:
    st.markdown('<div class="section-header">Country Analysis</div>', unsafe_allow_html=True)

    country_df = filtered_df.groupby('Country')['TotalPrice'].sum().reset_index()

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    fig5 = px.choropleth(
        country_df,
        locations="Country",
        locationmode="country names",
        color="TotalPrice",
        title="Sales by Country",
        color_continuous_scale=COLOR_SEQUENCE,
        projection="natural earth"
    )
    fig5.update_geos(
        bgcolor="rgba(0,0,0,0)",
        showframe=False,
        showcoastlines=True,
        coastlinecolor="rgba(255,255,255,0.15)",
        landcolor="rgba(255,255,255,0.04)"
    )
    st.plotly_chart(style_fig(fig5, height=520), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    top_countries = country_df.sort_values(by='TotalPrice', ascending=False).head(10)
    fig6 = px.bar(
        top_countries,
        x='TotalPrice',
        y='Country',
        orientation='h',
        title="Top 10 Countries by Sales",
        color='TotalPrice',
        color_continuous_scale=COLOR_SEQUENCE,
        text='TotalPrice'
    )
    fig6.update_traces(texttemplate='£%{text:,.0f}', textposition='outside', marker_line_width=0)
    fig6.update_layout(yaxis=dict(categoryorder="total ascending"))
    st.plotly_chart(style_fig(fig6, height=460), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)