"""
Solar Panel Cooling Optimizer - Web Interface
Streamlit app that uses the solar_cooling module
"""

import streamlit as st
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import our solar cooling functions
from solar_cooling import (
    get_coordinates,
    fetch_weather_data,
    physics_based_check,
    predict_from_model
)

# -----------------------------
# PAGE CONFIGURATION
# -----------------------------
st.set_page_config(
    page_title="Solar Panel Cooling Optimizer",
    page_icon="🌞",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# HELPER FUNCTIONS
# -----------------------------

def create_gauge_chart(value, title, max_value, color):
    """Create a gauge chart for metrics."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title},
        gauge={
            'axis': {'range': [None, max_value]},
            'bar': {'color': color},
            'steps': [
                {'range': [0, max_value * 0.33], 'color': "lightgray"},
                {'range': [max_value * 0.33, max_value * 0.66], 'color': "gray"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': max_value * 0.9
            }
        }
    ))
    fig.update_layout(height=250, margin=dict(l=20, r=20, t=50, b=20))
    return fig


# -----------------------------
# MAIN APP
# -----------------------------

def main():
    # Header
    st.title("🌞 Solar Panel Cooling Optimizer")
    st.markdown("### Optimize your solar panel performance with intelligent cooling decisions")
    
    # Sidebar for inputs
    st.sidebar.header("⚙️ Configuration")
    
    # Input method selection
    input_method = st.sidebar.radio(
        "Choose input method:",
        ["Use Real-Time Weather Data", "Manual Input"]
    )
    
    if input_method == "Use Real-Time Weather Data":
        # Location input
        place = st.sidebar.text_input(
            "Enter location (city, country):",
            value="New York, USA",
            help="Enter any city or location worldwide"
        )
        
        # Date and time inputs
        col1, col2 = st.sidebar.columns(2)
        with col1:
            selected_date = st.date_input(
                "Date:",
                value=datetime(2023, 7, 15),
                min_value=datetime(2020, 1, 1),
                max_value=datetime.now()
            )
        with col2:
            hour = st.selectbox(
                "Hour (0-23):",
                range(24),
                index=14
            )
        
        if st.sidebar.button("🔍 Fetch Weather Data", type="primary"):
            with st.spinner("Fetching coordinates..."):
                coords = get_coordinates(place)
                
            if coords:
                lat, lon, name = coords
                st.sidebar.success(f"📍 {name}")
                st.sidebar.info(f"Lat: {lat:.3f}, Lon: {lon:.3f}")
                
                year = selected_date.year
                month = selected_date.month
                day = selected_date.day
                
                try:
                    with st.spinner("Fetching weather data from NASA POWER..."):
                        real_data = fetch_weather_data(lat, lon, year, month, day, hour)
                    
                    T_amb = real_data["Temperature"]
                    G = real_data["Irradiance"]
                    
                    st.session_state['T_amb'] = T_amb
                    st.session_state['G'] = G
                    st.session_state['hour'] = hour
                    st.session_state['data_fetched'] = True
                    
                except Exception as e:
                    st.error(f"❌ Error fetching weather data: {str(e)}")
                    st.session_state['data_fetched'] = False
            else:
                st.error("❌ Could not find coordinates for that location")
                st.session_state['data_fetched'] = False
    
    else:  # Manual Input
        st.sidebar.subheader("Enter environmental conditions:")
        T_amb = st.sidebar.slider(
            "Ambient Temperature (°C):",
            min_value=-10.0,
            max_value=50.0,
            value=30.0,
            step=0.5
        )
        G = st.sidebar.slider(
            "Solar Irradiance (W/m²):",
            min_value=0.0,
            max_value=1200.0,
            value=800.0,
            step=10.0
        )
        hour = st.sidebar.selectbox(
            "Hour of day (0-23):",
            range(24),
            index=14
        )
        
        st.session_state['T_amb'] = T_amb
        st.session_state['G'] = G
        st.session_state['hour'] = hour
        st.session_state['data_fetched'] = True
    
    # Main content area
    if st.session_state.get('data_fetched', False):
        T_amb = st.session_state['T_amb']
        G = st.session_state['G']
        hour = st.session_state['hour']
        
        # Display current conditions
        st.subheader("📊 Current Conditions")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("🌡️ Temperature", f"{T_amb:.1f} °C")
        with col2:
            st.metric("☀️ Irradiance", f"{G:.0f} W/m²")
        with col3:
            st.metric("🕐 Hour", f"{hour}:00")
        
        # Perform calculations using imported function
        panel_temp, energy_gain, cooling_cost, should_cool, P_unc, P_cool = physics_based_check(T_amb, G)
        
        st.markdown("---")
        
        # Results section
        st.subheader("🎯 Analysis Results")
        
        # Recommendation card
        if should_cool:
            st.success("✅ **COOLING RECOMMENDED**")
            st.markdown(f"**Net Energy Gain:** {energy_gain:.2f} W")
        else:
            st.warning("⚠️ **COOLING NOT RECOMMENDED**")
            st.markdown(f"**Net Energy Loss:** {abs(energy_gain):.2f} W")
        
        # Detailed metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            fig1 = create_gauge_chart(panel_temp, "Panel Temperature (°C)", 70, "orange")
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            fig2 = create_gauge_chart(P_unc, "Uncooled Power (W)", 200, "red")
            st.plotly_chart(fig2, use_container_width=True)
        
        with col3:
            fig3 = create_gauge_chart(P_cool, "Cooled Power (W)", 200, "green")
            st.plotly_chart(fig3, use_container_width=True)
        
        # Energy comparison chart
        st.subheader("⚡ Energy Analysis")
        
        energy_df = pd.DataFrame({
            'Metric': ['Uncooled Power', 'Cooled Power', 'Cooling Cost', 'Net Gain'],
            'Value': [P_unc, P_cool, cooling_cost, energy_gain],
            'Color': ['red', 'green', 'orange', 'blue' if should_cool else 'gray']
        })
        
        fig_bar = px.bar(
            energy_df, 
            x='Metric', 
            y='Value',
            color='Metric',
            title="Energy Breakdown",
            labels={'Value': 'Power (W)'},
            color_discrete_map={
                'Uncooled Power': 'red',
                'Cooled Power': 'green',
                'Cooling Cost': 'orange',
                'Net Gain': 'blue' if should_cool else 'gray'
            }
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        
        # ML Model prediction using imported function
        st.markdown("---")
        st.subheader("🤖 Machine Learning Prediction")
        
        prediction, error = predict_from_model(T_amb, G, hour)
        
        if error:
            st.info(f"ℹ️ {error}")
            st.markdown("*Upload a trained model to `models/cooling_decision_model.pkl` to enable ML predictions*")
        else:
            col1, col2 = st.columns(2)
            with col1:
                st.metric("ML Model Says:", "COOL" if prediction else "DON'T COOL")
            with col2:
                agreement = prediction == should_cool
                st.metric("Agreement with Physics:", "✅ Yes" if agreement else "❌ No")
        
        # Technical details expander
        with st.expander("📖 Technical Details"):
            st.markdown(f"""
            **Panel Specifications:**
            - Area: 0.284 m²
            - Reference Efficiency: 18.0%
            - Temperature Coefficient: 0.5%/°C
            - NOCT: 45°C
            
            **Cooling System:**
            - Target Temperature: 35°C
            - Pump Power: 2.0 W
            - Pump Efficiency: 85%
            - Effective Cooling Cost: {cooling_cost:.2f} Wh
            
            **Calculations:**
            - Panel Temperature: {panel_temp:.2f}°C
            - Uncooled Efficiency: {max(0.18 * (1 - 0.005 * (panel_temp - 25)), 0)*100:.2f}%
            - Cooled Efficiency: {max(0.18 * (1 - 0.005 * (35 - 25)), 0)*100:.2f}%
            """)
    
    else:
        st.info("👈 Configure settings in the sidebar and fetch weather data to begin analysis")
        
        # Show some example info
        st.markdown("""
        ### How It Works
        
        This tool helps you optimize solar panel performance by determining when active cooling is beneficial.
        
        **Features:**
        - 🌍 Real-time weather data from NASA POWER API
        - 🔬 Physics-based calculations for panel temperature and efficiency
        - 🤖 Machine learning predictions (when model is available)
        - 📊 Interactive visualizations
        
        **Get Started:**
        1. Choose your input method (real-time data or manual)
        2. Enter your location or environmental conditions
        3. Click "Fetch Weather Data" or adjust manual inputs
        4. View the analysis and cooling recommendation
        """)


if __name__ == "__main__":
    # Initialize session state
    if 'data_fetched' not in st.session_state:
        st.session_state['data_fetched'] = False
    
    main()
