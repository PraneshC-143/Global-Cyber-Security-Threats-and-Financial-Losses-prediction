import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

# Set page config
st.set_page_config(page_title="Global Cyber Threats Dashboard", layout="wide", page_icon="🛡️")

# Custom CSS for a premium, interactive look
st.markdown("""
<style>
    /* Premium Dark Theme Elements */
    .stApp {
        background-color: #0F172A;
        color: #F8FAFC;
    }
    .main-header {
        font-size: 3rem;
        background: -webkit-linear-gradient(45deg, #3B82F6, #8B5CF6, #EC4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        text-align: center;
        margin-bottom: 1rem;
        animation: fadeIn 1.5s ease-in-out;
    }
    .sub-header {
        text-align: center;
        color: #94A3B8;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.4);
        border: 1px solid rgba(59, 130, 246, 0.4);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        background-color: #1E293B;
        padding: 10px 20px;
        border-radius: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 8px;
        color: #94A3B8;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stTabs [aria-selected="true"] {
        background-color: #3B82F6 !important;
        color: white !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(-20px); }
        100% { opacity: 1; transform: translateY(0); }
    }
</style>
""", unsafe_allow_html=True)

# Set plotly default theme to match dark UI
pio.templates.default = "plotly_dark"

# Create a session state to hold preprocessing logs
if 'preprocessing_logs' not in st.session_state:
    st.session_state['preprocessing_logs'] = []

def log_process(msg):
    st.session_state['preprocessing_logs'].append(msg)

# Load and Preprocess Data
@st.cache_data
def load_and_clean_data():
    try:
        # Load Raw Data
        df = pd.read_csv('c:/Users/ELCOT/.gemini/antigravity/scratch/Global_Cybersecurity_Threats_2015-2025.csv')
        raw_shape = df.shape
        st.session_state['preprocessing_logs'] = [] # Reset logs
        log_process(f"✅ Loaded raw dataset with {raw_shape[0]} rows and {raw_shape[1]} columns.")

        # Preprocessing Step 1: Missing Values
        missing_counts = df.isnull().sum().sum()
        if missing_counts > 0:
            df = df.dropna()
            log_process(f"⚠️ Found {missing_counts} missing values. Handled by dropping incomplete rows. New shape: {df.shape}")
        else:
            log_process("✅ No missing values detected in the dataset.")

        # Preprocessing Step 2: Data Types
        df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
        df['Financial Loss (in Million $)'] = pd.to_numeric(df['Financial Loss (in Million $)'], errors='coerce')
        df['Incident Resolution Time (in Hours)'] = pd.to_numeric(df['Incident Resolution Time (in Hours)'], errors='coerce')
        df['Number of Affected Users'] = pd.to_numeric(df['Number of Affected Users'], errors='coerce')
        
        # Drop any rows that became NaN during coercion
        dropped_count = df.isnull().sum().sum()
        if dropped_count > 0:
            df = df.dropna()
            log_process(f"⚠️ Dropped rows due to invalid data types during conversion.")
        log_process("✅ Standardized numerical columns (Year, Financial Loss, Resolution Time, Affected Users).")

        # Feature Engineering: Discretization of resolution time
        if 'Incident Resolution Time (in Hours)' in df.columns:
            df['Resolution Severity'] = pd.cut(df['Incident Resolution Time (in Hours)'], 
                                               bins=[0, 24, 72, np.inf], 
                                               labels=['Fast (<24h)', 'Medium (24-72h)', 'Slow (>72h)'])
            log_process("✅ Engineered 'Resolution Severity' feature based on resolution times.")

        return df, raw_shape
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame(), (0, 0)


def render_historical_dashboard():
    df, raw_shape = load_and_clean_data()

    if df.empty:
        st.warning("No data found or error loading the dataset.")
        st.stop()

    # --- HEADER ---
    st.markdown('<div class="main-header">Global Cyber Security Dashboard: Tracking Threats & Financial Loss</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Advanced Analysis, Statistical Insights, and Predictive Modeling (2015 - 2025)</div>', unsafe_allow_html=True)

    # --- MODERN FILTERS ---
    st.sidebar.markdown("### 🎛️ Modern Quick-Filters")

    # Year Range - Modern pill selection instead of slider
    all_years = sorted(df['Year'].dropna().unique())
    selected_year = st.sidebar.selectbox("📅 Year Selected", options=["All Time"] + list(all_years))
    if selected_year == "All Time":
        selected_years = (min(all_years), max(all_years))
    else:
        selected_years = (selected_year, selected_year)

    # Countries - Modern Popover expansion
    st.sidebar.markdown("**🌍 Geographic Scope**")
    with st.sidebar.popover("Configure Country Filter"):
        all_countries = sorted(df['Country'].dropna().unique())
        country_filter_type = st.radio("Selection Mode", ["Global (All)", "Custom Selection"], horizontal=True, key="c_mode")
        if country_filter_type == "Global (All)":
            selected_countries = all_countries
            st.info("Currently displaying data for all countries worldwide.")
        else:
            selected_countries = st.multiselect("Tap to add Countries", options=all_countries, default=[all_countries[0]], label_visibility="collapsed")

    # Industries - Modern Popover expansion
    st.sidebar.markdown("**🏢 Target Industries**")
    with st.sidebar.popover("Configure Industry Filter"):
        all_industries = sorted(df['Target Industry'].dropna().unique())
        industry_filter_type = st.radio("Selection Mode", ["All Sectors", "Custom Selection"], horizontal=True, key="i_mode")
        if industry_filter_type == "All Sectors":
            selected_industries = all_industries
            st.info("Currently displaying data across all industrial sectors.")
        else:
            selected_industries = st.multiselect("Tap to add Industries", options=all_industries, default=[all_industries[0]], label_visibility="collapsed")

    # Apply filters
    filtered_df = df[
        (df['Year'] >= selected_years[0]) & 
        (df['Year'] <= selected_years[1]) &
        (df['Country'].isin(selected_countries)) &
        (df['Target Industry'].isin(selected_industries))
    ]

    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**Filtered Records:** `{len(filtered_df):,}` / `{len(df):,}`")

    if filtered_df.empty:
        st.warning("No data available for the selected filters. Please broaden your specific criteria.")
        st.stop()

    # --- TABS LAYOUT ---
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Executive Dashboard", 
        "📈 Statistical Analysis", 
        "🔮 Predictive Modeling", 
        "🧹 Data Health & Preprocessing"
    ])

    # ==========================================
    # TAB 1: EXECUTIVE DASHBOARD
    # ==========================================
    with tab1:
        st.markdown("### 🎯 Key Performance Indicators")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h4 style="color:#94A3B8; margin:0; font-size:1rem;">Total Incidents</h4>
                <h2 style="color:#60A5FA; margin:10px 0 0 0;">{len(filtered_df):,}</h2>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            total_loss = filtered_df['Financial Loss (in Million $)'].sum()
            st.markdown(f"""
            <div class="metric-card">
                <h4 style="color:#94A3B8; margin:0; font-size:1rem;">Total Financial Loss</h4>
                <h2 style="color:#F87171; margin:10px 0 0 0;">${total_loss:,.2f}M</h2>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            avg_res = filtered_df['Incident Resolution Time (in Hours)'].mean()
            st.markdown(f"""
            <div class="metric-card">
                <h4 style="color:#94A3B8; margin:0; font-size:1rem;">Avg. Resolution Time</h4>
                <h2 style="color:#34D399; margin:10px 0 0 0;">{avg_res:.1f} Hrs</h2>
            </div>
            """, unsafe_allow_html=True)
        with col4:
            total_users = filtered_df['Number of Affected Users'].sum()
            st.markdown(f"""
            <div class="metric-card">
                <h4 style="color:#94A3B8; margin:0; font-size:1rem;">Affected Users</h4>
                <h2 style="color:#A78BFA; margin:10px 0 0 0;">{total_users/1e6:,.1f}M</h2>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        r1c1, r1c2 = st.columns(2)
        with r1c1:
            loss_trend = filtered_df.groupby('Year')['Financial Loss (in Million $)'].sum().reset_index()
            fig1 = px.area(loss_trend, x="Year", y="Financial Loss (in Million $)", 
                           title="Cumulative Financial Impact Over Time",
                           color_discrete_sequence=["#EF4444"])
            fig1.update_traces(mode="lines+markers", marker=dict(size=8), opacity=0.3)
            st.plotly_chart(fig1, use_container_width=True)

        with r1c2:
            top_attacks = filtered_df['Attack Type'].value_counts().reset_index().head(8)
            top_attacks.columns = ['Attack Type', 'Incidents']
            fig2 = px.bar(top_attacks, x="Incidents", y="Attack Type", orientation='h',
                          title="Prominent Attack Vectors", color="Incidents", color_continuous_scale="Purp")
            fig2.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig2, use_container_width=True)

        r2c1, r2c2 = st.columns(2)
        with r2c1:
            ind_loss = filtered_df.groupby('Target Industry')['Financial Loss (in Million $)'].sum().reset_index()
            fig3 = px.pie(ind_loss, values="Financial Loss (in Million $)", names="Target Industry",
                          title="Financial Liability by Sector", hole=0.4,
                          color_discrete_sequence=px.colors.diverging.Tealrose)
            st.plotly_chart(fig3, use_container_width=True)

        with r2c2:
            def_eff = filtered_df.groupby('Defense Mechanism Used')['Incident Resolution Time (in Hours)'].mean().reset_index()
            def_eff = def_eff.sort_values("Incident Resolution Time (in Hours)")
            fig4 = px.bar(def_eff, x="Defense Mechanism Used", y="Incident Resolution Time (in Hours)",
                          title="Defense Efficacy (Avg Time to Resolve)", color="Incident Resolution Time (in Hours)",
                          color_continuous_scale="Teal_r")
            st.plotly_chart(fig4, use_container_width=True)


    # ==========================================
    # TAB 2: STATISTICAL ANALYSIS
    # ==========================================
    with tab2:
        st.markdown("### 🔬 In-depth Statistical Analysis")
        st.markdown("Explore correlations and distributional metrics across different attack dimensions.")

        st_col1, st_col2 = st.columns([1, 1])

        with st_col1:
            st.markdown("#### Descriptive Statistics")
            numerical_cols = ['Financial Loss (in Million $)', 'Incident Resolution Time (in Hours)', 'Number of Affected Users']
            desc_stats = filtered_df[numerical_cols].describe().T
            st.dataframe(desc_stats.style.format("{:.2f}").background_gradient(cmap='Blues'), use_container_width=True)

        with st_col2:
            st.markdown("#### Correlation Heatmap")
            corr_matrix = filtered_df[numerical_cols].corr()
            fig_corr = px.imshow(corr_matrix, text_auto=True, aspect="auto", 
                                 color_continuous_scale='RdBu_r', title="Feature Auto-Correlation")
            st.plotly_chart(fig_corr, use_container_width=True)

        st.markdown("#### Distribution Analysis")
        dist_feature = st.selectbox("Select Feature to view Distribution", ['Financial Loss (in Million $)', 'Incident Resolution Time (in Hours)'])

        fig_dist = px.histogram(filtered_df, x=dist_feature, marginal="box", color="Attack Type", 
                                title=f"Distribution of {dist_feature} Across Attack Vectors", opacity=0.7)
        st.plotly_chart(fig_dist, use_container_width=True)


    # ==========================================
    # TAB 3: PREDICTIVE MODELING
    # ==========================================
    with tab3:
        st.markdown("### 🔮 Trend Forecasting & Predictive Analysis")
        st.markdown("Utilizing polynomial regression on historical data points to mathematically project future threat landscapes.")

        target_metric = st.radio("Select Variable to Forecast", 
                                 ["Financial Loss (in Million $)", "Incident Count"], horizontal=True)

        # Aggregate data by Year for forecasting
        if target_metric == "Financial Loss (in Million $)":
            ts_data = filtered_df.groupby('Year')[target_metric].sum().reset_index()
        else:
            ts_data = filtered_df.groupby('Year').size().reset_index(name='Incident Count')
            target_metric = 'Incident Count'

        if len(ts_data) >= 3:
            # Fit a 2nd degree polynomial curve (quadratic) for trend curve capture
            x_hist = ts_data['Year'].values
            y_hist = ts_data[target_metric].values

            if len(ts_data) <= 5:
                degree = 1
            else:
                degree = 2
            coefficients = np.polyfit(x_hist, y_hist, degree)
            poly_func = np.poly1d(coefficients)

            # Historical fit curve
            ts_data['Fitted Trend'] = poly_func(x_hist)

            # Future Predictions (forecast out +5 years)
            max_year = int(x_hist.max())
            future_years = np.arange(max_year + 1, max(2031, max_year + 5))
            future_predictions = poly_func(future_years)

            # Clip negative predictions to 0 as they don't mathematically make sense for these metrics
            future_predictions = np.maximum(future_predictions, 0)

            pred_df = pd.DataFrame({'Year': future_years, 'Forecast': future_predictions})

            fig_pred = go.Figure()
            # Historical actuals
            fig_pred.add_trace(go.Scatter(x=ts_data['Year'], y=ts_data[target_metric], 
                                          mode='markers+lines', name='Actual Recorded Data', marker=dict(size=10, color='#3B82F6')))
            # Fitted historical trend
            fig_pred.add_trace(go.Scatter(x=ts_data['Year'], y=ts_data['Fitted Trend'], 
                                          mode='lines', name='Regression Fit', line=dict(dash='dash', color='#94A3B8')))
            # Future forecast
            fig_pred.add_trace(go.Scatter(x=pred_df['Year'], y=pred_df['Forecast'], 
                                          mode='lines+markers', name='Predictive Forecast', marker=dict(size=10, symbol='star', color='#10B981'),
                                          line=dict(width=3, color='#10B981')))

            fig_pred.update_layout(title=f"Polynomial Model Forecast: {target_metric} (Projected to {future_years.max()})",
                                   xaxis_title="Year", yaxis_title=target_metric, hovermode="x unified")
            st.plotly_chart(fig_pred, use_container_width=True)

            st.info(f"💡 **Algorithmic Insight:** Using recent trajectory analysis, the model projects that by **{future_years.max()}**, the {target_metric.lower()} could mathematically reach approximately **{future_predictions[-1]:,.2f}**.")
        else:
            st.warning("Insufficient historical data points (< 3 years) available to perform reliable multi-year forecasting. Please expand the 'Analysis Horizon' in the sidebar parameters.")


    # ==========================================
    # TAB 4: DATA HEALTH & PREPROCESSING
    # ==========================================
    with tab4:
        st.markdown("### 🧹 Data Pipeline & Preprocessing Health")
        st.markdown("The underlying CSV datastore is automatically sanitized, encoded, and validated prior to visual rendering. Below is the operational footprint.")

        col_hlth1, col_hlth2 = st.columns(2)
        with col_hlth1:
            st.markdown("#### DataFrame Dimensionality")
            st.metric("Raw Initial Dataset", f"{raw_shape[0]:,} rows × {raw_shape[1]} cols")
            st.metric("Post-Cleaning Dataset", f"{df.shape[0]:,} rows × {df.shape[1]} cols")
            st.metric("Currently Rendered Subset", f"{filtered_df.shape[0]:,} rows")

        with col_hlth2:
            st.markdown("#### Execution Log")
            for log in st.session_state['preprocessing_logs']:
                if log.startswith("✅"):
                    st.success(log)
                elif log.startswith("⚠️"):
                    st.warning(log)
                else:
                    st.info(log)

        st.markdown("#### Cleaned Data Snapshot (Top 10 Rows)")
        st.dataframe(filtered_df.head(10), use_container_width=True)

    # Footer
    st.markdown("---")
    st.markdown("<div style='text-align: center; color: #64748B;'>Advanced Cybersecurity Intelligence Hub • Data Science & ML Engine</div>", unsafe_allow_html=True)

# ==========================================
# MAIN APPLICATION ROUTER
# ==========================================
import sys
import os

# Ensure the subfolder is in the path to import live_cyber_dashboard
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from realtime_analysis.live_cyber_dashboard import render_live_dashboard

def main():
    st.sidebar.markdown("### 🧭 Intelligence Mode")
    dashboard_mode = st.sidebar.radio(
        "Select Environment:",
        ["Historical ML Engine", "Live Threat Radar (OTX)"],
        index=0,
        help="Switch between historical dataset analysis and real-time global threat intel."
    )
    
    st.sidebar.markdown("---")
    
    if dashboard_mode == "Historical ML Engine":
        render_historical_dashboard()
    else:
        render_live_dashboard()

if __name__ == "__main__":
    main()
