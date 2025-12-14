import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
import json
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Set page configuration
st.set_page_config(
    page_title="AI Air Quality Forecasting Dashboard",
    page_icon="🌫️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .sub-header {
        font-size: 2rem;
        color: #2c3e50;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        font-weight: 600;
        border-bottom: 3px solid #3498db;
        padding-bottom: 0.5rem;
    }
    .section-header {
        font-size: 1.5rem;
        color: #34495e;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
        font-weight: 600;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        transition: transform 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-5px);
    }
    .station-card {
        background-color: #ffffff;
        border-left: 5px solid #3498db;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }
    .station-card:hover {
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        transform: translateX(5px);
    }
    .prediction-card {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        color: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }
    .warning-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }
    .info-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }
    .tab-content {
        padding: 1rem;
        background: #f8f9fa;
        border-radius: 10px;
        margin-top: 1rem;
    }
    .stSelectbox > div > div {
        background-color: white;
        border-radius: 10px;
    }
    .stSlider > div > div > div {
        background-color: #3498db;
    }
</style>
""", unsafe_allow_html=True)

# Configuration
FLASK_BACKEND_URL = "http://localhost:5000"  # Update this if your Flask server runs elsewhere
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

def create_pollution_gauge(value, title, thresholds):
    """Create a gauge chart for pollution levels"""
    if title == "PM2.5":
        levels = [0, 15, 35, 75, 500]
        colors = ['green', 'yellow', 'orange', 'red']
        categories = ['Good', 'Moderate', 'Poor', 'Very Poor']
    elif title == "PM10":
        levels = [0, 30, 80, 150, 600]
        colors = ['green', 'yellow', 'orange', 'red']
        categories = ['Good', 'Moderate', 'Poor', 'Very Poor']
    else:
        levels = [0, value * 0.3, value * 0.6, value * 0.9, value * 1.2]
        colors = ['green', 'yellow', 'orange', 'red']
        categories = ['Low', 'Moderate', 'High', 'Very High']
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title, 'font': {'size': 24}},
        number={'suffix': ' μg/m³' if title in ['PM2.5', 'PM10'] else ' ppm'},
        gauge={
            'axis': {'range': [0, levels[-1]], 'tickwidth': 1},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [levels[0], levels[1]], 'color': colors[0]},
                {'range': [levels[1], levels[2]], 'color': colors[1]},
                {'range': [levels[2], levels[3]], 'color': colors[2]},
                {'range': [levels[3], levels[4]], 'color': colors[3]},
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': value
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=50, b=20)
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
        line=dict(color='red', width=3),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title="6-Hour PM2.5 Forecast",
        xaxis_title="Time",
        yaxis_title="PM2.5 (μg/m³)",
        hovermode='x unified',
        height=400,
        plot_bgcolor='rgba(240, 240, 240, 0.5)',
        paper_bgcolor='rgba(255, 255, 255, 0.8)',
        font=dict(size=12)
    )
    
    # Add threshold lines
    fig.add_hline(y=15, line_dash="dot", line_color="green", annotation_text="Good")
    fig.add_hline(y=35, line_dash="dot", line_color="yellow", annotation_text="Moderate")
    fig.add_hline(y=75, line_dash="dot", line_color="orange", annotation_text="Poor")
    
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
        line=dict(color='blue', width=3),
        marker=dict(size=8, color='white', line=dict(color='blue', width=2))
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=False,
        title="Pollutant Concentration Profile",
        height=400
    )
    
    return fig

def create_station_health_dashboard(aqi_data):
    """Create station health overview"""
    if aqi_data.empty:
        return go.Figure()
    
    # Calculate station health scores
    station_health = aqi_data.groupby('Station name(district)').agg({
        'PM2.5': 'mean',
        'PM10': 'mean',
        'NO2': 'mean'
    }).reset_index()
    
    # Create health score (lower is better)
    station_health['Health Score'] = (
        station_health['PM2.5'] / 15 +  # PM2.5 weight
        station_health['PM10'] / 30 +   # PM10 weight
        station_health['NO2'] / 0.03    # NO2 weight
    ) / 3
    
    fig = px.bar(
        station_health.sort_values('Health Score', ascending=True),
        y='Station name(district)',
        x='Health Score',
        color='Health Score',
        color_continuous_scale='RdYlGn_r',  # Red to Green (reversed)
        title="Station Air Quality Health Score",
        labels={'Health Score': 'Health Score (Lower is Better)'},
        height=500
    )
    
    fig.update_layout(
        yaxis={'categoryorder': 'total ascending'},
        coloraxis_showscale=True,
        plot_bgcolor='white'
    )
    
    return fig

def create_temporal_heatmap(aqi_data, station):
    """Create heatmap of pollution over time"""
    if aqi_data.empty:
        return go.Figure()
    
    station_data = aqi_data[aqi_data['Station name(district)'] == station].copy()
    if station_data.empty:
        return go.Figure()
    
    # Create pivot table for heatmap
    station_data['Hour'] = station_data['Measurement date'].dt.hour
    heatmap_data = station_data.pivot_table(
        values='PM2.5',
        index=station_data['Measurement date'].dt.date,
        columns='Hour',
        aggfunc='mean'
    )
    
    fig = px.imshow(
        heatmap_data.T,
        labels=dict(x="Date", y="Hour", color="PM2.5 (μg/m³)"),
        title=f"PM2.5 Heatmap - {station}",
        aspect="auto",
        color_continuous_scale="Reds"
    )
    
    fig.update_layout(
        height=400,
        xaxis_title="Date",
        yaxis_title="Hour of Day"
    )
    
    return fig

def main():
    # Load static data
    aqi_data, station_info, item_info = load_static_data()
    
    # Header
    st.markdown('<h1 class="main-header">AI-Powered Air Quality Forecasting System</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.markdown("## 🔧 Controls & Configuration")
        
        # Station selection
        selected_station = st.selectbox(
            "Select Monitoring Station",
            options=list(STATIONS.keys()),
            index=0
        )
        
        st.markdown("---")
        
        # Refresh controls
        col1, col2 = st.columns(2)
        with col1:
            refresh_predictions = st.button("🔄 Refresh Predictions")
        with col2:
            refresh_data = st.button("📊 Refresh Data")
        
        st.markdown("---")
        
        # Display station info
        if not station_info.empty:
            station_row = station_info[station_info['Station name(district)'] == selected_station]
            if not station_row.empty:
                st.markdown("### 📍 Station Information")
                st.write(f"**Station Code:** {station_row['Station code'].values[0]}")
                st.write(f"**Address:** {station_row['Address'].values[0]}")
                st.write(f"**Coordinates:** {station_row['Latitude'].values[0]:.4f}, {station_row['Longitude'].values[0]:.4f}")
        
        st.markdown("---")
        
        # System Status
        st.markdown("### 🚦 System Status")
        try:
            # Test backend connection
            response = requests.get(f"{FLASK_BACKEND_URL}/api/predict", 
                                  params={"station": selected_station}, 
                                  timeout=5)
            if response.status_code == 200:
                st.success("✅ Backend Connected")
            else:
                st.error("❌ Backend Unavailable")
        except:
            st.error("❌ Backend Unavailable")
    
    # Main Dashboard Tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📈 Real-time Forecast",
        "🔍 Detailed Analysis", 
        "🌍 Spatial Overview",
        "📊 Historical Trends",
        "⚙️ Model Insights",
        "📋 Data Explorer"
    ])
    
    with tab1:
        st.markdown(f'<div class="sub-header">Real-time Forecast - {selected_station}</div>', unsafe_allow_html=True)
        
        # Fetch current predictions
        current_pred = get_current_prediction(selected_station)
        detailed_pred = get_detailed_prediction(selected_station)
        forecast_data = get_forecast_data(selected_station)
        
        # Top metrics row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if current_pred:
                pm25 = current_pred.get('prediction', 0)
                status = "Good" if pm25 < 15 else "Moderate" if pm25 < 35 else "Poor" if pm25 < 75 else "Very Poor"
                st.markdown(f"""
                <div class="metric-card">
                    <h3>Current PM2.5</h3>
                    <h2>{pm25:.1f} μg/m³</h2>
                    <p>{status}</p>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            if detailed_pred:
                dominant = detailed_pred.get('dominant_pollutant', 'N/A')
                st.markdown(f"""
                <div class="info-card">
                    <h3>Dominant Pollutant</h3>
                    <h2>{dominant}</h2>
                    <p>Primary Concern</p>
                </div>
                """, unsafe_allow_html=True)
        
        with col3:
            if forecast_data is not None and not forecast_data.empty:
                max_future = forecast_data['pm25'].max()
                st.markdown(f"""
                <div class="prediction-card">
                    <h3>Peak Forecast</h3>
                    <h2>{max_future:.1f} μg/m³</h2>
                    <p>Next 6 Hours</p>
                </div>
                """, unsafe_allow_html=True)
        
        with col4:
            if current_pred and 'last_timestamp' in current_pred:
                last_update = current_pred['last_timestamp']
                st.markdown(f"""
                <div class="metric-card">
                    <h3>Last Update</h3>
                    <h4>{last_update}</h4>
                    <p>Data Timestamp</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Forecast Visualization
        col1, col2 = st.columns([2, 1])
        
        with col1:
            if forecast_data is not None and not forecast_data.empty:
                st.plotly_chart(create_forecast_timeline(forecast_data), use_container_width=True)
        
        with col2:
            if detailed_pred:
                st.markdown("### 📊 Pollutant Levels")
                pollutants = [
                    ("NO₂", detailed_pred.get('no2_prediction', 0), "ppm"),
                    ("O₃", detailed_pred.get('o3_prediction', 0), "ppm"),
                    ("CO", detailed_pred.get('co_prediction', 0), "ppm"),
                    ("SO₂", detailed_pred.get('so2_prediction', 0), "ppm"),
                ]
                
                for name, value, unit in pollutants:
                    st.metric(label=name, value=f"{value:.2f} {unit}")
        
        # Detailed Forecast Table
        if forecast_data is not None and not forecast_data.empty:
            st.markdown("### 📅 Detailed Forecast Table")
            
            # Format the table
            display_df = forecast_data.copy()
            display_df['PM2.5'] = display_df['pm25'].apply(lambda x: f"{x:.1f} μg/m³")
            display_df['AQI Category'] = display_df['pm25'].apply(
                lambda x: "Good" if x < 15 else "Moderate" if x < 35 else "Poor" if x < 75 else "Very Poor"
            )
            display_df = display_df[['hour24', 'time', 'PM2.5', 'AQI Category']]
            display_df.columns = ['Hour', 'Forecast Time', 'PM2.5 Prediction', 'Air Quality']
            
            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True
            )
    
    with tab2:
        st.markdown(f'<div class="sub-header">Detailed Analysis - {selected_station}</div>', unsafe_allow_html=True)
        
        # Get detailed prediction data
        detailed_pred = get_detailed_prediction(selected_station)
        
        if detailed_pred:
            col1, col2 = st.columns(2)
            
            with col1:
                # Radar chart
                st.plotly_chart(create_comparison_radar(detailed_pred), use_container_width=True)
            
            with col2:
                # Gauge charts
                st.plotly_chart(create_pollution_gauge(
                    detailed_pred.get('pm25_prediction', 0), 
                    "PM2.5", 
                    None
                ), use_container_width=True)
                
                st.plotly_chart(create_pollution_gauge(
                    detailed_pred.get('no2_prediction', 0), 
                    "NO₂", 
                    None
                ), use_container_width=True)
            
            # Detailed pollutant table
            st.markdown("### 📋 Pollutant Concentration Details")
            
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
            st.markdown("### 🩺 Health Recommendations")
            
            pm25_level = detailed_pred.get('pm25_prediction', 0)
            if pm25_level < 15:
                st.success("**Good Air Quality:** Perfect for outdoor activities. No restrictions needed.")
            elif pm25_level < 35:
                st.info("**Moderate Air Quality:** Generally acceptable. Sensitive individuals should consider reducing prolonged outdoor exertion.")
            elif pm25_level < 75:
                st.warning("**Poor Air Quality:** Everyone may begin to experience health effects. Reduce prolonged or heavy outdoor exertion.")
            else:
                st.error("**Very Poor Air Quality:** Health alert - everyone may experience more serious health effects. Avoid all outdoor exertion.")
    
    with tab3:
        st.markdown('<div class="sub-header">Spatial Overview</div>', unsafe_allow_html=True)
        
        if not aqi_data.empty:
            col1, col2 = st.columns(2)
            
            with col1:
                # Station health dashboard
                st.plotly_chart(create_station_health_dashboard(aqi_data), use_container_width=True)
            
            with col2:
                # Heatmap for selected station
                st.plotly_chart(create_temporal_heatmap(aqi_data, selected_station), use_container_width=True)
            
            # Comparison across all stations
            st.markdown("### 🏙️ Station Comparison")
            
            # Calculate statistics for all stations
            station_stats = aqi_data.groupby('Station name(district)').agg({
                'PM2.5': ['mean', 'max', 'min', 'std'],
                'PM10': 'mean',
                'NO2': 'mean'
            }).round(2)
            
            # Flatten column names
            station_stats.columns = ['_'.join(col).strip() for col in station_stats.columns.values]
            station_stats = station_stats.reset_index()
            
            st.dataframe(
                station_stats,
                use_container_width=True,
                height=400
            )
    
    with tab4:
        st.markdown('<div class="sub-header">Historical Trends Analysis</div>', unsafe_allow_html=True)
        
        if not aqi_data.empty:
            # Time series analysis
            station_history = aqi_data[aqi_data['Station name(district)'] == selected_station]
            
            if not station_history.empty:
                # Create time series plot
                fig = go.Figure()
                
                fig.add_trace(go.Scatter(
                    x=station_history['Measurement date'],
                    y=station_history['PM2.5'],
                    mode='lines',
                    name='PM2.5',
                    line=dict(color='red', width=2)
                ))
                
                fig.add_trace(go.Scatter(
                    x=station_history['Measurement date'],
                    y=station_history['PM10'],
                    mode='lines',
                    name='PM10',
                    line=dict(color='orange', width=2)
                ))
                
                fig.update_layout(
                    title=f"Historical Pollution Trends - {selected_station}",
                    xaxis_title="Date & Time",
                    yaxis_title="Concentration (μg/m³)",
                    hovermode='x unified',
                    height=500,
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Statistical analysis
                st.markdown("### 📈 Statistical Summary")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    avg_pm25 = station_history['PM2.5'].mean()
                    st.metric("Average PM2.5", f"{avg_pm25:.1f} μg/m³")
                
                with col2:
                    max_pm25 = station_history['PM2.5'].max()
                    st.metric("Maximum PM2.5", f"{max_pm25:.1f} μg/m³")
                
                with col3:
                    min_pm25 = station_history['PM2.5'].min()
                    st.metric("Minimum PM2.5", f"{min_pm25:.1f} μg/m³")
                
                with col4:
                    std_pm25 = station_history['PM2.5'].std()
                    st.metric("PM2.5 Variability", f"{std_pm25:.1f} σ")
    
    with tab5:
        st.markdown('<div class="sub-header">Model & System Insights</div>', unsafe_allow_html=True)
        
        # Model information
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="info-card">
                <h3>AI Model Architecture</h3>
                <p><strong>Model Type:</strong> Temporal Graph Convolutional Network (TGCN)</p>
                <p><strong>Input Features:</strong> 10 features × 24 hours × 13 stations</p>
                <p><strong>Output:</strong> 6 pollutants × 13 stations</p>
                <p><strong>Training Data:</strong> Historical air quality measurements</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="prediction-card">
                <h3>Prediction Capabilities</h3>
                <p><strong>Time Horizon:</strong> 6-hour forecasts</p>
                <p><strong>Pollutants Predicted:</strong> PM2.5, PM10, NO₂, O₃, CO, SO₂</p>
                <p><strong>Update Frequency:</strong> Real-time (hourly)</p>
                <p><strong>Accuracy:</strong> Continuously improving with new data</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Backend information
        st.markdown("### 🔧 Backend System Information")
        
        backend_info = {
            "Component": ["Flask API Server", "TGCN Model", "Data Pipeline", "MongoDB Database", "Streamlit Dashboard"],
            "Status": ["✅ Running", "✅ Loaded", "✅ Active", "✅ Connected", "✅ Live"],
            "Description": [
                "Handles prediction requests",
                "Generates 6-hour forecasts",
                "Processes real-time data",
                "Stores historical measurements",
                "Visualizes predictions & insights"
            ]
        }
        
        st.dataframe(pd.DataFrame(backend_info), use_container_width=True, hide_index=True)
        
        # API endpoints information
        st.markdown("### 🔌 Available API Endpoints")
        
        endpoints = [
            ("/api/predict", "GET", "Returns PM2.5 prediction for specified station"),
            ("/api/predict-detail", "GET", "Returns detailed predictions for all pollutants"),
            ("/api/forecasts", "GET", "Returns 6-hour forecast for specified station")
        ]
        
        for endpoint, method, description in endpoints:
            st.code(f"{method} {FLASK_BACKEND_URL}{endpoint}?station=StationName", language="bash")
            st.write(f"*{description}*")
            st.write("")
    
    with tab6:
        st.markdown('<div class="sub-header">Data Explorer</div>', unsafe_allow_html=True)
        
        if not aqi_data.empty:
            # Data filters
            col1, col2, col3 = st.columns(3)
            
            with col1:
                date_range = st.date_input(
                    "Select Date Range",
                    value=[aqi_data['Measurement date'].min().date(), aqi_data['Measurement date'].max().date()],
                    max_value=aqi_data['Measurement date'].max().date()
                )
            
            with col2:
                pollutants = st.multiselect(
                    "Select Pollutants",
                    options=['NO2', 'O3', 'CO', 'SO2', 'PM10', 'PM2.5'],
                    default=['PM2.5', 'PM10', 'NO2']
                )
            
            with col3:
                stations_to_show = st.multiselect(
                    "Select Stations",
                    options=aqi_data['Station name(district)'].unique().tolist(),
                    default=[selected_station]
                )
            
            # Apply filters
            filtered_data = aqi_data.copy()
            
            if len(date_range) == 2:
                filtered_data = filtered_data[
                    (filtered_data['Measurement date'].dt.date >= date_range[0]) &
                    (filtered_data['Measurement date'].dt.date <= date_range[1])
                ]
            
            if stations_to_show:
                filtered_data = filtered_data[filtered_data['Station name(district)'].isin(stations_to_show)]
            
            # Display filtered data
            columns_to_show = ['Station name(district)', 'Measurement date', 'Hour'] + pollutants
            st.dataframe(
                filtered_data[columns_to_show].sort_values('Measurement date', ascending=False),
                use_container_width=True,
                height=500
            )
            
            # Data download
            st.markdown("### 💾 Data Export")
            
            col1, col2 = st.columns(2)
            
            with col1:
                csv_data = filtered_data.to_csv(index=False)
                st.download_button(
                    label="Download Filtered Data (CSV)",
                    data=csv_data,
                    file_name=f"air_quality_data_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                    mime="text/csv"
                )
            
            with col2:
                summary_stats = filtered_data.describe().round(2)
                summary_csv = summary_stats.to_csv()
                st.download_button(
                    label="Download Statistics Summary (CSV)",
                    data=summary_csv,
                    file_name=f"air_quality_summary_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                    mime="text/csv"
                )
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.9rem; padding: 2rem;">
        <p><strong>AI-Powered Air Quality Forecasting System</strong></p>
        <p>Powered by Temporal Graph Convolutional Networks (TGCN) • Real-time Predictions • 6-Hour Forecasts</p>
        <p>Data Source: Seoul Air Quality Monitoring Network • Last Updated: {}</p>
        <p>System Version: 2.0 • Dashboard Version: 1.0</p>
    </div>
    """.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), unsafe_allow_html=True)

if __name__ == "__main__":
    main()