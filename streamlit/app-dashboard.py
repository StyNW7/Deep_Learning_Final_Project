import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set page configuration
st.set_page_config(
    page_title="Air Quality Monitoring Dashboard",
    page_icon="🌫️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 700;
    }
    .sub-header {
        font-size: 1.8rem;
        color: #2c3e50;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    .card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
        color: black;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: black;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
    }
    .station-card {
        background-color: #ffffff;
        border-left: 5px solid #3498db;
        border-radius: 5px;
        padding: 1rem;
        margin-bottom: 0.5rem;
        color: black;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    # Load AQI data
    aqi_data = pd.read_csv('../backend/aqi_data_sorted.csv')
    aqi_data['Measurement date'] = pd.to_datetime(aqi_data['Measurement date'])
    aqi_data['Hour'] = aqi_data['Measurement date'].dt.hour
    aqi_data['Date'] = aqi_data['Measurement date'].dt.date
    
    # Load station info
    station_info = pd.read_csv('../backend/Measurement_station_info.csv')
    
    # Load item info
    item_info = pd.read_csv('../backend/Measurement_item_info.csv')
    
    # Merge station names into AQI data
    aqi_data = pd.merge(aqi_data, station_info[['Station code', 'Station name(district)']], 
                       on='Station code', how='left')
    
    return aqi_data, station_info, item_info

def create_summary_metrics(aqi_data):
    """Create summary metrics cards"""
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

def create_temporal_analysis(aqi_data):
    """Create temporal analysis visualizations"""
    st.markdown('<div class="sub-header">Temporal Analysis</div>', unsafe_allow_html=True)
    
    # Hourly trends
    hourly_avg = aqi_data.groupby('Hour').agg({
        'PM2.5': 'mean',
        'PM10': 'mean',
        'NO2': 'mean',
        'O3': 'mean'
    }).reset_index()
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('PM2.5 Hourly Trend', 'PM10 Hourly Trend', 
                       'NO2 Hourly Trend', 'O3 Hourly Trend'),
        vertical_spacing=0.15
    )
    
    # PM2.5
    fig.add_trace(
        go.Scatter(x=hourly_avg['Hour'], y=hourly_avg['PM2.5'], 
                  mode='lines+markers', name='PM2.5', line=dict(color='red')),
        row=1, col=1
    )
    
    # PM10
    fig.add_trace(
        go.Scatter(x=hourly_avg['Hour'], y=hourly_avg['PM10'], 
                  mode='lines+markers', name='PM10', line=dict(color='orange')),
        row=1, col=2
    )
    
    # NO2
    fig.add_trace(
        go.Scatter(x=hourly_avg['Hour'], y=hourly_avg['NO2'], 
                  mode='lines+markers', name='NO2', line=dict(color='blue')),
        row=2, col=1
    )
    
    # O3
    fig.add_trace(
        go.Scatter(x=hourly_avg['Hour'], y=hourly_avg['O3'], 
                  mode='lines+markers', name='O3', line=dict(color='green')),
        row=2, col=2
    )
    
    fig.update_layout(height=600, showlegend=False, title_text="Hourly Air Quality Trends")
    fig.update_xaxes(title_text="Hour of Day")
    fig.update_yaxes(title_text="Concentration")
    
    st.plotly_chart(fig, use_container_width=True)

def create_spatial_analysis(aqi_data, station_info):
    """Create spatial analysis visualizations"""
    st.markdown('<div class="sub-header">Spatial Analysis</div>', unsafe_allow_html=True)
    
    # Calculate station-wise averages
    station_avg = aqi_data.groupby(['Station code', 'Station name(district)']).agg({
        'PM2.5': 'mean',
        'PM10': 'mean',
        'NO2': 'mean',
        'O3': 'mean',
        'CO': 'mean',
        'SO2': 'mean'
    }).reset_index()
    
    # Merge with location data
    station_avg = pd.merge(station_avg, station_info[['Station code', 'Latitude', 'Longitude']], 
                          on='Station code', how='left')
    
    # Create map visualization
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Interactive map for PM2.5
        fig = px.scatter_mapbox(
            station_avg,
            lat="Latitude",
            lon="Longitude",
            size="PM2.5",
            color="PM2.5",
            hover_name="Station name(district)",
            hover_data=["PM10", "NO2", "O3"],
            color_continuous_scale=px.colors.sequential.Reds,
            size_max=30,
            zoom=10,
            height=500,
            title="PM2.5 Concentration by Station"
        )
        fig.update_layout(mapbox_style="carto-positron")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Top 5 most polluted stations
        st.markdown("**Top 5 Stations by PM2.5**")
        top_stations = station_avg.nlargest(5, 'PM2.5')[['Station name(district)', 'PM2.5']]
        
        for idx, row in top_stations.iterrows():
            with st.container():
                st.markdown(f"""
                <div class="station-card">
                    <strong>{row['Station name(district)']}</strong><br>
                    PM2.5: {row['PM2.5']:.1f} μg/m³
                </div>
                """, unsafe_allow_html=True)

def create_pollutant_correlation(aqi_data):
    """Create pollutant correlation analysis"""
    st.markdown('<div class="sub-header">Pollutant Correlations</div>', unsafe_allow_html=True)
    
    # Calculate correlation matrix
    pollutants = ['NO2', 'O3', 'CO', 'SO2', 'PM10', 'PM2.5']
    correlation_matrix = aqi_data[pollutants].corr()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Heatmap
        fig = px.imshow(
            correlation_matrix,
            text_auto='.2f',
            aspect="auto",
            color_continuous_scale='RdBu',
            title="Pollutant Correlation Matrix"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Key insights from correlations
        st.markdown("**Key Insights:**")
        
        # Find strongest correlations
        corr_values = correlation_matrix.unstack().sort_values(ascending=False)
        corr_values = corr_values[corr_values < 0.99]  # Remove self-correlations
        
        top_corr = corr_values.head(3)
        bottom_corr = corr_values.tail(3)
        
        st.markdown("**Strongest Positive Correlations:**")
        for idx, value in top_corr.items():
            pollutant1, pollutant2 = idx
            st.write(f"{pollutant1} - {pollutant2}: {value:.3f}")
        
        st.markdown("**Strongest Negative Correlations:**")
        for idx, value in bottom_corr.items():
            pollutant1, pollutant2 = idx
            st.write(f"{pollutant1} - {pollutant2}: {value:.3f}")

def create_station_comparison(aqi_data):
    """Create station comparison dashboard"""
    st.markdown('<div class="sub-header">Station Comparison</div>', unsafe_allow_html=True)
    
    # Get unique stations
    stations = aqi_data['Station name(district)'].unique()
    
    # Multi-select for stations
    selected_stations = st.multiselect(
        "Select stations to compare:",
        options=stations,
        default=stations[:3] if len(stations) >= 3 else stations
    )
    
    if selected_stations:
        filtered_data = aqi_data[aqi_data['Station name(district)'].isin(selected_stations)]
        
        # Create comparison chart
        fig = px.box(
            filtered_data,
            x='Station name(district)',
            y='PM2.5',
            color='Station name(district)',
            points='all',
            title="PM2.5 Distribution by Station"
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        
        # Create detailed comparison table
        station_stats = filtered_data.groupby('Station name(district)').agg({
            'PM2.5': ['mean', 'std', 'max', 'min'],
            'PM10': ['mean', 'std'],
            'NO2': ['mean'],
            'O3': ['mean']
        }).round(2)
        
        st.dataframe(station_stats, use_container_width=True)

def create_air_quality_index(aqi_data, item_info):
    """Calculate and display AQI scores"""
    st.markdown('<div class="sub-header">Air Quality Index (AQI) Analysis</div>', unsafe_allow_html=True)
    
    # Define AQI calculation function
    def calculate_aqi(pollutant, value):
        thresholds = {
            'PM2.5': [(0, 15), (16, 35), (36, 75), (76, 500)],
            'PM10': [(0, 30), (31, 80), (81, 150), (151, 600)],
            'NO2': [(0, 0.03), (0.031, 0.06), (0.061, 0.2), (0.201, 2.0)],
            'O3': [(0, 0.03), (0.031, 0.09), (0.091, 0.15), (0.151, 0.5)],
            'CO': [(0, 2), (2.1, 9), (9.1, 15), (15.1, 50)],
            'SO2': [(0, 0.02), (0.021, 0.05), (0.051, 0.15), (0.151, 1.0)]
        }
        
        aqi_categories = ['Good', 'Moderate', 'Poor', 'Very Poor']
        
        if pollutant in thresholds:
            for i, (low, high) in enumerate(thresholds[pollutant]):
                if value <= high:
                    return aqi_categories[i]
        return 'Very Poor'
    
    # Calculate AQI for each row
    aqi_data['PM2.5_AQI'] = aqi_data['PM2.5'].apply(lambda x: calculate_aqi('PM2.5', x))
    aqi_data['PM10_AQI'] = aqi_data['PM10'].apply(lambda x: calculate_aqi('PM10', x))
    
    # AQI distribution
    col1, col2 = st.columns(2)
    
    with col1:
        pm25_dist = aqi_data['PM2.5_AQI'].value_counts()
        fig1 = px.pie(
            values=pm25_dist.values,
            names=pm25_dist.index,
            title="PM2.5 AQI Distribution",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        pm10_dist = aqi_data['PM10_AQI'].value_counts()
        fig2 = px.bar(
            x=pm10_dist.index,
            y=pm10_dist.values,
            title="PM10 AQI Distribution",
            color=pm10_dist.values,
            color_continuous_scale='Viridis'
        )
        st.plotly_chart(fig2, use_container_width=True)

def create_data_table(aqi_data):
    """Display raw data table with filters"""
    st.markdown('<div class="sub-header">Raw Data Explorer</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        selected_stations = st.multiselect(
            "Filter by Station:",
            options=aqi_data['Station name(district)'].unique(),
            default=[]
        )
    
    with col2:
        hour_range = st.slider(
            "Select Hour Range:",
            min_value=0,
            max_value=23,
            value=(0, 23)
        )
    
    with col3:
        pollutants = st.multiselect(
            "Select Pollutants to Display:",
            options=['NO2', 'O3', 'CO', 'SO2', 'PM10', 'PM2.5'],
            default=['PM2.5', 'PM10', 'NO2']
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

def main():
    # Load data
    aqi_data, station_info, item_info = load_data()
    
    # Header
    st.markdown('<h1 class="main-header">Air Quality Monitoring Dashboard</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Create tabs for different sections
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Overview", 
        "Temporal Analysis", 
        "Spatial Analysis", 
        "Pollutant Analysis",
        "Data Explorer"
    ])
    
    with tab1:
        st.markdown('<div class="sub-header">Dashboard Overview</div>', unsafe_allow_html=True)
        
        # Summary metrics
        create_summary_metrics(aqi_data)
        
        # Quick insights
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Key Statistics")
            stats_data = {
                'Metric': ['Total Records', 'Data Collection Period', 
                          'Average Temperature', 'Highest PM2.5', 'Lowest PM2.5'],
                'Value': [
                    f"{len(aqi_data):,}",
                    f"{aqi_data['Date'].min()} to {aqi_data['Date'].max()}",
                    "N/A",
                    f"{aqi_data['PM2.5'].max():.1f} μg/m³",
                    f"{aqi_data['PM2.5'].min():.1f} μg/m³"
                ]
            }
            st.dataframe(pd.DataFrame(stats_data), use_container_width=True, hide_index=True)
        
        with col2:
            st.markdown("### Data Quality")
            completeness = (1 - aqi_data.isnull().mean()) * 100
            fig = px.bar(
                x=completeness.index,
                y=completeness.values,
                title="Data Completeness by Pollutant",
                labels={'x': 'Pollutant', 'y': 'Completeness (%)'},
                color=completeness.values,
                color_continuous_scale='Blues'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        create_temporal_analysis(aqi_data)
        
        # Additional temporal insights
        col1, col2 = st.columns(2)
        
        with col1:
            # Daily pattern
            daily_pattern = aqi_data.groupby('Hour').agg({'PM2.5': 'mean'}).reset_index()
            fig = px.area(daily_pattern, x='Hour', y='PM2.5', 
                         title="Daily PM2.5 Pattern", 
                         line_shape='spline')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Peak pollution hours
            peak_hours = aqi_data.groupby('Hour')['PM2.5'].mean().nlargest(3)
            st.markdown("**Peak Pollution Hours (PM2.5):**")
            for hour, value in peak_hours.items():
                st.write(f"Hour {hour:02d}:00 - {value:.1f} μg/m³")
    
    with tab3:
        create_spatial_analysis(aqi_data, station_info)
        
        # Station ranking
        st.markdown("### Station Ranking by Pollution Level")
        
        pollutant_to_rank = st.selectbox(
            "Rank by Pollutant:",
            options=['PM2.5', 'PM10', 'NO2', 'O3', 'CO', 'SO2']
        )
        
        station_ranking = aqi_data.groupby('Station name(district)')[pollutant_to_rank].mean().sort_values(ascending=False)
        
        fig = px.bar(
            x=station_ranking.values,
            y=station_ranking.index,
            orientation='h',
            title=f"Station Ranking by {pollutant_to_rank}",
            color=station_ranking.values,
            color_continuous_scale='thermal'
        )
        fig.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        create_pollutant_correlation(aqi_data)
        
        # Pollutant distribution
        st.markdown("### Pollutant Distribution Analysis")
        
        pollutant = st.selectbox(
            "Select Pollutant for Distribution:",
            options=['PM2.5', 'PM10', 'NO2', 'O3', 'CO', 'SO2']
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.histogram(
                aqi_data,
                x=pollutant,
                nbins=30,
                title=f"{pollutant} Distribution",
                marginal="box"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            stats = aqi_data[pollutant].describe()
            st.markdown(f"**{pollutant} Statistics:**")
            for stat, value in stats.items():
                st.write(f"{stat}: {value:.2f}")
            
            # Outlier detection
            Q1 = aqi_data[pollutant].quantile(0.25)
            Q3 = aqi_data[pollutant].quantile(0.75)
            IQR = Q3 - Q1
            outliers = ((aqi_data[pollutant] < (Q1 - 1.5 * IQR)) | 
                       (aqi_data[pollutant] > (Q3 + 1.5 * IQR))).sum()
            st.write(f"Outliers detected: {outliers} ({outliers/len(aqi_data)*100:.1f}%)")
    
    with tab5:
        create_data_table(aqi_data)
        
        # Data download option
        st.markdown("### Data Export")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Convert to CSV for download
            csv = aqi_data.to_csv(index=False)
            st.download_button(
                label="Download Full Dataset (CSV)",
                data=csv,
                file_name="air_quality_data.csv",
                mime="text/csv"
            )
        
        with col2:
            # Summary statistics download
            summary_stats = aqi_data.describe().round(2)
            summary_csv = summary_stats.to_csv()
            st.download_button(
                label="Download Summary Statistics (CSV)",
                data=summary_csv,
                file_name="air_quality_summary.csv",
                mime="text/csv"
            )
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.9rem;">
        Air Quality Monitoring Dashboard | Data Source: Seoul Air Quality Monitoring Network
        <br>Last Updated: December 2025 | Dashboard Version 1.0
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()