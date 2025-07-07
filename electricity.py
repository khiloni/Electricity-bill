import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="⚡ Electricity Usage Calculator",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .metric-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 0.5rem 0;
    }
    
    .info-box {
        background-color: #34495e;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    
    .stSelectbox > div > div {
        background-color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown('<h1 class="main-header">⚡ Electricity Usage Calculator</h1>', unsafe_allow_html=True)

# Sidebar for user inputs
with st.sidebar:
    st.header("📋 Personal Information")
    
    # Personal details
    name = st.text_input("👤 Enter your name:", placeholder="Your name here...")
    age = st.number_input("🎂 Enter your age:", min_value=1, max_value=120, value=25)
    area = st.text_input("📍 Enter your area:", placeholder="Your area...")
    city = st.text_input("🏙️ Enter your city:", placeholder="Your city...")
    
    st.header("🏠 House Information")
    
    # House details
    house_type = st.selectbox(
        "🏠 Where do you live?",
        ["Flat", "Tenement", "Independent House", "Villa"]
    )
    
    house_size = st.selectbox(
        "📏 Size of your house:",
        ["1BHK", "2BHK", "3BHK", "4BHK", "5BHK+"]
    )
    
    st.header("🔌 Appliances")
    
    # Appliances
    has_washing_machine = st.checkbox("🧺 Washing Machine")
    has_refrigerator = st.checkbox("❄️ Refrigerator")
    has_ac = st.checkbox("🌡️ Air Conditioner")
    
    num_ac = 0
    if has_ac:
        num_ac = st.number_input("How many ACs?", min_value=1, max_value=10, value=1)
    
    # Additional appliances
    st.subheader("Additional Appliances")
    has_tv = st.checkbox("📺 Television")
    num_tv = 0
    if has_tv:
        num_tv = st.number_input("How many TVs?", min_value=1, max_value=5, value=1)
    
    has_microwave = st.checkbox("🔥 Microwave")
    has_dishwasher = st.checkbox("🍽️ Dishwasher")
    has_water_heater = st.checkbox("🚿 Water Heater")

# Calculate energy consumption
def calculate_energy_consumption(house_size, appliances):
    """Calculate daily energy consumption in kWh"""
    
    # Base consumption based on house size (lights and fans)
    base_consumption = {
        "1BHK": 2 * 0.04 + 2 * 0.08,  # 2 lights (40W each) + 2 fans (80W each) for 10 hours
        "2BHK": 3 * 0.04 + 3 * 0.08,  # 3 lights + 3 fans
        "3BHK": 4 * 0.04 + 4 * 0.08,  # 4 lights + 4 fans
        "4BHK": 5 * 0.04 + 5 * 0.08,  # 5 lights + 5 fans
        "5BHK+": 6 * 0.04 + 6 * 0.08  # 6 lights + 6 fans
    }
    
    daily_consumption = base_consumption.get(house_size, 0)
    
    # Add appliance consumption (kWh per day)
    appliance_consumption = {
        'washing_machine': 0.5,  # 500W for 1 hour
        'refrigerator': 1.2,     # 50W for 24 hours
        'ac': 2.4,               # 1000W for 2.4 hours average
        'tv': 0.15,              # 150W for 1 hour
        'microwave': 0.2,        # 1000W for 0.2 hours
        'dishwasher': 0.8,       # 800W for 1 hour
        'water_heater': 1.5      # 1500W for 1 hour
    }
    
    for appliance, power in appliances.items():
        if power > 0:
            if appliance == 'ac':
                daily_consumption += appliance_consumption[appliance] * power
            elif appliance == 'tv':
                daily_consumption += appliance_consumption[appliance] * power
            else:
                daily_consumption += appliance_consumption[appliance]
    
    return daily_consumption

# Prepare appliances dictionary
appliances = {
    'washing_machine': 1 if has_washing_machine else 0,
    'refrigerator': 1 if has_refrigerator else 0,
    'ac': num_ac if has_ac else 0,
    'tv': num_tv if has_tv else 0,
    'microwave': 1 if has_microwave else 0,
    'dishwasher': 1 if has_dishwasher else 0,
    'water_heater': 1 if has_water_heater else 0
}

# Calculate consumption
daily_consumption = calculate_energy_consumption(house_size, appliances)
weekly_consumption = daily_consumption * 7
monthly_consumption = daily_consumption * 30

# Main content area
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="⚡ Daily Usage",
        value=f"{daily_consumption:.2f} kWh",
        delta=f"₹{daily_consumption * 6:.2f}"  # Assuming ₹6 per kWh
    )

with col2:
    st.metric(
        label="📅 Weekly Usage",
        value=f"{weekly_consumption:.2f} kWh",
        delta=f"₹{weekly_consumption * 6:.2f}"
    )

with col3:
    st.metric(
        label="📊 Monthly Usage",
        value=f"{monthly_consumption:.2f} kWh",
        delta=f"₹{monthly_consumption * 6:.2f}"
    )

# Usage breakdown chart
st.subheader("📈 Energy Consumption Breakdown")

# Create breakdown data
breakdown_data = []
base_consumption = {
    "1BHK": 2 * 0.04 + 2 * 0.08,
    "2BHK": 3 * 0.04 + 3 * 0.08,
    "3BHK": 4 * 0.04 + 4 * 0.08,
    "4BHK": 5 * 0.04 + 5 * 0.08,
    "5BHK+": 6 * 0.04 + 6 * 0.08
}

breakdown_data.append(["Lights & Fans", base_consumption.get(house_size, 0)])

if has_washing_machine:
    breakdown_data.append(["Washing Machine", 0.5])
if has_refrigerator:
    breakdown_data.append(["Refrigerator", 1.2])
if has_ac:
    breakdown_data.append(["Air Conditioner", 2.4 * num_ac])
if has_tv:
    breakdown_data.append(["Television", 0.15 * num_tv])
if has_microwave:
    breakdown_data.append(["Microwave", 0.2])
if has_dishwasher:
    breakdown_data.append(["Dishwasher", 0.8])
if has_water_heater:
    breakdown_data.append(["Water Heater", 1.5])

# Create charts
col1, col2 = st.columns(2)

with col1:
    if breakdown_data:
        df_breakdown = pd.DataFrame(breakdown_data, columns=['Appliance', 'Consumption (kWh)'])
        fig_pie = px.pie(df_breakdown, values='Consumption (kWh)', names='Appliance', 
                        title="Daily Energy Distribution")
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)

with col2:
    # Usage trend over time
    dates = [datetime.now() + timedelta(days=i) for i in range(30)]
    daily_usage = [daily_consumption + (i % 3) * 0.1 for i in range(30)]  # Slight variation
    
    df_trend = pd.DataFrame({
        'Date': dates,
        'Usage (kWh)': daily_usage
    })
    
    fig_trend = px.line(df_trend, x='Date', y='Usage (kWh)', 
                       title="30-Day Usage Trend")
    st.plotly_chart(fig_trend, use_container_width=True)

# Cost analysis
st.subheader("💰 Cost Analysis")

# Different tariff slabs (example rates)
slab_rates = [
    (0, 100, 3.5),    # First 100 units at ₹3.5/unit
    (100, 200, 4.5),  # Next 100 units at ₹4.5/unit
    (200, 400, 6.0),  # Next 200 units at ₹6.0/unit
    (400, float('inf'), 7.5)  # Above 400 units at ₹7.5/unit
]

def calculate_bill(units):
    """Calculate electricity bill based on slab rates"""
    total_cost = 0
    remaining_units = units
    
    for min_units, max_units, rate in slab_rates:
        if remaining_units <= 0:
            break
        
        slab_units = min(remaining_units, max_units - min_units)
        total_cost += slab_units * rate
        remaining_units -= slab_units
    
    return total_cost

monthly_bill = calculate_bill(monthly_consumption)
yearly_bill = monthly_bill * 12

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("💳 Monthly Bill", f"₹{monthly_bill:.2f}")

with col2:
    st.metric("💰 Yearly Bill", f"₹{yearly_bill:.2f}")

with col3:
    st.metric("⚡ Cost per kWh", f"₹{monthly_bill/monthly_consumption:.2f}")

with col4:
    st.metric("📊 Efficiency Rating", 
             "⭐⭐⭐⭐⭐" if daily_consumption < 5 else 
             "⭐⭐⭐⭐" if daily_consumption < 8 else 
             "⭐⭐⭐" if daily_consumption < 12 else "⭐⭐")

# Tips for energy saving
st.subheader("💡 Energy Saving Tips")

tips = [
    "🌟 Use LED bulbs instead of incandescent bulbs to save up to 80% energy",
    "❄️ Set your AC temperature to 24°C for optimal energy efficiency",
    "🔌 Unplug devices when not in use to avoid phantom power consumption",
    "🌞 Use natural light during the day and switch off unnecessary lights",
    "🧺 Use washing machine with full loads and cold water when possible",
    "🌡️ Regular maintenance of appliances improves their efficiency"
]

for tip in tips:
    st.markdown(f"• {tip}")

# User summary
if name:
    st.subheader(f"📋 Summary for {name}")
    st.markdown(f"""
    <div class="info-box">
    <strong>Personal Details:</strong><br>
    Name: {name}<br>
    Age: {age}<br>
    Location: {area}, {city}<br>
    House Type: {house_type} ({house_size})<br><br>
    
    <strong>Energy Consumption:</strong><br>
    Daily: {daily_consumption:.2f} kWh (₹{daily_consumption * 6:.2f})<br>
    Weekly: {weekly_consumption:.2f} kWh (₹{weekly_consumption * 6:.2f})<br>
    Monthly: {monthly_consumption:.2f} kWh (₹{monthly_bill:.2f})<br>
    Yearly: {monthly_consumption * 12:.2f} kWh (₹{yearly_bill:.2f})
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("⚡ **Electricity Usage Calculator** | Built with Streamlit | Data is for estimation purposes only")
