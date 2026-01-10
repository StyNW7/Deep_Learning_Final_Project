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
        color: #ff2a6d;
        text-align: center;
        margin-bottom: 1.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #ff2a6d 0%, #0055ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #2d3748;
    }
    .section-header {
        font-size: 2.2rem;
        color: #e2e8f0;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        font-weight: 600;
        padding-left: 0.5rem;
        border-left: 5px solid #ff2a6d;
        background: linear-gradient(90deg, #2d3748 0%, #1a202c 100%);
        padding: 1rem;
        border-radius: 8px;
    }
    .subsection-header {
        font-size: 1.5rem;
        color: #cbd5e0;
        margin-top: 1.2rem;
        margin-bottom: 0.8rem;
        font-weight: 600;
        padding-left: 0.5rem;
        border-left: 3px solid #0055ff;
    }
    .card-container {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        border: 1px solid rgba(255, 42, 109, 0.3);
        color: #e2e8f0;
        border-radius: 15px;
        padding: 2.5rem;
        text-align: center;
        box-shadow: 0 15px 35px rgba(255, 42, 109, 0.1);
        margin-bottom: 2rem;
        transition: all 0.4s ease;
        cursor: pointer;
        height: 300px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        position: relative;
        overflow: hidden;
    }
    .card-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #ff2a6d 0%, #0055ff 100%);
    }
    .card-container:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 20px 40px rgba(255, 42, 109, 0.2);
        border-color: rgba(255, 42, 109, 0.6);
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 45%, #0f3460 100%);
    }
    .dashboard-card {
        color: #e2e8f0;
        background: linear-gradient(145deg, #1a202c 0%, #2d3748 100%);
        border-radius: 12px;
        padding: 1.8rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        margin-bottom: 1.5rem;
        border: 1px solid rgba(255, 42, 109, 0.2);
        transition: all 0.3s ease;
    }
    .dashboard-card:hover {
        box-shadow: 0 12px 48px rgba(255, 42, 109, 0.25);
        transform: translateY(-4px);
        border-color: rgba(255, 42, 109, 0.4);
    }
    .metric-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #0f3460 100%);
        color: #e2e8f0;
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(255, 42, 109, 0.15);
        margin-bottom: 1rem;
        border: 1px solid rgba(255, 42, 109, 0.2);
        position: relative;
        overflow: hidden;
    }
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #ff2a6d 0%, #0055ff 100%);
    }
    .info-card {
        background: linear-gradient(135deg, #0f3460 0%, #1a1a2e 100%);
        color: #e2e8f0;
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0, 85, 255, 0.15);
        margin-bottom: 1rem;
        border: 1px solid rgba(0, 85, 255, 0.2);
        position: relative;
        overflow: hidden;
    }
    .info-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #0055ff 0%, #ff2a6d 100%);
    }
    .station-card {
        color: #e2e8f0;
        background: linear-gradient(145deg, #2d3748 0%, #1a202c 100%);
        border-left: 4px solid #ff2a6d;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 0.8rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
        border-top: 1px solid rgba(255, 42, 109, 0.1);
        border-right: 1px solid rgba(255, 42, 109, 0.1);
        border-bottom: 1px solid rgba(255, 42, 109, 0.1);
    }
    .station-card:hover {
        border-left-color: #0055ff;
        border-left-width: 6px;
        box-shadow: 0 8px 32px rgba(255, 42, 109, 0.2);
        transform: translateX(4px);
        background: linear-gradient(145deg, #2d3748 0%, #1a202c 80%);
    }
    .status-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
        box-shadow: 0 0 10px currentColor;
    }
    .status-online {
        background-color: #00ff88;
        color: #00ff88;
    }
    .status-offline {
        background-color: #ff2a6d;
        color: #ff2a6d;
    }
    .tab-content {
        padding: 1.5rem;
        background: linear-gradient(145deg, #1a202c 0%, #2d3748 100%);
        border-radius: 10px;
        margin-top: 1rem;
        color: #e2e8f0;
        border: 1px solid rgba(255, 42, 109, 0.1);
        box-shadow: inset 0 2px 10px rgba(0, 0, 0, 0.2);
    }
    .stSelectbox > div > div {
        background-color: #2d3748;
        border-radius: 8px;
        border: 1px solid rgba(255, 42, 109, 0.3);
        color: #e2e8f0;
    }
    .stSlider > div > div > div {
        background: linear-gradient(90deg, #ff2a6d 0%, #0055ff 100%);
        color: white;
    }
    .data-table {
        background: linear-gradient(145deg, #1a202c 0%, #2d3748 100%);
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        color: #e2e8f0;
        border: 1px solid rgba(255, 42, 109, 0.1);
    }
    .footer {
        text-align: center;
        color: #a0aec0;
        font-size: 0.9rem;
        padding: 2rem;
        margin-top: 3rem;
        border-top: 1px solid rgba(255, 42, 109, 0.2);
        background: linear-gradient(145deg, #1a202c 0%, #2d3748 100%);
        border-radius: 10px;
    }
    .navigation-button {
        background: linear-gradient(90deg, #ff2a6d 0%, #0055ff 100%);
        padding: 0.8rem 2rem;
        border-radius: 25px;
        border: none;
        color: white;
        font-size: 1rem;
        font-weight: 600;
        cursor: pointer;
        margin-top: 1.5rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(255, 42, 109, 0.3);
    }
    .navigation-button:hover {
        background: linear-gradient(90deg, #0055ff 0%, #ff2a6d 100%);
        transform: scale(1.05) translateY(-2px);
        box-shadow: 0 8px 25px rgba(255, 42, 109, 0.4);
        color: white;
    }
    
    /* Additional styling for better contrast */
    body {
        background-color: #0f172a !important;
        color: #e2e8f0 !important;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1a202c;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #ff2a6d 0%, #0055ff 100%);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #0055ff 0%, #ff2a6d 100%);
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

# Pollutant information
POLLUTANTS = {
    'PM2.5': {
        'name': 'PM2.5',
        'unit': 'μg/m³',
        'thresholds': [0, 15, 35, 75, 500],
        'categories': ['Good', 'Moderate', 'Poor', 'Very Poor'],
        'colors': ['#2ecc71', '#f1c40f', '#e67e22', '#e74c3c']
    },
    'PM10': {
        'name': 'PM10',
        'unit': 'μg/m³',
        'thresholds': [0, 30, 80, 150, 600],
        'categories': ['Good', 'Moderate', 'Poor', 'Very Poor'],
        'colors': ['#2ecc71', '#f1c40f', '#e67e22', '#e74c3c']
    },
    'NO2': {
        'name': 'NO₂',
        'unit': 'ppm',
        'thresholds': [0, 0.03, 0.06, 0.2, 2],
        'categories': ['Good', 'Moderate', 'Poor', 'Very Poor'],
        'colors': ['#2ecc71', '#f1c40f', '#e67e22', '#e74c3c']
    },
    'O3': {
        'name': 'O₃',
        'unit': 'ppm',
        'thresholds': [0, 0.05, 0.09, 0.15, 0.5],
        'categories': ['Good', 'Moderate', 'Poor', 'Very Poor'],
        'colors': ['#2ecc71', '#f1c40f', '#e67e22', '#e74c3c']
    },
    'CO': {
        'name': 'CO',
        'unit': 'ppm',
        'thresholds': [0, 4.5, 9, 15, 50],
        'categories': ['Good', 'Moderate', 'Poor', 'Very Poor'],
        'colors': ['#2ecc71', '#f1c40f', '#e67e22', '#e74c3c']
    },
    'SO2': {
        'name': 'SO₂',
        'unit': 'ppm',
        'thresholds': [0, 0.02, 0.05, 0.15, 1],
        'categories': ['Good', 'Moderate', 'Poor', 'Very Poor'],
        'colors': ['#2ecc71', '#f1c40f', '#e67e22', '#e74c3c']
    }
}

# Initialize session state for navigation and pollutant selection
if 'page' not in st.session_state:
    st.session_state.page = 'home'

if 'selected_pollutant' not in st.session_state:
    st.session_state.selected_pollutant = 'PM2.5'

@st.cache_data
def load_static_data():
    """Load static CSV data for historical analysis"""
    try:
        aqi_data = pd.read_csv('../backend/aqi_data.csv')
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

def get_forecast_data(station, pollutant='PM2.5'):
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

def get_current_prediction(station, pollutant='PM2.5'):
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

def get_pollutant_value(detailed_data, pollutant):
    """Get pollutant value from detailed data"""
    mapping = {
        'PM2.5': 'pm25_prediction',
        'PM10': 'pm10_prediction',
        'NO2': 'no2_prediction',
        'O3': 'o3_prediction',
        'CO': 'co_prediction',
        'SO2': 'so2_prediction'
    }
    return detailed_data.get(mapping.get(pollutant, 'pm25_prediction'), 0)

def create_pollution_gauge(value, pollutant_info):
    """Create a gauge chart for pollution levels"""
    title = pollutant_info['name']
    unit = pollutant_info['unit']
    levels = pollutant_info['thresholds']
    colors = pollutant_info['colors']
    
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

def create_forecast_timeline(forecast_df, pollutant='PM2.5'):
    """Create timeline visualization for forecast"""
    if forecast_df.empty:
        return go.Figure()
    
    # Map pollutant to column name
    pollutant_col = {
        'PM2.5': 'pm25',
        'PM10': 'pm10',
        'NO2': 'no2',
        'O3': 'o3',
        'CO': 'co',
        'SO2': 'so2'
    }.get(pollutant, 'pm25')
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=forecast_df['hour'],
        y=forecast_df[pollutant_col] if pollutant_col in forecast_df.columns else [0] * len(forecast_df),
        mode='lines+markers',
        name=f'{pollutant} Forecast',
        line=dict(color='#e74c3c', width=3),
        marker=dict(size=10, color='white', line=dict(width=2, color='#e74c3c'))
    ))
    
    # Add threshold areas based on selected pollutant
    pollutant_info = POLLUTANTS.get(pollutant, POLLUTANTS['PM2.5'])
    levels = pollutant_info['thresholds']
    
    fig.add_hrect(y0=levels[0], y1=levels[1], fillcolor="rgba(46, 204, 113, 0.2)", 
                  line_width=0, layer="below", annotation_text="Good")
    fig.add_hrect(y0=levels[1], y1=levels[2], fillcolor="rgba(241, 196, 15, 0.2)", 
                  line_width=0, layer="below", annotation_text="Moderate")
    fig.add_hrect(y0=levels[2], y1=levels[3], fillcolor="rgba(230, 126, 34, 0.2)", 
                  line_width=0, layer="below", annotation_text="Poor")
    fig.add_hrect(y0=levels[3], y1=levels[4], 
                  fillcolor="rgba(231, 76, 60, 0.2)", line_width=0, 
                  layer="below", annotation_text="Very Poor")
    
    fig.update_layout(
        title=dict(text=f"6-Hour {pollutant} Forecast", font=dict(size=20)),
        xaxis_title="Time",
        yaxis_title=f"{pollutant} ({pollutant_info['unit']})",
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

def create_temporal_analysis(aqi_data, pollutant='PM2.5', station_name=None):
    """Create temporal analysis visualizations"""
    if station_name:
        data = aqi_data[aqi_data['Station name(district)'] == station_name]
    else:
        data = aqi_data
    
    # Get available pollutants in data
    available_pollutants = [p for p in ['PM2.5', 'PM10', 'NO2', 'O3', 'CO', 'SO2'] if p in data.columns]
    
    # If selected pollutant is not available, use first available
    if pollutant not in available_pollutants and available_pollutants:
        pollutant = available_pollutants[0]
    
    # Create hourly averages for all available pollutants
    hourly_avg = data.groupby('Hour')[available_pollutants[:4]].mean().reset_index()
    
    # Create subplots for the selected pollutant and others
    selected_idx = available_pollutants.index(pollutant) if pollutant in available_pollutants else 0
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            f'{pollutant} Hourly Trend',
            f'{available_pollutants[(selected_idx + 1) % len(available_pollutants)]} Hourly Trend' if len(available_pollutants) > 1 else pollutant + ' Trend',
            f'{available_pollutants[(selected_idx + 2) % len(available_pollutants)]} Hourly Trend' if len(available_pollutants) > 2 else pollutant + ' Trend',
            f'{available_pollutants[(selected_idx + 3) % len(available_pollutants)]} Hourly Trend' if len(available_pollutants) > 3 else pollutant + ' Trend'
        ),
        vertical_spacing=0.15,
        horizontal_spacing=0.1
    )
    
    colors = ['#e74c3c', '#e67e22', '#3498db', '#27ae60']
    
    # Plot selected pollutant
    if pollutant in hourly_avg.columns:
        fig.add_trace(
            go.Scatter(x=hourly_avg['Hour'], y=hourly_avg[pollutant], 
                      mode='lines+markers', name=pollutant, 
                      line=dict(color=colors[0], width=2.5)),
            row=1, col=1
        )
    
    # Plot other pollutants
    for i in range(1, 4):
        if len(available_pollutants) > i:
            other_poll = available_pollutants[(selected_idx + i) % len(available_pollutants)]
            if other_poll in hourly_avg.columns:
                row = (i + 1) // 2
                col = (i + 1) % 2 + 1
                fig.add_trace(
                    go.Scatter(x=hourly_avg['Hour'], y=hourly_avg[other_poll], 
                              mode='lines+markers', name=other_poll, 
                              line=dict(color=colors[i % len(colors)], width=2.5)),
                    row=row, col=col
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

def create_station_comparison(aqi_data, selected_stations, pollutant='PM2.5'):
    """Create station comparison visualization"""
    filtered_data = aqi_data[aqi_data['Station name(district)'].isin(selected_stations)]
    
    fig = px.box(
        filtered_data,
        x='Station name(district)',
        y=pollutant,
        color='Station name(district)',
        points='all',
        title=f"{pollutant} Distribution by Station",
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
    # Filter only pollutants that exist in data
    existing_pollutants = [p for p in pollutants if p in aqi_data.columns]
    correlation_matrix = aqi_data[existing_pollutants].corr()
    
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

def create_spatial_map(aqi_data, station_info, pollutant='PM2.5'):
    """Create spatial map visualization"""
    station_avg = aqi_data.groupby(['Station code', 'Station name(district)']).agg({
        pollutant: 'mean'
    }).reset_index()
    
    station_avg = pd.merge(station_avg, station_info[['Station code', 'Latitude', 'Longitude']], 
                          on='Station code', how='left')
    
    fig = px.scatter_mapbox(
        station_avg,
        lat="Latitude",
        lon="Longitude",
        size=pollutant,
        color=pollutant,
        hover_name="Station name(district)",
        hover_data=[pollutant],
        color_continuous_scale=px.colors.sequential.Reds,
        size_max=25,
        zoom=10,
        height=500,
        title=f"{pollutant} Spatial Distribution"
    )
    
    fig.update_layout(mapbox_style="carto-positron")
    return fig

def get_pollutant_health_impact(pollutant, value):
    """Get health impact description for pollutant value"""
    if pollutant == 'PM2.5':
        if value < 15:
            return "Minimal impact"
        elif value < 35:
            return "Mild respiratory effects"
        elif value < 75:
            return "Respiratory issues"
        else:
            return "Serious health risk"
    elif pollutant == 'PM10':
        if value < 30:
            return "Minimal impact"
        elif value < 80:
            return "Mild respiratory effects"
        elif value < 150:
            return "Respiratory issues"
        else:
            return "Serious health risk"
    elif pollutant == 'NO2':
        if value < 0.03:
            return "Minimal impact"
        elif value < 0.06:
            return "Mild respiratory irritation"
        elif value < 0.2:
            return "Respiratory irritation"
        else:
            return "Serious respiratory effects"
    elif pollutant == 'O3':
        if value < 0.05:
            return "Minimal impact"
        elif value < 0.09:
            return "Mild effects"
        elif value < 0.15:
            return "Lung tissue damage risk"
        else:
            return "Serious lung damage risk"
    elif pollutant == 'CO':
        if value < 4.5:
            return "Minimal impact"
        elif value < 9:
            return "Mild cardiovascular effects"
        elif value < 15:
            return "Cardiovascular effects"
        else:
            return "Serious health risk"
    elif pollutant == 'SO2':
        if value < 0.02:
            return "Minimal impact"
        elif value < 0.05:
            return "Mild respiratory effects"
        elif value < 0.15:
            return "Respiratory problems"
        else:
            return "Serious respiratory damage"
    return "Unknown impact"

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
    
    # Pollutant selection
    available_pollutants = [col for col in POLLUTANTS.keys() if col in aqi_data.columns]
    if not available_pollutants:
        available_pollutants = list(POLLUTANTS.keys())
    
    col1, col2, col3 = st.columns([2, 2, 2])
    
    with col1:
        selected_pollutant = st.selectbox(
            "Select Pollutant for Analysis:",
            options=available_pollutants,
            index=available_pollutants.index(st.session_state.selected_pollutant) if st.session_state.selected_pollutant in available_pollutants else 0,
            key="data_pollutant_select"
        )
        st.session_state.selected_pollutant = selected_pollutant
    
    # Summary metrics for selected pollutant
    pollutant_info = POLLUTANTS.get(selected_pollutant, POLLUTANTS['PM2.5'])
    
    st.markdown('<div class="section-header">Key Performance Indicators</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_value = aqi_data[selected_pollutant].mean()
        levels = pollutant_info['thresholds']
        if avg_value < levels[1]:
            status = "Good"
        elif avg_value < levels[2]:
            status = "Moderate"
        elif avg_value < levels[3]:
            status = "Poor"
        else:
            status = "Very Poor"
        
        st.metric(f"Average {selected_pollutant}", 
                 f"{avg_value:.1f} {pollutant_info['unit']}", 
                 delta=status)
    
    with col2:
        max_value = aqi_data[selected_pollutant].max()
        st.metric(f"Maximum {selected_pollutant}", 
                 f"{max_value:.1f} {pollutant_info['unit']}")
    
    with col3:
        station_max = aqi_data.groupby('Station name(district)')[selected_pollutant].mean().idxmax()
        st.metric("Highest Station", station_max)
    
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
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            station_filter = st.selectbox(
                "Select Station for Analysis:",
                options=["All Stations"] + list(aqi_data['Station name(district)'].unique()),
                index=0
            )
        
        with col2:
            # Optional: Add time range filter
            pass
        
        if station_filter == "All Stations":
            fig = create_temporal_analysis(aqi_data, selected_pollutant)
        else:
            fig = create_temporal_analysis(aqi_data, selected_pollutant, station_filter)
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Additional temporal insights
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f'<div class="subsection-header">{selected_pollutant} Daily Pattern</div>', unsafe_allow_html=True)
            daily_pattern = aqi_data.groupby('Hour').agg({selected_pollutant: 'mean'}).reset_index()
            fig2 = px.area(daily_pattern, x='Hour', y=selected_pollutant, 
                         title="", 
                         line_shape='spline',
                         color_discrete_sequence=['#e74c3c'])
            fig2.update_layout(plot_bgcolor='white', paper_bgcolor='white')
            st.plotly_chart(fig2, use_container_width=True)
        
        with col2:
            st.markdown(f'<div class="subsection-header">{selected_pollutant} Peak Hours</div>', unsafe_allow_html=True)
            peak_hours = aqi_data.groupby('Hour')[selected_pollutant].mean().nlargest(5)
            peak_df = pd.DataFrame({
                'Hour': [f"{hour:02d}:00" for hour in peak_hours.index],
                selected_pollutant: peak_hours.values
            })
            
            fig3 = px.bar(peak_df, x='Hour', y=selected_pollutant, 
                         color=selected_pollutant,
                         color_continuous_scale='Reds',
                         title="")
            fig3.update_layout(plot_bgcolor='white', paper_bgcolor='white')
            st.plotly_chart(fig3, use_container_width=True)
    
    with tab2:
        st.markdown('<div class="subsection-header">Geographical Distribution</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            fig = create_spatial_map(aqi_data, station_info, selected_pollutant)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown(f'<div class="subsection-header">Top Stations - {selected_pollutant}</div>', unsafe_allow_html=True)
            station_avg = aqi_data.groupby('Station name(district)')[selected_pollutant].mean().sort_values(ascending=False)
            
            for idx, (station, value) in enumerate(station_avg.head(5).items(), 1):
                st.markdown(f"""
                <div class="station-card">
                    <strong>{idx}. {station}</strong><br>
                    <span style="color: #e74c3c; font-weight: bold;">{value:.1f} {pollutant_info['unit']}</span>
                </div>
                """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown('<div class="subsection-header">Pollutant Relationships</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = create_correlation_heatmap(aqi_data)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown(f'<div class="subsection-header">{selected_pollutant} Distribution</div>', unsafe_allow_html=True)
            
            fig2 = px.histogram(
                aqi_data,
                x=selected_pollutant,
                nbins=30,
                title=f"{selected_pollutant} Distribution",
                marginal="box",
                color_discrete_sequence=['#3498db']
            )
            fig2.update_layout(plot_bgcolor='white', paper_bgcolor='white')
            st.plotly_chart(fig2, use_container_width=True)
            
            # Statistics
            stats_col1, stats_col2, stats_col3 = st.columns(3)
            with stats_col1:
                st.metric("Mean", f"{aqi_data[selected_pollutant].mean():.1f}")
            with stats_col2:
                st.metric("Std Dev", f"{aqi_data[selected_pollutant].std():.1f}")
            with stats_col3:
                st.metric("Median", f"{aqi_data[selected_pollutant].median():.1f}")
    
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
            # Get available pollutants from data, remove duplicates
            available_pollutants_in_data = [col for col in ['NO2', 'O3', 'CO', 'SO2', 'PM10', 'PM2.5'] if col in aqi_data.columns]
            # Remove duplicates and ensure selected_pollutant is included
            pollutants = st.multiselect(
                "Select Pollutants:",
                options=available_pollutants_in_data,
                default=[selected_pollutant] if selected_pollutant in available_pollutants_in_data else [available_pollutants_in_data[0]] if available_pollutants_in_data else []
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
        
        # Display table - ensure no duplicate columns
        if pollutants:
            # Remove duplicates from pollutants list
            pollutants = list(dict.fromkeys(pollutants))
            columns_to_show = ['Station name(district)', 'Measurement date', 'Hour'] + pollutants
            # Ensure all columns exist in the dataframe
            existing_columns = [col for col in columns_to_show if col in filtered_data.columns]
            
            if existing_columns:
                st.dataframe(
                    filtered_data[existing_columns].sort_values('Measurement date', ascending=False),
                    use_container_width=True,
                    height=400
                )
            else:
                st.info("No data available with the current filters.")
        else:
            st.info("Please select at least one pollutant to display data.")

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
    
    # Sidebar for station and pollutant selection
    with st.sidebar:
        st.markdown("### System Configuration")
        
        selected_station = st.selectbox(
            "Select Monitoring Station",
            options=list(STATIONS.keys()),
            index=0
        )
        
        st.markdown("---")
        
        selected_pollutant = st.selectbox(
            "Select Pollutant for Analysis",
            options=list(POLLUTANTS.keys()),
            index=list(POLLUTANTS.keys()).index(st.session_state.selected_pollutant) if st.session_state.selected_pollutant in POLLUTANTS else 0
        )
        st.session_state.selected_pollutant = selected_pollutant
        
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
    pollutant_info = POLLUTANTS.get(selected_pollutant, POLLUTANTS['PM2.5'])
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="section-header">Current Predictions</div>', unsafe_allow_html=True)
        
        # Get current predictions
        current_pred = get_current_prediction(selected_station, selected_pollutant)
        detailed_pred = get_detailed_prediction(selected_station)
        forecast_data = get_forecast_data(selected_station, selected_pollutant)
        
        if current_pred:
            pm25 = current_pred.get('prediction', 0)
            
            # Determine AQI category based on selected pollutant
            value = pm25  # Default to PM2.5 prediction
            if detailed_pred:
                value = get_pollutant_value(detailed_pred, selected_pollutant)
            
            levels = pollutant_info['thresholds']
            if value < levels[1]:
                category = "Good"
                color = "#2ecc71"
            elif value < levels[2]:
                category = "Moderate"
                color = "#f1c40f"
            elif value < levels[3]:
                category = "Poor"
                color = "#e67e22"
            else:
                category = "Very Poor"
                color = "#e74c3c"
            
            st.markdown(f"""
            <div class="dashboard-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h3 style="color: #2c3e50; margin-bottom: 0.5rem;">Current {selected_pollutant}</h3>
                        <h1 style="color: {color}; margin: 0;">{value:.1f} {pollutant_info['unit']}</h1>
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
            fig = create_forecast_timeline(forecast_data, selected_pollutant)
            st.plotly_chart(fig, use_container_width=True)
    
    # Detailed predictions
    st.markdown('<div class="section-header">Detailed Analysis</div>', unsafe_allow_html=True)
    
    if detailed_pred:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.plotly_chart(create_pollution_gauge(
                get_pollutant_value(detailed_pred, selected_pollutant),
                pollutant_info
            ), use_container_width=True)
        
        with col2:
            # Show second pollutant
            other_pollutants = [p for p in POLLUTANTS.keys() if p != selected_pollutant]
            if other_pollutants:
                second_pollutant = other_pollutants[0]
                second_info = POLLUTANTS[second_pollutant]
                st.plotly_chart(create_pollution_gauge(
                    get_pollutant_value(detailed_pred, second_pollutant),
                    second_info
                ), use_container_width=True)
        
        with col3:
            # Show third pollutant
            if len(other_pollutants) > 1:
                third_pollutant = other_pollutants[1]
                third_info = POLLUTANTS[third_pollutant]
                st.plotly_chart(create_pollution_gauge(
                    get_pollutant_value(detailed_pred, third_pollutant),
                    third_info
                ), use_container_width=True)
    
    # Pollutant details table
    if detailed_pred:
        st.markdown('<div class="subsection-header">Pollutant Details</div>', unsafe_allow_html=True)
        
        pollutant_data = []
        for poll, info in POLLUTANTS.items():
            value = get_pollutant_value(detailed_pred, poll)
            health_impact = get_pollutant_health_impact(poll, value)
            
            pollutant_data.append({
                'Pollutant': info['name'],
                'Concentration': f"{value:.2f} {info['unit']}",
                'Health Impact': health_impact,
                'Status': 'Good' if value < info['thresholds'][1] else 
                         'Moderate' if value < info['thresholds'][2] else 
                         'Poor' if value < info['thresholds'][3] else 'Very Poor'
            })
        
        df = pd.DataFrame(pollutant_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Health recommendations for selected pollutant
        st.markdown('<div class="subsection-header">Health Recommendations</div>', unsafe_allow_html=True)
        
        selected_value = get_pollutant_value(detailed_pred, selected_pollutant)
        levels = pollutant_info['thresholds']
        
        if selected_value < levels[1]:
            st.success(f"**Good Air Quality for {selected_pollutant}:** Perfect for outdoor activities. No restrictions needed.")
        elif selected_value < levels[2]:
            st.info(f"**Moderate Air Quality for {selected_pollutant}:** Generally acceptable. Sensitive individuals should consider reducing prolonged outdoor exertion.")
        elif selected_value < levels[3]:
            st.warning(f"**Poor Air Quality for {selected_pollutant}:** Everyone may begin to experience health effects. Reduce prolonged or heavy outdoor exertion.")
        else:
            st.error(f"**Very Poor Air Quality for {selected_pollutant}:** Health alert - everyone may experience more serious health effects. Avoid all outdoor exertion.")

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
        <p><strong>AeroSeoul - Air Quality Intelligence Dashboard</strong></p>
        <p>Powered by Temporal Graph Convolutional Networks • Seoul Air Quality Monitoring Network</p>
        <p>Data Analytics | AI Forecasting | Real-time Monitoring</p>
        <p style="margin-top: 1rem; font-size: 0.8rem; color: #95a5a6;">
            Stanley | Nathaniel | Roderich
        </p>
    </div>
    """.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), unsafe_allow_html=True)

if __name__ == "__main__":
    main()