import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import random # For unique keys if needed

# --- Page Configuration ---
st.set_page_config(
    page_title="Art Forms Explorer | Cultural Canvas India",
    layout="wide",
    initial_sidebar_state="auto",
    page_icon="🎨"
)

# --- Snowflake Connection ---
# This function helps in getting the snowflake connection
# Ensure your secrets.toml is configured correctly.
def get_snowflake_connection():
    return st.connection("snowflake")

# --- Data Fetching Functions ---

def get_crafts_from_snowflake():
    """Fetch crafts data from Snowflake CRAFTS table."""
    try:
        conn = get_snowflake_connection()
        # Using column names C1, C2, C3, C4 as identified from your image
        # C1: State/UT, C2: District, C3: Craft, C4: Village/Sub District
        # Aliases (state_ut, district, etc.) will likely become uppercase in the Pandas DataFrame (STATE_UT, DISTRICT, etc.)
        query = 'SELECT "C1" AS state_ut, "C2" AS district, "C3" AS craft_name, "C4" AS village_sub_district FROM "CRAFTS";'
        df = conn.query(query, ttl=3600) # Cache for 1 hour
        return df
    except Exception as e:
        st.error(f"Error fetching crafts from Snowflake: {e}")
        return pd.DataFrame() # Return empty DataFrame on error

def get_art_forms_combined():
    """
    Fetch art forms data, combining hardcoded data with crafts from Snowflake.
    """
    # 1. Get hardcoded art forms (paintings, dance, textiles, etc.)
    hardcoded_art_forms_df = pd.DataFrame({
        'name': [
            'Madhubani Painting', 'Kathakali', 'Bharatanatyam', 'Pashmina Shawls',
            'Banarasi Silk', 'Pattachitra', 'Warli Painting', 'Phulkari',
            'Chikankari', 'Kantha', 'Kalamkari', 'Bidriware', 
            'Dhokra', 'Tanjore Painting', 'Gond Art'
        ],
        'type': [
            'Painting', 'Dance', 'Dance', 'Textile',
            'Textile', 'Painting', 'Painting', 'Textile',
            'Textile', 'Textile', 'Painting', 'Craft', # Bidriware is a craft
            'Craft', 'Painting', 'Painting'           # Dhokra is a craft
        ],
        'state': [
            'Bihar', 'Kerala', 'Tamil Nadu', 'Jammu & Kashmir',
            'Uttar Pradesh', 'Odisha', 'Maharashtra', 'Punjab',
            'Uttar Pradesh', 'West Bengal', 'Andhra Pradesh', 'Karnataka',
            'Chhattisgarh', 'Tamil Nadu', 'Madhya Pradesh'
        ],
        'gi_tag': [
            True, False, False, True,
            True, True, False, True,
            True, False, True, True, 
            False, False, False      
        ],
        'description': [
            'Characterized by geometric patterns and nature motifs, this ancient art form has been practiced for centuries.',
            'A classical dance-drama known for its elaborate costumes, makeup, and facial expressions.',
            'One of India\'s oldest classical dance forms, characterized by grace, purity, and sculpturesque poses.',
            'Exquisite handwoven shawls made from the finest cashmere wool, known for their warmth and intricate embroidery.',
            'Luxurious silk textiles woven with intricate gold and silver brocade, traditionally used for wedding attire.',
            'Traditional cloth-based scroll painting with rich colorful applications, motifs of Hindu mythology.',
            'Tribal art form using basic geometric shapes like circles, triangles, and squares to form compositions.',
            'Embroidery technique from Punjab with colorful thread work on cotton fabric.',
            'Delicate and intricate hand embroidery from Lucknow, known for its subtle elegance.',
            'Running stitch embroidery used to make quilts and decorative items.',
            'Hand-painted or block-printed cotton textile, produced in parts of Andhra Pradesh.',
            'Metal handicraft from Bidar, Karnataka, known for its striking inlay work.',
            'Ancient bell metal craft practiced by the Dhokra Damar tribes of central and eastern India.',
            'Classical South Indian painting style characterized by rich, vivid colors and gold foil overlays.',
            'Traditional tribal art form with distinctive patterns and vibrant colors.'
        ],
        'image_url': [
            'https://raw.githubusercontent.com/yashgupta17402/hero/main/madhubani.PNG',
            'https://raw.githubusercontent.com/yashgupta17402/hero/main/kathakali.PNG',
            'https://raw.githubusercontent.com/yashgupta17402/hero/main/bharatanatyam.jpg',
            'https://raw.githubusercontent.com/yashgupta17402/hero/main/pashmina.jpg',
            'https://raw.githubusercontent.com/yashgupta17402/hero/main/banarasi.jpg',
            'https://raw.githubusercontent.com/yashgupta17402/hero/main/pattachitra.jpg',
            'https://raw.githubusercontent.com/yashgupta17402/hero/main/warli.jpg',
            'https://raw.githubusercontent.com/yashgupta17402/hero/main/phulkari.jpg',
            'https://raw.githubusercontent.com/yashgupta17402/hero/main/chikankari.jpg',
            'https://raw.githubusercontent.com/yashgupta17402/hero/main/kantha.jpg',
            'https://raw.githubusercontent.com/yashgupta17402/hero/main/kalamkari.jpg',
            'https://raw.githubusercontent.com/yashgupta17402/hero/main/bidriware.jpg',
            'https://raw.githubusercontent.com/yashgupta17402/hero/main/dhokra.jpg',
            'https://raw.githubusercontent.com/yashgupta17402/hero/main/tanjore.jpg',
            'https://raw.githubusercontent.com/yashgupta17402/hero/main/gond.jpg'
        ],
        'latitude': [
            25.4, 10.8, 13.1, 34.1, 25.3, 20.3, 19.2, 31.1,
            26.8, 22.6, 16.5, 17.9, 21.3, 10.8, 23.2
        ],
        'longitude': [
            85.4, 76.3, 80.3, 74.8, 83.0, 85.8, 73.2, 75.3,
            80.9, 88.4, 80.6, 77.5, 81.6, 79.1, 77.4
        ],
        'govt_scheme': [
            'National Handicraft Development Program', 'Cultural Function Grant Scheme', 'Cultural Function Grant Scheme', 'National Handicraft Development Program',
            'National Handicraft Development Program', 'National Handicraft Development Program', 'Tribal Art Development Scheme', 'National Handicraft Development Program',
            'National Handicraft Development Program', 'Women Artisan Development Initiative', 'National Handicraft Development Program', 'National Handicraft Development Program',
            'Tribal Art Development Scheme', 'Cultural Function Grant Scheme', 'Tribal Art Development Scheme'
        ],
        'allocation_amount': [
            '₹2.5 Crore', '₹1.8 Crore', '₹2.2 Crore', '₹3.1 Crore',
            '₹2.7 Crore', '₹1.5 Crore', '₹1.2 Crore', '₹1.9 Crore',
            '₹2.3 Crore', '₹1.4 Crore', '₹1.7 Crore', '₹1.6 Crore',
            '₹1.1 Crore', '₹1.3 Crore', '₹1.0 Crore'
        ],
        'artisan_cooperative': [
            'Mithila Art Institute', 'Kerala Kalamandalam', 'Kalakshetra Foundation', 'Kashmir Pashmina Artisans Cooperative',
            'Varanasi Weavers Association', 'Raghurajpur Artisans Cooperative', 'Warli Art Cooperative', 'Punjab Phulkari Cooperative',
            'Lucknow Chikankari Kala Kendra', 'Bengal Women Artisans Cooperative', 'Srikalahasti Kalamkari Cooperative', 'Bidri Craft Association',
            'Bastar Dhokra Shilp Cooperative', 'Thanjavur Art Gallery Association', 'Gond Tribal Art Cooperative'
        ]
    })

    # 2. Get crafts from Snowflake
    crafts_sf_df_raw = get_crafts_from_snowflake()
    
    # --- ADD THIS DEBUG LINE TEMPORARILY if you still have issues ---
    # if not crafts_sf_df_raw.empty:
    #    st.write("Debug: Columns from Snowflake CRAFTS query:", crafts_sf_df_raw.columns.tolist())
    #    st.write("Debug: First few rows from CRAFTS query:", crafts_sf_df_raw.head())
    # else:
    #    st.write("Debug: CRAFTS query returned an empty DataFrame.")
    # --- END DEBUG LINE ---

    transformed_crafts_list = []

    if not crafts_sf_df_raw.empty:
        state_coords_dict = get_state_coordinates() # For lat/long mapping

        for _, row in crafts_sf_df_raw.iterrows():
            # Access by UPPERCASE versions of aliases used in SQL query
            state = row.get('STATE_UT', None) # Use .get for safety
            craft_name_from_db = row.get('CRAFT_NAME', 'Unknown Craft')
            district_from_db = row.get('DISTRICT', 'Unknown District')
            village_from_db = row.get('VILLAGE_SUB_DISTRICT', 'Unknown Village')
            
            lat, lon = None, None
            if state: # Only get coords if state is not None
                 lat, lon = state_coords_dict.get(state, [None, None])

            image_text = craft_name_from_db.replace(" ", "+") if pd.notna(craft_name_from_db) else "Craft"

            transformed_crafts_list.append({
                'name': craft_name_from_db,
                'type': 'Craft', 
                'state': state,
                'gi_tag': False,  # Placeholder
                'description': f"A traditional {craft_name_from_db} from {district_from_db}, {state if state else 'N/A'}. Practiced in {village_from_db}.",
                'image_url': f'https://via.placeholder.com/300x200.png?text={image_text}', # Placeholder
                'latitude': lat,
                'longitude': lon,
                'govt_scheme': 'To be updated', 
                'allocation_amount': 'N/A',     
                'artisan_cooperative': 'To be updated' 
            })

    transformed_crafts_df = pd.DataFrame(transformed_crafts_list)

    # 3. Combine the two DataFrames
    if not transformed_crafts_df.empty:
        combined_df = pd.concat([hardcoded_art_forms_df, transformed_crafts_df], ignore_index=True)
    else:
        combined_df = hardcoded_art_forms_df.copy() # Use a copy to avoid modifying original

    # Deduplicate based on 'name' and 'state', keeping the first occurrence
    if not combined_df.empty and 'name' in combined_df.columns and 'state' in combined_df.columns:
        combined_df.drop_duplicates(subset=['name', 'state'], keep='first', inplace=True)

    return combined_df


def get_state_coordinates():
    """Get approximate coordinates for Indian states (simplified)"""
    return {
        'Andhra Pradesh': [16.5, 80.6], 'Bihar': [25.4, 85.4], 'Chhattisgarh': [21.3, 81.6],
        'Gujarat': [22.3, 72.6], 'Jammu & Kashmir': [34.1, 74.8], 'Karnataka': [15.3, 75.7],
        'Kerala': [10.8, 76.3], 'Madhya Pradesh': [23.2, 77.4], 'Maharashtra': [19.2, 73.2],
        'Odisha': [20.3, 85.8], 'Punjab': [31.1, 75.3], 'Rajasthan': [27.0, 74.2],
        'Tamil Nadu': [11.1, 78.7], 'Uttar Pradesh': [26.8, 80.9], 'West Bengal': [22.6, 88.4],
        'Arunachal Pradesh': [27.1004, 93.6167], 'Sikkim': [27.5330, 88.5122],
        'Nagaland': [26.1584, 94.5624], 'Mizoram': [23.1645, 92.9376],
        'Meghalaya': [25.4670, 91.3662], 'Tripura': [23.9408, 91.9882],
        'Manipur': [24.6637, 93.9063], 'Assam': [26.2006, 92.9376],
        'Jharkhand': [23.6102, 85.2799], 'Uttarakhand': [30.0668, 79.0193],
        'Himachal Pradesh': [31.1048, 77.1734], 'Telangana': [18.1124, 79.0193]
        # Add any other states from your CRAFTS table if they are not here and have crafts
    }

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

/* Filter Section */
.filter-section {
    background-color: #f8f9fa;
    padding: 1.5rem;
    border-radius: 10px;
    margin-bottom: 2rem;
    box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}

/* Art Form Cards */
.art-card {
    background-color: white;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    height: 100%; 
    display: flex;
    flex-direction: column;
}
.art-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 16px rgba(0,0,0,0.15);
}
.art-card-image {
    width: 100%;
    height: 200px; 
    object-fit: cover; 
}
.art-card-content {
    padding: 1.5rem;
    flex-grow: 1; 
    display: flex;
    flex-direction: column;
}
.art-card-title {
    font-size: 1.4rem;
    font-weight: 600;
    color: #2c3e50;
    margin-bottom: 0.5rem;
}
.art-card-subtitle {
    font-size: 1rem;
    color: #7f8c8d;
    margin-bottom: 1rem;
}
.art-card-description {
    font-size: 0.95rem;
    color: #555;
    line-height: 1.5;
    flex-grow: 1; 
    margin-bottom: 1rem; 
}
.art-card-footer {
    margin-top: auto; 
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.gi-tag {
    background-color: #2ecc71;
    color: white;
    padding: 0.3rem 0.6rem;
    border-radius: 4px;
    font-size: 0.8rem;
    font-weight: 500;
}

/* Detail View */
.detail-container {
    background-color: white;
    border-radius: 10px;
    padding: 2rem;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    margin-top: 2rem;
}
.detail-header {
    display: flex;
    align-items: center;
    margin-bottom: 1.5rem;
}
.detail-title {
    font-size: 2rem;
    font-weight: 700;
    color: #2c3e50;
    margin-right: 1rem;
}
.detail-image {
    width: 100%;
    max-height: 400px;
    object-fit: cover;
    border-radius: 8px;
    margin-bottom: 1.5rem;
}
.detail-info {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 1.5rem;
    margin-bottom: 1.5rem;
}
.info-card {
    background-color: #f8f9fa;
    padding: 1.2rem;
    border-radius: 8px;
    border-left: 4px solid #3498db;
}
.info-card h4 {
    font-size: 1.2rem;
    color: #2c3e50;
    margin-bottom: 0.5rem;
}
.info-card p {
    color: #555;
    font-size: 1rem;
    line-height: 1.5;
}
.map-container {
    height: 400px;
    width: 100%;
    border-radius: 8px;
    overflow: hidden;
    margin-top: 1.5rem;
}
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("""
<div class="header">
    <h1>🎨 Art Forms Explorer</h1>
    <p>Discover India's rich artistic heritage through its diverse traditional art forms. Filter by state, type, or search for specific art forms to begin your cultural journey.</p>
</div>
""", unsafe_allow_html=True)

# --- Load Data ---
art_forms_df = get_art_forms_combined()

# --- Filters ---
st.markdown('<div class="filter-section">', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    unique_states = []
    if not art_forms_df.empty and 'state' in art_forms_df.columns:
        unique_states = sorted(art_forms_df['state'].dropna().unique().tolist())
    selected_state = st.selectbox(
        "Filter by State",
        ["All States"] + unique_states
    )

with col2:
    unique_types = []
    if not art_forms_df.empty and 'type' in art_forms_df.columns:
        unique_types = sorted(art_forms_df['type'].dropna().unique().tolist())
    selected_type = st.selectbox(
        "Filter by Art Type",
        ["All Types"] + unique_types
    )

with col3:
    search_term = st.text_input("Search Art Forms", "")

st.markdown('</div>', unsafe_allow_html=True)

# --- Apply Filters ---
filtered_df = art_forms_df.copy()

if selected_state != "All States":
    if not filtered_df.empty: 
        filtered_df = filtered_df[filtered_df['state'] == selected_state]

if selected_type != "All Types":
    if not filtered_df.empty: 
        filtered_df = filtered_df[filtered_df['type'] == selected_type]

if search_term:
    if not filtered_df.empty: 
        name_condition = pd.Series([False] * len(filtered_df), index=filtered_df.index)
        desc_condition = pd.Series([False] * len(filtered_df), index=filtered_df.index)

        if 'name' in filtered_df.columns:
            name_condition = filtered_df['name'].str.contains(search_term, case=False, na=False)
        if 'description' in filtered_df.columns:
            desc_condition = filtered_df['description'].str.contains(search_term, case=False, na=False)
        
        filtered_df = filtered_df[name_condition | desc_condition]


# --- Display Art Forms Grid ---
if filtered_df.empty:
    st.info("No art forms match your filters. Try adjusting your criteria.")
else:
    num_columns = 3
    for i in range(0, len(filtered_df), num_columns):
        cols = st.columns(num_columns)
        for j in range(num_columns):
            if i + j < len(filtered_df):
                art = filtered_df.iloc[i + j]
                with cols[j]:
                    art_description = str(art.get('description', 'No description available.'))
                    if len(art_description) > 100:
                        art_description = art_description[:100] + "..."
                    
                    art_image_url = art.get('image_url', 'https://via.placeholder.com/300x200.png?text=Image+Not+Available')
                    art_name_for_key = str(art.get('name', '')).replace(" ", "_").replace("/", "_") # Sanitize name for key

                    st.markdown(f"""
                    <div class="art-card">
                        <img src="{art_image_url}" class="art-card-image" alt="{art.get('name', 'N/A')}">
                        <div class="art-card-content">
                            <div class="art-card-title">{art.get('name', 'N/A')}</div>
                            <div class="art-card-subtitle">{art.get('type', 'N/A')} • {art.get('state', 'N/A')}</div>
                            <div class="art-card-description">{art_description}</div>
                            <div class="art-card-footer">
                                {'<span class="gi-tag">GI Tagged</span>' if art.get('gi_tag', False) else ''}
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"View Details: {art.get('name', 'N/A')}", key=f"view_{art_name_for_key}_{i+j}"): 
                        st.session_state.selected_art = art.get('name')
                        st.rerun()

# --- Detailed View ---
if 'selected_art' in st.session_state and st.session_state.selected_art:
    art_series_list = art_forms_df[art_forms_df['name'] == st.session_state.selected_art]
    if not art_series_list.empty:
        art = art_series_list.iloc[0] # Use .iloc[0] to get the Series
    
        st.markdown('<div class="detail-container">', unsafe_allow_html=True)
        
        if st.button("← Back to Art Forms"):
            del st.session_state.selected_art
            st.rerun()
        
        st.markdown(f"""
        <div class="detail-header">
            <div class="detail-title">{art.get('name', 'N/A')}</div>
            {'<span class="gi-tag">GI Tagged</span>' if art.get('gi_tag', False) else ''}
        </div>
        """, unsafe_allow_html=True)
        
        st.image(art.get('image_url', 'https://via.placeholder.com/300x200.png?text=Image+Not+Available'), use_container_width=True, caption=f"{art.get('name', 'N/A')} - {art.get('type', 'N/A')} from {art.get('state', 'N/A')}")
        
        st.markdown(f"### About {art.get('name', 'N/A')}")
        st.write(art.get('description', 'No description available.'))
        
        st.markdown("### Details")
        col1_detail, col2_detail = st.columns(2) # Renamed to avoid conflict with outer scope col1, col2
        
        with col1_detail:
            st.markdown(f"""
            <div class="info-card">
                <h4>Origin</h4>
                <p>{art.get('state', 'N/A')}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="info-card">
                <h4>Government Support</h4>
                <p>Scheme: {art.get('govt_scheme', 'N/A')}<br>Allocation: {art.get('allocation_amount', 'N/A')}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2_detail:
            st.markdown(f"""
            <div class="info-card">
                <h4>Art Type</h4>
                <p>{art.get('type', 'N/A')}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="info-card">
                <h4>Artisan Cooperative</h4>
                <p>{art.get('artisan_cooperative', 'N/A')}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("### Data Story")
        st.write(f"""
        This art form originates from {art.get('state', 'N/A')}.
        Government initiatives like {art.get('govt_scheme', 'N/A')} have allocated {art.get('allocation_amount', 'N/A')} for its promotion.
        It has a GI Tag: {"Yes" if art.get('gi_tag', False) else "No"}.
        Supporting local artisans through {art.get('artisan_cooperative', 'N/A')} helps preserve this cultural heritage and provides sustainable livelihoods.
        """)
        
        st.markdown("### Where to Find")
        art_lat = art.get('latitude')
        art_lon = art.get('longitude')

        if pd.notna(art_lat) and pd.notna(art_lon):
            try:
                art_lat_float = float(art_lat)
                art_lon_float = float(art_lon)
                m = folium.Map(location=[art_lat_float, art_lon_float], zoom_start=7)
                folium.Marker(
                    [art_lat_float, art_lon_float],
                    popup=f"{art.get('name', 'N/A')}<br>{art.get('state', 'N/A')}",
                    tooltip=art.get('name', 'N/A'),
                    icon=folium.Icon(color="red", icon="palette", prefix="fa")
                ).add_to(m)
                
                folium.Circle(
                    [art_lat_float, art_lon_float],
                    radius=50000,
                    color="#FF6347",
                    fill=True,
                    fill_color="#FF6347",
                    fill_opacity=0.2
                ).add_to(m)
                folium_static(m)
            except ValueError:
                st.warning("Map could not be displayed due to invalid coordinates for this art form.")
        else:
            st.info("Location data (latitude/longitude) is not available for this art form to display on the map.")
        
        st.markdown("</div>", unsafe_allow_html=True)
    elif 'selected_art' in st.session_state and st.session_state.selected_art: # Only show warning if art was selected but not found
        st.warning(f"Details for '{st.session_state.selected_art}' could not be found. It might have been removed by a filter or data change.")