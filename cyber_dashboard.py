import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, r2_score

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
    /* Make st.metric widgets readable on dark background */
    [data-testid="stMetricLabel"] p { color: #94A3B8 !important; font-size: 0.85rem !important; }
    [data-testid="stMetricValue"] { color: #F1F5F9 !important; font-size: 1.8rem !important; font-weight: 700 !important; }
    [data-testid="stMetricDelta"] { color: #34D399 !important; }
    [data-testid="metric-container"] {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 16px 20px;
        border-radius: 15px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    [data-testid="metric-container"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.4);
        border: 1px solid rgba(59, 130, 246, 0.4);
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
    st.markdown('<div class="main-header">🛡️ Cyber Threats Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Explore Historical Attack Trends, Financial Impact, and Future Forecasts (2015 - 2025)</div>', unsafe_allow_html=True)

    # --- MODERN FILTERS ---
    st.sidebar.markdown("### 🔍 Filter Data")

    # Year Range - Modern pill selection instead of slider
    all_years = sorted(df['Year'].dropna().unique())
    selected_year = st.sidebar.selectbox("📅 Year Selected", options=["All Time"] + list(all_years), help="Choose 'All Time' to see the full scope of data, or pick a specific year to zoom in.")
    if selected_year == "All Time":
        selected_years = (min(all_years), max(all_years))
    else:
        selected_years = (selected_year, selected_year)

    # Countries - Modern Popover expansion
    st.sidebar.markdown("**🌍 Filter by Country**")
    with st.sidebar.popover("Select Countries"):
        all_countries = sorted(df['Country'].dropna().unique())
        country_filter_type = st.radio("Selection Mode", ["Global (All)", "Custom Selection"], horizontal=True, key="c_mode")
        if country_filter_type == "Global (All)":
            selected_countries = all_countries
            st.info("Currently displaying data for all countries worldwide.")
        else:
            selected_countries = st.multiselect("Tap to add Countries", options=all_countries, default=[all_countries[0]], label_visibility="collapsed", help="Filter the dashboard to show attacks that happened exclusively in the selected countries.")

    # Industries - Modern Popover expansion
    st.sidebar.markdown("**🏢 Filter by Industry**")
    with st.sidebar.popover("Select Industries"):
        all_industries = sorted(df['Target Industry'].dropna().unique())
        industry_filter_type = st.radio("Selection Mode", ["All Sectors", "Custom Selection"], horizontal=True, key="i_mode")
        if industry_filter_type == "All Sectors":
            selected_industries = all_industries
            st.info("Currently displaying data across all industrial sectors.")
        else:
            selected_industries = st.multiselect("Tap to add Industries", options=all_industries, default=[all_industries[0]], label_visibility="collapsed", help="Focus the data on specific business sectors, like Healthcare or Finance.")

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
        "📊 Dashboard Overview", 
        "📈 Detailed Stats", 
        "🔮 Future Predictions", 
        "⚙️ Data Details"
    ])

    # ==========================================
    # TAB 1: EXECUTIVE DASHBOARD
    # ==========================================
    with tab1:
        st.markdown("### 🎯 Quick Summary")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(label="Total Attacks", value=f"{len(filtered_df):,}", help="The total number of individual cyber attacks recorded in the selected filters.")
        with col2:
            total_loss = filtered_df['Financial Loss (in Million $)'].sum()
            st.metric(label="Financial Impact", value=f"${total_loss:,.2f}M", help="The estimated total monetary damages caused by the attacks in your current filter.")
        with col3:
            avg_res = filtered_df['Incident Resolution Time (in Hours)'].mean()
            st.metric(label="Avg. Time to Fix", value=f"{avg_res:.1f} Hrs", help="The average number of hours it took for the organization to stop the attack and restore normal operations.")
        with col4:
            total_users = filtered_df['Number of Affected Users'].sum()
            st.metric(label="People Affected", value=f"{total_users/1e6:,.1f}M", help="The total number of individual people whose data or accounts were exposed during these attacks.")

        st.markdown("<br>", unsafe_allow_html=True)

        r1c1, r1c2 = st.columns(2)
        with r1c1:
            loss_trend = filtered_df.groupby('Year')['Financial Loss (in Million $)'].sum().reset_index()
            fig1 = px.area(loss_trend, x="Year", y="Financial Loss (in Million $)", 
                           title="Financial Impact Over Time",
                           color_discrete_sequence=["#EF4444"])
            fig1.update_traces(mode="lines+markers", marker=dict(size=8), opacity=0.3)
            fig1.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font={'color': '#E2E8F0', 'family': "'Inter', sans-serif"})
            st.plotly_chart(fig1, use_container_width=True)

        with r1c2:
            # Plain-English descriptions for every attack type
            ATTACK_DESCRIPTIONS = {
                "SQL Injection":             "🗄️ Hacker tricks a database with sneaky code to steal or delete your data",
                "DDoS":                      "🌊 Flooding a website/server with fake traffic to crash it completely",
                "Phishing":                  "🎣 Fake email or website designed to steal your password or bank details",
                "Ransomware":                "🔒 Virus that locks all your files and demands money to unlock them",
                "Malware":                   "🦠 Harmful software secretly installed on your device without permission",
                "Man-in-the-Middle":         "🕵️ Hacker secretly reads messages sent between two people",
                "AI-Powered Phishing":       "🤖 Smart AI bots craft highly convincing fake messages to trick you",
                "Deepfake Social Engineering":"🎭 Fake AI-generated videos/voices used to impersonate real people",
                "Zero-Day Exploit":          "💥 Attacking a security flaw before the software company knows it exists",
                "Credential Stuffing":       "🔑 Using stolen username/password lists to break into many accounts",
                "Supply Chain Attack":       "🏭 Attacking a trusted software vendor to infect all its customers",
                "Insider Threat":            "👤 Employee or contractor intentionally leaking or stealing company data",
                "Brute Force":               "🔨 Trying millions of password combinations until the right one is found",
                "Cross-Site Scripting":      "📝 Injecting malicious code into a trusted website to attack its visitors",
            }
            top_attacks = filtered_df['Attack Type'].value_counts().reset_index().head(8)
            top_attacks.columns = ['Attack Type', 'Incidents']
            top_attacks['💡 What does this mean?'] = top_attacks['Attack Type'].map(ATTACK_DESCRIPTIONS).fillna("A type of cyber attack targeting computer systems or data.")
            fig2 = px.bar(top_attacks, x="Incidents", y="Attack Type", orientation='h',
                          title="Most Common Attack Types", color="Incidents", color_continuous_scale="Purp",
                          hover_data={"💡 What does this mean?": True, "Incidents": True, "Attack Type": False})
            fig2.update_layout(yaxis={'categoryorder':'total ascending'}, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font={'color': '#E2E8F0', 'family': "'Inter', sans-serif"})
            st.plotly_chart(fig2, use_container_width=True)

        r2c1, r2c2 = st.columns(2)
        with r2c1:
            ind_loss = filtered_df.groupby('Target Industry')['Financial Loss (in Million $)'].sum().reset_index()
            fig3 = px.pie(ind_loss, values="Financial Loss (in Million $)", names="Target Industry",
                          title="Financial Impact by Industry", hole=0.4,
                          color_discrete_sequence=px.colors.diverging.Tealrose)
            st.plotly_chart(fig3, use_container_width=True)

        with r2c2:
            def_eff = filtered_df.groupby('Defense Mechanism Used')['Incident Resolution Time (in Hours)'].mean().reset_index()
            def_eff = def_eff.sort_values("Incident Resolution Time (in Hours)")
            fig4 = px.bar(def_eff, x="Defense Mechanism Used", y="Incident Resolution Time (in Hours)",
                          title="Which Defenses Work Best? (Time to Fix)", color="Incident Resolution Time (in Hours)",
                          color_continuous_scale="Teal_r")
            fig4.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font={'color': '#E2E8F0', 'family': "'Inter', sans-serif"})
            st.plotly_chart(fig4, use_container_width=True)


    # ==========================================
    # TAB 2: STATISTICAL ANALYSIS
    # ==========================================
    with tab2:
        st.markdown("### 📈 Detailed Statistical Breakdown")
        st.markdown("Take a closer look at the numbers behind the attacks, including how different factors relate to each other.")

        st_col1, st_col2 = st.columns([1, 1])

        with st_col1:
            st.markdown("#### Key Numbers (Averages & Totals)")
            numerical_cols = ['Financial Loss (in Million $)', 'Incident Resolution Time (in Hours)', 'Number of Affected Users']
            desc_stats = filtered_df[numerical_cols].describe().T
            st.dataframe(desc_stats.style.format("{:.2f}").background_gradient(cmap='Blues'), use_container_width=True)

        with st_col2:
            st.markdown("#### Correlation Heatmap")
            corr_matrix = filtered_df[numerical_cols].corr()
            fig_corr = px.imshow(corr_matrix, text_auto=True, aspect="auto", 
                                 color_continuous_scale='RdBu_r', title="Feature Auto-Correlation (Darker colors = stronger connection)")
            fig_corr.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': '#E2E8F0', 'family': "'Inter', sans-serif"})
            st.plotly_chart(fig_corr, use_container_width=True)

        st.markdown("#### Distribution Analysis")
        dist_feature = st.selectbox("Select Feature to view Distribution", ['Financial Loss (in Million $)', 'Incident Resolution Time (in Hours)'])

        fig_dist = px.histogram(filtered_df, x=dist_feature, marginal="box", color="Attack Type", 
                                title=f"Distribution of {dist_feature} Across Attack Vectors", opacity=0.7)
        fig_dist.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font={'color': '#E2E8F0', 'family': "'Inter', sans-serif"})
        st.plotly_chart(fig_dist, use_container_width=True)


    # ==========================================
    # TAB 3: PREDICTIVE MODELING
    # ==========================================
    with tab3:
        st.markdown("### 🔮 Future Predictions & Trends")
        st.markdown("Using AI and past trends to estimate what the cybersecurity landscape might look like in the coming years.")

        target_metric = st.radio("Select Variable to Forecast", 
                                 ["Financial Loss (in Million $)", "Incident Count"], horizontal=True, help="Choose which data point you want the AI to predict for the future.")

        # Aggregate data by Year for forecasting
        if target_metric == "Financial Loss (in Million $)":
            ts_data = filtered_df.groupby('Year')[target_metric].sum().reset_index()
        else:
            ts_data = filtered_df.groupby('Year').size().reset_index(name='Incident Count')
            target_metric = 'Incident Count'

        if len(ts_data) >= 5:
            # --- DATA PREPROCESSING: SPLITTING & SCALING ---
            # To align with formal ML methodology (Chapters 2.4 & 2.5)
            x_raw = ts_data[['Year']].values
            y_raw = ts_data[target_metric].values

            # Normalization and Scaling
            scaler_x = MinMaxScaler()
            scaler_y = MinMaxScaler()
            
            x_scaled = scaler_x.fit_transform(x_raw).flatten()
            y_scaled = scaler_y.fit_transform(y_raw.reshape(-1, 1)).flatten()

            # Data Splitting
            x_train, x_test, y_train, y_test = train_test_split(x_scaled, y_scaled, test_size=0.2, random_state=42, shuffle=False)

            # Fit Polynomial Regression on Scaled Training Data
            degree = 2 if len(x_train) > 5 else 1
            coefficients = np.polyfit(x_train, y_train, degree)
            poly_func = np.poly1d(coefficients)

            # Historical fit curve (reversing transform for visualization)
            y_fit_scaled = poly_func(x_scaled)
            ts_data['Fitted Trend'] = scaler_y.inverse_transform(y_fit_scaled.reshape(-1, 1)).flatten()

            # Future Predictions (forecast out +5 years)
            max_year = int(ts_data['Year'].max())
            future_years = np.arange(max_year + 1, max(2031, max_year + 5))
            
            # Scale future years
            future_years_scaled = scaler_x.transform(future_years.reshape(-1, 1)).flatten()
            future_predictions_scaled = poly_func(future_years_scaled)
            
            # Inverse transform predictions back to original metric magnitude
            future_predictions = scaler_y.inverse_transform(future_predictions_scaled.reshape(-1, 1)).flatten()

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
                                   xaxis_title="Year", yaxis_title=target_metric, hovermode="x unified",
                                   paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font={'color': '#E2E8F0', 'family': "'Inter', sans-serif"})
            st.plotly_chart(fig_pred, use_container_width=True)

            st.info(f"💡 **AI Prediction:** Based on historical trends, our model projects that by **{future_years.max()}**, the {target_metric.lower()} could reach approximately **{future_predictions[-1]:,.2f}**.")
        else:
            st.warning("Insufficient historical data points (< 5 years) available to perform formal ML Train/Test Splitting. Please expand the 'Analysis Horizon'.")


    # ==========================================
    # TAB 4: DATA HEALTH & PREPROCESSING
    # ==========================================
    with tab4:
        st.markdown("### ⚙️ Data Pipeline Details")
        st.markdown("Behind the scenes, the data is automatically cleaned and prepared before being shown on the dashboard. Here are the logs of that process.")

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
        # Force Streamlit to drop cached .pyc of the sub-module and reload the new fixes
        import importlib
        if 'realtime_analysis.live_cyber_dashboard' in sys.modules:
            importlib.reload(sys.modules['realtime_analysis.live_cyber_dashboard'])
        from realtime_analysis.live_cyber_dashboard import render_live_dashboard
        render_live_dashboard()

if __name__ == "__main__":
    main()
