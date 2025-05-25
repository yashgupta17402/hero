import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium # Use st_folium consistently
# Removed folium_static as st_folium is generally preferred for interactivity
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import random

# --- Page Configuration ---
st.set_page_config(
    page_title="UNESCO World Heritage Sites Map | Cultural Canvas India",
    layout="wide",
    initial_sidebar_state="auto",
    page_icon="🗺️"
)

# --- Snowflake Connection ---
def get_snowflake_connection():
    """Helper function to get Snowflake connection."""
    return st.connection("snowflake")

# --- Load UNESCO Sites Data from Snowflake ---
# @st.cache_data # conn.query() has its own caching via ttl, so this might be redundant or conflict
def load_unesco_sites_from_snowflake():
    """Load UNESCO World Heritage Sites data from Snowflake."""
    try:
        conn = get_snowflake_connection()
        # Query the UNESCO_INDIA_SITES table
        # Alias column names to match what the script expects (e.g., 'Name' from 'NAME')
        query = """
        SELECT
            NAME AS "Name",  -- CSV used 'Name'
            CITY AS "City",
            DISTRICT AS "District",
            STATE_UT AS "State/UT", -- CSV used 'State/UT'
            DESCRIPTION AS "Short Description", -- CSV used 'Short Description'
            LATITUDE AS "Latitude",
            LONGITUDE AS "Longitude"
        FROM UNESCO_INDIA_SITES;
        """
        df = conn.query(query, ttl=3600) # Cache for 1 hour
        
        # Ensure Latitude and Longitude are numeric
        if "Latitude" in df.columns:
            df["Latitude"] = pd.to_numeric(df["Latitude"], errors='coerce')
        if "Longitude" in df.columns:
            df["Longitude"] = pd.to_numeric(df["Longitude"], errors='coerce')
        df.dropna(subset=["Latitude", "Longitude"], inplace=True) # Drop rows with invalid coordinates

        return df
    except Exception as e:
        st.error(f"Error loading UNESCO sites from Snowflake: {e}")
        return pd.DataFrame() # Return empty DataFrame on error

# Dictionary of official URLs for UNESCO sites (remains the same)
UNESCO_SITE_URLS = {
    "Khajuraho Group of Monuments": "https://www.indiaculture.gov.in/khajuraho-group-monuments",
    "Taj Mahal": "https://www.indiaculture.gov.in/taj-mahal",
    "Agra Fort": "https://www.indiaculture.gov.in/agra-fort",
    "Ajanta Caves": "https://www.indiaculture.gov.in/ajanta-caves",
    "Ellora Caves": "https://www.indiaculture.gov.in/ellora-caves",
    "Sun Temple, Konark": "https://www.indiaculture.gov.in/sun-temple-konark", # Matches Snowflake 'Sun Temple , Konrak' if name is exact
    "Group of Monuments at Mahabalipuram": "https://www.indiaculture.gov.in/group-monuments-mahabalipuram",
    "Group of Monuments at Hampi": "https://www.indiaculture.gov.in/group-monuments-hampi",
    "Fatehpur Sikri": "https://www.indiaculture.gov.in/fatehpur-sikri", # Matches Snowflake 'Fatehpur Silvi' if name is exact
    "Group of Monuments at Pattadakal": "https://www.indiaculture.gov.in/group-monuments-pattadakal",
    "Elephanta Caves": "https://www.indiaculture.gov.in/elephanta-caves",
    "Great Living Chola Temples": "https://www.indiaculture.gov.in/great-living-chola-temples", # Matches Snowflake 'Great IIving Chola Temples'
    "Buddhist Monuments at Sanchi": "https://www.indiaculture.gov.in/buddhist-monuments-sanchi",
    "Humayun's Tomb, Delhi": "https://www.indiaculture.gov.in/humayuns-tomb-delhi", # Matches Snowflake "Humayun's Tomb , Delhi"
    "Qutb Minar and its Monuments, Delhi": "https://www.indiaculture.gov.in/qutb-minar-and-its-monuments-delhi", # Matches Snowflake "Qutb Minar and its Monuments , Dell"
    "Mountain Railways of India": "https://www.indiaculture.gov.in/mountain-railways-india", # Matches Snowflake "Mountain Railways of india"
    "Mahabodhi Temple Complex at Bodh Gaya": "https://www.indiaculture.gov.in/mahabodhi-temple-complex-bodh-gaya",
    "Rock Shelters of Bhimbetka": "https://www.indiaculture.gov.in/rock-shelters-bhimbetka", # Matches Snowflake "Rock Shelters of Bhimbetka"
    "Champaner-Pavagadh Archaeological Park": "https://www.indiaculture.gov.in/champaner-pavagadh-archaeological-park",
    "Red Fort Complex": "https://www.indiaculture.gov.in/red-fort-complex", # Matches Snowflake "Red Forl Complex"
    "The Jantar Mantar, Jaipur": "https://www.indiaculture.gov.in/jantar-mantar-jaipur",
    "Western Ghats": "https://www.indiaculture.gov.in/western-ghats",
    "Hill Forts of Rajasthan": "https://www.indiaculture.gov.in/hill-forts-rajasthan",
    "Rani-ki-Vav at Patan": "https://www.indiaculture.gov.in/rani-ki-vav-patan", # Matches Snowflake "Rani-ki-Vav at Patan"
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
    # Note: The names in UNESCO_SITE_URLS must exactly match the 'Name' column from the Snowflake table after aliasing.
    # You might need to adjust the keys in this dictionary or the names in your Snowflake table for perfect matches.
}


# --- CSS Styling --- (remains the same)
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

/* Site Details */
.site-details {
    background-color: white;
    border-radius: 10px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    padding: 2rem;
    margin-top: 2rem;
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
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("""
<div class="header">
    <h1>🗺️ UNESCO World Heritage Sites in India</h1>
    <p>Explore India's rich cultural and natural heritage through an interactive map of UNESCO World Heritage Sites. Discover monuments, temples, national parks, and more.</p>
</div>
""", unsafe_allow_html=True)

# --- Load Data ---
# Now call the function to load from Snowflake
sites_df = load_unesco_sites_from_snowflake()

# --- Create Map ---
st.markdown('<div class="map-container">', unsafe_allow_html=True)

if sites_df.empty:
    st.warning("Could not load UNESCO site data. Please check the connection or data source.")
else:
    # Create map
    m = folium.Map(
        location=[20.5937, 78.9629], # Center of India
        zoom_start=5,
        tiles="cartodbpositron",
        control_scale=True
    )

    # Custom icon HTML (remains the same)
    def create_custom_icon():
        return """
        <div style="
            background-color: #3498db;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            border: 2px solid white;
            box-shadow: 0 0 4px rgba(0,0,0,0.3);
            position: relative;
        ">
            <div style="
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                width: 4px;
                height: 4px;
                background-color: white;
                border-radius: 50%;
            "></div>
        </div>
        """

    # Add markers to map
    for _, site_row in sites_df.iterrows(): # Renamed 'site' to 'site_row' to avoid conflict if 'site' is used elsewhere
        icon_html = create_custom_icon()
        
        # Use .get() for safer dictionary access, provide default if key missing
        site_name_from_df = site_row.get("Name", "Unknown Site")
        official_url = UNESCO_SITE_URLS.get(site_name_from_df) # Match against the 'Name' column from DataFrame

        popup_html = f"""
        <div style="width: 250px; padding: 10px;">
            <h3 style="margin: 0 0 10px 0; color: #2c3e50; font-size: 16px;">{site_name_from_df}</h3>
            <div style="margin-bottom: 10px;">
                <span style="background-color: #f8f9fa; padding: 3px 8px; border-radius: 4px; font-size: 12px; color: #666;">
                    {site_row.get("City", "N/A")} • {site_row.get("State/UT", "N/A")}
                </span>
            </div>
            <p style="margin: 0 0 10px 0; font-size: 13px; color: #555; line-height: 1.4;">
                {site_row.get("Short Description", "No description available.")}
            </p>
            <div style="margin-bottom: 10px;">
                <span style="background-color: #3498db; color: white; padding: 2px 6px; border-radius: 3px; font-size: 11px;">UNESCO World Heritage Site</span>
            </div>
            {f'<a href="{official_url}" target="_blank" style="display: inline-block; background-color: #3498db; color: white; padding: 5px 10px; text-decoration: none; border-radius: 4px; font-size: 12px;">View Full Details</a>' if official_url else ''}
        </div>
        """
        
        icon = folium.DivIcon(
            html=icon_html,
            icon_size=(12, 12),
            icon_anchor=(6, 6)
        )
        
        # Ensure Latitude and Longitude are valid numbers
        try:
            lat = float(site_row["Latitude"])
            lon = float(site_row["Longitude"])
            marker = folium.Marker(
                [lat, lon],
                popup=folium.Popup(popup_html, max_width=300),
                tooltip=site_name_from_df,
                icon=icon
            )
            marker.add_to(m)
        except (ValueError, TypeError):
            st.warning(f"Skipping site '{site_name_from_df}' due to invalid coordinates.")


    # Display map
    st_folium(m, width=1200, height=600, key="unesco_map_from_sf") # Changed key to avoid conflict if old map key exists
st.markdown('</div>', unsafe_allow_html=True)


# --- Site Details ---
# Initialize selected_site in session_state if it's not there from a map click
# This part usually relies on st_folium's return value or a click event handler
# For simplicity, let's assume selected_site is set by clicking a marker (which st_folium can handle via last_object_clicked)
# Or by the search below.

# We need to handle how 'selected_site' is populated.
# st_folium can return the last clicked marker's data.
# For now, the existing search logic will set st.session_state.selected_site

if 'selected_site' in st.session_state and st.session_state.selected_site:
    # Ensure sites_df is not empty before trying to filter
    if not sites_df.empty:
        selected_site_data_list = sites_df[sites_df['Name'] == st.session_state.selected_site]
        if not selected_site_data_list.empty:
            site_detail = selected_site_data_list.iloc[0] # Use a different variable name like site_detail
        
            st.markdown('<div class="site-details">', unsafe_allow_html=True)
            
            if st.button("← Back to Map", key="back_to_map_button_detail"): # Added key
                del st.session_state.selected_site
                st.rerun()
            
            site_name_detail = site_detail.get("Name", "N/A")
            st.markdown(f'<div class="site-title">{site_name_detail}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="site-subtitle">{site_detail.get("City", "N/A")} • {site_detail.get("State/UT", "N/A")}</div>', unsafe_allow_html=True)
            
            st.markdown('<span class="badge badge-unesco">UNESCO World Heritage Site</span>', unsafe_allow_html=True)
            
            st.markdown(f'<div class="site-description">{site_detail.get("Short Description", "No description available.")}</div>', unsafe_allow_html=True)
            
            st.subheader("Location Details")
            col1_detail_loc, col2_detail_loc = st.columns(2) # Unique variable names
            
            with col1_detail_loc:
                st.markdown(f"""
                <div style="background-color: #f8f9fa; padding: 1rem; border-radius: 8px;">
                    <h4 style="margin: 0 0 10px 0; color: #2c3e50;">City</h4>
                    <p style="margin: 0; color: #555;">{site_detail.get('City', "N/A")}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2_detail_loc:
                st.markdown(f"""
                <div style="background-color: #f8f9fa; padding: 1rem; border-radius: 8px;">
                    <h4 style="margin: 0 0 10px 0; color: #2c3e50;">District</h4>
                    <p style="margin: 0; color: #555;">{site_detail.get('District', "N/A")}</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.subheader("Coordinates")
            st.markdown(f"""
            <div style="background-color: #f8f9fa; padding: 1rem; border-radius: 8px;">
                <p style="margin: 0; color: #555;">
                    Latitude: {site_detail.get('Latitude', "N/A")}<br>
                    Longitude: {site_detail.get('Longitude', "N/A")}
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning(f"Details for '{st.session_state.selected_site}' not found in the current dataset.")
            # Optionally clear selected_site if not found
            # if 'selected_site' in st.session_state: del st.session_state.selected_site
            # st.rerun() # To refresh view if selected_site is cleared
    else:
        st.info("UNESCO site data is not available to display details.")

elif not sites_df.empty: # Only show this if data was loaded but no site is selected
    st.info("👆 Click on a marker on the map to view detailed information about a UNESCO World Heritage Site.")

# --- Handle site search ---
# Ensure sites_df is not empty before allowing search
if not sites_df.empty:
    search_site_name = st.text_input("Search for a UNESCO World Heritage Site", "", key="unesco_site_search_input") # Changed key
    if search_site_name:
        matching_sites = sites_df[sites_df['Name'].str.contains(search_site_name, case=False, na=False)]
        if not matching_sites.empty:
            st.session_state.selected_site = matching_sites.iloc[0]['Name']
            st.rerun()
        else:
            st.warning(f"No sites found matching '{search_site_name}'")
elif sites_df.empty and 'load_unesco_sites_from_snowflake' in locals(): # Check if function exists to infer data loading was attempted
     pass # Error message for loading failure is already shown by load_unesco_sites_from_snowflake