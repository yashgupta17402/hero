import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import folium_static
import random
from streamlit_folium import st_folium


# --- Page Configuration ---
st.set_page_config(
    page_title="Untouched India Discovery | Cultural Canvas India",
    layout="wide",
    initial_sidebar_state="auto",
    page_icon="🏞️"
)

# --- Simulated Database Functions ---
def get_cultural_assets():
    """Fetch cultural assets data (simulated)"""
    states = [
        'Arunachal Pradesh', 'Sikkim', 'Nagaland', 'Mizoram', 'Meghalaya',
        'Tripura', 'Manipur', 'Assam', 'Chhattisgarh', 'Jharkhand',
        'Uttarakhand', 'Himachal Pradesh', 'Odisha', 'Telangana', 'Gujarat'
    ]
    
    data = []
    for state in states:
        # Randomly assign number of sites, tourists, and infrastructure scores
        num_sites = random.randint(5, 50)
        domestic_tourists = random.randint(10000, 500000)
        foreign_tourists = random.randint(1000, 50000)
        infrastructure_score = random.randint(1, 10)
        promotion_score = random.randint(1, 10)
        accessibility_score = random.randint(1, 10)
        
        # Calculate potential score (inverse of tourist numbers)
        max_tourists = 500000
        potential_score = 10 - int((domestic_tourists / max_tourists) * 10)
        if potential_score < 1:
            potential_score = 1
        
        # Generate unique art forms for each state
        art_forms = []
        for i in range(random.randint(2, 5)):
            art_forms.append(f"Traditional {state} Art Form {i+1}")
        
        # Generate unique festivals for each state
        festivals = []
        for i in range(random.randint(2, 4)):
            festivals.append(f"{state} Festival {i+1}")
        
        data.append({
            'state': state,
            'num_sites': num_sites,
            'domestic_tourists': domestic_tourists,
            'foreign_tourists': foreign_tourists,
            'total_tourists': domestic_tourists + foreign_tourists,
            'infrastructure_score': infrastructure_score,
            'promotion_score': promotion_score,
            'accessibility_score': accessibility_score,
            'potential_score': potential_score,
            'art_forms': ', '.join(art_forms),
            'festivals': ', '.join(festivals),
            'latitude': random.uniform(8.0, 35.0),
            'longitude': random.uniform(68.0, 97.0)
        })
    
    return pd.DataFrame(data)

def get_state_coordinates():
    """Get approximate coordinates for Indian states (simplified)"""
    return {
        'Arunachal Pradesh': [27.1004, 93.6167],
        'Sikkim': [27.5330, 88.5122],
        'Nagaland': [26.1584, 94.5624],
        'Mizoram': [23.1645, 92.9376],
        'Meghalaya': [25.4670, 91.3662],
        'Tripura': [23.9408, 91.9882],
        'Manipur': [24.6637, 93.9063],
        'Assam': [26.2006, 92.9376],
        'Chhattisgarh': [21.2787, 81.8661],
        'Jharkhand': [23.6102, 85.2799],
        'Uttarakhand': [30.0668, 79.0193],
        'Himachal Pradesh': [31.1048, 77.1734],
        'Odisha': [20.9517, 85.0985],
        'Telangana': [18.1124, 79.0193],
        'Gujarat': [22.2587, 71.1924]
    }

def get_challenges_data():
    """Generate challenges data for each state (simulated)"""
    states = [
        'Arunachal Pradesh', 'Sikkim', 'Nagaland', 'Mizoram', 'Meghalaya',
        'Tripura', 'Manipur', 'Assam', 'Chhattisgarh', 'Jharkhand',
        'Uttarakhand', 'Himachal Pradesh', 'Odisha', 'Telangana', 'Gujarat'
    ]
    
    challenges = [
        'Limited transportation infrastructure',
        'Lack of quality accommodations',
        'Insufficient promotion and marketing',
        'Limited tourism-related services',
        'Connectivity issues (roads, railways)',
        'Inadequate tourist information',
        'Limited digital presence',
        'Seasonal accessibility issues',
        'Language barriers',
        'Limited trained tourism workforce'
    ]
    
    opportunities = [
        'Authentic cultural experiences',
        'Pristine natural landscapes',
        'Unique traditional art forms',
        'Rich biodiversity',
        'Unexplored heritage sites',
        'Traditional cuisine exploration',
        'Community-based tourism potential',
        'Tribal cultural exchanges',
        'Eco-tourism development',
        'Craft tourism opportunities'
    ]
    
    data = []
    for state in states:
        # Randomly select 3-5 challenges and opportunities for each state
        state_challenges = random.sample(challenges, random.randint(3, 5))
        state_opportunities = random.sample(opportunities, random.randint(3, 5))
        
        data.append({
            'state': state,
            'challenges': ', '.join(state_challenges),
            'opportunities': ', '.join(state_opportunities)
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

/* Section Styling */
.section-container {
    background-color: white;
    border-radius: 10px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    padding: 2rem;
    margin-bottom: 2rem;
}
.section-title {
    font-size: 1.8rem;
    font-weight: 600;
    color: #2c3e50;
    margin-bottom: 1rem;
    text-align: center;
}
.section-subtitle {
    font-size: 1.2rem;
    color: #7f8c8d;
    margin-bottom: 1.5rem;
    text-align: center;
}

/* State Card Styling */
.state-card {
    background-color: #f8f9fa;
    border-radius: 10px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    border-left: 5px solid #3498db;
    transition: transform 0.3s ease;
}
.state-card:hover {
    transform: translateY(-5px);
}
.state-card-title {
    font-size: 1.5rem;
    font-weight: 600;
    color: #2c3e50;
    margin-bottom: 0.5rem;
}
.state-card-subtitle {
    font-size: 1rem;
    color: #7f8c8d;
    margin-bottom: 1rem;
}
.state-card-stats {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 1rem;
    margin-bottom: 1rem;
}
.stat-box {
    background-color: white;
    padding: 0.8rem;
    border-radius: 8px;
    text-align: center;
}
.stat-value {
    font-size: 1.3rem;
    font-weight: 700;
    color: #FF6347;
    margin-bottom: 0.3rem;
}
.stat-label {
    font-size: 0.8rem;
    color: #7f8c8d;
}

/* Challenge & Opportunity Styling */
.challenge-box {
    background-color: #fff8f8;
    padding: 1rem;
    border-radius: 8px;
    margin-bottom: 1rem;
    border-left: 3px solid #e74c3c;
}
.opportunity-box {
    background-color: #f0fff4;
    padding: 1rem;
    border-radius: 8px;
    margin-bottom: 1rem;
    border-left: 3px solid #2ecc71;
}
.box-title {
    font-size: 1.1rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
}
.challenge-box .box-title {
    color: #e74c3c;
}
.opportunity-box .box-title {
    color: #2ecc71;
}
.box-content {
    font-size: 0.95rem;
    color: #555;
    line-height: 1.5;
}

/* Map Container */
.map-container {
    height: 500px;
    width: 100%;
    border-radius: 8px;
    overflow: hidden;
    margin-bottom: 1.5rem;
}

/* Potential Score Badge */
.potential-badge {
    display: inline-block;
    padding: 0.3rem 0.6rem;
    border-radius: 4px;
    font-size: 0.9rem;
    font-weight: 500;
    margin-left: 0.5rem;
    background-color: #3498db;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("""
<div class="header">
    <h1>🏞️ Untouched India Discovery</h1>
    <p>Explore India's hidden cultural treasures - regions rich in heritage but less frequented by tourists. Discover the potential for responsible, community-focused tourism in these untapped destinations.</p>
</div>
""", unsafe_allow_html=True)

# --- Load Data ---
assets_df = get_cultural_assets()
state_coords = get_state_coordinates()
challenges_df = get_challenges_data()

# Merge datasets
merged_df = pd.merge(assets_df, challenges_df, on='state')

# Sort by potential (high potential and low tourists)
potential_df = merged_df.sort_values(by=['potential_score', 'total_tourists'], ascending=[False, True])

# --- Potential Map Section ---
st.markdown('<div class="section-container">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Untapped Cultural Potential Map</div>', unsafe_allow_html=True)
st.markdown('<div class="section-subtitle">Discover regions with rich cultural assets but lower tourist numbers</div>', unsafe_allow_html=True)

# Create map
m = folium.Map(location=[22.5937, 82.9629], zoom_start=5, tiles="cartodbpositron")

# Add markers for each state
for _, state in potential_df.iterrows():
    # Determine marker size based on number of sites
    radius = state['num_sites'] * 1000
    
    # Determine color based on potential score
    if state['potential_score'] >= 8:
        color = '#2ecc71'  # Green for high potential
    elif state['potential_score'] >= 5:
        color = '#f39c12'  # Orange for medium potential
    else:
        color = '#e74c3c'  # Red for low potential
    
    # Create popup content
    popup_html = f"""
    <div style="width: 200px;">
        <h4>{state['state']}</h4>
        <p>Cultural Sites: {state['num_sites']}</p>
        <p>Annual Tourists: {state['total_tourists']:,}</p>
        <p>Potential Score: {state['potential_score']}/10</p>
        <a href="#" onclick="parent.postMessage({{'type': 'streamlit:setComponentValue', 'value': '{state['state']}'}}, '*')">View Details</a>
    </div>
    """
    
    # Add circle marker
    folium.CircleMarker(
        location=[state['latitude'], state['longitude']],
        radius=10,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.7,
        popup=folium.Popup(popup_html, max_width=300),
        tooltip=f"{state['state']} - Potential: {state['potential_score']}/10"
    ).add_to(m)
    
    # Add circle to represent number of sites
    folium.Circle(
        location=[state['latitude'], state['longitude']],
        radius=radius,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.1
    ).add_to(m)

# Display map
# folium_static(m, width=1200, height=600)
st_folium(m, width=1200, height=600)

# Map legend
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div style="display: flex; align-items: center;">
        <div style="width: 15px; height: 15px; border-radius: 50%; background-color: #2ecc71; margin-right: 10px;"></div>
        <span>High Potential (8-10)</span>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div style="display: flex; align-items: center;">
        <div style="width: 15px; height: 15px; border-radius: 50%; background-color: #f39c12; margin-right: 10px;"></div>
        <span>Medium Potential (5-7)</span>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div style="display: flex; align-items: center;">
        <div style="width: 15px; height: 15px; border-radius: 50%; background-color: #e74c3c; margin-right: 10px;"></div>
        <span>Lower Potential (1-4)</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("*Circle size represents the number of cultural sites in each state*")

st.markdown('</div>', unsafe_allow_html=True)

# --- Analysis Dashboard ---
st.markdown('<div class="section-container">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Cultural Assets vs. Tourism Analysis</div>', unsafe_allow_html=True)
st.markdown('<div class="section-subtitle">Understanding the gap between cultural richness and tourist numbers</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    # Scatter plot of sites vs tourists
    fig = px.scatter(
        potential_df,
        x='num_sites',
        y='total_tourists',
        size='potential_score',
        color='potential_score',
        hover_name='state',
        color_continuous_scale=px.colors.sequential.Viridis,
        title='Cultural Sites vs. Tourist Numbers',
        labels={
            'num_sites': 'Number of Cultural Sites',
            'total_tourists': 'Annual Tourists',
            'potential_score': 'Potential Score'
        },
        height=500
    )
    
    fig.update_layout(
        template="plotly_white",
        coloraxis_colorbar=dict(title="Potential Score")
    )
    
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Bar chart of infrastructure challenges
    fig = px.bar(
        potential_df,
        x='state',
        y=['infrastructure_score', 'promotion_score', 'accessibility_score'],
        title='Infrastructure & Promotion Challenges',
        labels={
            'state': 'State',
            'value': 'Score (1-10)',
            'variable': 'Category'
        },
        height=500,
        color_discrete_map={
            'infrastructure_score': '#3498db',
            'promotion_score': '#2ecc71',
            'accessibility_score': '#f39c12'
        }
    )
    
    fig.update_layout(
        template="plotly_white",
        xaxis={'categoryorder': 'total descending'},
        legend=dict(
            title="Challenge Category",
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    # Update legend labels
    newnames = {'infrastructure_score': 'Infrastructure', 'promotion_score': 'Promotion', 'accessibility_score': 'Accessibility'}
    fig.for_each_trace(lambda t: t.update(name = newnames[t.name]))
    
    st.plotly_chart(fig, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# --- Top Untouched Destinations ---
st.markdown('<div class="section-container">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Top Untouched Cultural Destinations</div>', unsafe_allow_html=True)
st.markdown('<div class="section-subtitle">Regions with rich cultural assets but low tourist numbers - perfect for responsible tourism development</div>', unsafe_allow_html=True)

# Display top 5 states with highest potential
top_states = potential_df.head(5)

for _, state in top_states.iterrows():
    st.markdown(f"""
    <div class="state-card">
        <div class="state-card-title">{state['state']} <span class="potential-badge">Potential: {state['potential_score']}/10</span></div>
        <div class="state-card-subtitle">A hidden cultural treasure with {state['num_sites']} significant sites and only {state['total_tourists']:,} annual visitors</div>
        
        <div class="state-card-stats">
            <div class="stat-box">
                <div class="stat-value">{state['num_sites']}</div>
                <div class="stat-label">Cultural Sites</div>
            </div>
            <div class="stat-box">
                <div class="stat-value">{state['domestic_tourists']:,}</div>
                <div class="stat-label">Domestic Tourists</div>
            </div>
            <div class="stat-box">
                <div class="stat-value">{state['foreign_tourists']:,}</div>
                <div class="stat-label">Foreign Tourists</div>
            </div>
            <div class="stat-box">
                <div class="stat-value">{state['infrastructure_score']}/10</div>
                <div class="stat-label">Infrastructure</div>
            </div>
        </div>
        
        <div class="challenge-box">
            <div class="box-title">Why It's Untouched</div>
            <div class="box-content">{state['challenges']}</div>
        </div>
        
        <div class="opportunity-box">
            <div class="box-title">Opportunities for Responsible Tourism</div>
            <div class="box-content">
                {state['opportunities']}<br><br>
                <strong>Unique Cultural Assets:</strong> {state['art_forms']}<br>
                <strong>Local Festivals:</strong> {state['festivals']}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# --- Call to Action ---
st.markdown("""
<div style="background-color: #f8f9fa; padding: 2rem; border-radius: 10px; text-align: center; margin-top: 2rem;">
    <h2 style="color: #2c3e50; margin-bottom: 1rem;">Be a Pioneer in Responsible Tourism</h2>
    <p style="color: #555; font-size: 1.1rem; margin-bottom: 1.5rem;">
        These untouched destinations offer authentic experiences while helping preserve cultural heritage and support local communities.
        Explore these hidden gems and make a positive impact with your travels.
    </p>
    <div style="display: flex; justify-content: center; gap: 1rem;">
        <a href="/Responsible_Tourism_Guide" style="background-color: #FF6347; color: white; padding: 0.8rem 1.5rem; border-radius: 5px; text-decoration: none; font-weight: 500;">Learn About Responsible Tourism</a>
        <a href="/Cultural_Hotspots_Map" style="background-color: #3498db; color: white; padding: 0.8rem 1.5rem; border-radius: 5px; text-decoration: none; font-weight: 500;">Explore All Destinations</a>
    </div>
</div>
""", unsafe_allow_html=True)

# --- Handle map marker clicks ---
if 'selected_state' in st.session_state:
    state_data = potential_df[potential_df['state'] == st.session_state.selected_state].iloc[0]
    
    st.markdown('<div class="section-container">', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">{state_data["state"]} - Detailed Analysis</div>', unsafe_allow_html=True)
    
    # Back button
    if st.button("← Back to Overview"):
        del st.session_state.selected_state
        st.rerun()
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Radar chart for scores
        categories = ['Infrastructure', 'Promotion', 'Accessibility', 'Potential']
        values = [
            state_data['infrastructure_score'],
            state_data['promotion_score'],
            state_data['accessibility_score'],
            state_data['potential_score']
        ]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name=state_data['state'],
            line_color='#FF6347'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 10]
                )
            ),
            title=f"{state_data['state']} - Development Scores",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Pie chart for tourist distribution
        labels = ['Domestic Tourists', 'Foreign Tourists']
        values = [state_data['domestic_tourists'], state_data['foreign_tourists']]
        
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=.4,
            marker_colors=['#3498db', '#2ecc71']
        )])
        
        fig.update_layout(
            title=f"Tourist Distribution in {state_data['state']}",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Challenges and opportunities
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="challenge-box">
            <div class="box-title">Challenges to Tourism Development</div>
            <div class="box-content">{state_data['challenges']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="opportunity-box">
            <div class="box-title">Opportunities for Responsible Tourism</div>
            <div class="box-content">{state_data['opportunities']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Cultural assets
    st.subheader("Cultural Assets")
    st.markdown(f"""
    <div style="background-color: #f8f9fa; padding: 1.5rem; border-radius: 10px; margin-bottom: 1.5rem;">
        <h4 style="color: #2c3e50; margin-bottom: 1rem;">Traditional Art Forms</h4>
        <p>{state_data['art_forms']}</p>
        
        <h4 style="color: #2c3e50; margin-top: 1.5rem; margin-bottom: 1rem;">Local Festivals</h4>
        <p>{state_data['festivals']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Recommendations
    st.subheader("Recommendations for Sustainable Development")
    
    recommendations = [
        f"Improve infrastructure while preserving the natural and cultural environment",
        f"Develop digital presence to showcase {state_data['state']}'s unique cultural offerings",
        f"Create community-based tourism initiatives that directly benefit local artisans",
        f"Establish partnerships with responsible tour operators specializing in cultural tourism",
        f"Develop training programs for local guides to share authentic cultural stories"
    ]
    
    for i, rec in enumerate(recommendations):
        st.markdown(f"""
        <div style="display: flex; align-items: flex-start; margin-bottom: 1rem;">
            <div style="background-color: #FF6347; color: white; width: 25px; height: 25px; border-radius: 50%; display: flex; justify-content: center; align-items: center; margin-right: 10px; flex-shrink: 0;">{i+1}</div>
            <div>{rec}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)