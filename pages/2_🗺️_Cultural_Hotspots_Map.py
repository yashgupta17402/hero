import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.express as px
import plotly.graph_objects as go
# from datetime import datetime # Not used in the provided snippet
# import random # Not used in the provided snippet

# --- Page Configuration ---
st.set_page_config(
    page_title="Cultural Canvas India | Heritage Sites & Visitor Stats",
    layout="wide",
    initial_sidebar_state="auto",
    page_icon="🏛️"
)

# --- Snowflake Connection ---
def get_snowflake_connection():
    """Helper function to get Snowflake connection."""
    return st.connection("snowflake")

# --- Load UNESCO Sites Data from Snowflake ---
def load_unesco_sites_from_snowflake():
    """Load UNESCO World Heritage Sites data from Snowflake."""
    try:
        conn = get_snowflake_connection()
        query = """
        SELECT
            NAME AS "Name",
            CITY AS "City",
            DISTRICT AS "District",
            STATE_UT AS "State/UT",
            DESCRIPTION AS "Short Description",
            LATITUDE AS "Latitude",
            LONGITUDE AS "Longitude"
        FROM UNESCO_INDIA_SITES;
        """
        df = conn.query(query, ttl=3600)
        if "Latitude" in df.columns:
            df["Latitude"] = pd.to_numeric(df["Latitude"], errors='coerce')
        if "Longitude" in df.columns:
            df["Longitude"] = pd.to_numeric(df["Longitude"], errors='coerce')
        df.dropna(subset=["Latitude", "Longitude"], inplace=True)
        return df
    except Exception as e:
        st.error(f"Error loading UNESCO sites from Snowflake: {e}")
        return pd.DataFrame()

# --- Dummy Data Loaders for ASI Visitor Statistics ---
# !!! IMPORTANT: Replace these with your actual data loading functions !!!
def load_asi_visitor_trends_data():
    """
    Loads dummy data mimicking Table 4.2.1: Visitors to Centrally Protected Ticketed Monuments.
    Replace this with your actual data source.
    """
    data = {
        'Year': ['1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016-17*', '2017-18', '2018-19', '2019-20', '2020-21', '2021-22', '2022-23', '2023-24'],
        'No. of Centrally Protected Ticketed ASI Monuments': [68, 68, 68, 68, 126, 126, 126, 126, 116, 116, 116, 116, 117, 119, 116, 116, 116, 116, 116, 116, 116, 116, 116, 116, 136, 144, 144, 145],
        'Domestic Visitors': ['N.A', 'N.A', 'N.A', 'N.A', 'N.A', 'N.A', 17333055, 19551820, 20356940, 21035864, 23815252, 23450419, 28786608, 30804103, 35770242, 40534481, 43259075, 43019998, 45425859, 50988730, 40167938, 48394768, 47316029, 43607075, 13153076, 26046891, 47901021, 53090007],
        'Foreign Visitors': ['N.A', 'N.A', 'N.A', 'N.A', 'N.A', 'N.A', 837012, 1216615, 1788753, 2122436, 2250502, 2614254, 2679763, 2195382, 2998175, 2948065, 3064778, 2995852, 2792272, 2620228, 2379389, 3397673, 3576837, 2756561, 415859, 116114, 1445363, 2314641],
        'Total Visitors': [10956764, 15767820, 13317242, 20502547, 19539127, 20364901, 18170067, 20768435, 22145693, 23158300, 26065754, 26064673, 31466371, 32999485, 38768417, 43482546, 46323853, 46015850, 48218131, 53608958, 42547327, 51792441, 50892866, 46363636, 13568935, 26163005, 49346384, 55404648],
        'Domestic Growth Rate (%)': ['-', '-', '-', '-', '-', '-', '-', 12.80, 4.1, 3.3, 13.2, -1.5, 22.8, 7.0, 16.1, 13.3, 6.7, -0.6, 5.6, 12.2, -21.2, 20.5, -2.2, -7.8, -69.8, 98.0, 83.9, 10.8],
        'Foreign Growth Rate (%)': ['-', '-', '-', '-', '-', '-', '-', 45.4, 47.0, 18.7, 6.0, 16.2, 2.5, -18.1, 36.6, -1.7, 4.0, -2.2, -6.8, -6.2, -9.2, 42.8, 5.3, -22.9, -84.9, -72.0, 1144.7, 60.1],
        'Total Growth Rate (%)': ['-', '-', 43.9, -15.5, 54.0, -4.7, -4.2, 10.8, 14.3, 6.6, 4.6, 12.6, 0.0, 20.7, 4.9, 17.5, 12.0, 6.5, -0.7, 4.8, -11.2, -20.6, 25.4, -1.7, -7.0, -70.7, 92.8, 88.6] # Corrected length
    }
    df = pd.DataFrame(data)
    # Convert growth rates to numeric, coercing errors for '-'
    for col in ['Domestic Growth Rate (%)', 'Foreign Growth Rate (%)', 'Total Growth Rate (%)']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    # Convert visitor numbers to numeric, coercing errors for 'N.A'
    for col in ['Domestic Visitors', 'Foreign Visitors', 'Total Visitors', 'No. of Centrally Protected Ticketed ASI Monuments']: # Added last one for potential charting
        df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', ''), errors='coerce')
    return df

def load_asi_top_monuments_data():
    """
    Loads dummy data mimicking Table 4.2.2: Top 10 ASI Monuments by Visitors FY 2023-24.
    Replace this with your actual data source.
    """
    domestic_data = {
        'Rank': list(range(1, 11)) + ['Others', 'Total'],
        'Name of Monument (Domestic)': [
            'Taj Mahal', 'Sun Temple, Konark', 'Qutub Minar', 'Red Fort', 'Ellora Caves',
            'Golconda Fort', 'Agra Fort', 'Tomb of Rabia Durani (Bibi ka Maqbara)',
            'Charminar', 'Shaniwarwada', 'Various Others', 'Grand Total Domestic' # Made generic for dummy
        ],
        'No. of Domestic Visitors': [
            6098876, 3196903, 3123643, 2794083, 1740513, 1608085, 1410397,
            1295076, 1290074, 1260792, 29271565, 53090007
        ],
        '% Share (Domestic)': [
            11.5, 6.0, 5.9, 5.3, 3.3, 3.0, 2.7, 2.4, 2.4, 2.4, 55.1, 100.0
        ]
    }
    foreign_data = {
        'Rank': list(range(1, 11)) + ['Others', 'Total'],
        'Name of Monument (Foreign)': [
            'Taj Mahal', 'Qutub Minar', 'Agra Fort', "Humayun's Tomb", 'Step Well (Baori) at Abhaneri',
            'Fatehpur Sikri', 'Itimad-Ud-Daulah Tomb', 'Red Fort', 'Excavated Remains, Sarnath',
            'Site of Sahet Mahet', 'Various Others', 'Grand Total Foreign' # Made generic for dummy
        ],
        'No. of Foreign Visitors': [
            681339, 220017, 218144, 116904, 96080, 93963, 84326, 84177, 76785, 71120, 571786, 2314641
        ],
        '% Share (Foreign)': [
            29.4, 9.5, 9.4, 5.1, 4.2, 4.1, 3.6, 3.6, 3.3, 3.1, 24.7, 100.0
        ]
    }
    df_domestic = pd.DataFrame(domestic_data)
    df_foreign = pd.DataFrame(foreign_data)
    return df_domestic, df_foreign

# Dictionary of official URLs for UNESCO sites
UNESCO_SITE_URLS = {
    "Khajuraho Group of Monuments": "https://www.indiaculture.gov.in/khajuraho-group-monuments",
    "Taj Mahal": "https://www.indiaculture.gov.in/taj-mahal",
    "Agra Fort": "https://www.indiaculture.gov.in/agra-fort",
    "Ajanta Caves": "https://www.indiaculture.gov.in/ajanta-caves",
    "Ellora Caves": "https://www.indiaculture.gov.in/ellora-caves",
    "Sun Temple, Konark": "https://www.indiaculture.gov.in/sun-temple-konark",
    "Group of Monuments at Mahabalipuram": "https://www.indiaculture.gov.in/group-monuments-mahabalipuram",
    "Group of Monuments at Hampi": "https://www.indiaculture.gov.in/group-monuments-hampi",
    "Fatehpur Sikri": "https://www.indiaculture.gov.in/fatehpur-sikri",
    "Group of Monuments at Pattadakal": "https://www.indiaculture.gov.in/group-monuments-pattadakal",
    "Elephanta Caves": "https://www.indiaculture.gov.in/elephanta-caves",
    "Great Living Chola Temples": "https://www.indiaculture.gov.in/great-living-chola-temples",
    "Buddhist Monuments at Sanchi": "https://www.indiaculture.gov.in/buddhist-monuments-sanchi",
    "Humayun's Tomb, Delhi": "https://www.indiaculture.gov.in/humayuns-tomb-delhi",
    "Qutb Minar and its Monuments, Delhi": "https://www.indiaculture.gov.in/qutb-minar-and-its-monuments-delhi",
    "Mountain Railways of India": "https://www.indiaculture.gov.in/mountain-railways-india",
    "Mahabodhi Temple Complex at Bodh Gaya": "https://www.indiaculture.gov.in/mahabodhi-temple-complex-bodh-gaya",
    "Rock Shelters of Bhimbetka": "https://www.indiaculture.gov.in/rock-shelters-bhimbetka",
    "Champaner-Pavagadh Archaeological Park": "https://www.indiaculture.gov.in/champaner-pavagadh-archaeological-park",
    "Red Fort Complex": "https://www.indiaculture.gov.in/red-fort-complex",
    "The Jantar Mantar, Jaipur": "https://www.indiaculture.gov.in/jantar-mantar-jaipur",
    "Western Ghats": "https://www.indiaculture.gov.in/western-ghats",
    "Hill Forts of Rajasthan": "https://www.indiaculture.gov.in/hill-forts-rajasthan",
    "Rani-ki-Vav at Patan": "https://www.indiaculture.gov.in/rani-ki-vav-patan",
    "Great Himalayan National Park": "https://www.indiaculture.gov.in/great-himalayan-national-park",
    "Nanda Devi and Valley of Flowers National Parks": "https://www.indiaculture.gov.in/nanda-devi-and-valley-flowers-national-parks",
    "Kaziranga National Park": "https://www.indiaculture.gov.in/kaziranga-national-park",
    "Keoladeo National Park": "https://www.indiaculture.gov.in/keoladeo-national-park",
    "Manas Wildlife Sanctuary": "https://www.indiaculture.gov.in/manas-wildlife-sanctuary",
    "Sundarbans National Park": "https://www.indiaculture.gov.in/sundarbans-national-park",
    "Chhatrapati Shivaji Terminus": "https://www.indiaculture.gov.in/chhatrapati-shivaji-terminus", # Matches Snowflake "Chhatrapati Shival Terminus"
    "Churches and Convents of Goa": "https://www.indiaculture.gov.in/churches-and-convents-goa",
    "Archaeological Site of Nalanda Mahavihara": "https://www.indiaculture.gov.in/archaeological-site-nalanda-mahavihara", # Matches "Archaeological Site of Nalanda Mahavihara at Nalanda, Bihar" if you adjust
    "The Architectural Work of Le Corbusier": "https://www.indiaculture.gov.in/architectural-work-le-corbusier",
    "Historic City of Ahmadabad": "https://www.indiaculture.gov.in/historic-city-ahmadabad",
    "Victorian Gothic and Art Deco Ensembles of Mumbai": "https://www.indiaculture.gov.in/victorian-gothic-and-art-deco-ensembles-mumbai",
    "Jaipur city, Rajasthan": "https://www.indiaculture.gov.in/jaipur-city-rajasthan"
}

# --- CSS Styling ---
st.markdown("""
<style>
/* Global Page Styling */
.main { background-color: white; color: #333; }
/* Header Styling */
.header { padding: 1rem 0; text-align: center; margin-bottom: 1rem; /* Reduced margin-bottom */ }
.header h1 { color: #2c3e50; font-size: 2.5rem; font-weight: 700; }
.header p { color: #555; font-size: 1.2rem; max-width: 800px; margin: 0 auto; }
/* Map Container */
.map-container {
    background-color: white; border-radius: 10px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1); padding: 1rem;
    margin-bottom: 1.5rem; /* Adjusted for closer search bar */
}
/* Site Details */
.site-details {
    background-color: white; border-radius: 10px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1); padding: 2rem;
    margin-top: 1.5rem; /* Adjusted margin */
}
.site-title { font-size: 1.8rem; font-weight: 700; color: #2c3e50; margin-bottom: 0.5rem; }
.site-subtitle { font-size: 1.1rem; color: #7f8c8d; margin-bottom: 1rem; }
.site-description { font-size: 1rem; color: #555; line-height: 1.6; margin-bottom: 1.5rem; }
/* Badge Styles */
.badge { display: inline-block; padding: 0.3rem 0.6rem; border-radius: 4px; font-size: 0.8rem; font-weight: 500; margin-right: 0.5rem; }
.badge-unesco { background-color: #3498db; color: white; }
/* Style for statistics section cards */
.stats-card { background-color: #f8f9fa; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; }
.stats-card h4 { margin: 0 0 10px 0; color: #2c3e50; }
.stats-card p { margin: 0; color: #555; }
/* Table styling for ASI stats for better readability */
.stDataFrame table { font-size: 0.9rem; }
.stDataFrame th { background-color: #f0f2f6; }
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("""
<div class="header">
    <h1>🏛️ Cultural Canvas India</h1>
    <p>Explore India's UNESCO World Heritage Sites and ASI Monument Visitor Statistics. Discover, analyze, and learn about India's rich heritage.</p>
</div>
""", unsafe_allow_html=True)

# --- Load UNESCO Data ---
sites_df = load_unesco_sites_from_snowflake()

# --- Create Map (UNESCO Sites) ---
st.markdown('<div class="map-container">', unsafe_allow_html=True)
if sites_df.empty:
    st.warning("Could not load UNESCO site data for the map. Please check the connection or data source.")
else:
    m = folium.Map(location=[20.5937, 78.9629], zoom_start=5, tiles="cartodbpositron", control_scale=True)
    def create_custom_icon():
        return """<div style="background-color: #3498db; width: 12px; height: 12px; border-radius: 50%; border: 2px solid white; box-shadow: 0 0 4px rgba(0,0,0,0.3); position: relative;"><div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 4px; height: 4px; background-color: white; border-radius: 50%;"></div></div>"""
    for _, site_row in sites_df.iterrows():
        icon_html = create_custom_icon()
        site_name_from_df = site_row.get("Name", "Unknown Site")
        official_url = UNESCO_SITE_URLS.get(site_name_from_df) # Match against the 'Name' column from DataFrame
        popup_html = f"""<div style="width: 250px; padding: 10px;"><h3 style="margin: 0 0 10px 0; color: #2c3e50; font-size: 16px;">{site_name_from_df}</h3><div style="margin-bottom: 10px;"><span style="background-color: #f8f9fa; padding: 3px 8px; border-radius: 4px; font-size: 12px; color: #666;">{site_row.get("City", "N/A")} • {site_row.get("State/UT", "N/A")}</span></div><p style="margin: 0 0 10px 0; font-size: 13px; color: #555; line-height: 1.4;">{site_row.get("Short Description", "No description available.")}</p><div style="margin-bottom: 10px;"><span class="badge badge-unesco">UNESCO World Heritage Site</span></div>{f'<a href="{official_url}" target="_blank" style="display: inline-block; background-color: #3498db; color: white; padding: 5px 10px; text-decoration: none; border-radius: 4px; font-size: 12px;">View Full Details</a>' if official_url else ''}</div>"""
        icon = folium.DivIcon(html=icon_html, icon_size=(12, 12), icon_anchor=(6, 6))
        try:
            lat = float(site_row["Latitude"]); lon = float(site_row["Longitude"])
            folium.Marker([lat, lon], popup=folium.Popup(popup_html, max_width=300), tooltip=site_name_from_df, icon=icon).add_to(m)
        except (ValueError, TypeError):
            st.warning(f"Skipping UNESCO site '{site_name_from_df}' due to invalid coordinates.")
    st_folium(m, width=1200, height=550, key="unesco_map_from_sf_v2")
st.markdown('</div>', unsafe_allow_html=True)

# --- Handle UNESCO site search (Placed after map) ---
if not sites_df.empty:
    search_site_name = st.text_input(
        "Search for a UNESCO World Heritage Site by name:", "",
        key="unesco_site_search_input_v2",
        help="Type part of the UNESCO site name to see details below."
    )
    if search_site_name:
        matching_sites = sites_df[sites_df['Name'].str.contains(search_site_name, case=False, na=False)]
        if not matching_sites.empty:
            st.session_state.selected_site = matching_sites.iloc[0]['Name']
            # Consider if rerun is needed or if UI updates implicitly:
            # st.rerun()
        elif st.session_state.get('selected_site'): # Clear selection if search yields no results
            del st.session_state.selected_site
            # st.rerun() # Optionally rerun to clear details
        else: # Only show warning if no match and nothing was previously selected or search is active
            if search_site_name: # Avoid warning on initial empty search
                 st.warning(f"No UNESCO sites found matching '{search_site_name}'")


# --- UNESCO Site Details ---
if 'selected_site' in st.session_state and st.session_state.selected_site:
    if not sites_df.empty:
        # Ensure selected_site is valid within the current sites_df
        selected_site_data_list = sites_df[sites_df['Name'] == st.session_state.selected_site]
        if not selected_site_data_list.empty:
            site_detail = selected_site_data_list.iloc[0]
            st.markdown('<div class="site-details">', unsafe_allow_html=True)
            site_name_detail = site_detail.get("Name", "N/A")
            st.markdown(f'<div class="site-title">{site_name_detail}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="site-subtitle">{site_detail.get("City", "N/A")} • {site_detail.get("State/UT", "N/A")}</div>', unsafe_allow_html=True)
            st.markdown('<span class="badge badge-unesco">UNESCO World Heritage Site</span>', unsafe_allow_html=True)
            st.markdown(f'<div class="site-description">{site_detail.get("Short Description", "No description available.")}</div>', unsafe_allow_html=True)

            st.subheader("Location Details")
            col1_loc, col2_loc = st.columns(2)
            with col1_loc: st.markdown(f"""<div class="stats-card"><h4>City</h4><p>{site_detail.get('City', "N/A")}</p></div>""", unsafe_allow_html=True)
            with col2_loc: st.markdown(f"""<div class="stats-card"><h4>District</h4><p>{site_detail.get('District', "N/A")}</p></div>""", unsafe_allow_html=True)

            st.subheader("Coordinates")
            st.markdown(f"""<div class="stats-card"><p>Latitude: {site_detail.get('Latitude', "N/A")}<br>Longitude: {site_detail.get('Longitude', "N/A")}</p></div>""", unsafe_allow_html=True)

            if st.button("Clear Selection / Back to Map Overview", key="clear_selection_button"):
                del st.session_state.selected_site
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        else: # Selected site name not found in current df (e.g., after data refresh)
            if st.session_state.get('selected_site'):
                st.warning(f"Details for '{st.session_state.selected_site}' no longer found. Clearing selection.")
                del st.session_state.selected_site
                st.rerun()
elif not sites_df.empty:
    st.info("👆 Click on a marker on the map or use the search above to view detailed information about a UNESCO World Heritage Site.")


# --- UNESCO Site Statistics Dashboard ---
st.markdown("---") # Horizontal line
if not sites_df.empty:
    st.subheader("📊 UNESCO World Heritage Sites: At a Glance")
    st.markdown("Overview of the listed UNESCO sites in India from the loaded data.")

    col_stats1, col_stats2 = st.columns([1,2])

    with col_stats1:
        total_sites = sites_df.shape[0]
        st.metric(label="Total UNESCO Sites Loaded", value=total_sites)
        if 'State/UT' in sites_df.columns and not sites_df['State/UT'].empty:
             st.metric(label="States/UTs Represented", value=sites_df['State/UT'].nunique())

    with col_stats2:
        st.markdown("##### UNESCO Sites per State/UT")
        if 'State/UT' in sites_df.columns and not sites_df['State/UT'].empty:
            state_counts = sites_df['State/UT'].value_counts().reset_index()
            state_counts.columns = ['State/UT', 'Number of Sites']
            
            fig_state_distribution = px.bar(
                state_counts,
                x='State/UT',
                y='Number of Sites',
                color='Number of Sites',
                color_continuous_scale=px.colors.sequential.Teal,
                labels={'Number of Sites': 'Count', 'State/UT': 'State or Union Territory'}
            )
            fig_state_distribution.update_layout(
                xaxis_title=None, # Cleaner look if states are many
                yaxis_title="Number of Sites",
                showlegend=False,
                height=350 # Adjust height as needed
            )
            st.plotly_chart(fig_state_distribution, use_container_width=True)
        else:
            st.warning("Column 'State/UT' for UNESCO sites not found or is empty in the data for state distribution chart.")

    st.markdown("---")
    st.markdown("#### UNESCO Sites Quick Overview Table")
    st.dataframe(
        sites_df[['Name', 'City', 'State/UT', 'District']].reset_index(drop=True).head(10),
        use_container_width=True,
        height=300 # Set a fixed height to make it scrollable
    )
    if len(sites_df) > 10:
        st.caption(f"Showing first 10 of {len(sites_df)} UNESCO sites.")
else:
    st.info("UNESCO site data is not loaded, so no related statistics can be displayed.")


# --- ASI Monument Visitor Statistics ---
st.markdown("---")
st.subheader("🇮🇳 Visitor Statistics: Centrally Protected Ticketed ASI Monuments")
st.caption("Data presented below is based on information from the Archaeological Survey of India (ASI). Illustrative data is used here; please replace with actual figures from your data source.")

# Load ASI Data (using dummy functions)
# !!! REPLACE THESE WITH YOUR ACTUAL DATA LOADING !!!
asi_visitor_trends_df = load_asi_visitor_trends_data()
asi_top_domestic_df, asi_top_foreign_df = load_asi_top_monuments_data()

# Section 1: Visitor Trends (Table 4.2.1 like)
st.markdown("#### Annual Visitor Trends to ASI Monuments")
if not asi_visitor_trends_df.empty:
    with st.expander("View Detailed Visitor Trends Table (Illustrative Data)", expanded=False):
        st.dataframe(asi_visitor_trends_df, use_container_width=True)
        st.caption("*Source: Archaeological Survey of India (ASI) - Using illustrative data.*")

    st.markdown("##### Visitor Numbers Over Time (Illustrative)")
    # Filter years for charting to avoid clutter if too many 'N.A' or very old data
    # Attempt to convert 'Year' to a numeric start year for filtering and sorting
    try:
        trends_chart_df = asi_visitor_trends_df.copy()
        trends_chart_df['SortableYear'] = trends_chart_df['Year'].astype(str).str.extract(r'(\d{4})').astype(int)
        trends_chart_df = trends_chart_df[trends_chart_df['SortableYear'] >= 2002] # Example filter
        trends_chart_df.dropna(subset=['Domestic Visitors', 'Foreign Visitors', 'Total Visitors'], inplace=True)
        trends_chart_df.sort_values('SortableYear', inplace=True)
    except Exception as e:
        st.warning(f"Could not prepare data for trends chart: {e}")
        trends_chart_df = pd.DataFrame() # Empty df if prep fails


    if not trends_chart_df.empty:
        fig_visitor_trends = go.Figure()
        fig_visitor_trends.add_trace(go.Scatter(x=trends_chart_df['Year'], y=trends_chart_df['Domestic Visitors'], mode='lines+markers', name='Domestic Visitors'))
        fig_visitor_trends.add_trace(go.Scatter(x=trends_chart_df['Foreign Visitors'], mode='lines+markers', name='Foreign Visitors'))
        fig_visitor_trends.add_trace(go.Scatter(x=trends_chart_df['Year'], y=trends_chart_df['Total Visitors'], mode='lines+markers', name='Total Visitors', line=dict(dash='dot', color='green')))
        fig_visitor_trends.update_layout(title='Domestic, Foreign, and Total Visitors (ASI Monuments)',
                                         xaxis_title='Year', yaxis_title='Number of Visitors (Illustrative)', height=450,
                                         legend_title_text='Visitor Type')
        st.plotly_chart(fig_visitor_trends, use_container_width=True)
    else:
        st.info("Not enough valid data for the ASI visitor trends chart after filtering.")
else:
    st.warning("ASI visitor trend data could not be loaded (currently using dummy data placeholders).")

st.markdown("---")
# Section 2: Top 10 Monuments (Table 4.2.2 like)
st.markdown("#### Top 10 Most Popular ASI Monuments (FY 2023-24 - Illustrative Data)")
if not asi_top_domestic_df.empty and not asi_top_foreign_df.empty:
    col_top_dom, col_top_for = st.columns(2)
    with col_top_dom:
        st.markdown("##### Top by Domestic Visitors (Illustrative)")
        st.dataframe(asi_top_domestic_df.set_index('Rank'), use_container_width=True)
        st.caption("*Source: ASI - Illustrative data.*")

        # Bar chart for top domestic (excluding 'Others' and 'Total' for cleaner chart)
        chart_df_dom = asi_top_domestic_df[~asi_top_domestic_df['Rank'].isin(['Others', 'Total'])].head(10)
        if not chart_df_dom.empty:
            fig_dom = px.bar(chart_df_dom,
                             x='No. of Domestic Visitors', y='Name of Monument (Domestic)', orientation='h',
                             title='Top Domestic Visitor Sites', text='No. of Domestic Visitors')
            fig_dom.update_layout(yaxis={'categoryorder':'total ascending'}, height=400, margin=dict(l=200, r=20, t=50, b=20))
            fig_dom.update_traces(texttemplate='%{text:,.0f}', textposition='outside') # Format number
            st.plotly_chart(fig_dom, use_container_width=True)

    with col_top_for:
        st.markdown("##### Top by Foreign Visitors (Illustrative)")
        st.dataframe(asi_top_foreign_df.set_index('Rank'), use_container_width=True)
        st.caption("*Source: ASI - Illustrative data.*")

        # Bar chart for top foreign
        chart_df_for = asi_top_foreign_df[~asi_top_foreign_df['Rank'].isin(['Others', 'Total'])].head(10)
        if not chart_df_for.empty:
            fig_for = px.bar(chart_df_for,
                             x='No. of Foreign Visitors', y='Name of Monument (Foreign)', orientation='h',
                             title='Top Foreign Visitor Sites', text='No. of Foreign Visitors')
            fig_for.update_layout(yaxis={'categoryorder':'total ascending'}, height=400, margin=dict(l=200, r=20, t=50, b=20))
            fig_for.update_traces(texttemplate='%{text:,.0f}', textposition='outside') # Format number
            st.plotly_chart(fig_for, use_container_width=True)
else:
    st.warning("ASI top monuments data could not be loaded (currently using dummy data placeholders).")


# --- Footer ---
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #777; font-size: 0.9em; padding: 1rem 0;">
        <p>Cultural Canvas India | Explore India's Heritage.</p>
        <p>UNESCO Site data sourced via Snowflake. ASI Visitor statistics are illustrative and should be replaced with actual data from ASI.</p>
    </div>
    """, unsafe_allow_html=True
)