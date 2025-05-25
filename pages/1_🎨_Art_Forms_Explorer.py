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
def get_snowflake_connection():
    return st.connection("snowflake")

# --- Image Overrides ---
# Add names of art forms (as they appear from Snowflake) and their real image URLs here
# This dictionary will be used to override the default placeholder images.
# Example:
# ART_FORM_IMAGE_OVERRIDES = {
# "Metalware - Dhokra": "https://link_to_your_dhokra_image.jpg",
# "Nirmal Painting": "https://link_to_your_nirmal_painting_image.jpg",
# }
ART_FORM_IMAGE_OVERRIDES = {
    # Add your specific art form names and their image URLs here
    # e.g., "Pattachitra Painting from Snowflake": "your_real_image_url.jpg",
}

# --- Data Fetching Functions ---

def get_crafts_from_snowflake():
    """Fetch crafts data from Snowflake CRAFTS table."""
    try:
        conn = get_snowflake_connection()
        # If your CRAFTS table has an IMAGE_URL column, add it here: e.g., "C5" AS CRAFT_IMAGE_URL_SF
        query = 'SELECT "C1" AS CRAFT_STATE_UT, "C2" AS CRAFT_DISTRICT, "C3" AS CRAFT_NAME_SF, "C4" AS CRAFT_VILLAGE FROM "CRAFTS";'
        df = conn.query(query, ttl=3600)
        return df
    except Exception as e:
        st.error(f"Error fetching crafts from Snowflake: {e}")
        return pd.DataFrame()

def get_paintings_from_snowflake():
    """Fetch painting data from Snowflake PAINTING table."""
    try:
        conn = get_snowflake_connection()
        # If your PAINTING table has an IMAGE_URL column, add it here: e.g., "IMAGE_FILE_NAME" AS PAINTING_IMAGE_URL_SF
        query = 'SELECT "PAINTING" AS PAINTING_NAME_SF, "REGION_STATE" AS PAINTING_REGION_STATE, "DESCRIPTION" AS PAINTING_DESC FROM "PAINTING";'
        df = conn.query(query, ttl=3600)
        return df
    except Exception as e:
        st.error(f"Error fetching paintings from Snowflake: {e}")
        return pd.DataFrame()

def get_dances_from_snowflake():
    """Fetch dance data from Snowflake DANCE table."""
    try:
        conn = get_snowflake_connection()
        # If your DANCE table has an IMAGE_URL column, add it here: e.g., "URL_FOR_IMAGE" AS DANCE_IMAGE_URL_SF
        query = 'SELECT "DANCE" AS DANCE_NAME_SF, "REGION_STATE" AS DANCE_REGION_STATE, "DESCRIPTION" AS DANCE_DESC FROM "DANCE";'
        df = conn.query(query, ttl=3600)
        return df
    except Exception as e:
        st.error(f"Error fetching dances from Snowflake: {e}")
        return pd.DataFrame()

def get_art_forms_combined():
    """
    Fetch art forms data, combining hardcoded data with data from Snowflake.
    """
    all_data_frames = []
    state_coords_dict = get_state_coordinates()

    # 1. Get hardcoded art forms
    hardcoded_art_forms_df = pd.DataFrame({
        'name': [ 
            'Pashmina Shawls', 'Banarasi Silk', 'Phulkari', 'Chikankari', 'Kantha', 
            'Bidriware', 'Dhokra' 
        ],
        'type': ['Textile']*5 + ['Craft']*2,
        'state': [
            'Jammu & Kashmir', 'Uttar Pradesh', 'Punjab', 'Uttar Pradesh', 'West Bengal',
            'Karnataka', 'Chhattisgarh'
        ],
        'gi_tag': [ True, True, True, True, False, True, False],
        'description': [
            'Exquisite handwoven shawls made from the finest cashmere wool...', 'Luxurious silk textiles woven with intricate gold and silver brocade...',
            'Embroidery technique from Punjab with colorful thread work...', 'Delicate and intricate hand embroidery from Lucknow...',
            'Running stitch embroidery used to make quilts and decorative items.', 'Metal handicraft from Bidar, Karnataka...',
            'Ancient bell metal craft practiced by the Dhokra Damar tribes...'
        ],
        'image_url': [ # These are real URLs
            'https://raw.githubusercontent.com/yashgupta17402/hero/main/pashmina.jpg', # Pashmina Shawls
            'https://raw.githubusercontent.com/yashgupta17402/hero/main/banarasi.jpg', # Banarasi Silk
            'https://raw.githubusercontent.com/yashgupta17402/hero/main/phulkari.jpg', # Phulkari
            'https://raw.githubusercontent.com/yashgupta17402/hero/main/chikankari.jpg', # Chikankari
            'https://raw.githubusercontent.com/yashgupta17402/hero/main/kantha.jpg', # Kantha
            'https://raw.githubusercontent.com/yashgupta17402/hero/main/bidriware.jpg', # Bidriware
            'https://raw.githubusercontent.com/yashgupta17402/hero/main/dhokra.jpg'  # Dhokra
        ],
        'latitude': [34.1, 25.3, 31.1, 26.8, 22.6, 17.9, 21.3],
        'longitude': [74.8, 83.0, 75.3, 80.9, 88.4, 77.5, 81.6],
        'govt_scheme': ['National Handicraft Development Program'] * 7,
        'allocation_amount': ['₹3.1 Cr', '₹2.7 Cr', '₹1.9 Cr', '₹2.3 Cr', '₹1.4 Cr', '₹1.6 Cr', '₹1.1 Cr'],
        'artisan_cooperative': ['Kashmir Pashmina Artisans Cooperative', 'Varanasi Weavers Association', 
                                'Punjab Phulkari Cooperative', 'Lucknow Chikankari Kala Kendra', 
                                'Bengal Women Artisans Cooperative', 'Bidri Craft Association',
                                'Bastar Dhokra Shilp Cooperative']
    })
    if not hardcoded_art_forms_df.empty:
        all_data_frames.append(hardcoded_art_forms_df)

    # Helper function for image URL
    def get_image_url(name, default_text, sf_image_url_value=None):
        if sf_image_url_value and pd.notna(sf_image_url_value): # If URL provided from Snowflake
            return sf_image_url_value
        if name in ART_FORM_IMAGE_OVERRIDES: # Check override dictionary
            return ART_FORM_IMAGE_OVERRIDES[name]
        image_text = name.replace(" ", "+").replace("/", "_") if pd.notna(name) else default_text
        return f'https://via.placeholder.com/300x200.png?text={image_text}'


    # 2. Get PAINTINGS from Snowflake
    paintings_sf_df_raw = get_paintings_from_snowflake()
    if not paintings_sf_df_raw.empty:
        transformed_paintings_list = []
        for _, row in paintings_sf_df_raw.iterrows():
            state = row.get('PAINTING_REGION_STATE', None)
            name = row.get('PAINTING_NAME_SF', 'Unknown Painting')
            desc = row.get('PAINTING_DESC', f'Traditional painting style from {state if state else "India"}.')
            sf_image_url = row.get('PAINTING_IMAGE_URL_SF', None) # Assuming you added this alias if col exists in SF
            image_to_use = get_image_url(name, "Painting", sf_image_url)
            lat, lon = (state_coords_dict.get(state, [None, None])) if state else (None, None)
            transformed_paintings_list.append({
                'name': name, 'type': 'Painting', 'state': state, 'gi_tag': False, 
                'description': desc, 'image_url': image_to_use, 
                'latitude': lat, 'longitude': lon,
                'govt_scheme': 'To be updated', 'allocation_amount': 'N/A', 'artisan_cooperative': 'To be updated'
            })
        all_data_frames.append(pd.DataFrame(transformed_paintings_list))

    # 3. Get DANCES from Snowflake
    dances_sf_df_raw = get_dances_from_snowflake()
    if not dances_sf_df_raw.empty:
        transformed_dances_list = []
        for _, row in dances_sf_df_raw.iterrows():
            state = row.get('DANCE_REGION_STATE', None)
            name = row.get('DANCE_NAME_SF', 'Unknown Dance')
            desc = row.get('DANCE_DESC', f'Traditional dance form from {state if state else "India"}.')
            sf_image_url = row.get('DANCE_IMAGE_URL_SF', None) # Assuming you added this alias
            image_to_use = get_image_url(name, "Dance", sf_image_url)
            lat, lon = (state_coords_dict.get(state, [None, None])) if state else (None, None)
            transformed_dances_list.append({
                'name': name, 'type': 'Dance', 'state': state, 'gi_tag': False, 
                'description': desc, 'image_url': image_to_use,
                'latitude': lat, 'longitude': lon,
                'govt_scheme': 'To be updated', 'allocation_amount': 'N/A', 'artisan_cooperative': 'To be updated'
            })
        all_data_frames.append(pd.DataFrame(transformed_dances_list))

    # 4. Get CRAFTS from Snowflake
    crafts_sf_df_raw = get_crafts_from_snowflake()
    if not crafts_sf_df_raw.empty:
        transformed_crafts_list = []
        for _, row in crafts_sf_df_raw.iterrows():
            state = row.get('CRAFT_STATE_UT', None)
            name = row.get('CRAFT_NAME_SF', 'Unknown Craft')
            district = row.get('CRAFT_DISTRICT', 'Unknown District')
            village = row.get('CRAFT_VILLAGE', 'Unknown Village')
            sf_image_url = row.get('CRAFT_IMAGE_URL_SF', None) # Assuming you added this alias
            image_to_use = get_image_url(name, "Craft", sf_image_url)
            lat, lon = (state_coords_dict.get(state, [None, None])) if state else (None, None)
            transformed_crafts_list.append({
                'name': name, 'type': 'Craft', 'state': state, 'gi_tag': False,
                'description': f"A traditional {name} from {district}, {state if state else 'N/A'}. Practiced in {village}.",
                'image_url': image_to_use,
                'latitude': lat, 'longitude': lon,
                'govt_scheme': 'To be updated', 'allocation_amount': 'N/A', 'artisan_cooperative': 'To be updated'
            })
        all_data_frames.append(pd.DataFrame(transformed_crafts_list))

    if not all_data_frames: 
        return pd.DataFrame(columns=['name', 'type', 'state', 'gi_tag', 'description', 'image_url', 'latitude', 'longitude', 'govt_scheme', 'allocation_amount', 'artisan_cooperative'])
    combined_df = pd.concat(all_data_frames, ignore_index=True)
    if not combined_df.empty and 'name' in combined_df.columns and 'state' in combined_df.columns:
        combined_df.drop_duplicates(subset=['name', 'state'], keep='first', inplace=True)
    return combined_df

def get_state_coordinates():
    """Get approximate coordinates for Indian states. Ensure this is comprehensive."""
    # (Same as previous version - ensure it's complete for your states)
    return {
        'Andhra Pradesh': [16.5, 80.6], 'Arunachal Pradesh': [27.1004, 93.6167], 'Assam': [26.2006, 92.9376],
        'Bihar': [25.4, 85.4], 'Chhattisgarh': [21.3, 81.6], 'Goa': [15.2993, 74.1240], 
        'Gujarat': [22.3, 72.6], 'Haryana': [29.0588, 76.0856], 
        'Himachal Pradesh': [31.1048, 77.1734], 'Jharkhand': [23.6102, 85.2799],
        'Jammu & Kashmir': [34.1, 74.8], 'Karnataka': [15.3, 75.7], 'Kerala': [10.8, 76.3],
        'Madhya Pradesh': [23.2, 77.4], 'Maharashtra': [19.2, 73.2], 'Manipur': [24.6637, 93.9063],
        'Meghalaya': [25.4670, 91.3662], 'Mizoram': [23.1645, 92.9376], 'Nagaland': [26.1584, 94.5624],
        'Odisha': [20.3, 85.8], 'Punjab': [31.1, 75.3], 'Rajasthan': [27.0, 74.2],
        'Sikkim': [27.5330, 88.5122], 'Tamil Nadu': [11.1, 78.7], 'Telangana': [18.1124, 79.0193],
        'Tripura': [23.9408, 91.9882], 'Uttar Pradesh': [26.8, 80.9], 'Uttarakhand': [30.0668, 79.0193],
        'West Bengal': [22.6, 88.4],
        'Odisha, West Bengal': [21.5, 87.0], 'Odisha, Jharkhand, West Bengal': [22.5, 87.0], 
        'Gujarat, Madhya Pradesh': [22.8, 73.0], 'Rajasthan, Himachal Pradesh': [29.0, 76.0],
        'Andhra Pradesh, Telangana': [17.0, 79.5] 
    }

# --- CSS Styling ---
# (Your existing CSS - no changes needed here)
st.markdown("""
<style>
/* Global Page Styling */
.main { background-color: white; color: #333; }
/* Header Styling */
.header { padding: 1rem 0; text-align: center; margin-bottom: 2rem; }
.header h1 { color: #2c3e50; font-size: 2.5rem; font-weight: 700; }
.header p { color: #555; font-size: 1.2rem; max-width: 800px; margin: 0 auto; }
/* Filter Section */
.filter-section { background-color: #f8f9fa; padding: 1.5rem; border-radius: 10px; margin-bottom: 2rem; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
/* Art Form Cards */
.art-card { background-color: white; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 8px rgba(0,0,0,0.1); transition: transform 0.3s ease, box-shadow 0.3s ease; height: 100%; display: flex; flex-direction: column; }
.art-card:hover { transform: translateY(-5px); box-shadow: 0 8px 16px rgba(0,0,0,0.15); }
.art-card-image { width: 100%; height: 200px; object-fit: cover; }
.art-card-content { padding: 1.5rem; flex-grow: 1; display: flex; flex-direction: column; }
.art-card-title { font-size: 1.4rem; font-weight: 600; color: #2c3e50; margin-bottom: 0.5rem; }
.art-card-subtitle { font-size: 1rem; color: #7f8c8d; margin-bottom: 1rem; }
.art-card-description { font-size: 0.95rem; color: #555; line-height: 1.5; flex-grow: 1; margin-bottom: 1rem; }
.art-card-footer { margin-top: auto; display: flex; justify-content: space-between; align-items: center; }
.gi-tag { background-color: #2ecc71; color: white; padding: 0.3rem 0.6rem; border-radius: 4px; font-size: 0.8rem; font-weight: 500; }
.non-gi-tag { background-color: #e74c3c; color: white; padding: 0.3rem 0.6rem; border-radius: 4px; font-size: 0.8rem; font-weight: 500; } /* Style for Non GI */
/* Detail View */
.detail-container { background-color: white; border-radius: 10px; padding: 2rem; box-shadow: 0 4px 12px rgba(0,0,0,0.1); margin-top: 2rem; }
.detail-header { display: flex; align-items: center; margin-bottom: 1.5rem; }
.detail-title { font-size: 2rem; font-weight: 700; color: #2c3e50; margin-right: 1rem; }
.detail-image { width: 100%; max-height: 400px; object-fit: cover; border-radius: 8px; margin-bottom: 1.5rem; }
.detail-info { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 1.5rem; margin-bottom: 1.5rem; }
.info-card { background-color: #f8f9fa; padding: 1.2rem; border-radius: 8px; border-left: 4px solid #3498db; }
.info-card h4 { font-size: 1.2rem; color: #2c3e50; margin-bottom: 0.5rem; }
.info-card p { color: #555; font-size: 1rem; line-height: 1.5; }
.map-container { height: 400px; width: 100%; border-radius: 8px; overflow: hidden; margin-top: 1.5rem; }
</style>
""", unsafe_allow_html=True)

# --- Header ---
# (Header markdown remains the same)
st.markdown("""
<div class="header">
    <h1>🎨 Art Forms Explorer</h1>
    <p>Discover India's rich artistic heritage through its diverse traditional art forms. Filter by state, type, or search for specific art forms to begin your cultural journey.</p>
</div>
""", unsafe_allow_html=True)

# --- Load Data ---
art_forms_df = get_art_forms_combined()

# --- Filters ---
# (Filters section remains the same - ensure unique_states and unique_types are handled if art_forms_df is empty)
st.markdown('<div class="filter-section">', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    unique_states = []
    if not art_forms_df.empty and 'state' in art_forms_df.columns:
        valid_states = [s for s in art_forms_df['state'].unique() if pd.notna(s)]
        unique_states = sorted(list(set(valid_states)))
    selected_state = st.selectbox(
        "Filter by State", ["All States"] + unique_states, key="state_filter_select_main"
    )

with col2:
    unique_types = []
    if not art_forms_df.empty and 'type' in art_forms_df.columns:
        valid_types = [t for t in art_forms_df['type'].unique() if pd.notna(t)]
        unique_types = sorted(list(set(valid_types)))
    selected_type = st.selectbox(
        "Filter by Art Type", ["All Types"] + unique_types, key="type_filter_select_main"
    )

with col3:
    search_term = st.text_input("Search Art Forms", key="search_art_forms_input_main")

st.markdown('</div>', unsafe_allow_html=True)

# --- Apply Filters ---
# (Apply Filters section remains the same)
filtered_df = art_forms_df.copy()
if selected_state != "All States":
    if not filtered_df.empty and 'state' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['state'] == selected_state]
if selected_type != "All Types":
    if not filtered_df.empty and 'type' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['type'] == selected_type]
if search_term:
    if not filtered_df.empty:
        name_condition = pd.Series([False] * len(filtered_df), index=filtered_df.index)
        desc_condition = pd.Series([False] * len(filtered_df), index=filtered_df.index)
        if 'name' in filtered_df.columns:
            name_condition = filtered_df['name'].astype(str).str.contains(search_term, case=False, na=False)
        if 'description' in filtered_df.columns:
            desc_condition = filtered_df['description'].astype(str).str.contains(search_term, case=False, na=False)
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
                    art_description_text = str(art.get('description', 'No description available.'))
                    if len(art_description_text) > 100:
                        art_description_text = art_description_text[:100] + "..."
                    
                    art_image_url_val = art.get('image_url', 'https://via.placeholder.com/300x200.png?text=Image+Not+Available')
                    art_name_for_key_val = str(art.get('name', 'N/A')).replace(" ", "_").replace("/", "_").replace("&","").replace("'", "")

                    # GI Tag display updated
                    gi_tag_html = ''
                    if art.get('gi_tag', False): # If True
                        gi_tag_html = '<span class="gi-tag">GI Tagged</span>'
                    else: # If False or missing (defaults to False)
                        gi_tag_html = '<span class="non-gi-tag">Non GI</span>'


                    st.markdown(f"""
                    <div class="art-card">
                        <img src="{art_image_url_val}" class="art-card-image" alt="{art.get('name', 'N/A')}">
                        <div class="art-card-content">
                            <div class="art-card-title">{art.get('name', 'N/A')}</div>
                            <div class="art-card-subtitle">{art.get('type', 'N/A')} • {art.get('state', 'N/A')}</div>
                            <div class="art-card-description">{art_description_text}</div>
                            <div class="art-card-footer">
                                {gi_tag_html}
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    button_key = f"view_details_{art_name_for_key_val}_{i}_{j}" 
                    if st.button(f"View Details: {art.get('name', 'N/A')}", key=button_key): 
                        st.session_state.selected_art = art.get('name')
                        st.rerun()

# --- Detailed View ---
if 'selected_art' in st.session_state and st.session_state.selected_art:
    if not art_forms_df.empty and 'name' in art_forms_df.columns:
        art_series_list = art_forms_df[art_forms_df['name'] == st.session_state.selected_art]
        if not art_series_list.empty:
            art = art_series_list.iloc[0]
        
            st.markdown('<div class="detail-container">', unsafe_allow_html=True)
            
            if st.button("← Back to Art Forms", key="detail_view_back_button"): 
                del st.session_state.selected_art
                st.rerun()
            
            # GI Tag display updated for detail view
            gi_tag_detail_html = ''
            if art.get('gi_tag', False):
                gi_tag_detail_html = '<span class="gi-tag">GI Tagged</span>'
            else:
                gi_tag_detail_html = '<span class="non-gi-tag">Non GI</span>'

            st.markdown(f"""
            <div class="detail-header">
                <div class="detail-title">{art.get('name', 'N/A')}</div>
                {gi_tag_detail_html}
            </div>
            """, unsafe_allow_html=True)
            
            st.image(art.get('image_url', 'https://via.placeholder.com/300x200.png?text=Image+Not+Available'), use_column_width=True, caption=f"{art.get('name', 'N/A')} - {art.get('type', 'N/A')} from {art.get('state', 'N/A')}")
            
            st.markdown(f"### About {art.get('name', 'N/A')}")
            st.write(art.get('description', 'No description available.'))
            
            st.markdown("### Details")
            col1_detail_view, col2_detail_view = st.columns(2)
            
            with col1_detail_view:
                st.markdown(f"""<div class="info-card"><h4>Origin</h4><p>{art.get('state', 'N/A')}</p></div>""", unsafe_allow_html=True)
                st.markdown(f"""<div class="info-card"><h4>Government Support</h4><p>Scheme: {art.get('govt_scheme', 'N/A')}<br>Allocation: {art.get('allocation_amount', 'N/A')}</p></div>""", unsafe_allow_html=True)
            
            with col2_detail_view:
                st.markdown(f"""<div class="info-card"><h4>Art Type</h4><p>{art.get('type', 'N/A')}</p></div>""", unsafe_allow_html=True)
                st.markdown(f"""<div class="info-card"><h4>Artisan Cooperative</h4><p>{art.get('artisan_cooperative', 'N/A')}</p></div>""", unsafe_allow_html=True)
            
            st.markdown("### Data Story") # GI Tag info in data story remains "Yes/No" which is fine.
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
                        [art_lat_float, art_lon_float], radius=50000, color="#FF6347",
                        fill=True, fill_color="#FF6347", fill_opacity=0.2
                    ).add_to(m)
                    folium_static(m)
                except ValueError:
                    st.warning(f"Map could not be displayed for '{art.get('name', 'N/A')}' due to invalid coordinates.")
            else:
                st.info(f"Location data (latitude/longitude) is not available for '{art.get('name', 'N/A')}' to display on the map.")
            st.markdown("</div>", unsafe_allow_html=True)
        elif 'selected_art' in st.session_state and st.session_state.selected_art: 
            st.warning(f"Details for '{st.session_state.selected_art}' could not be found in the current dataset.")
    elif 'selected_art' in st.session_state and st.session_state.selected_art :
         st.warning(f"Art forms data is not available. Cannot display details for '{st.session_state.selected_art}'.")