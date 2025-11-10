import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
import os
from datetime import datetime
import folium
from streamlit_folium import st_folium

# Set page config to match the React dashboard design
st.set_page_config(
    page_title="Urban Mobility Dashboard",
    page_icon="🚕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS to replicate React dashboard styling
st.markdown("""
<style>
    .stApp {
        background-color: #f5f7fa;
    }
    .main-header {
        font-size: 2rem;
        font-weight: 600;
        color: #1a1a1a;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: white;
        border-radius: 8px;
        padding: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .metric-title {
        font-size: 1rem;
        color: #666;
        margin: 0;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #1a1a1a;
        margin: 0;
    }
    .chart-container {
        background-color: white;
        border-radius: 8px;
        padding: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .chart-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #1a1a1a;
        margin-bottom: 1rem;
    }
    .sidebar .sidebar-content {
        background-color: #2c3e50;
    }
    .css-1d391kg {
        background-color: #2c3e50;
    }
</style>
""", unsafe_allow_html=True)

# Function to format large numbers (replicating React dashboard functionality)
def format_number(num):
    if num >= 1000000:
        return f"{num/1000000:.1f}M"
    if num >= 1000:
        return f"{num/1000:.1f}K"
    return str(num)

# Sidebar navigation (replicating React sidebar)
with st.sidebar:
    st.title("🧭 Navigation")
    page = st.selectbox(
        "Select Dashboard",
        ["Dashboard", "Analytics", "Maps", "Predictive", "Real-Time"]
    )
    
    st.markdown("---")
    st.subheader("⚙️ Settings")
    st.checkbox("Auto-refresh", value=True)
    refresh_interval = st.slider("Refresh interval (seconds)", 5, 60, 30)

# Main Dashboard Page
if page == "Dashboard":
    st.markdown('<h1 class="main-header">Urban Mobility Dashboard</h1>', unsafe_allow_html=True)
    
    # Key Metrics Cards (replicating React dashboard)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-title">Total Trips</p>
            <p class="metric-value">{format_number(1250000)}</p>
            <p>All time trips</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-title">Average Fare</p>
            <p class="metric-value">$18.75</p>
            <p>Per trip</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-title">Total Revenue</p>
            <p class="metric-value">${format_number(23450000)}</p>
            <p>All time revenue</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-title">Avg Trip Distance</p>
            <p class="metric-value">3.2 mi</p>
            <p>Per trip</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Charts Section
    # Trip Volume by Hour (Area Chart)
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<h3 class="chart-title">Trip Volume by Hour</h3>', unsafe_allow_html=True)
    
    trip_stats = pd.DataFrame([
        {"hour": "00:00", "trips": 1200},
        {"hour": "04:00", "trips": 800},
        {"hour": "08:00", "trips": 4200},
        {"hour": "12:00", "trips": 3800},
        {"hour": "16:00", "trips": 5200},
        {"hour": "20:00", "trips": 3200}
    ])
    
    fig_area = px.area(trip_stats, x="hour", y="trips", 
                       template="plotly_white")
    fig_area.update_traces(fillcolor='rgba(136, 132, 216, 0.3)', 
                          line_color='#8884d8', line_width=3)
    fig_area.update_layout(
        xaxis_title="Hour",
        yaxis_title="Trips",
        height=400
    )
    st.plotly_chart(fig_area, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Two-column layout for Payment Types and other charts
    col1, col2 = st.columns(2)
    
    # Payment Types Distribution (Pie Chart)
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<h3 class="chart-title">Payment Types</h3>', unsafe_allow_html=True)
        
        payment_types = pd.DataFrame([
            {"name": "Credit Card", "value": 65},
            {"name": "Cash", "value": 30},
            {"name": "Digital", "value": 5}
        ])
        
        fig_pie = px.pie(payment_types, values='value', names='name',
                         color_discrete_sequence=['#0088FE', '#00C49F', '#FFBB28'],
                         template="plotly_white")
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Zone Performance (Bar Chart)
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<h3 class="chart-title">Zone Performance</h3>', unsafe_allow_html=True)
        
        zone_performance = pd.DataFrame([
            {"zone": "Manhattan", "trips": 450000, "revenue": 8500000},
            {"zone": "Brooklyn", "trips": 280000, "revenue": 5200000},
            {"zone": "Queens", "trips": 190000, "revenue": 3500000},
            {"zone": "Bronx", "trips": 150000, "revenue": 2800000},
            {"zone": "Staten Island", "trips": 80000, "revenue": 1500000}
        ])
        
        # Create subplot with secondary y-axis
        fig_bar = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Add trips bar
        fig_bar.add_trace(
            go.Bar(x=zone_performance['zone'], y=zone_performance['trips'], 
                   name='Trips', marker_color='#8884d8'),
            secondary_y=False,
        )
        
        # Add revenue bar
        fig_bar.add_trace(
            go.Bar(x=zone_performance['zone'], y=zone_performance['revenue'], 
                   name='Revenue', marker_color='#82ca9d'),
            secondary_y=True,
        )
        
        # Set axis titles
        fig_bar.update_xaxes(title_text="Zone")
        fig_bar.update_yaxes(title_text="Trips", secondary_y=False, 
                            tickformat=",.0f")
        fig_bar.update_yaxes(title_text="Revenue ($)", secondary_y=True, 
                            tickprefix="$", tickformat=",.0f")
        
        fig_bar.update_layout(
            template="plotly_white",
            height=400,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        st.plotly_chart(fig_bar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Weekly Trend (Line Chart)
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<h3 class="chart-title">Weekly Trend</h3>', unsafe_allow_html=True)
    
    trend_data = pd.DataFrame([
        {"day": "Mon", "trips": 180000, "revenue": 3400000},
        {"day": "Tue", "trips": 195000, "revenue": 3650000},
        {"day": "Wed", "trips": 210000, "revenue": 3950000},
        {"day": "Thu", "trips": 225000, "revenue": 4200000},
        {"day": "Fri", "trips": 240000, "revenue": 4500000},
        {"day": "Sat", "trips": 160000, "revenue": 3000000},
        {"day": "Sun", "trips": 140000, "revenue": 2600000}
    ])
    
    # Create subplot with secondary y-axis
    fig_line = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Add trips line
    fig_line.add_trace(
        go.Scatter(x=trend_data['day'], y=trend_data['trips'], 
                   mode='lines+markers', name='Trips', line=dict(color='#8884d8', width=3)),
        secondary_y=False,
    )
    
    # Add revenue line
    fig_line.add_trace(
        go.Scatter(x=trend_data['day'], y=trend_data['revenue'], 
                   mode='lines+markers', name='Revenue', line=dict(color='#82ca9d', width=3)),
        secondary_y=True,
    )
    
    # Set axis titles
    fig_line.update_xaxes(title_text="Day")
    fig_line.update_yaxes(title_text="Trips", secondary_y=False, 
                         tickformat=",.0f")
    fig_line.update_yaxes(title_text="Revenue ($)", secondary_y=True, 
                         tickprefix="$", tickformat=",.0f")
    
    fig_line.update_layout(
        template="plotly_white",
        height=400,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig_line, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Analytics Page
elif page == "Analytics":
    st.markdown('<h1 class="main-header">Advanced Analytics</h1>', unsafe_allow_html=True)
    
    # Trip Distribution by Day and Service (Bar Chart)
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<h3 class="chart-title">Trip Distribution by Day and Service</h3>', unsafe_allow_html=True)
    
    trip_distribution = pd.DataFrame([
        {"day": "Monday", "yellow": 4000, "green": 2500, "uber": 3500},
        {"day": "Tuesday", "yellow": 4200, "green": 2600, "uber": 3700},
        {"day": "Wednesday", "yellow": 4500, "green": 2800, "uber": 4000},
        {"day": "Thursday", "yellow": 4700, "green": 3000, "uber": 4200},
        {"day": "Friday", "yellow": 5000, "green": 3200, "uber": 4500},
        {"day": "Saturday", "yellow": 3500, "green": 2200, "uber": 3000},
        {"day": "Sunday", "yellow": 3000, "green": 2000, "uber": 2500}
    ])
    
    fig_trip_dist = go.Figure(data=[
        go.Bar(name='Yellow Taxi', x=trip_distribution['day'], y=trip_distribution['yellow'], marker_color='#FFD700'),
        go.Bar(name='Green Taxi', x=trip_distribution['day'], y=trip_distribution['green'], marker_color='#32CD32'),
        go.Bar(name='Uber', x=trip_distribution['day'], y=trip_distribution['uber'], marker_color='#000000')
    ])
    
    fig_trip_dist.update_layout(
        barmode='group',
        template="plotly_white",
        height=400,
        xaxis_title="Day",
        yaxis_title="Trips",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig_trip_dist, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Two-column layout for Fare Analysis and Speed Analysis
    col1, col2 = st.columns(2)
    
    # Fare Analysis (Pie Chart)
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<h3 class="chart-title">Fare Distribution</h3>', unsafe_allow_html=True)
        
        fare_analysis = pd.DataFrame([
            {"range": "< $10", "count": 15000},
            {"range": "$10-20", "count": 35000},
            {"range": "$20-30", "count": 25000},
            {"range": "$30-50", "count": 18000},
            {"range": "> $50", "count": 7000}
        ])
        
        fig_fare = px.pie(fare_analysis, values='count', names='range',
                          color_discrete_sequence=['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8'],
                          template="plotly_white")
        fig_fare.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_fare, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Speed Analysis (Line Chart)
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<h3 class="chart-title">Average Speed by Hour</h3>', unsafe_allow_html=True)
        
        speed_analysis = pd.DataFrame([
            {"hour": "00:00", "speed": 15.2},
            {"hour": "04:00", "speed": 18.5},
            {"hour": "08:00", "speed": 8.7},
            {"hour": "12:00", "speed": 12.3},
            {"hour": "16:00", "speed": 9.8},
            {"hour": "20:00", "speed": 14.1}
        ])
        
        fig_speed = px.line(speed_analysis, x="hour", y="speed",
                            markers=True, template="plotly_white")
        fig_speed.update_traces(line_color='#8884d8', line_width=3,
                                marker=dict(size=8, color='#8884d8'))
        fig_speed.update_layout(
            height=400,
            xaxis_title="Hour",
            yaxis_title="Speed (mph)",
            yaxis=dict(range=[0, 20])
        )
        
        st.plotly_chart(fig_speed, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Passenger Demand Heatmap (Radar Chart)
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<h3 class="chart-title">Passenger Demand by Location</h3>', unsafe_allow_html=True)
    
    passenger_demand = pd.DataFrame([
        {"location": "Times Square", "demand": 95},
        {"location": "Penn Station", "demand": 88},
        {"location": "Union Square", "demand": 82},
        {"location": "Brooklyn Bridge", "demand": 75},
        {"location": "Central Park", "demand": 70},
        {"location": "Wall Street", "demand": 85},
        {"location": "LaGuardia", "demand": 65},
        {"location": "JFK Airport", "demand": 60}
    ])
    
    fig_radar = go.Figure()
    
    fig_radar.add_trace(go.Scatterpolar(
        r=passenger_demand['demand'],
        theta=passenger_demand['location'],
        fill='toself',
        name='Demand',
        fillcolor='rgba(136, 132, 216, 0.6)',
        line_color='#8884d8'
    ))
    
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=False,
        template="plotly_white",
        height=500
    )
    
    st.plotly_chart(fig_radar, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Two-column layout for Trip Duration and Weather Correlation
    col1, col2 = st.columns(2)
    
    # Trip Duration Distribution (Horizontal Bar Chart)
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<h3 class="chart-title">Trip Duration Distribution</h3>', unsafe_allow_html=True)
        
        trip_duration = pd.DataFrame([
            {"duration": "< 5 min", "percentage": 15},
            {"duration": "5-15 min", "percentage": 45},
            {"duration": "15-30 min", "percentage": 25},
            {"duration": "30-60 min", "percentage": 10},
            {"duration": "> 60 min", "percentage": 5}
        ])
        
        fig_duration = px.bar(trip_duration, x="percentage", y="duration",
                              orientation='h', template="plotly_white",
                              color_discrete_sequence=['#82ca9d'])
        fig_duration.update_layout(
            height=400,
            xaxis_title="Percentage (%)",
            yaxis_title="Duration",
            xaxis=dict(range=[0, 50])
        )
        
        st.plotly_chart(fig_duration, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Temperature vs Trip Volume (Scatter Chart)
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<h3 class="chart-title">Temperature vs Trip Volume</h3>', unsafe_allow_html=True)
        
        correlation_data = pd.DataFrame([
            {"temp": 32, "trips": 2800},
            {"temp": 45, "trips": 3200},
            {"temp": 55, "trips": 3800},
            {"temp": 65, "trips": 4500},
            {"temp": 75, "trips": 5200},
            {"temp": 85, "trips": 4800},
            {"temp": 95, "trips": 4200}
        ])
        
        fig_correlation = px.scatter(correlation_data, x="temp", y="trips",
                                     trendline="ols", template="plotly_white",
                                     color_discrete_sequence=['#8884d8'])
        fig_correlation.update_layout(
            height=400,
            xaxis_title="Temperature (°F)",
            yaxis_title="Trips",
            yaxis=dict(tickformat=",.0f")
        )
        fig_correlation.update_traces(marker=dict(size=10))
        
        st.plotly_chart(fig_correlation, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# Maps Page
elif page == "Maps":
    st.markdown('<h1 class="main-header">Geospatial Analytics</h1>', unsafe_allow_html=True)
    
    # Interactive NYC Map with Taxi Zones
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<h3 class="chart-title">NYC Taxi Zones - Interactive Map</h3>', unsafe_allow_html=True)
    
    # Create an interactive map centered on NYC
    nyc_map = folium.Map(location=[40.7128, -74.0060], zoom_start=11, tiles='OpenStreetMap')
    
    # Add sample taxi zone markers
    taxi_zones = [
        {'name': 'Manhattan', 'lat': 40.7580, 'lon': -73.9855, 'trips': 450000, 'color': 'red'},
        {'name': 'Brooklyn', 'lat': 40.6782, 'lon': -73.9442, 'trips': 280000, 'color': 'blue'},
        {'name': 'Queens', 'lat': 40.7282, 'lon': -73.7949, 'trips': 190000, 'color': 'green'},
        {'name': 'Bronx', 'lat': 40.8448, 'lon': -73.8648, 'trips': 150000, 'color': 'purple'},
        {'name': 'Staten Island', 'lat': 40.5795, 'lon': -74.1502, 'trips': 80000, 'color': 'orange'}
    ]
    
    # Add markers for each taxi zone
    for zone in taxi_zones:
        folium.CircleMarker(
            location=[zone['lat'], zone['lon']],
            radius=zone['trips'] / 50000,  # Scale radius based on trips
            popup=f"{zone['name']}<br>Trip Volume: {zone['trips']:,}",
            color=zone['color'],
            fill=True,
            fill_color=zone['color'],
            fill_opacity=0.6
        ).add_to(nyc_map)
    
    # Display the map
    st_folium(nyc_map, width=700, height=500)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Traffic Flow Patterns
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<h3 class="chart-title">Traffic Flow Patterns</h3>', unsafe_allow_html=True)
    
    # Sample data for traffic flow
    hours = [f"{i:02d}:00" for i in range(24)]
    zones = ["Manhattan", "Brooklyn", "Queens", "Bronx", "Staten Island"]
    
    # Generate sample traffic data
    np.random.seed(42)
    traffic_data = []
    for hour in hours:
        for zone in zones:
            traffic_data.append({
                "hour": hour,
                "zone": zone,
                "congestion": np.random.randint(20, 100)
            })
    
    traffic_df = pd.DataFrame(traffic_data)
    
    fig_heatmap = px.density_heatmap(traffic_df, x="hour", y="zone", z="congestion",
                                     color_continuous_scale="Reds",
                                     template="plotly_white")
    fig_heatmap.update_layout(
        height=500,
        xaxis_title="Hour of Day",
        yaxis_title="Zone"
    )
    
    st.plotly_chart(fig_heatmap, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Predictive Page
elif page == "Predictive":
    st.markdown('<h1 class="main-header">Predictive Analytics</h1>', unsafe_allow_html=True)
    
    # Demand Forecasting
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<h3 class="chart-title">Ride Demand Forecast</h3>', unsafe_allow_html=True)
    
    # Generate sample forecast data
    dates = pd.date_range(start="2025-11-01", periods=30, freq='D')
    actual = 15000 + np.cumsum(np.random.randn(30) * 1000)
    forecast = actual[-1] + np.cumsum(np.random.randn(30) * 800)
    upper_bound = forecast + np.random.rand(30) * 2000
    lower_bound = forecast - np.random.rand(30) * 2000
    
    forecast_df = pd.DataFrame({
        'date': list(dates) + list(dates),
        'type': ['Actual'] * 30 + ['Forecast'] * 30,
        'value': list(actual) + list(forecast)
    })
    
    confidence_df = pd.DataFrame({
        'date': dates,
        'upper': upper_bound,
        'lower': lower_bound
    })
    
    fig_forecast = go.Figure()
    
    # Add actual data
    fig_forecast.add_trace(go.Scatter(
        x=dates, y=actual,
        mode='lines',
        name='Actual',
        line=dict(color='#8884d8')
    ))
    
    # Add forecast data
    fig_forecast.add_trace(go.Scatter(
        x=dates, y=forecast,
        mode='lines',
        name='Forecast',
        line=dict(color='#ff7f0e')
    ))
    
    # Add confidence interval
    fig_forecast.add_trace(go.Scatter(
        x=list(dates) + list(dates[::-1]),
        y=list(upper_bound) + list(lower_bound[::-1]),
        fill='toself',
        fillcolor='rgba(255, 127, 14, 0.2)',
        line=dict(color='rgba(255,255,255,0)'),
        hoverinfo="skip",
        showlegend=True,
        name='Confidence Interval'
    ))
    
    fig_forecast.update_layout(
        template="plotly_white",
        height=500,
        xaxis_title="Date",
        yaxis_title="Ride Requests",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig_forecast, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Anomaly Detection
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<h3 class="chart-title">Anomaly Detection</h3>', unsafe_allow_html=True)
    
    # Generate sample anomaly data
    time_points = pd.date_range(start="2025-11-01", periods=100, freq='H')
    normal_values = 50 + np.random.normal(0, 5, 100)
    
    # Inject some anomalies
    anomalies_idx = [15, 35, 72, 88]
    for idx in anomalies_idx:
        normal_values[idx] += np.random.choice([-1, 1]) * np.random.uniform(20, 30)
    
    anomaly_df = pd.DataFrame({
        'time': time_points,
        'value': normal_values,
        'is_anomaly': [i in anomalies_idx for i in range(100)]
    })
    
    fig_anomaly = px.scatter(anomaly_df, x="time", y="value", color="is_anomaly",
                             color_discrete_map={True: '#ff0000', False: '#8884d8'},
                             template="plotly_white")
    fig_anomaly.update_layout(
        height=400,
        xaxis_title="Time",
        yaxis_title="Metric Value"
    )
    
    st.plotly_chart(fig_anomaly, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Real-Time Page
elif page == "Real-Time":
    st.markdown('<h1 class="main-header">Real-Time Analytics</h1>', unsafe_allow_html=True)
    
    # Live Data Stream
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<h3 class="chart-title">Live Trip Stream</h3>', unsafe_allow_html=True)
    
    st.info("Real-time data streaming would be displayed here in a full implementation.")
    
    # Sample real-time metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-title">Current Trips/min</p>
            <p class="metric-value">{np.random.randint(100, 500)}</p>
            <p>Live rate</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-title">Active Vehicles</p>
            <p class="metric-value">{np.random.randint(5000, 15000)}</p>
            <p>Currently operating</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-title">Avg Wait Time</p>
            <p class="metric-value">{np.random.randint(2, 8)} min</p>
            <p>Current estimate</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Recent Events
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<h3 class="chart-title">Recent Events</h3>', unsafe_allow_html=True)
    
    # Sample events data
    events_data = [
        {"time": "10:45:22", "event": "High demand in Manhattan", "severity": "High"},
        {"time": "10:42:15", "event": "Traffic congestion on FDR", "severity": "Medium"},
        {"time": "10:38:47", "event": "New surge pricing in Brooklyn", "severity": "Low"},
        {"time": "10:35:33", "event": "Service disruption in Queens", "severity": "High"},
        {"time": "10:32:11", "event": "Normal operations restored", "severity": "Low"}
    ]
    
    for event in events_data:
        color = "#ff4444" if event["severity"] == "High" else "#ffaa00" if event["severity"] == "Medium" else "#44aa44"
        st.markdown(f"""
        <div style="padding: 0.5rem; border-left: 4px solid {color}; margin-bottom: 0.5rem; background-color: #ffffff;">
            <div style="display: flex; justify-content: space-between;">
                <span><b>{event['time']}</b></span>
                <span style="color: {color};"><b>{event['severity']}</b></span>
            </div>
            <div>{event['event']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.caption("Urban Mobility & Transportation Analytics Dashboard | Data refreshed automatically")