import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random
from datetime import datetime

# --- Page Configuration ---
st.set_page_config(
    page_title="Government Impact Dashboard | Cultural Canvas India",
    layout="wide",
    initial_sidebar_state="auto",
    page_icon="📊"
)

# --- Simulated Database Functions ---
def get_government_funding():
    """Fetch government funding data (simulated)"""
    states = [
        'Andhra Pradesh', 'Assam', 'Bihar', 'Chhattisgarh', 'Gujarat',
        'Haryana', 'Himachal Pradesh', 'Jharkhand', 'Karnataka', 'Kerala',
        'Madhya Pradesh', 'Maharashtra', 'Odisha', 'Punjab', 'Rajasthan',
        'Tamil Nadu', 'Telangana', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal'
    ]
    
    schemes = [
        'Swadesh Darshan Scheme',
        'PRASAD (Pilgrimage Rejuvenation and Spiritual Augmentation Drive)',
        'Museum Grant Scheme',
        'Cultural Function Grant Scheme',
        'National Mission on Cultural Mapping',
        'Tribal Art Development Scheme',
        'Heritage City Development and Augmentation Yojana (HRIDAY)',
        'National Handicraft Development Program',
        'Preservation and Development of Cultural Heritage of Himalayas',
        'Scheme for Safeguarding the Intangible Cultural Heritage'
    ]
    
    objectives = [
        'Preservation', 'Promotion', 'Infrastructure', 'Education',
        'Documentation', 'Digitization', 'Skill Development', 'Research'
    ]
    
    years = list(range(2018, 2024))
    
    data = []
    for state in states:
        # Each state gets 3-5 schemes
        state_schemes = random.sample(schemes, random.randint(3, 5))
        
        for scheme in state_schemes:
            # Each scheme has 1-3 objectives
            scheme_objectives = random.sample(objectives, random.randint(1, 3))
            
            for year in years:
                # Generate random funding amount (in lakhs)
                funding = random.randint(50, 1000)
                
                # Generate random utilization percentage
                utilization = random.randint(60, 100)
                
                # Generate random number of beneficiaries
                beneficiaries = random.randint(500, 10000)
                
                data.append({
                    'state': state,
                    'scheme': scheme,
                    'objective': ', '.join(scheme_objectives),
                    'year': year,
                    'funding_lakhs': funding,
                    'utilization_percentage': utilization,
                    'beneficiaries': beneficiaries
                })
    
    return pd.DataFrame(data)

def get_artisan_registrations():
    """Fetch artisan registration data (simulated)"""
    states = [
        'Andhra Pradesh', 'Assam', 'Bihar', 'Chhattisgarh', 'Gujarat',
        'Haryana', 'Himachal Pradesh', 'Jharkhand', 'Karnataka', 'Kerala',
        'Madhya Pradesh', 'Maharashtra', 'Odisha', 'Punjab', 'Rajasthan',
        'Tamil Nadu', 'Telangana', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal'
    ]
    
    years = list(range(2018, 2024))
    
    data = []
    for state in states:
        # Base number of artisans for each state
        base_artisans = random.randint(1000, 5000)
        
        for year in years:
            # Growth factor (increasing over years)
            growth_factor = 1 + (year - 2018) * 0.05
            
            # Calculate number of artisans with some randomness
            artisans = int(base_artisans * growth_factor * random.uniform(0.9, 1.1))
            
            # Calculate percentage of women artisans
            women_percentage = random.randint(30, 60)
            
            # Calculate percentage with digital presence
            digital_percentage = min(80, 20 + (year - 2018) * 10)  # Increasing digital presence over years
            
            data.append({
                'state': state,
                'year': year,
                'registered_artisans': artisans,
                'women_percentage': women_percentage,
                'digital_percentage': digital_percentage
            })
    
    return pd.DataFrame(data)

def get_tourism_impact():
    """Fetch tourism impact data (simulated)"""
    states = [
        'Andhra Pradesh', 'Assam', 'Bihar', 'Chhattisgarh', 'Gujarat',
        'Haryana', 'Himachal Pradesh', 'Jharkhand', 'Karnataka', 'Kerala',
        'Madhya Pradesh', 'Maharashtra', 'Odisha', 'Punjab', 'Rajasthan',
        'Tamil Nadu', 'Telangana', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal'
    ]
    
    years = list(range(2018, 2024))
    
    data = []
    for state in states:
        # Base values for each state
        base_revenue = random.randint(500, 5000)  # in crores
        base_employment = random.randint(10000, 100000)
        base_tourists = random.randint(500000, 5000000)
        
        for year in years:
            # Growth factor (increasing over years, with dip in 2020-2021 for COVID)
            if year in [2020, 2021]:
                growth_factor = 0.6  # COVID impact
            else:
                growth_factor = 1 + (year - 2018) * 0.08
            
            # Calculate values with some randomness
            revenue = int(base_revenue * growth_factor * random.uniform(0.9, 1.1))
            employment = int(base_employment * growth_factor * random.uniform(0.9, 1.1))
            tourists = int(base_tourists * growth_factor * random.uniform(0.9, 1.1))
            
            # Calculate cultural tourism percentage
            cultural_percentage = random.randint(30, 70)
            
            data.append({
                'state': state,
                'year': year,
                'tourism_revenue_crores': revenue,
                'tourism_employment': employment,
                'tourist_arrivals': tourists,
                'cultural_tourism_percentage': cultural_percentage
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

/* Dashboard Section Styling */
.dashboard-section {
    background-color: white;
    border-radius: 10px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    padding: 1.5rem;
    margin-bottom: 2rem;
}
.section-title {
    font-size: 1.5rem;
    font-weight: 600;
    color: #2c3e50;
    margin-bottom: 1rem;
    border-bottom: 2px solid #f0f0f0;
    padding-bottom: 0.5rem;
}

/* Filter Section */
.filter-section {
    background-color: #f8f9fa;
    padding: 1.5rem;
    border-radius: 10px;
    margin-bottom: 2rem;
    box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}

/* KPI Card Styling */
.kpi-container {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    margin-bottom: 1.5rem;
}
.kpi-card {
    background-color: #f8f9fa;
    border-radius: 10px;
    padding: 1.2rem;
    flex: 1;
    min-width: 200px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    text-align: center;
    transition: transform 0.3s ease;
}
.kpi-card:hover {
    transform: translateY(-5px);
}
.kpi-value {
    font-size: 2rem;
    font-weight: 700;
    color: #3498db;
    margin-bottom: 0.5rem;
}
.kpi-label {
    font-size: 1rem;
    color: #7f8c8d;
}
.kpi-trend {
    font-size: 0.9rem;
    margin-top: 0.5rem;
}
.trend-up {
    color: #2ecc71;
}
.trend-down {
    color: #e74c3c;
}

/* Chart Container */
.chart-container {
    background-color: white;
    border-radius: 10px;
    padding: 1rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}

/* Insight Box */
.insight-box {
    background-color: #f0f9ff;
    border-radius: 10px;
    padding: 1.5rem;
    margin-top: 1.5rem;
    border-left: 5px solid #3498db;
}
.insight-title {
    font-size: 1.2rem;
    font-weight: 600;
    color: #2c3e50;
    margin-bottom: 0.5rem;
}
.insight-content {
    font-size: 1rem;
    color: #555;
    line-height: 1.5;
}

/* Table Styling */
.styled-table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 1.5rem;
    font-size: 0.9rem;
}
.styled-table th {
    background-color: #f8f9fa;
    color: #2c3e50;
    font-weight: 600;
    text-align: left;
    padding: 0.8rem;
    border-bottom: 2px solid #e0e0e0;
}
.styled-table td {
    padding: 0.8rem;
    border-bottom: 1px solid #e0e0e0;
}
.styled-table tr:hover {
    background-color: #f8f9fa;
}
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("""
<div class="header">
    <h1>📊 Government Impact Dashboard</h1>
    <p>Explore how government funds are being utilized to preserve and promote India's cultural heritage. This dashboard provides transparency on funding allocation, utilization, and outcomes.</p>
</div>
""", unsafe_allow_html=True)

# --- Load Data ---
funding_df = get_government_funding()
artisan_df = get_artisan_registrations()
tourism_df = get_tourism_impact()

# --- Filters ---
st.markdown('<div class="filter-section">', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    selected_year = st.selectbox(
        "Select Year",
        sorted(funding_df['year'].unique(), reverse=True)
    )

with col2:
    all_states = sorted(funding_df['state'].unique())
    selected_state = st.selectbox(
        "Select State",
        ["All States"] + all_states
    )

with col3:
    all_schemes = sorted(funding_df['scheme'].unique())
    selected_scheme = st.selectbox(
        "Select Scheme",
        ["All Schemes"] + all_schemes
    )

st.markdown('</div>', unsafe_allow_html=True)

# --- Filter Data ---
filtered_funding = funding_df.copy()
filtered_artisan = artisan_df.copy()
filtered_tourism = tourism_df.copy()

# Apply year filter to all datasets
filtered_funding = filtered_funding[filtered_funding['year'] == selected_year]
filtered_artisan = filtered_artisan[filtered_artisan['year'] == selected_year]
filtered_tourism = filtered_tourism[filtered_tourism['year'] == selected_year]

# Apply state filter if not "All States"
if selected_state != "All States":
    filtered_funding = filtered_funding[filtered_funding['state'] == selected_state]
    filtered_artisan = filtered_artisan[filtered_artisan['state'] == selected_state]
    filtered_tourism = filtered_tourism[filtered_tourism['state'] == selected_state]

# Apply scheme filter if not "All Schemes"
if selected_scheme != "All Schemes":
    filtered_funding = filtered_funding[filtered_funding['scheme'] == selected_scheme]

# --- KPI Section ---
st.markdown('<div class="dashboard-section">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Key Performance Indicators</div>', unsafe_allow_html=True)

# Calculate KPIs
total_funding = filtered_funding['funding_lakhs'].sum()
avg_utilization = filtered_funding['utilization_percentage'].mean()
total_beneficiaries = filtered_funding['beneficiaries'].sum()
total_artisans = filtered_artisan['registered_artisans'].sum()
total_tourism_revenue = filtered_tourism['tourism_revenue_crores'].sum()
total_employment = filtered_tourism['tourism_employment'].sum()

# Calculate year-over-year changes
prev_year = selected_year - 1
prev_funding = funding_df[funding_df['year'] == prev_year]
prev_artisan = artisan_df[artisan_df['year'] == prev_year]
prev_tourism = tourism_df[tourism_df['year'] == prev_year]

# Apply state filter to previous year data if needed
if selected_state != "All States":
    prev_funding = prev_funding[prev_funding['state'] == selected_state]
    prev_artisan = prev_artisan[prev_artisan['state'] == selected_state]
    prev_tourism = prev_tourism[prev_tourism['state'] == selected_state]

# Apply scheme filter to previous year data if needed
if selected_scheme != "All Schemes":
    prev_funding = prev_funding[prev_funding['scheme'] == selected_scheme]

# Calculate previous year KPIs
prev_total_funding = prev_funding['funding_lakhs'].sum() if not prev_funding.empty else 0
prev_total_artisans = prev_artisan['registered_artisans'].sum() if not prev_artisan.empty else 0
prev_total_tourism_revenue = prev_tourism['tourism_revenue_crores'].sum() if not prev_tourism.empty else 0

# Calculate percentage changes
funding_change = ((total_funding - prev_total_funding) / prev_total_funding * 100) if prev_total_funding > 0 else 0
artisan_change = ((total_artisans - prev_total_artisans) / prev_total_artisans * 100) if prev_total_artisans > 0 else 0
revenue_change = ((total_tourism_revenue - prev_total_tourism_revenue) / prev_total_tourism_revenue * 100) if prev_total_tourism_revenue > 0 else 0

# Display KPIs
st.markdown('<div class="kpi-container">', unsafe_allow_html=True)

# Funding KPI
st.markdown(f"""
<div class="kpi-card">
    <div class="kpi-value">₹{total_funding:,.0f} Lakhs</div>
    <div class="kpi-label">Total Funding Allocated</div>
    <div class="kpi-trend {'trend-up' if funding_change >= 0 else 'trend-down'}">
        {'+' if funding_change >= 0 else ''}{funding_change:.1f}% from previous year
    </div>
</div>
""", unsafe_allow_html=True)

# Utilization KPI
st.markdown(f"""
<div class="kpi-card">
    <div class="kpi-value">{avg_utilization:.1f}%</div>
    <div class="kpi-label">Average Fund Utilization</div>
</div>
""", unsafe_allow_html=True)

# Beneficiaries KPI
st.markdown(f"""
<div class="kpi-card">
    <div class="kpi-value">{total_beneficiaries:,}</div>
    <div class="kpi-label">Total Beneficiaries</div>
</div>
""", unsafe_allow_html=True)

# Artisans KPI
st.markdown(f"""
<div class="kpi-card">
    <div class="kpi-value">{total_artisans:,}</div>
    <div class="kpi-label">Registered Artisans</div>
    <div class="kpi-trend {'trend-up' if artisan_change >= 0 else 'trend-down'}">
        {'+' if artisan_change >= 0 else ''}{artisan_change:.1f}% from previous year
    </div>
</div>
""", unsafe_allow_html=True)

# Tourism Revenue KPI
st.markdown(f"""
<div class="kpi-card">
    <div class="kpi-value">₹{total_tourism_revenue:,} Cr</div>
    <div class="kpi-label">Tourism Revenue</div>
    <div class="kpi-trend {'trend-up' if revenue_change >= 0 else 'trend-down'}">
        {'+' if revenue_change >= 0 else ''}{revenue_change:.1f}% from previous year
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# --- Funding Allocation Section ---
st.markdown('<div class="dashboard-section">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Funding Allocation Analysis</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    # State-wise funding allocation
    if selected_state == "All States":
        state_funding = filtered_funding.groupby('state')['funding_lakhs'].sum().reset_index()
        state_funding = state_funding.sort_values('funding_lakhs', ascending=False)
        
        fig = px.bar(
            state_funding,
            x='state',
            y='funding_lakhs',
            title='Funding Allocation by State',
            labels={'state': 'State', 'funding_lakhs': 'Funding (Lakhs)'},
            color='funding_lakhs',
            color_continuous_scale=px.colors.sequential.Blues
        )
        
        fig.update_layout(
            xaxis={'categoryorder': 'total descending'},
            height=500,
            template="plotly_white"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        # Scheme-wise funding for selected state
        scheme_funding = filtered_funding.groupby('scheme')['funding_lakhs'].sum().reset_index()
        scheme_funding = scheme_funding.sort_values('funding_lakhs', ascending=False)
        
        fig = px.bar(
            scheme_funding,
            x='scheme',
            y='funding_lakhs',
            title=f'Funding Allocation by Scheme in {selected_state}',
            labels={'scheme': 'Scheme', 'funding_lakhs': 'Funding (Lakhs)'},
            color='funding_lakhs',
            color_continuous_scale=px.colors.sequential.Blues
        )
        
        fig.update_layout(
            xaxis={'categoryorder': 'total descending'},
            height=500,
            template="plotly_white"
        )
        
        st.plotly_chart(fig, use_container_width=True)

with col2:
    # Objective-wise funding allocation
    # First, split the comma-separated objectives into separate rows
    objectives_expanded = []
    for _, row in filtered_funding.iterrows():
        for objective in row['objective'].split(', '):
            objectives_expanded.append({
                'state': row['state'],
                'scheme': row['scheme'],
                'objective': objective.strip(),
                'funding_lakhs': row['funding_lakhs'] / len(row['objective'].split(', '))  # Divide funding equally among objectives
            })
    
    objectives_df = pd.DataFrame(objectives_expanded)
    objective_funding = objectives_df.groupby('objective')['funding_lakhs'].sum().reset_index()
    objective_funding = objective_funding.sort_values('funding_lakhs', ascending=False)
    
    fig = px.pie(
        objective_funding,
        values='funding_lakhs',
        names='objective',
        title='Funding Allocation by Objective',
        color_discrete_sequence=px.colors.qualitative.Set3,
        hole=0.4
    )
    
    fig.update_layout(
        height=500,
        template="plotly_white"
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Funding utilization analysis
utilization_data = filtered_funding.copy()
utilization_data['utilized_funding'] = utilization_data['funding_lakhs'] * utilization_data['utilization_percentage'] / 100
utilization_data['unutilized_funding'] = utilization_data['funding_lakhs'] - utilization_data['utilized_funding']

# Group by scheme for utilization analysis
scheme_utilization = utilization_data.groupby('scheme').agg({
    'funding_lakhs': 'sum',
    'utilized_funding': 'sum',
    'unutilized_funding': 'sum'
}).reset_index()

scheme_utilization['utilization_percentage'] = scheme_utilization['utilized_funding'] / scheme_utilization['funding_lakhs'] * 100
scheme_utilization = scheme_utilization.sort_values('utilization_percentage', ascending=False)

fig = px.bar(
    scheme_utilization,
    x='scheme',
    y=['utilized_funding', 'unutilized_funding'],
    title='Fund Utilization by Scheme',
    labels={
        'scheme': 'Scheme',
        'value': 'Funding (Lakhs)',
        'variable': 'Category'
    },
    color_discrete_map={
        'utilized_funding': '#2ecc71',
        'unutilized_funding': '#e74c3c'
    },
    barmode='stack'
)

fig.update_layout(
    xaxis={'categoryorder': 'total descending'},
    height=500,
    template="plotly_white",
    legend=dict(
        title="",
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    )
)

# Update legend labels
newnames = {'utilized_funding': 'Utilized Funds', 'unutilized_funding': 'Unutilized Funds'}
fig.for_each_trace(lambda t: t.update(name = newnames[t.name]))

st.plotly_chart(fig, use_container_width=True)

# Insights box
st.markdown('<div class="insight-box">', unsafe_allow_html=True)
st.markdown('<div class="insight-title">Key Insights on Funding Allocation</div>', unsafe_allow_html=True)

# Generate insights based on the data
top_funded_state = state_funding.iloc[0]['state'] if 'state_funding' in locals() else filtered_funding['state'].iloc[0]
top_funded_scheme = scheme_funding.iloc[0]['scheme'] if 'scheme_funding' in locals() else filtered_funding['scheme'].iloc[0]
top_objective = objective_funding.iloc[0]['objective']
highest_utilization_scheme = scheme_utilization.iloc[0]['scheme']
lowest_utilization_scheme = scheme_utilization.iloc[-1]['scheme']
highest_utilization_percentage = scheme_utilization.iloc[0]['utilization_percentage']
lowest_utilization_percentage = scheme_utilization.iloc[-1]['utilization_percentage']

insights = f"""
- The highest funding allocation is directed towards {'states like ' + top_funded_state if selected_state == 'All States' else 'schemes like ' + top_funded_scheme}.
- {top_objective} is the primary objective receiving the largest share of funding.
- {highest_utilization_scheme} shows the highest fund utilization rate at {highest_utilization_percentage:.1f}%.
- {lowest_utilization_scheme} has the lowest utilization at {lowest_utilization_percentage:.1f}%, suggesting potential implementation challenges.
"""

st.markdown(f'<div class="insight-content">{insights}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# --- Artisan Impact Section ---
st.markdown('<div class="dashboard-section">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Artisan Development & Cultural Preservation</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    # Artisan registration trend over years
    if selected_state != "All States":
        artisan_trend = artisan_df[artisan_df['state'] == selected_state].groupby('year').agg({
            'registered_artisans': 'sum',
            'women_percentage': 'mean',
            'digital_percentage': 'mean'
        }).reset_index()
    else:
        artisan_trend = artisan_df.groupby('year').agg({
            'registered_artisans': 'sum',
            'women_percentage': 'mean',
            'digital_percentage': 'mean'
        }).reset_index()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=artisan_trend['year'],
        y=artisan_trend['registered_artisans'],
        mode='lines+markers',
        name='Registered Artisans',
        line=dict(color='#3498db', width=3),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title=f"Artisan Registration Trend ({selected_state if selected_state != 'All States' else 'All India'})",
        xaxis_title="Year",
        yaxis_title="Number of Artisans",
        template="plotly_white",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Women artisans and digital presence
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=artisan_trend['year'],
        y=artisan_trend['women_percentage'],
        name='Women Artisans (%)',
        marker_color='#e74c3c'
    ))
    
    fig.add_trace(go.Scatter(
        x=artisan_trend['year'],
        y=artisan_trend['digital_percentage'],
        mode='lines+markers',
        name='Digital Presence (%)',
        line=dict(color='#2ecc71', width=3),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title="Women Participation & Digital Presence",
        xaxis_title="Year",
        yaxis_title="Percentage",
        template="plotly_white",
        height=400,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)

# State-wise artisan comparison
if selected_state == "All States":
    artisan_state = filtered_artisan.copy()
    artisan_state = artisan_state.sort_values('registered_artisans', ascending=False)
    
    fig = px.scatter(
        artisan_state,
        x='women_percentage',
        y='digital_percentage',
        size='registered_artisans',
        color='registered_artisans',
        hover_name='state',
        color_continuous_scale=px.colors.sequential.Viridis,
        title='State-wise Artisan Analysis',
        labels={
            'women_percentage': 'Women Artisans (%)',
            'digital_percentage': 'Digital Presence (%)',
            'registered_artisans': 'Registered Artisans'
        }
    )
    
    fig.update_layout(
        height=500,
        template="plotly_white"
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Correlation between funding and artisan growth
if selected_state == "All States":
    # Prepare data for correlation analysis
    funding_by_state = filtered_funding.groupby('state')['funding_lakhs'].sum().reset_index()
    artisan_by_state = filtered_artisan.groupby('state')['registered_artisans'].sum().reset_index()
    
    correlation_data = pd.merge(funding_by_state, artisan_by_state, on='state')
    
    fig = px.scatter(
        correlation_data,
        x='funding_lakhs',
        y='registered_artisans',
        hover_name='state',
        trendline="ols",
        title='Correlation: Funding vs. Artisan Registration',
        labels={
            'funding_lakhs': 'Funding Allocation (Lakhs)',
            'registered_artisans': 'Registered Artisans'
        }
    )
    
    fig.update_layout(
        height=500,
        template="plotly_white"
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Insights box
st.markdown('<div class="insight-box">', unsafe_allow_html=True)
st.markdown('<div class="insight-title">Key Insights on Artisan Development</div>', unsafe_allow_html=True)

# Generate insights based on the data
latest_year_data = artisan_trend.iloc[-1]
earliest_year_data = artisan_trend.iloc[0]
artisan_growth = (latest_year_data['registered_artisans'] - earliest_year_data['registered_artisans']) / earliest_year_data['registered_artisans'] * 100
women_growth = latest_year_data['women_percentage'] - earliest_year_data['women_percentage']
digital_growth = latest_year_data['digital_percentage'] - earliest_year_data['digital_percentage']

if 'correlation_data' in locals():
    correlation = correlation_data['funding_lakhs'].corr(correlation_data['registered_artisans'])
    correlation_insight = f"There is a {'strong' if abs(correlation) > 0.7 else 'moderate' if abs(correlation) > 0.4 else 'weak'} correlation ({correlation:.2f}) between funding allocation and artisan registration, suggesting that {'government funding is effectively supporting artisan development' if correlation > 0 else 'funding may not be reaching artisan communities effectively'}."
else:
    correlation_insight = ""

insights = f"""
- Artisan registration has {'increased' if artisan_growth > 0 else 'decreased'} by {abs(artisan_growth):.1f}% from {earliest_year_data['year']} to {latest_year_data['year']}.
- Women's participation in artisanal crafts has {'increased' if women_growth > 0 else 'decreased'} by {abs(women_growth):.1f} percentage points.
- Digital presence of artisans has {'increased' if digital_growth > 0 else 'decreased'} by {abs(digital_growth):.1f} percentage points, reflecting {'successful digital empowerment initiatives' if digital_growth > 0 else 'challenges in digital adoption'}.
- {correlation_insight}
"""

st.markdown(f'<div class="insight-content">{insights}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# --- Tourism Impact Section ---
st.markdown('<div class="dashboard-section">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Tourism Impact & Economic Outcomes</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    # Tourism revenue trend
    if selected_state != "All States":
        tourism_trend = tourism_df[tourism_df['state'] == selected_state].groupby('year').agg({
            'tourism_revenue_crores': 'sum',
            'tourism_employment': 'sum',
            'tourist_arrivals': 'sum',
            'cultural_tourism_percentage': 'mean'
        }).reset_index()
    else:
        tourism_trend = tourism_df.groupby('year').agg({
            'tourism_revenue_crores': 'sum',
            'tourism_employment': 'sum',
            'tourist_arrivals': 'sum',
            'cultural_tourism_percentage': 'mean'
        }).reset_index()
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=tourism_trend['year'],
        y=tourism_trend['tourism_revenue_crores'],
        name='Tourism Revenue (Crores)',
        marker_color='#3498db'
    ))
    
    fig.add_trace(go.Scatter(
        x=tourism_trend['year'],
        y=tourism_trend['cultural_tourism_percentage'],
        mode='lines+markers',
        name='Cultural Tourism (%)',
        line=dict(color='#e74c3c', width=3),
        marker=dict(size=8),
        yaxis='y2'
    ))
    
    fig.update_layout(
        title=f"Tourism Revenue & Cultural Tourism Percentage ({selected_state if selected_state != 'All States' else 'All India'})",
        xaxis_title="Year",
        yaxis_title="Revenue (Crores)",
        yaxis2=dict(
            title="Cultural Tourism (%)",
            overlaying="y",
            side="right",
            range=[0, 100]
        ),
        template="plotly_white",
        height=400,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Tourism employment and arrivals
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=tourism_trend['year'],
        y=tourism_trend['tourism_employment'],
        name='Tourism Employment',
        marker_color='#2ecc71'
    ))
    
    fig.add_trace(go.Scatter(
        x=tourism_trend['year'],
        y=tourism_trend['tourist_arrivals'],
        mode='lines+markers',
        name='Tourist Arrivals',
        line=dict(color='#f39c12', width=3),
        marker=dict(size=8),
        yaxis='y2'
    ))
    
    fig.update_layout(
        title="Tourism Employment & Tourist Arrivals",
        xaxis_title="Year",
        yaxis_title="Employment",
        yaxis2=dict(
            title="Tourist Arrivals",
            overlaying="y",
            side="right"
        ),
        template="plotly_white",
        height=400,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)

# State-wise tourism comparison
if selected_state == "All States":
    tourism_state = filtered_tourism.copy()
    tourism_state = tourism_state.sort_values('tourism_revenue_crores', ascending=False)
    
    fig = px.scatter(
        tourism_state,
        x='cultural_tourism_percentage',
        y='tourism_revenue_crores',
        size='tourist_arrivals',
        color='tourism_employment',
        hover_name='state',
        color_continuous_scale=px.colors.sequential.Viridis,
        title='State-wise Tourism Analysis',
        labels={
            'cultural_tourism_percentage': 'Cultural Tourism (%)',
            'tourism_revenue_crores': 'Tourism Revenue (Crores)',
            'tourist_arrivals': 'Tourist Arrivals',
            'tourism_employment': 'Tourism Employment'
        }
    )
    
    fig.update_layout(
        height=500,
        template="plotly_white"
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Correlation between funding and tourism revenue
if selected_state == "All States":
    # Prepare data for correlation analysis
    funding_by_state = filtered_funding.groupby('state')['funding_lakhs'].sum().reset_index()
    tourism_by_state = filtered_tourism.groupby('state')['tourism_revenue_crores'].sum().reset_index()
    
    correlation_data_tourism = pd.merge(funding_by_state, tourism_by_state, on='state')
    
    fig = px.scatter(
        correlation_data_tourism,
        x='funding_lakhs',
        y='tourism_revenue_crores',
        hover_name='state',
        trendline="ols",
        title='Correlation: Cultural Funding vs. Tourism Revenue',
        labels={
            'funding_lakhs': 'Cultural Funding Allocation (Lakhs)',
            'tourism_revenue_crores': 'Tourism Revenue (Crores)'
        }
    )
    
    fig.update_layout(
        height=500,
        template="plotly_white"
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Insights box
st.markdown('<div class="insight-box">', unsafe_allow_html=True)
st.markdown('<div class="insight-title">Key Insights on Tourism Impact</div>', unsafe_allow_html=True)

# Generate insights based on the data
latest_year_data = tourism_trend.iloc[-1]
earliest_year_data = tourism_trend.iloc[0]
revenue_growth = (latest_year_data['tourism_revenue_crores'] - earliest_year_data['tourism_revenue_crores']) / earliest_year_data['tourism_revenue_crores'] * 100
employment_growth = (latest_year_data['tourism_employment'] - earliest_year_data['tourism_employment']) / earliest_year_data['tourism_employment'] * 100
arrivals_growth = (latest_year_data['tourist_arrivals'] - earliest_year_data['tourist_arrivals']) / earliest_year_data['tourist_arrivals'] * 100
cultural_tourism_change = latest_year_data['cultural_tourism_percentage'] - earliest_year_data['cultural_tourism_percentage']

if 'correlation_data_tourism' in locals():
    correlation = correlation_data_tourism['funding_lakhs'].corr(correlation_data_tourism['tourism_revenue_crores'])
    correlation_insight = f"There is a {'strong' if abs(correlation) > 0.7 else 'moderate' if abs(correlation) > 0.4 else 'weak'} correlation ({correlation:.2f}) between cultural funding and tourism revenue, suggesting that {'investments in cultural preservation and promotion are effectively driving tourism growth' if correlation > 0 else 'cultural funding may need better alignment with tourism development strategies'}."
else:
    correlation_insight = ""

# Find this problematic section (around line 976):
cultural_heritage_text = "growing interest in India's cultural heritage" if cultural_tourism_change > 0 else "potential need for better cultural tourism promotion"

insights = f"""
- Tourism revenue has {'increased' if revenue_growth > 0 else 'decreased'} by {abs(revenue_growth):.1f}% from {earliest_year_data['year']} to {latest_year_data['year']}.
- Tourism-related employment has {'grown' if employment_growth > 0 else 'declined'} by {abs(employment_growth):.1f}%, creating {'new opportunities in the cultural tourism sector' if employment_growth > 0 else 'challenges for workers in the tourism industry'}.
- Tourist arrivals have {'increased' if arrivals_growth > 0 else 'decreased'} by {abs(arrivals_growth):.1f}%.
- Cultural tourism as a percentage of overall tourism has {'increased' if cultural_tourism_change > 0 else 'decreased'} by {abs(cultural_tourism_change):.1f} percentage points, indicating {cultural_heritage_text}.
- {correlation_insight}
"""

st.markdown(f'<div class="insight-content">{insights}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# --- Detailed Data Tables ---
st.markdown('<div class="dashboard-section">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Detailed Data Tables</div>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["Funding Data", "Artisan Data", "Tourism Data"])

with tab1:
    st.dataframe(filtered_funding.sort_values('funding_lakhs', ascending=False), use_container_width=True)

with tab2:
    st.dataframe(filtered_artisan.sort_values('registered_artisans', ascending=False), use_container_width=True)

with tab3:
    st.dataframe(filtered_tourism.sort_values('tourism_revenue_crores', ascending=False), use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# --- Footer ---
st.markdown("""
<div style="text-align: center; padding: 20px; font-size: 0.9rem; color: #555; margin-top: 2rem;">
    <p><strong>Government Impact Dashboard</strong> - Part of the Cultural Canvas of India project</p>
    <p>Data sourced from public records including <a href="https://data.gov.in" target="_blank">data.gov.in</a>, Ministry of Culture, and Ministry of Tourism.</p>
    <p>Last updated: May 2023</p>
</div>
""", unsafe_allow_html=True)