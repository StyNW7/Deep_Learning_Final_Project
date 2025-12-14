import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Set page configuration
st.set_page_config(
    page_title="Air Quality Intelligence Platform",
    page_icon="🌫️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        font-size: 3.2rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #1f77b4 0%, #2ca02c 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #f0f0f0;
    }
    .section-header {
        font-size: 2.2rem;
        color: #2c3e50;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        font-weight: 600;
        padding-left: 0.5rem;
        border-left: 5px solid #3498db;
    }
    .subsection-header {
        font-size: 1.5rem;
        color: #black;
        margin-top: 1.2rem;
        margin-bottom: 0.8rem;
        font-weight: 600;
    }
    .card-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: black;
        border-radius: 15px;
        padding: 2.5rem;
        text-align: center;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        cursor: pointer;
        height: 300px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    .card-container:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.15);
    }
    .dashboard-card {
        color: black;
        background: white;
        border-radius: 12px;
        padding: 1.8rem;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        margin-bottom: 1.5rem;
        border: 1px solid #eaeaea;
        transition: all 0.3s ease;
    }
    .dashboard-card:hover {
        box-shadow: 0 10px 25px rgba(0,0,0,0.12);
        transform: translateY(-2px);
    }
    .metric-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: black;
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .info-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: black;
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .station-card {
        color: black
        background: white;
        border-left: 4px solid #3498db;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 0.8rem;
        box-shadow: 0 3px 10px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }
    .station-card:hover {
        border-left-color: #2980b9;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    .status-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
    }
    .status-online {
        background-color: #2ecc71;
    }
    .status-offline {
        background-color: #e74c3c;
    }
    .tab-content {
        padding: 1.5rem;
        background: #f8f9fa;
        border-radius: 10px;
        margin-top: 1rem;
        color: black;
    }
    .stSelectbox > div > div {
        background-color: white;
        border-radius: 8px;
        border: 1px solid #ddd;
    }
    .stSlider > div > div > div {
        background-color: #3498db;
    }
    .data-table {
        background: white;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 3px 10px rgba(0,0,0,0.05);
        color: black;
    }
    .footer {
        text-align: center;
        color: #7f8c8d;
        font-size: 0.9rem;
        padding: 2rem;
        margin-top: 3rem;
        border-top: 1px solid #ecf0f1;
    }
    .navigation-button {
        background: rgba(255,255,255,0.2);
        padding: 0.5rem 1rem;
        border-radius: 25px;
        border: none;
        color: black;
        font-size: 1rem;
        cursor: pointer;
        margin-top: 1.5rem;
        transition: all 0.3s ease;
    }
    .navigation-button:hover {
        background: rgba(255,255,255,0.3);
        transform: scale(1.05);
        color: black;
    }
</style>
""", unsafe_allow_html=True)

# Configuration
FLASK_BACKEND_URL = "http://localhost:5000"
STATIONS = {
    "Jongno-gu": 101,
    "Jung-gu": 102,
    "Seodaemun-gu": 105,
    "Mapo-gu": 106,
    "Seongdong-gu": 107,
    "Dongdaemun-gu": 109,
    "Seongbuk-gu": 111,
    "Gangbuk-gu": 112,
    "Dobong-gu": 113,
    "Yeongdeungpo-gu": 119,
    "Dongjak-gu": 120,
    "Gwanak-gu": 121,
    "Seocho-gu": 122,
}

# Initialize session state for navigation
if 'page' not in st.session_state:
    st.session_state.page = 'home'

@st.cache_data
def load_static_data():
    """Load static CSV data for historical analysis"""
    try:
        aqi_data = pd.read_csv('../backend/aqi_data_sorted.csv')
        aqi_data['Measurement date'] = pd.to_datetime(aqi_data['Measurement date'])
        aqi_data['Hour'] = aqi_data['Measurement date'].dt.hour
        aqi_data['Date'] = aqi_data['Measurement date'].dt.date
        
        station_info = pd.read_csv('../backend/Measurement_station_info.csv')
        item_info = pd.read_csv('../backend/Measurement_item_info.csv')
        
        # Merge station names
        aqi_data = pd.merge(aqi_data, station_info[['Station code', 'Station name(district)']], 
                          on='Station code', how='left')
        
        return aqi_data, station_info, item_info
    except Exception as e:
        st.error(f"Error loading static data: {e}")
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

def call_flask_api(endpoint, params=None):
    """Make API call to Flask backend"""
    try:
        url = f"{FLASK_BACKEND_URL}{endpoint}"
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {e}")
        return None

def get_forecast_data(station):
    """Get 6-hour forecast for a station"""
    try:
        data = call_flask_api("/api/forecasts", {"station": station})
        if data and isinstance(data, list):
            df = pd.DataFrame(data)
            df['time'] = pd.to_datetime(df['time'])
            df['hour'] = df['time'].dt.strftime('%H:%M')
            return df
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error getting forecast: {e}")
        return pd.DataFrame()

def get_current_prediction(station):
    """Get current pollution prediction for a station"""
    try:
        data = call_flask_api("/api/predict", {"station": station})
        if data and data.get("status") == "success":
            return data
        return None
    except Exception as e:
        st.error(f"Error getting current prediction: {e}")
        return None

def get_detailed_prediction(station):
    """Get detailed pollution prediction for a station"""
    try:
        data = call_flask_api("/api/predict-detail", {"station": station})
        if data and data.get("status") == "success":
            return data
        return None
    except Exception as e:
        st.error(f"Error getting detailed prediction: {e}")
        return None

def create_pollution_gauge(value, title, unit="μg/m³"):
    """Create a gauge chart for pollution levels"""
    if title == "PM2.5":
        levels = [0, 15, 35, 75, 500]
        colors = ['#2ecc71', '#f1c40f', '#e67e22', '#e74c3c']
        categories = ['Good', 'Moderate', 'Poor', 'Very Poor']
    elif title == "PM10":
        levels = [0, 30, 80, 150, 600]
        colors = ['#2ecc71', '#f1c40f', '#e67e22', '#e74c3c']
        categories = ['Good', 'Moderate', 'Poor', 'Very Poor']
    else:
        levels = [0, value * 0.3, value * 0.6, value * 0.9, value * 1.2]
        colors = ['#2ecc71', '#f1c40f', '#e67e22', '#e74c3c']
        categories = ['Low', 'Moderate', 'High', 'Very High']
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title, 'font': {'size': 22}},
        number={'suffix': f' {unit}', 'font': {'size': 28}},
        gauge={
            'axis': {'range': [0, levels[-1]], 'tickwidth': 1, 'tickcolor': "black"},
            'bar': {'color': "#34495e"},
            'steps': [
                {'range': [levels[0], levels[1]], 'color': colors[0]},
                {'range': [levels[1], levels[2]], 'color': colors[1]},
                {'range': [levels[2], levels[3]], 'color': colors[2]},
                {'range': [levels[3], levels[4]], 'color': colors[3]},
            ],
            'threshold': {
                'line': {'color': "black", 'width': 3},
                'thickness': 0.8,
                'value': value
            }
        }
    ))
    
    fig.update_layout(
        height=280,
        margin=dict(l=20, r=20, t=60, b=20),
        paper_bgcolor='white',
        font={'color': "#2c3e50", 'family': "Arial"}
    )
    return fig

def create_forecast_timeline(forecast_df):
    """Create timeline visualization for forecast"""
    if forecast_df.empty:
        return go.Figure()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=forecast_df['hour'],
        y=forecast_df['pm25'],
        mode='lines+markers',
        name='PM2.5 Forecast',
        line=dict(color='#e74c3c', width=3),
        marker=dict(size=10, color='white', line=dict(width=2, color='#e74c3c'))
    ))
    
    # Add threshold areas
    fig.add_hrect(y0=0, y1=15, fillcolor="rgba(46, 204, 113, 0.2)", 
                  line_width=0, layer="below", annotation_text="Good")
    fig.add_hrect(y0=15, y1=35, fillcolor="rgba(241, 196, 15, 0.2)", 
                  line_width=0, layer="below", annotation_text="Moderate")
    fig.add_hrect(y0=35, y1=75, fillcolor="rgba(230, 126, 34, 0.2)", 
                  line_width=0, layer="below", annotation_text="Poor")
    fig.add_hrect(y0=75, y1=forecast_df['pm25'].max() * 1.1, 
                  fillcolor="rgba(231, 76, 60, 0.2)", line_width=0, 
                  layer="below", annotation_text="Very Poor")
    
    fig.update_layout(
        title=dict(text="6-Hour PM2.5 Forecast", font=dict(size=20)),
        xaxis_title="Time",
        yaxis_title="PM2.5 (μg/m³)",
        hovermode='x unified',
        height=450,
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(size=12),
        showlegend=False
    )
    
    return fig

def create_comparison_radar(detailed_data):
    """Create radar chart for pollutant comparison"""
    if not detailed_data:
        return go.Figure()
    
    pollutants = ['NO₂', 'O₃', 'CO', 'SO₂', 'PM2.5']
    values = [
        detailed_data.get('no2_prediction', 0),
        detailed_data.get('o3_prediction', 0),
        detailed_data.get('co_prediction', 0),
        detailed_data.get('so2_prediction', 0),
        detailed_data.get('pm25_prediction', 0)
    ]
    
    # Normalize values for radar chart
    max_val = max(values) if max(values) > 0 else 1
    normalized_values = [v/max_val * 100 for v in values]
    
    fig = go.Figure(data=go.Scatterpolar(
        r=normalized_values,
        theta=pollutants,
        fill='toself',
        line=dict(color='#3498db', width=3),
        marker=dict(size=10, color='white', line=dict(color='#3498db', width=2))
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                gridcolor='#e0e0e0'
            ),
            bgcolor='white'
        ),
        showlegend=False,
        title=dict(text="Pollutant Concentration Profile", font=dict(size=18)),
        height=400,
        paper_bgcolor='white'
    )
    
    return fig

def create_temporal_analysis(aqi_data, station_name=None):
    """Create temporal analysis visualizations"""
    if station_name:
        data = aqi_data[aqi_data['Station name(district)'] == station_name]
    else:
        data = aqi_data
    
    hourly_avg = data.groupby('Hour').agg({
        'PM2.5': 'mean',
        'PM10': 'mean',
        'NO2': 'mean',
        'O3': 'mean'
    }).reset_index()
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('PM2.5 Hourly Trend', 'PM10 Hourly Trend', 
                       'NO2 Hourly Trend', 'O3 Hourly Trend'),
        vertical_spacing=0.15,
        horizontal_spacing=0.1
    )
    
    colors = ['#e74c3c', '#e67e22', '#3498db', '#27ae60']
    
    fig.add_trace(
        go.Scatter(x=hourly_avg['Hour'], y=hourly_avg['PM2.5'], 
                  mode='lines+markers', name='PM2.5', 
                  line=dict(color=colors[0], width=2.5)),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(x=hourly_avg['Hour'], y=hourly_avg['PM10'], 
                  mode='lines+markers', name='PM10', 
                  line=dict(color=colors[1], width=2.5)),
        row=1, col=2
    )
    
    fig.add_trace(
        go.Scatter(x=hourly_avg['Hour'], y=hourly_avg['NO2'], 
                  mode='lines+markers', name='NO2', 
                  line=dict(color=colors[2], width=2.5)),
        row=2, col=1
    )
    
    fig.add_trace(
        go.Scatter(x=hourly_avg['Hour'], y=hourly_avg['O3'], 
                  mode='lines+markers', name='O3', 
                  line=dict(color=colors[3], width=2.5)),
        row=2, col=2
    )
    
    fig.update_layout(
        height=600, 
        showlegend=False, 
        title_text="Hourly Air Quality Trends",
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    fig.update_xaxes(title_text="Hour of Day", gridcolor='#f0f0f0')
    fig.update_yaxes(title_text="Concentration", gridcolor='#f0f0f0')
    
    return fig

def create_station_comparison(aqi_data, selected_stations):
    """Create station comparison visualization"""
    filtered_data = aqi_data[aqi_data['Station name(district)'].isin(selected_stations)]
    
    fig = px.box(
        filtered_data,
        x='Station name(district)',
        y='PM2.5',
        color='Station name(district)',
        points='all',
        title="PM2.5 Distribution by Station",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    fig.update_layout(
        showlegend=False,
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=500
    )
    
    return fig

def create_correlation_heatmap(aqi_data):
    """Create correlation heatmap for pollutants"""
    pollutants = ['NO2', 'O3', 'CO', 'SO2', 'PM10', 'PM2.5']
    correlation_matrix = aqi_data[pollutants].corr()
    
    fig = px.imshow(
        correlation_matrix,
        text_auto='.2f',
        aspect="auto",
        color_continuous_scale='RdBu',
        title="Pollutant Correlation Matrix",
        labels=dict(color="Correlation")
    )
    
    fig.update_layout(
        height=500,
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    return fig

def create_spatial_map(aqi_data, station_info):
    """Create spatial map visualization"""
    station_avg = aqi_data.groupby(['Station code', 'Station name(district)']).agg({
        'PM2.5': 'mean',
        'PM10': 'mean',
        'NO2': 'mean'
    }).reset_index()
    
    station_avg = pd.merge(station_avg, station_info[['Station code', 'Latitude', 'Longitude']], 
                          on='Station code', how='left')
    
    fig = px.scatter_mapbox(
        station_avg,
        lat="Latitude",
        lon="Longitude",
        size="PM2.5",
        color="PM2.5",
        hover_name="Station name(district)",
        hover_data=["PM10", "NO2"],
        color_continuous_scale=px.colors.sequential.Reds,
        size_max=25,
        zoom=10,
        height=500,
        title="Air Quality Spatial Distribution"
    )
    
    fig.update_layout(mapbox_style="carto-positron")
    return fig

def render_home_page():
    """Render the home page with dashboard selection"""
    st.markdown('<h1 class="main-header">Air Quality Intelligence Platform</h1>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown("""
        <div class="card-container">
            <h2 style="font-size: 2.2rem; margin-bottom: 1rem;">Data Analytics Dashboard</h2>
            <p style="font-size: 1.1rem; opacity: 0.9;">
                Comprehensive analysis of historical air quality data<br>
                Statistical insights and trend visualization<br>
                Spatial and temporal analysis<br>
                Correlation studies between pollutants
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Use Streamlit button for navigation
        if st.button("Explore Historical Data", key="data_analytics_btn", use_container_width=True):
            st.session_state.page = "data_overview"
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="card-container">
            <h2 style="font-size: 2.2rem; margin-bottom: 1rem;">AI Forecasting System</h2>
            <p style="font-size: 1.1rem; opacity: 0.9;">
                Real-time pollution predictions<br>
                6-hour forecast models<br>
                AI-powered TGCN predictions<br>
                Health impact assessments
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Use Streamlit button for navigation
        if st.button("View AI Predictions", key="ai_predictions_btn", use_container_width=True):
            st.session_state.page = "predictions"
            st.rerun()
    
    # Quick stats
    st.markdown("---")
    st.markdown('<div class="section-header">System Overview</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="dashboard-card">
            <h3 style="color: #2c3e50; margin-bottom: 0.5rem;">13 Stations</h3>
            <p style="color: #7f8c8d; margin: 0;">Monitoring Network</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="dashboard-card">
            <h3 style="color: #2c3e50; margin-bottom: 0.5rem;">6 Pollutants</h3>
            <p style="color: #7f8c8d; margin: 0;">Tracked Continuously</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="dashboard-card">
            <h3 style="color: #2c3e50; margin-bottom: 0.5rem;">24/7 Monitoring</h3>
            <p style="color: #7f8c8d; margin: 0;">Real-time Data</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="dashboard-card">
            <h3 style="color: #2c3e50; margin-bottom: 0.5rem;">TGCN AI Model</h3>
            <p style="color: #7f8c8d; margin: 0;">Advanced Predictions</p>
        </div>
        """, unsafe_allow_html=True)

def render_data_overview(aqi_data, station_info, item_info):
    """Render the data analytics dashboard"""
    # Navigation header with back button
    col1, col2 = st.columns([1, 5])
    
    with col1:
        if st.button("← Back to Home"):
            st.session_state.page = "home"
            st.rerun()
    
    with col2:
        st.markdown('<h1 class="main-header">Data Analytics Dashboard</h1>', unsafe_allow_html=True)
    
    # Summary metrics
    st.markdown('<div class="section-header">Key Performance Indicators</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_pm25 = aqi_data['PM2.5'].mean()
        st.metric("Average PM2.5", f"{avg_pm25:.1f} μg/m³", 
                 delta="Good" if avg_pm25 < 15 else "Moderate" if avg_pm25 < 35 else "Poor")
    
    with col2:
        avg_pm10 = aqi_data['PM10'].mean()
        st.metric("Average PM10", f"{avg_pm10:.1f} μg/m³",
                 delta="Good" if avg_pm10 < 30 else "Moderate" if avg_pm10 < 80 else "Poor")
    
    with col3:
        max_pollutant = aqi_data[['NO2', 'O3', 'CO', 'SO2', 'PM10', 'PM2.5']].mean().idxmax()
        st.metric("Primary Pollutant", max_pollutant)
    
    with col4:
        station_count = aqi_data['Station code'].nunique()
        st.metric("Monitoring Stations", station_count)
    
    # Data insights tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "Temporal Analysis", 
        "Spatial Analysis", 
        "Pollutant Analysis",
        "Data Explorer"
    ])
    
    with tab1:
        st.markdown('<div class="subsection-header">Temporal Patterns</div>', unsafe_allow_html=True)
        
        station_filter = st.selectbox(
            "Select Station for Analysis:",
            options=["All Stations"] + list(aqi_data['Station name(district)'].unique()),
            index=0
        )
        
        if station_filter == "All Stations":
            fig = create_temporal_analysis(aqi_data)
        else:
            fig = create_temporal_analysis(aqi_data, station_filter)
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Additional temporal insights
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="subsection-header">Daily Pattern</div>', unsafe_allow_html=True)
            daily_pattern = aqi_data.groupby('Hour').agg({'PM2.5': 'mean'}).reset_index()
            fig2 = px.area(daily_pattern, x='Hour', y='PM2.5', 
                         title="", 
                         line_shape='spline',
                         color_discrete_sequence=['#e74c3c'])
            fig2.update_layout(plot_bgcolor='white', paper_bgcolor='white')
            st.plotly_chart(fig2, use_container_width=True)
        
        with col2:
            st.markdown('<div class="subsection-header">Peak Hours Analysis</div>', unsafe_allow_html=True)
            peak_hours = aqi_data.groupby('Hour')['PM2.5'].mean().nlargest(5)
            peak_df = pd.DataFrame({
                'Hour': [f"{hour:02d}:00" for hour in peak_hours.index],
                'PM2.5': peak_hours.values
            })
            
            fig3 = px.bar(peak_df, x='Hour', y='PM2.5', 
                         color='PM2.5',
                         color_continuous_scale='Reds',
                         title="")
            fig3.update_layout(plot_bgcolor='white', paper_bgcolor='white')
            st.plotly_chart(fig3, use_container_width=True)
    
    with tab2:
        st.markdown('<div class="subsection-header">Geographical Distribution</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            fig = create_spatial_map(aqi_data, station_info)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown('<div class="subsection-header">Top Stations</div>', unsafe_allow_html=True)
            station_avg = aqi_data.groupby('Station name(district)')['PM2.5'].mean().sort_values(ascending=False)
            
            for idx, (station, value) in enumerate(station_avg.head(5).items(), 1):
                st.markdown(f"""
                <div class="station-card">
                    <strong>{idx}. {station}</strong><br>
                    <span style="color: #e74c3c; font-weight: bold;">{value:.1f} μg/m³</span>
                </div>
                """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown('<div class="subsection-header">Pollutant Relationships</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = create_correlation_heatmap(aqi_data)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown('<div class="subsection-header">Distribution Analysis</div>', unsafe_allow_html=True)
            pollutant = st.selectbox(
                "Select Pollutant:",
                options=['PM2.5', 'PM10', 'NO2', 'O3', 'CO', 'SO2'],
                index=0
            )
            
            fig2 = px.histogram(
                aqi_data,
                x=pollutant,
                nbins=30,
                title=f"{pollutant} Distribution",
                marginal="box",
                color_discrete_sequence=['#3498db']
            )
            fig2.update_layout(plot_bgcolor='white', paper_bgcolor='white')
            st.plotly_chart(fig2, use_container_width=True)
    
    with tab4:
        st.markdown('<div class="subsection-header">Data Exploration</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            selected_stations = st.multiselect(
                "Filter by Station:",
                options=aqi_data['Station name(district)'].unique(),
                default=[]
            )
        
        with col2:
            pollutants = st.multiselect(
                "Select Pollutants:",
                options=['NO2', 'O3', 'CO', 'SO2', 'PM10', 'PM2.5'],
                default=['PM2.5', 'PM10', 'NO2']
            )
        
        with col3:
            hour_range = st.slider(
                "Hour Range:",
                min_value=0,
                max_value=23,
                value=(0, 23)
            )
        
        # Apply filters
        filtered_data = aqi_data.copy()
        
        if selected_stations:
            filtered_data = filtered_data[filtered_data['Station name(district)'].isin(selected_stations)]
        
        filtered_data = filtered_data[
            (filtered_data['Hour'] >= hour_range[0]) & 
            (filtered_data['Hour'] <= hour_range[1])
        ]
        
        # Display table
        columns_to_show = ['Station name(district)', 'Measurement date', 'Hour'] + pollutants
        st.dataframe(
            filtered_data[columns_to_show].sort_values('Measurement date', ascending=False),
            use_container_width=True,
            height=400
        )

def render_predictions_page(aqi_data):
    """Render the AI predictions dashboard"""
    # Navigation header with back button
    col1, col2 = st.columns([1, 5])
    
    with col1:
        if st.button("← Back to Home"):
            st.session_state.page = "home"
            st.rerun()
    
    with col2:
        st.markdown('<h1 class="main-header">AI Forecasting System</h1>', unsafe_allow_html=True)
    
    # Sidebar for station selection
    with st.sidebar:
        st.markdown("### System Configuration")
        
        selected_station = st.selectbox(
            "Select Monitoring Station",
            options=list(STATIONS.keys()),
            index=0
        )
        
        st.markdown("---")
        
        # Backend connection status
        st.markdown("### System Status")
        try:
            response = requests.get(f"{FLASK_BACKEND_URL}/api/predict", 
                                  params={"station": selected_station}, 
                                  timeout=5)
            if response.status_code == 200:
                st.markdown('<span class="status-indicator status-online"></span> Backend Connected', unsafe_allow_html=True)
            else:
                st.markdown('<span class="status-indicator status-offline"></span> Backend Unavailable', unsafe_allow_html=True)
        except:
            st.markdown('<span class="status-indicator status-offline"></span> Backend Unavailable', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Refresh button
        if st.button("Refresh Predictions", use_container_width=True):
            st.rerun()
    
    # Main prediction content
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="section-header">Current Predictions</div>', unsafe_allow_html=True)
        
        # Get current predictions
        current_pred = get_current_prediction(selected_station)
        detailed_pred = get_detailed_prediction(selected_station)
        forecast_data = get_forecast_data(selected_station)
        
        if current_pred:
            pm25 = current_pred.get('prediction', 0)
            
            # Determine AQI category
            if pm25 < 15:
                category = "Good"
                color = "#2ecc71"
            elif pm25 < 35:
                category = "Moderate"
                color = "#f1c40f"
            elif pm25 < 75:
                category = "Poor"
                color = "#e67e22"
            else:
                category = "Very Poor"
                color = "#e74c3c"
            
            st.markdown(f"""
            <div class="dashboard-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h3 style="color: #2c3e50; margin-bottom: 0.5rem;">Current PM2.5</h3>
                        <h1 style="color: {color}; margin: 0;">{pm25:.1f} μg/m³</h1>
                        <p style="color: #7f8c8d; margin-top: 0.5rem;">{category} Air Quality</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        if detailed_pred:
            dominant = detailed_pred.get('dominant_pollutant', 'N/A')
            st.markdown(f"""
            <div class="dashboard-card">
                <h3 style="color: #2c3e50; margin-bottom: 0.5rem;">Dominant Pollutant</h3>
                <h2 style="color: #34495e; margin: 0;">{dominant}</h2>
                <p style="color: #7f8c8d; margin-top: 0.5rem;">Primary Health Concern</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="section-header">6-Hour Forecast</div>', unsafe_allow_html=True)
        
        if forecast_data is not None and not forecast_data.empty:
            fig = create_forecast_timeline(forecast_data)
            st.plotly_chart(fig, use_container_width=True)
    
    # Detailed predictions
    st.markdown('<div class="section-header">Detailed Analysis</div>', unsafe_allow_html=True)
    
    if detailed_pred:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.plotly_chart(create_pollution_gauge(
                detailed_pred.get('pm25_prediction', 0), 
                "PM2.5", 
                "μg/m³"
            ), use_container_width=True)
        
        with col2:
            st.plotly_chart(create_pollution_gauge(
                detailed_pred.get('no2_prediction', 0), 
                "NO₂", 
                "ppm"
            ), use_container_width=True)
        
        with col3:
            st.plotly_chart(create_pollution_gauge(
                detailed_pred.get('o3_prediction', 0), 
                "O₃", 
                "ppm"
            ), use_container_width=True)
    
    # Pollutant details table
    if detailed_pred:
        st.markdown('<div class="subsection-header">Pollutant Details</div>', unsafe_allow_html=True)
        
        pollutant_data = {
            'Pollutant': ['PM2.5', 'NO₂', 'O₃', 'CO', 'SO₂'],
            'Concentration': [
                f"{detailed_pred.get('pm25_prediction', 0):.2f} μg/m³",
                f"{detailed_pred.get('no2_prediction', 0):.2f} ppm",
                f"{detailed_pred.get('o3_prediction', 0):.2f} ppm",
                f"{detailed_pred.get('co_prediction', 0):.2f} ppm",
                f"{detailed_pred.get('so2_prediction', 0):.2f} ppm"
            ],
            'Health Impact': [
                'Respiratory issues' if detailed_pred.get('pm25_prediction', 0) > 35 else 'Minimal impact',
                'Respiratory irritation' if detailed_pred.get('no2_prediction', 0) > 0.06 else 'Minimal impact',
                'Lung tissue damage' if detailed_pred.get('o3_prediction', 0) > 0.09 else 'Minimal impact',
                'Cardiovascular effects' if detailed_pred.get('co_prediction', 0) > 9 else 'Minimal impact',
                'Respiratory problems' if detailed_pred.get('so2_prediction', 0) > 0.05 else 'Minimal impact'
            ]
        }
        
        st.dataframe(pd.DataFrame(pollutant_data), use_container_width=True, hide_index=True)
        
        # Health recommendations
        st.markdown('<div class="subsection-header">Health Recommendations</div>', unsafe_allow_html=True)
        
        pm25_level = detailed_pred.get('pm25_prediction', 0)
        if pm25_level < 15:
            st.success("**Good Air Quality:** Perfect for outdoor activities. No restrictions needed.")
        elif pm25_level < 35:
            st.info("**Moderate Air Quality:** Generally acceptable. Sensitive individuals should consider reducing prolonged outdoor exertion.")
        elif pm25_level < 75:
            st.warning("**Poor Air Quality:** Everyone may begin to experience health effects. Reduce prolonged or heavy outdoor exertion.")
        else:
            st.error("**Very Poor Air Quality:** Health alert - everyone may experience more serious health effects. Avoid all outdoor exertion.")

def main():
    # Load data
    aqi_data, station_info, item_info = load_static_data()
    
    # Navigation based on session state
    if st.session_state.page == "home":
        render_home_page()
    elif st.session_state.page == "data_overview":
        render_data_overview(aqi_data, station_info, item_info)
    elif st.session_state.page == "predictions":
        render_predictions_page(aqi_data)
    else:
        render_home_page()
    
    # Footer
    st.markdown("""
    <div class="footer">
        <p><strong>Air Quality Intelligence Platform</strong></p>
        <p>Powered by Temporal Graph Convolutional Networks • Seoul Air Quality Monitoring Network</p>
        <p>System Version 2.0 • Last Updated: {}</p>
        <p style="margin-top: 1rem; font-size: 0.8rem; color: #95a5a6;">
            Data Analytics | AI Forecasting | Real-time Monitoring
        </p>
    </div>
    """.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), unsafe_allow_html=True)

if __name__ == "__main__":
    main()