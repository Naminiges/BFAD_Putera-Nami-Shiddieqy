import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import streamlit as st
from pathlib import Path

# ============================================================
# Page Configuration
# ============================================================
st.set_page_config(
    page_title="E-Commerce Dashboard | Putera Nami Shiddieqy",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# Custom CSS
# ============================================================
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1rem;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.2rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .metric-card h3 {
        font-size: 0.85rem;
        margin: 0;
        opacity: 0.9;
    }
    .metric-card h2 {
        font-size: 1.8rem;
        margin: 0.3rem 0 0 0;
        font-weight: 700;
    }
    .metric-blue {
        background: linear-gradient(135deg, #2196F3 0%, #1565C0 100%);
    }
    .metric-green {
        background: linear-gradient(135deg, #4CAF50 0%, #2E7D32 100%);
    }
    .metric-orange {
        background: linear-gradient(135deg, #FF9800 0%, #E65100 100%);
    }
    .metric-purple {
        background: linear-gradient(135deg, #9C27B0 0%, #6A1B9A 100%);
    }
    .section-header {
        font-size: 1.4rem;
        font-weight: 600;
        border-left: 4px solid #1565C0;
        padding-left: 12px;
        margin: 1.5rem 0 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# Load Data
# ============================================================
@st.cache_data
def load_data():
    """Load and preprocess the main dataset."""
    # Determine the path to main_data.csv
    script_dir = Path(__file__).parent
    data_path = script_dir / "main_data.csv"

    if not data_path.exists():
        st.error(f"File main_data.csv tidak ditemukan di {data_path}. "
                 "Jalankan notebook terlebih dahulu untuk menghasilkan file ini.")
        st.stop()

    df = pd.read_csv(data_path)
    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
    df['order_month'] = df['order_purchase_timestamp'].dt.to_period('M').astype(str)
    df['order_date'] = df['order_purchase_timestamp'].dt.date
    return df


df = load_data()

# ============================================================
# Sidebar – Date Range Filter
# ============================================================
st.sidebar.markdown("## Filter Data")

min_date = df['order_purchase_timestamp'].min().date()
max_date = df['order_purchase_timestamp'].max().date()

start_date = st.sidebar.date_input(
    "Tanggal Mulai", min_date, min_value=min_date, max_value=max_date
)
end_date = st.sidebar.date_input(
    "Tanggal Akhir", max_date, min_value=min_date, max_value=max_date
)

# Validate date range
if start_date > end_date:
    st.sidebar.error("Tanggal mulai tidak boleh lebih besar dari tanggal akhir!")
    st.stop()

# Filter data by date range
mask = (df['order_purchase_timestamp'].dt.date >= start_date) & \
       (df['order_purchase_timestamp'].dt.date <= end_date)
filtered_df = df[mask].copy()

if filtered_df.empty:
    st.warning("Tidak ada data untuk rentang tanggal yang dipilih.")
    st.stop()

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Data:** {len(filtered_df):,} baris")
st.sidebar.markdown(f"**Periode:** {start_date} s/d {end_date}")

# ============================================================
# Header
# ============================================================
st.markdown('<p class="main-header">E-Commerce Public Dataset Dashboard</p>',
            unsafe_allow_html=True)
st.markdown('<p class="sub-header">Analisis interaktif data e-commerce Brasil | '
            'Putera Nami Shiddieqy</p>', unsafe_allow_html=True)

# ============================================================
# Key Metrics
# ============================================================
total_orders = filtered_df['order_id'].nunique()
total_revenue = filtered_df['price'].sum()
total_customers = filtered_df['customer_unique_id'].nunique()
avg_review = filtered_df['review_score'].mean()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card metric-blue">
        <h3>Total Pesanan</h3>
        <h2>{total_orders:,}</h2>
    </div>""", unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card metric-green">
        <h3>Total Pendapatan</h3>
        <h2>R$ {total_revenue:,.0f}</h2>
    </div>""", unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card metric-orange">
        <h3>Total Pelanggan</h3>
        <h2>{total_customers:,}</h2>
    </div>""", unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card metric-purple">
        <h3>Rata-rata Review</h3>
        <h2>{avg_review:.2f}</h2>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================
# 1. Monthly Order & Revenue Trend
# ============================================================
st.markdown('<p class="section-header">Tren Pesanan & Pendapatan Bulanan</p>',
            unsafe_allow_html=True)

monthly = filtered_df.groupby('order_month').agg(
    total_orders=('order_id', 'nunique'),
    total_revenue=('price', 'sum')
).reset_index()

fig, ax1 = plt.subplots(figsize=(14, 5))

color_bar = '#2196F3'
color_line = '#FF5722'

x = range(len(monthly))
ax1.bar(x, monthly['total_orders'], color=color_bar, alpha=0.7,
        label='Jumlah Pesanan', width=0.6)
ax1.set_xlabel('Bulan', fontsize=11, fontweight='bold')
ax1.set_ylabel('Jumlah Pesanan', color=color_bar, fontsize=11, fontweight='bold')
ax1.tick_params(axis='y', labelcolor=color_bar)

step = max(1, len(monthly) // 12)
ax1.set_xticks(list(x)[::step])
ax1.set_xticklabels(monthly['order_month'].values[::step], rotation=45,
                    ha='right', fontsize=9)

ax2 = ax1.twinx()
ax2.plot(x, monthly['total_revenue'], color=color_line, linewidth=2.5,
         marker='o', markersize=4, label='Total Pendapatan (R$)')
ax2.set_ylabel('Total Pendapatan (R$)', color=color_line, fontsize=11,
               fontweight='bold')
ax2.tick_params(axis='y', labelcolor=color_line)
ax2.yaxis.set_major_formatter(
    ticker.FuncFormatter(lambda val, p: f'R$ {val:,.0f}'))

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=10)

plt.title('Tren Jumlah Pesanan dan Total Pendapatan per Bulan',
          fontsize=14, fontweight='bold', pad=12)
fig.tight_layout()
st.pyplot(fig)
plt.close()

# ============================================================
# 2. Top Product Categories
# ============================================================
st.markdown('<p class="section-header">Kategori Produk Terpopuler</p>',
            unsafe_allow_html=True)

col_left, col_right = st.columns(2)

# By order count
category_stats = filtered_df.groupby('product_category_name_english').agg(
    total_orders=('order_id', 'nunique'),
    total_revenue=('price', 'sum')
).reset_index()

with col_left:
    st.markdown("**Top 10 – Berdasarkan Jumlah Pesanan**")
    top_orders = category_stats.nlargest(10, 'total_orders')

    fig, ax = plt.subplots(figsize=(8, 5))
    colors = ['#1565C0' if i == 0 else '#90CAF9' for i in range(len(top_orders))]
    bars = ax.barh(
        top_orders['product_category_name_english'].values[::-1],
        top_orders['total_orders'].values[::-1],
        color=colors[::-1], edgecolor='white'
    )
    for bar, val in zip(bars, top_orders['total_orders'].values[::-1]):
        ax.text(bar.get_width() + 30, bar.get_y() + bar.get_height() / 2.,
                f'{val:,}', ha='left', va='center', fontweight='bold', fontsize=9)
    ax.set_xlabel('Jumlah Pesanan', fontsize=10)
    ax.set_title('Top 10 Kategori (Pesanan)', fontsize=12, fontweight='bold')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col_right:
    st.markdown("**Top 10 – Berdasarkan Total Pendapatan**")
    top_revenue = category_stats.nlargest(10, 'total_revenue')

    fig, ax = plt.subplots(figsize=(8, 5))
    colors = ['#C62828' if i == 0 else '#EF9A9A' for i in range(len(top_revenue))]
    bars = ax.barh(
        top_revenue['product_category_name_english'].values[::-1],
        top_revenue['total_revenue'].values[::-1],
        color=colors[::-1], edgecolor='white'
    )
    for bar, val in zip(bars, top_revenue['total_revenue'].values[::-1]):
        ax.text(bar.get_width() + 1000, bar.get_y() + bar.get_height() / 2.,
                f'R$ {val:,.0f}', ha='left', va='center', fontweight='bold',
                fontsize=9)
    ax.set_xlabel('Total Pendapatan (R$)', fontsize=10)
    ax.set_title('Top 10 Kategori (Revenue)', fontsize=12, fontweight='bold')
    ax.xaxis.set_major_formatter(
        ticker.FuncFormatter(lambda val, p: f'R$ {val:,.0f}'))
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

# ============================================================
# 3. Customer Distribution by State
# ============================================================
st.markdown('<p class="section-header">Distribusi Pelanggan per State</p>',
            unsafe_allow_html=True)

state_stats = filtered_df.groupby('customer_state').agg(
    total_customers=('customer_unique_id', 'nunique'),
    total_orders=('order_id', 'nunique'),
    total_revenue=('price', 'sum')
).sort_values('total_orders', ascending=False).reset_index()

col_map, col_table = st.columns([2, 1])

with col_map:
    top_states = state_stats.head(10)
    fig, ax = plt.subplots(figsize=(10, 5))
    colors_state = sns.color_palette("Blues_r", len(top_states))
    bars = ax.bar(top_states['customer_state'], top_states['total_orders'],
                  color=colors_state, edgecolor='white')
    for bar, val in zip(bars, top_states['total_orders']):
        ax.text(bar.get_x() + bar.get_width() / 2., bar.get_height() + 50,
                f'{val:,}', ha='center', va='bottom', fontweight='bold',
                fontsize=9)
    ax.set_title('Top 10 State berdasarkan Jumlah Pesanan',
                 fontsize=13, fontweight='bold')
    ax.set_xlabel('State', fontsize=11)
    ax.set_ylabel('Jumlah Pesanan', fontsize=11)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col_table:
    st.markdown("**Detail per State**")
    display_df = state_stats[['customer_state', 'total_customers',
                               'total_orders']].head(10).copy()
    display_df.columns = ['State', 'Pelanggan', 'Pesanan']
    display_df = display_df.reset_index(drop=True)
    display_df.index = display_df.index + 1
    st.dataframe(display_df, use_container_width=True)

# ============================================================
# 4. RFM Analysis
# ============================================================
st.markdown('<p class="section-header">RFM Analysis – Segmentasi Pelanggan</p>',
            unsafe_allow_html=True)

reference_date = filtered_df['order_purchase_timestamp'].max() + pd.Timedelta(days=1)

rfm = filtered_df.groupby('customer_unique_id').agg(
    recency=('order_purchase_timestamp', lambda x: (reference_date - x.max()).days),
    frequency=('order_id', 'nunique'),
    monetary=('price', 'sum')
).reset_index()

# Scoring
rfm['r_score'] = pd.qcut(rfm['recency'], q=4, labels=[4, 3, 2, 1])
rfm['f_score'] = pd.qcut(rfm['frequency'].rank(method='first'), q=4,
                          labels=[1, 2, 3, 4])
rfm['m_score'] = pd.qcut(rfm['monetary'], q=4, labels=[1, 2, 3, 4])


def rfm_segment(row):
    r = int(row['r_score'])
    f = int(row['f_score'])
    m = int(row['m_score'])
    if r >= 3 and f >= 3 and m >= 3:
        return 'Best Customers'
    elif r >= 3 and f >= 2:
        return 'Loyal Customers'
    elif r >= 3 and m >= 3:
        return 'Big Spenders'
    elif r >= 3:
        return 'Recent Customers'
    elif f >= 3:
        return 'Frequent Buyers'
    elif r <= 2 and f <= 2 and m <= 2:
        return 'Lost Customers'
    elif r <= 2:
        return 'At Risk'
    else:
        return 'Others'


rfm['segment'] = rfm.apply(rfm_segment, axis=1)

# --- RFM metrics cards ---
col_r, col_f, col_m = st.columns(3)
with col_r:
    avg_r = int(rfm['recency'].mean())
    st.metric("Avg Recency (hari)", f"{avg_r}")
with col_f:
    avg_f = round(rfm['frequency'].mean(), 2)
    st.metric("Avg Frequency", f"{avg_f}")
with col_m:
    avg_m = round(rfm['monetary'].mean(), 2)
    st.metric("Avg Monetary (R$)", f"R$ {avg_m:,.2f}")

# --- Segment bar charts ---
segment_colors = {
    'Best Customers': '#4CAF50',
    'Loyal Customers': '#2196F3',
    'Big Spenders': '#FF9800',
    'Recent Customers': '#9C27B0',
    'Frequent Buyers': '#00BCD4',
    'At Risk': '#F44336',
    'Lost Customers': '#795548',
    'Others': '#9E9E9E'
}

seg_summary = rfm.groupby('segment').agg(
    count=('customer_unique_id', 'count'),
    avg_recency=('recency', 'mean'),
    avg_frequency=('frequency', 'mean'),
    avg_monetary=('monetary', 'mean')
).sort_values('count', ascending=False)

col_chart, col_detail = st.columns([2, 1])

with col_chart:
    fig, ax = plt.subplots(figsize=(10, 5))
    seg_data = rfm['segment'].value_counts()
    colors_pie = [segment_colors.get(s, '#9E9E9E') for s in seg_data.index]

    wedges, texts, autotexts = ax.pie(
        seg_data.values, labels=seg_data.index, autopct='%1.1f%%',
        colors=colors_pie, startangle=90, pctdistance=0.82,
        wedgeprops=dict(width=0.5, edgecolor='white', linewidth=2)
    )
    for at in autotexts:
        at.set_fontsize(9)
        at.set_fontweight('bold')

    centre = plt.Circle((0, 0), 0.55, fc='white')
    ax.add_artist(centre)
    ax.set_title('Distribusi Segmen Pelanggan', fontsize=13, fontweight='bold',
                 pad=15)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col_detail:
    st.markdown("**Detail Segmen Pelanggan**")
    detail_df = seg_summary.copy()
    detail_df.columns = ['Jumlah', 'Avg Recency', 'Avg Frequency', 'Avg Monetary']
    detail_df = detail_df.round(2)
    st.dataframe(detail_df, use_container_width=True)

# ============================================================
# 5. Review Score Distribution
# ============================================================
st.markdown('<p class="section-header">Distribusi Review Score</p>',
            unsafe_allow_html=True)

col_rev1, col_rev2 = st.columns(2)

with col_rev1:
    review_dist = filtered_df['review_score'].value_counts().sort_index()
    fig, ax = plt.subplots(figsize=(8, 4))
    colors_rev = ['#F44336', '#FF9800', '#FFC107', '#8BC34A', '#4CAF50']
    bars = ax.bar(review_dist.index.astype(str), review_dist.values,
                  color=colors_rev, edgecolor='white', linewidth=0.5)
    for bar, val in zip(bars, review_dist.values):
        ax.text(bar.get_x() + bar.get_width() / 2., bar.get_height() + 200,
                f'{val:,}', ha='center', va='bottom', fontweight='bold',
                fontsize=10)
    ax.set_title('Distribusi Review Score', fontsize=13, fontweight='bold')
    ax.set_xlabel('Review Score', fontsize=11)
    ax.set_ylabel('Jumlah', fontsize=11)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col_rev2:
    # Review by top 5 categories
    top5 = category_stats.nlargest(5, 'total_orders')[
        'product_category_name_english'].values
    top5_data = filtered_df[
        filtered_df['product_category_name_english'].isin(top5)]
    avg_review_cat = top5_data.groupby(
        'product_category_name_english')['review_score'].mean().sort_values(
        ascending=False)

    fig, ax = plt.subplots(figsize=(8, 4))
    colors_cat = sns.color_palette("YlGn_r", len(avg_review_cat))
    bars = ax.barh(avg_review_cat.index[::-1], avg_review_cat.values[::-1],
                   color=colors_cat[::-1], edgecolor='white')
    for bar, val in zip(bars, avg_review_cat.values[::-1]):
        ax.text(bar.get_width() + 0.02, bar.get_y() + bar.get_height() / 2.,
                f'{val:.2f}', ha='left', va='center', fontweight='bold',
                fontsize=10)
    ax.set_title('Rata-rata Review – Top 5 Kategori', fontsize=13,
                 fontweight='bold')
    ax.set_xlabel('Rata-rata Review Score', fontsize=11)
    ax.set_xlim(0, 5.5)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

# ============================================================
# Footer
# ============================================================
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#999; font-size:0.85rem;'>"
    "Dashboard E-Commerce Public Dataset | "
    "Dibuat oleh <strong>Putera Nami Shiddieqy</strong> | "
    "Dicoding CodingCamp 2026</p>",
    unsafe_allow_html=True
)
