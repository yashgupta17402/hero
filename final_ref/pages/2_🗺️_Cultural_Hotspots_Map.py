import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import random
from streamlit_folium import st_folium

# --- Page Configuration ---
st.set_page_config(
    page_title="Cultural Hotspots Map | Cultural Canvas India",
    layout="wide",
    initial_sidebar_state="auto",
    page_icon="🗺️"
)

# --- Simulated Database Functions ---
def get_cultural_sites():
    """Fetch cultural sites data (simulated)"""
    return pd.DataFrame({
        'site_id': range(1, 21),
        'name': [
            'Taj Mahal', 'Qutub Minar', 'Ajanta Caves', 'Khajuraho Temples', 
            'Hampi', 'Konark Sun Temple', 'Mahabodhi Temple', 'Red Fort',
            'Fatehpur Sikri', 'Ellora Caves', 'Meenakshi Temple', 'Hawa Mahal',
            'Sanchi Stupa', 'Brihadeeswara Temple', 'Golconda Fort', 'Jaisalmer Fort',
            'Rani ki Vav', 'Victoria Memorial', 'Gateway of India', 'Mysore Palace'
        ],
        'type': [
            'Monument', 'Monument', 'Cave', 'Temple', 
            'Archaeological Site', 'Temple', 'Temple', 'Fort',
            'Archaeological Site', 'Cave', 'Temple', 'Palace',
            'Stupa', 'Temple', 'Fort', 'Fort',
            'Stepwell', 'Memorial', 'Monument', 'Palace'
        ],
        'state': [
            'Uttar Pradesh', 'Delhi', 'Maharashtra', 'Madhya Pradesh',
            'Karnataka', 'Odisha', 'Bihar', 'Delhi',
            'Uttar Pradesh', 'Maharashtra', 'Tamil Nadu', 'Rajasthan',
            'Madhya Pradesh', 'Tamil Nadu', 'Telangana', 'Rajasthan',
            'Gujarat', 'West Bengal', 'Maharashtra', 'Karnataka'
        ],
        'latitude': [
            27.1751, 28.5245, 20.5519, 24.8318,
            15.3350, 19.8876, 24.6961, 28.6562,
            27.0940, 20.0215, 9.9252, 26.9239,
            23.4795, 10.7828, 17.3833, 26.9157,
            23.8594, 22.5448, 18.9220, 12.3052
        ],
        'longitude': [
            78.0421, 77.1855, 75.7033, 79.9199,
            76.4600, 86.0945, 84.9911, 77.2410,
            77.6710, 75.1795, 78.1198, 75.8267,
            77.7382, 79.1318, 78.4011, 70.9083,
            72.1175, 88.3426, 72.8347, 76.6552
        ],
        'unesco': [
            True, True, True, True,
            True, True, True, True,
            True, True, False, False,
            True, True, False, False,
            True, False, False, False
        ],
        'asi_protected': [
            True, True, True, True,
            True, True, True, True,
            True, True, False, True,
            True, True, True, True,
            True, False, True, False
        ],
        'domestic_tourists': [
            random.randint(500000, 7000000) for _ in range(20)
        ],
        'foreign_tourists': [
            random.randint(50000, 1000000) for _ in range(20)
        ],
        'description': [
            'An ivory-white marble mausoleum built by Emperor Shah Jahan in memory of his wife Mumtaz Mahal.',
            'A 73-meter tall minaret built by Qutb al-Din Aibak, founder of the Delhi Sultanate.',
            'Buddhist cave monuments dating from the 2nd century BCE to about 480 CE.',
            'A group of Hindu and Jain temples famous for their nagara-style architectural symbolism and erotic sculptures.',
            'The ruins of the Vijayanagara Empire capital, known for its stunning temples and architectural marvels.',
            'A 13th-century Sun Temple known for its exquisite stone carvings and architectural grandeur.',
            'One of the oldest Buddhist temples built by Emperor Ashoka, marking the spot where Buddha attained enlightenment.',
            'A historic fort that served as the main residence of the Mughal Emperors for nearly 200 years.',
            'A city founded by Mughal Emperor Akbar, serving briefly as the empire\'s capital.',
            'A series of 34 monasteries and temples, extending over more than 2 km, famous for their Buddhist, Hindu and Jain monuments.',
            'A historic Hindu temple dedicated to Goddess Meenakshi, known for its towering gopurams and intricate carvings.',
            'A palace built with red and pink sandstone, known for its honeycomb-like structure of small windows.',
            'The oldest stone structure in India, housing Buddha\'s relics, known for its Great Stupa.',
            'A Hindu temple dedicated to Lord Shiva, built by Raja Raja Chola I, known for its Dravidian architecture.',
            'A ruined fortress complex, known for its acoustic effects and innovative water supply system.',
            'A massive yellow sandstone fortress, known as the "Golden Fort" due to its golden hue.',
            'An intricately constructed stepwell built as a memorial to a king, known for its inverted temple design.',
            'A large marble building dedicated to Queen Victoria, now serving as a museum and tourist destination.',
            'An arch monument built during the British Raj, overlooking the Arabian Sea.',
            'A historical palace known for its Indo-Saracenic style of architecture, featuring a blend of Hindu, Muslim, Rajput, and Gothic styles.'
        ],
        'image_url': [
            'https://raw.githubusercontent.com/yashgupta17402/hero/main/taj_mahal.jpg',
            'https://raw.githubusercontent.com/yashgupta17402/hero/main/qutub_minar.jpg',
            'https://raw.githubusercontent.com/yashgupta17402/hero/main/ajanta.jpg',
            'https://raw.githubusercontent.com/yashgupta17402/hero/main/khajuraho.jpg',
            'https://raw.githubusercontent.com/yashgupta17402/hero/main/hampi.jpg',
            'https://raw.githubusercontent.com/yashgupta17402/hero/main/konark.jpg',
            'https://raw.githubusercontent.com/yashgupta17402/hero/main/mahabodhi.jpg',
            'https://raw.githubusercontent.com/yashgupta17402/hero/main/red_fort.jpg',
            'https://raw.githubusercontent.com/yashgupta17402/hero/main/fatehpur_sikri.jpg',
            'https://raw.githubusercontent.com/yashgupta17402/hero/main/ellora.jpg',
            'https://raw.githubusercontent.com/yashgupta17402/hero/main/meenakshi.jpg',
            'https://raw.githubusercontent.com/yashgupta17402/hero/main/hawa_mahal.jpg',
            'https://raw.githubusercontent.com/yashgupta17402/hero/main/sanchi.jpg',
            'https://raw.githubusercontent.com/yashgupta17402/hero/main/brihadeeswara.jpg',
            'https://raw.githubusercontent.com/yashgupta17402/hero/main/golconda.jpg',
            'https://raw.githubusercontent.com/yashgupta17402/hero/main/jaisalmer.jpg',
            'https://raw.githubusercontent.com/yashgupta17402/hero/main/rani_ki_vav.jpg',
            'https://raw.githubusercontent.com/yashgupta17402/hero/main/victoria.jpg',
            'https://raw.githubusercontent.com/yashgupta17402/hero/main/gateway.jpg',
            'https://raw.githubusercontent.com/yashgupta17402/hero/main/mysore.jpg'
        ]
    })

def get_tourism_data():
    """Generate monthly tourism data for the past 3 years (simulated)"""
    states = [
        'Uttar Pradesh', 'Delhi', 'Maharashtra', 'Madhya Pradesh',
        'Karnataka', 'Odisha', 'Bihar', 'Tamil Nadu',
        'Rajasthan', 'Telangana', 'Gujarat', 'West Bengal'
    ]
    
    # Generate dates for the past 3 years
    current_year = datetime.now().year
    dates = []
    for year in range(current_year-3, current_year):
        for month in range(1, 13):
            dates.append(f"{year}-{month:02d}-01")
    
    # Create dataframe
    data = []
    for state in states:
        # Base number of tourists for each state (different for each state)
        base_domestic = random.randint(100000, 1000000)
        base_foreign = random.randint(10000, 100000)
        
        for date in dates:
            year, month, _ = date.split('-')
            month = int(month)
            
            # Seasonal variations
            # Peak season: October to March (winter)
            # Off season: April to September (summer/monsoon)
            season_factor = 1.5 if month in [10, 11, 12, 1, 2, 3] else 0.7
            
            # Random variation
            random_factor = random.uniform(0.8, 1.2)
            
            # Calculate tourist numbers
            domestic = int(base_domestic * season_factor * random_factor)
            foreign = int(base_foreign * season_factor * random_factor)
            
            data.append({
                'date': date,
                'state': state,
                'domestic_tourists': domestic,
                'foreign_tourists': foreign,
                'total_tourists': domestic + foreign
            })
    
    return pd.DataFrame(data)

# --- CSS Styling ---
st.markdown("""
<style>
/* Global Page Styling */
.main {
    background-color: white;
    color: #333;
}

/* Header Styling */
.header {
    padding: 1rem 0;
    text-align: center;
    margin-bottom: 2rem;
}
.header h1 {
    color: #2c3e50;
    font-size: 2.5rem;
    font-weight: 700;
}
.header p {
    color: #555;
    font-size: 1.2rem;
    max-width: 800px;
    margin: 0 auto;
}

/* Map Container */
.map-container {
    background-color: white;
    border-radius: 10px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    padding: 1rem;
    margin-bottom: 2rem;
}

/* Layer Controls */
.layer-controls {
    background-color: #f8f9fa;
    padding: 1.5rem;
    border-radius: 10px;
    margin-bottom: 1.5rem;
    box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}

/* Site Details */
.site-details {
    background-color: white;
    border-radius: 10px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    padding: 2rem;
    margin-top: 2rem;
}
.site-image {
    width: 100%;
    border-radius: 8px;
    margin-bottom: 1rem;
}
.site-title {
    font-size: 1.8rem;
    font-weight: 700;
    color: #2c3e50;
    margin-bottom: 0.5rem;
}
.site-subtitle {
    font-size: 1.1rem;
    color: #7f8c8d;
    margin-bottom: 1rem;
}
.site-description {
    font-size: 1rem;
    color: #555;
    line-height: 1.6;
    margin-bottom: 1.5rem;
}
.site-stats {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 1rem;
    margin-bottom: 1.5rem;
}
.stat-card {
    background-color: #f8f9fa;
    padding: 1rem;
    border-radius: 8px;
    text-align: center;
}
.stat-value {
    font-size: 1.5rem;
    font-weight: 700;
    color: #FF6347;
    margin-bottom: 0.3rem;
}
.stat-label {
    font-size: 0.9rem;
    color: #7f8c8d;
}

/* Seasonality Chart */
.chart-container {
    background-color: white;
    border-radius: 10px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    padding: 2rem;
    margin-top: 2rem;
}
.chart-title {
    font-size: 1.5rem;
    font-weight: 600;
    color: #2c3e50;
    margin-bottom: 1rem;
    text-align: center;
}

/* Badge Styles */
.badge {
    display: inline-block;
    padding: 0.3rem 0.6rem;
    border-radius: 4px;
    font-size: 0.8rem;
    font-weight: 500;
    margin-right: 0.5rem;
}
.badge-unesco {
    background-color: #3498db;
    color: white;
}
.badge-asi {
    background-color: #2ecc71;
    color: white;
}
.badge-high {
    background-color: #e74c3c;
    color: white;
}
.badge-low {
    background-color: #f39c12;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("""
<div class="header">
    <h1>🗺️ Cultural Hotspots Map</h1>
    <p>Explore India's rich cultural heritage through an interactive map of monuments, temples, and historical sites. Discover popular destinations and hidden gems waiting to share their stories.</p>
</div>
""", unsafe_allow_html=True)

# --- Load Data ---
sites_df = get_cultural_sites()
tourism_df = get_tourism_data()

# --- Layer Controls ---
st.markdown('<div class="layer-controls">', unsafe_allow_html=True)
st.subheader("Map Layers")
col1, col2, col3, col4 = st.columns(4)

with col1:
    show_unesco = st.checkbox("UNESCO World Heritage Sites", value=True)
with col2:
    show_asi = st.checkbox("ASI Protected Sites", value=True)
with col3:
    show_high_traffic = st.checkbox("High Tourist Traffic", value=True)
with col4:
    show_low_traffic = st.checkbox("Low Tourist Traffic", value=True)

st.markdown('</div>', unsafe_allow_html=True)

# --- Create Map ---
st.markdown('<div class="map-container">', unsafe_allow_html=True)

# Center map on India
m = folium.Map(location=[20.5937, 78.9629], zoom_start=5, tiles="cartodbpositron")

# Add layer control
folium.LayerControl().add_to(m)

# Filter sites based on selected layers
filtered_sites = sites_df.copy()

# Define high and low traffic thresholds
high_traffic_threshold = sites_df['domestic_tourists'].quantile(0.7)
low_traffic_threshold = sites_df['domestic_tourists'].quantile(0.3)

# Add markers to map
for _, site in filtered_sites.iterrows():
    # Determine marker color based on traffic
    if site['domestic_tourists'] >= high_traffic_threshold:
        traffic_type = "High Traffic"
        color = "red"
        show_condition = show_high_traffic
    elif site['domestic_tourists'] <= low_traffic_threshold:
        traffic_type = "Low Traffic"
        color = "orange"
        show_condition = show_low_traffic
    else:
        traffic_type = "Medium Traffic"
        color = "blue"
        show_condition = True  # Always show medium traffic
    
    # Check UNESCO and ASI conditions
    unesco_condition = not show_unesco or (show_unesco and site['unesco'])
    asi_condition = not show_asi or (show_asi and site['asi_protected'])
    
    # Add marker if it meets all conditions
    if show_condition and unesco_condition and asi_condition:
        popup_html = f"""
        <div style="width: 200px;">
            <h4>{site['name']}</h4>
            <p>{site['type']} in {site['state']}</p>
            <p>Annual Visitors: {site['domestic_tourists'] + site['foreign_tourists']:,}</p>
            <p>
                {f'<span style="background-color: #3498db; color: white; padding: 2px 5px; border-radius: 3px; font-size: 10px;">UNESCO</span>' if site['unesco'] else ''}
                {f'<span style="background-color: #2ecc71; color: white; padding: 2px 5px; border-radius: 3px; font-size: 10px;">ASI</span>' if site['asi_protected'] else ''}
            </p>
            <a href="#" onclick="parent.postMessage({{'type': 'streamlit:setComponentValue', 'value': '{site['name']}'}}, '*')">View Details</a>
        </div>
        """
        
        folium.Marker(
            [site['latitude'], site['longitude']],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=site['name'],
            icon=folium.Icon(color=color, icon="info-sign")
        ).add_to(m)

# Display map
# folium_static(m, width=1200, height=600)
st_folium(m, width=1200, height=600)
st.markdown('</div>', unsafe_allow_html=True)

# --- Site Details ---
if 'selected_site' in st.session_state:
    site = sites_df[sites_df['name'] == st.session_state.selected_site].iloc[0]
    
    st.markdown('<div class="site-details">', unsafe_allow_html=True)
    
    # Back button
    if st.button("← Back to Map"):
        del st.session_state.selected_site
        st.rerun()
    
    # Site header
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.image(site['image_url'], use_column_width=True)
    
    with col2:
        st.markdown(f'<div class="site-title">{site["name"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="site-subtitle">{site["type"]} • {site["state"]}</div>', unsafe_allow_html=True)
        
        # Badges
        badges_html = ""
        if site['unesco']:
            badges_html += '<span class="badge badge-unesco">UNESCO World Heritage</span>'
        if site['asi_protected']:
            badges_html += '<span class="badge badge-asi">ASI Protected</span>'
        if site['domestic_tourists'] >= high_traffic_threshold:
            badges_html += '<span class="badge badge-high">High Tourist Traffic</span>'
        elif site['domestic_tourists'] <= low_traffic_threshold:
            badges_html += '<span class="badge badge-low">Low Tourist Traffic</span>'
        
        st.markdown(badges_html, unsafe_allow_html=True)
        
        st.markdown(f'<div class="site-description">{site["description"]}</div>', unsafe_allow_html=True)
    
    # Site statistics
    st.markdown('<div class="site-stats">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{site['domestic_tourists']:,}</div>
            <div class="stat-label">Domestic Tourists Annually</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{site['foreign_tourists']:,}</div>
            <div class="stat-label">Foreign Tourists Annually</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{site['domestic_tourists'] + site['foreign_tourists']:,}</div>
            <div class="stat-label">Total Visitors Annually</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Seasonality Chart
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Tourist Seasonality Trends</div>', unsafe_allow_html=True)
    
    # Filter tourism data for the selected state
    state_tourism = tourism_df[tourism_df['state'] == site['state']].copy()
    state_tourism['date'] = pd.to_datetime(state_tourism['date'])
    state_tourism['month'] = state_tourism['date'].dt.month
    state_tourism['month_name'] = state_tourism['date'].dt.strftime('%b')
    state_tourism['year'] = state_tourism['date'].dt.year
    
    # Group by month and calculate average
    monthly_avg = state_tourism.groupby('month')[['domestic_tourists', 'foreign_tourists']].mean().reset_index()
    monthly_avg['month_name'] = pd.to_datetime(monthly_avg['month'], format='%m').dt.strftime('%b')
    monthly_avg = monthly_avg.sort_values('month')
    
    # Create line chart
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=monthly_avg['month_name'],
        y=monthly_avg['domestic_tourists'],
        mode='lines+markers',
        name='Domestic Tourists',
        line=dict(color='#FF6347', width=3),
        marker=dict(size=8)
    ))
    
    fig.add_trace(go.Scatter(
        x=monthly_avg['month_name'],
        y=monthly_avg['foreign_tourists'],
        mode='lines+markers',
        name='Foreign Tourists',
        line=dict(color='#3498db', width=3),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title=f"Monthly Tourism Trends in {site['state']}",
        xaxis_title="Month",
        yaxis_title="Average Number of Tourists",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        template="plotly_white",
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Travel tips
    st.subheader("Best Time to Visit")
    
    # Determine peak and off seasons
    peak_months = monthly_avg.nlargest(3, 'domestic_tourists')['month_name'].tolist()
    off_months = monthly_avg.nsmallest(3, 'domestic_tourists')['month_name'].tolist()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div style="background-color: #f8f9fa; padding: 1rem; border-radius: 8px; border-left: 4px solid #e74c3c;">
            <h4 style="color: #e74c3c;">Peak Season: {', '.join(peak_months)}</h4>
            <p>Expect larger crowds and higher accommodation prices. Book in advance for a smoother experience.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background-color: #f8f9fa; padding: 1rem; border-radius: 8px; border-left: 4px solid #2ecc71;">
            <h4 style="color: #2ecc71;">Off Season: {', '.join(off_months)}</h4>
            <p>Enjoy a more peaceful experience with fewer tourists and better deals on accommodations.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
else:
    # Instructions when no site is selected
    st.info("👆 Click on a marker on the map to view detailed information about a cultural site.")

# --- Handle map marker clicks ---
site_name = st.text_input("Search for a cultural site", "", key="site_search")
if site_name:
    matching_sites = sites_df[sites_df['name'].str.contains(site_name, case=False)]
    if not matching_sites.empty:
        st.session_state.selected_site = matching_sites.iloc[0]['name']
        st.rerun()
    else:
        st.warning(f"No sites found matching '{site_name}'")