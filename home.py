import streamlit as st
import time
import pandas as pd
import random
from datetime import datetime

# --- Global Configuration ---
AUTOPLAY_INTERVAL = 5 # seconds

# --- Page Configuration ---
st.set_page_config(
    page_title="Cultural Canvas India: Explore, Experience, Preserve",
    layout="wide",
    initial_sidebar_state="auto",
    page_icon="🎨"
)

# --- Simulated Database Functions & Snowflake Data Loading ---
def get_slideshow_data():
    """Fetch slideshow data from database (simulated)"""
    return [
        {
            "imgSrc": "https://raw.githubusercontent.com/yashgupta17402/hero/main/kathakali.PNG",
            "title": "Vibrant Traditions: A Tapestry of Art",
            "description": "India's artistic heritage is a kaleidoscope of color, skill, and ancient wisdom. From intricate paintings to mesmerizing dance forms, discover the soul of a nation expressed through its art.",
            "cta_button_text": "Explore Art Forms",
            "cta_link": "Art_Forms_Explorer"
        },
        {
            "imgSrc": "https://raw.githubusercontent.com/yashgupta17402/hero/main/AGRA_FORT.PNG",
            "title": "Journey Through Time: Uncover Cultural Hotspots",
            "description": "Explore majestic forts, ancient temples, and bustling cultural hubs. Find popular destinations and unearth hidden gems waiting to share their stories.",
            "cta_button_text": "Discover Destinations",
            "cta_link": "Cultural_Hotspots_Map"
        },
        {
            "imgSrc": "https://raw.githubusercontent.com/yashgupta17402/hero/main/handloom.PNG",
            "title": "Travel with Purpose: Embrace Responsible Tourism",
            "description": "Be a part of preserving India's cultural treasures. Learn how your travels can support local communities, protect heritage, and ensure these traditions thrive for generations.",
            "cta_button_text": "Learn About Responsible Travel",
            "cta_link": "Responsible_Tourism_Guide"
        }
    ]

def get_top_cultural_states():
    """Fetch top 3 most visited cultural states (simulated) based on 2023 data"""
    return [
        {
            "state": "Uttar Pradesh", "visitors": "478.5M", "image": "https://raw.githubusercontent.com/yashgupta17402/hero/main/up.PNG",
            "description": "Featuring iconic monuments like the Taj Mahal, the spiritual city of Varanasi, and a rich historical tapestry.", "explore_url": "https://www.uptourism.gov.in/"
        },
        {
            "state": "Tamil Nadu", "visitors": "286.0M", "image": "https://raw.githubusercontent.com/yashgupta17402/hero/main/tamilnadu.PNG",
            "description": "Home to magnificent ancient temples, classical dance forms, vibrant festivals, and rich Dravidian culture.", "explore_url": "https://www.tamilnadutourism.tn.gov.in/"
        },
        {
            "state": "Karnataka", "visitors": "284.1M", "image": "https://raw.githubusercontent.com/yashgupta17402/hero/main/karnataka.PNG",
            "description": "A blend of ancient heritage with stunning palaces like Mysore, vibrant IT hubs, and rich traditions.", "explore_url": "https://www.karnatakatourism.org/"
        }
    ]

def get_all_gi_art_forms():
    """Fetch all GI-tagged art forms (simulated)"""
    gi_art_forms = [
        {
            "name": "Madhubani Painting", "region": "Bihar", "image": "https://raw.githubusercontent.com/yashgupta17402/hero/main/madhubani.PNG",
            "description": "Characterized by geometric patterns and nature motifs, this ancient art form has been practiced for centuries.", "learn_more_url": "https://en.wikipedia.org/wiki/Madhubani_art"
        },
        {
            "name": "Kani Shawls", "region": "Kashmir", "image": "https://raw.githubusercontent.com/yashgupta17402/hero/main/kani.PNG",
            "description": "It is one of the oldest handicrafts of Kashmir. This craft has been a part of the valley since the time of the Mughals. The shawls are woven from pashmina yarn.", "learn_more_url": "https://en.wikipedia.org/wiki/Kani_shawl"
        },
        {
            "name": "Banarasi Silk", "region": "Uttar Pradesh", "image": "https://raw.githubusercontent.com/yashgupta17402/hero/main/banaras_1.PNG",
            "description": " Finest traditional sarees in India, renowned for their opulent embroidery and luxurious silk. These sarees are distinguished by their intricate brocade work, often featuring gold (zari) and silver (brocade) threads, woven into elaborate designs", "learn_more_url": "https://en.wikipedia.org/wiki/Banarasi_sari"
        }
    ]
    return gi_art_forms

def get_upcoming_festival():
    """Fetch a major upcoming festival (simulated)"""
    year = datetime.now().year
    festivals_data = [
        {"name": "Diwali", "month": 11, "day": 1, "location": "Nationwide", "image": "https://raw.githubusercontent.com/yashgupta17402/hero/main/diwali.PNG", "description": "The festival of lights celebrates the victory of light over darkness with lamps, fireworks, and family gatherings."},
        {"name": "Holi", "month": 3, "day": 25, "location": "Nationwide", "image": "https://raw.githubusercontent.com/yashgupta17402/hero/main/holi.jpg", "description": "The colorful spring festival where people throw colored powders and water at each other in joyful celebration."},
        {"name": "Pongal", "month": 1, "day": 14, "location": "Tamil Nadu", "image": "https://raw.githubusercontent.com/yashgupta17402/hero/main/pongal.jpg", "description": "A harvest festival dedicated to the Sun God, featuring elaborate kolam designs and special rice dishes."}
    ]
    now = datetime.now()
    upcoming_festivals = []
    for fest_template in festivals_data:
        try:
            fest_date_current_year = datetime(year, fest_template["month"], fest_template["day"])
            if fest_date_current_year >= now:
                upcoming_festivals.append({**fest_template, "date_obj": fest_date_current_year, "date": fest_date_current_year.strftime("%B %d, %Y")})
            else:
                fest_date_next_year = datetime(year + 1, fest_template["month"], fest_template["day"])
                upcoming_festivals.append({**fest_template, "date_obj": fest_date_next_year, "date": fest_date_next_year.strftime("%B %d, %Y")})
        except ValueError:
            try:
                fest_date_next_year = datetime(year + 1, fest_template["month"], fest_template["day"])
                if fest_date_next_year >= now: upcoming_festivals.append({**fest_template, "date_obj": fest_date_next_year, "date": fest_date_next_year.strftime("%B %d, %Y")})
                else: upcoming_festivals.append({**fest_template, "date_obj": datetime(year + 2, fest_template["month"], fest_template["day"]), "date": datetime(year + 2, fest_template["month"], fest_template["day"]).strftime("%B %d, %Y")})
            except ValueError: print(f"Warning: Could not parse date for {fest_template['name']}")
    if upcoming_festivals:
        upcoming_festivals.sort(key=lambda x: x["date_obj"])
        return upcoming_festivals[0]
    return {"name": "No Upcoming Festivals Found", "date": "", "location": "", "image": "", "description": ""}

@st.cache_data(ttl=3600)
def load_tourism_trends_data():
    try:
        conn = st.connection("snowflake")
        query = """
            SELECT 
                YEAR, 
                DOMESTIC_TOURIST_VISITS, 
                FOREIGN_TOURIST_VISITS,
                ANNUAL_GROWTH_RATE_DOMESTIC,
                ANNUAL_GROWTH_RATE_FOREIGN
            FROM CULTURE_HERITAGE.PUBLIC.TOURISM_TRENDS
            ORDER BY YEAR ASC;
        """
        df = conn.query(query)
        if not df.empty:
            df['YEAR_NUM'] = df['YEAR']
            df['YEAR'] = pd.to_datetime(df['YEAR'].astype(str), format='%Y')
            for col in ['DOMESTIC_TOURIST_VISITS', 'FOREIGN_TOURIST_VISITS']:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            for col in ['ANNUAL_GROWTH_RATE_DOMESTIC', 'ANNUAL_GROWTH_RATE_FOREIGN']:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        return df
    except Exception as e:
        st.error(f"Error loading tourism trends data from Snowflake: {e}")
        return pd.DataFrame()

# --- CSS Styling ---
st.markdown("""
<style>
/* Global Page Styling */
html, body { min-height: 100vh; background-color: white !important; color: #000000 !important; }
div[data-testid="stAppViewContainer"], .stApp { background-color: white !important; color: #000000 !important; }
body { display: flex; flex-direction: column; align-items: center; padding-top: 1rem; }
/* Slideshow Styling */
.slide-display-container { background-color: white; border-radius: 22px; box-shadow: 0 20px 45px rgba(0,0,0,0.2); padding: 40px; width: 100%; max-width: 2000px; margin: 10px auto 30px auto; animation: fadeInAnimation 0.8s ease-in-out; display: flex; flex-direction: column; }
@keyframes fadeInAnimation { from { opacity: 0.6; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
.slide-image-wrapper { width: 100%; margin-bottom: 30px; display: flex; justify-content: center; align-items: center; }
.slide-image { width: 100%; max-width: 100%; max-height: 60vh; object-fit: cover; border-radius: 18px; }
.slide-text-content { text-align: center; }
.slide-text-content h3 { font-size: 2.8rem; font-weight: 700; color: #1a202c !important; margin-bottom: 15px; }
.slide-text-content p { font-size: 1.4rem; color: #4a5568 !important; line-height: 1.7; margin-bottom: 20px; }
.slide-cta-button { background-color: #FF6347; color: white !important; padding: 12px 25px; border-radius: 8px; text-decoration: none; font-weight: bold; margin-top: 10px; display: inline-block; border: none; cursor: pointer; transition: background-color 0.3s ease; }
.slide-cta-button:hover { background-color: #E5533D; }
@media (min-width: 768px) { .slide-display-container { flex-direction: row; align-items: center; padding: 50px; } .slide-image-wrapper { flex: 0 0 50%; padding-right: 40px; margin-bottom: 0; } .slide-text-content { flex: 1; padding-left: 0; text-align: left; } .slide-text-content h3 { font-size: 3rem; } .slide-text-content p { font-size: 1.6rem; } }
/* Slideshow Navigation Buttons */
div[data-testid="stButton-prev_side_btn"] > button, div[data-testid="stButton-next_side_btn"] > button { border-radius: 50% !important; width: 50px !important; height: 50px !important; min-width: 50px !important; padding: 0 !important; font-size: 1.5rem !important; line-height: 50px !important; text-align: center !important; background-color: #fff !important; box-shadow: 0 5px 15px rgba(0,0,0,0.12) !important; border: 1px solid #dde1e6 !important; color: #2d3748 !important; transition: background-color 0.2s ease, transform 0.2s ease, box-shadow 0.2s ease; }
div[data-testid="stButton-prev_side_btn"] > button:hover, div[data-testid="stButton-next_side_btn"] > button:hover { background-color: #f8f9fa !important; transform: translateY(-2px) scale(1.08); border-color: #ced4da !important; box-shadow: 0 8px 20px rgba(0,0,0,0.15) !important; }
div[data-testid="stButton-prev_side_btn"] > button:active, div[data-testid="stButton-next_side_btn"] > button:active { transform: translateY(0px) scale(1); box-shadow: 0 3px 10px rgba(0,0,0,0.1) !important; }
/* Content Styling */
.part2-content-wrapper { padding: 1rem 1rem; width: 100%; max-width: 2000px; margin: 0 auto; color: #000000 !important; }
.part2-content-wrapper .big-font { font-size: 2.8rem !important; font-weight: 600; color: #000000 !important; margin-bottom: 0.5rem; margin-top: 2rem; text-align: center; }
.part2-content-wrapper .subtitle { font-size: 1.6rem !important; color: #333333 !important; margin-bottom: 2.5rem; text-align: center; }
/* Feature Cards */
.feature-card { background-color: #f9f9f9; border-radius: 10px; padding: 20px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); transition: transform 0.3s ease, box-shadow 0.3s ease; height: 100%; display: flex; flex-direction: column; justify-content: space-between; }
.feature-card:hover { transform: translateY(-5px); box-shadow: 0 6px 12px rgba(0,0,0,0.15); }
.feature-card img { width: 100%; height: 200px; object-fit: cover; border-radius: 8px; margin-bottom: 15px; }
.feature-card h3 { font-size: 1.5rem; color: #000000 !important; margin-bottom: 10px; }
.feature-card p { font-size: 1rem; color: #333333 !important; line-height: 1.6; flex-grow: 1; }
.feature-card .stat { font-size: 1.2rem; font-weight: bold; color: #FF6347; margin-bottom: 10px; }
.feature-card form button { width: 100%; background-color: #FF6347; color: white !important; border: none; border-radius: 5px; padding: 10px 0; transition: background-color 0.3s ease; margin-top: 15px; cursor: pointer; font-weight: bold; }
.feature-card form button:hover { background-color: #E5533D; }
/* Section Headings */
.part2-content-wrapper h1, .part2-content-wrapper h2, .part2-content-wrapper .stMarkdown h1, .part2-content-wrapper .stMarkdown h2 { color: #000000 !important; font-weight: 600; margin-top: 1.5rem; text-align: center; }
/* Data-driven section styling */
.data-card { background-color: #ffffff; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); padding: 20px; margin-bottom: 20px; transition: transform 0.3s ease; border-left: 5px solid #FF6347; height: 100%; display: flex; flex-direction: column; }
.data-card:hover { transform: translateY(-5px); }
.data-card h4 { color: #1a202c; font-size: 1.3rem; margin-bottom: 10px; }
.data-card .stat { font-size: 1.5rem; font-weight: bold; color: #FF6347; margin: 8px 0; }
.data-card .description { color: #4a5568; font-size: 0.95rem; flex-grow: 1; }
.data-card form { margin-top: auto; }
.data-card form button { width: 100%; background-color: #FF6347; color: white !important; border: none; border-radius: 5px; padding: 10px 0; transition: background-color 0.3s ease; margin-top: 15px; cursor: pointer; font-weight: bold; }
.data-card form button:hover { background-color: #E5533D; }
</style>
""", unsafe_allow_html=True)

# --- Session State Initialization ---
if 'slide_index' not in st.session_state:
    st.session_state.slide_index = 0
if 'last_user_action_time' not in st.session_state:
    st.session_state.last_user_action_time = time.time() - AUTOPLAY_INTERVAL

# --- App Welcome ---
st.markdown("""
<div style="text-align: center; margin-bottom: 2rem; margin-top: 1rem;">
    <h1 style="color: #2c3e50; font-weight: 700; font-size: 3.5rem;">Cultural Canvas of India</h1>
    <p style="color: #555; font-size: 1.5rem; max-width: 800px; margin: 0 auto;">
        Embark on a journey to explore India's rich tapestry of art, vibrant cultural experiences, and timeless heritage. 
        Discover, learn, and travel responsibly with insights powered by data.
    </p>
</div>
""", unsafe_allow_html=True)

# --- Fetch Data ---
slides_data = get_slideshow_data()
top_states = get_top_cultural_states()
all_gi_art_forms = get_all_gi_art_forms()
upcoming_festival = get_upcoming_festival()
tourism_trends_df = load_tourism_trends_data()

# --- Navigation Functions ---
def next_slide_action():
    if slides_data and len(slides_data) > 0:
        st.session_state.slide_index = (st.session_state.slide_index + 1) % len(slides_data)
    st.session_state.last_user_action_time = time.time()

def prev_slide_action():
    if slides_data and len(slides_data) > 0:
        st.session_state.slide_index = (st.session_state.slide_index - 1 + len(slides_data)) % len(slides_data)
    st.session_state.last_user_action_time = time.time()

# --- Determine current featured GI art form based on slide_index ---
featured_art_form = None 
if all_gi_art_forms and len(all_gi_art_forms) > 0 :
    current_gi_art_index = st.session_state.slide_index % len(all_gi_art_forms)
    featured_art_form = all_gi_art_forms[current_gi_art_index]
else:
    featured_art_form = {"name": "No Art Form Data", "region": "", "image": "https://via.placeholder.com/300x200.png?text=No+Image", "description": "Please check data source.", "learn_more_url": "#"}

# --- Display Current Slide and Side Navigation ---
if slides_data:
    if st.session_state.slide_index >= len(slides_data): 
        st.session_state.slide_index = 0
        
    current_slide_data = slides_data[st.session_state.slide_index]
    
    col_prev, col_content, col_next = st.columns([1, 20, 1], vertical_alignment="center")

    with col_prev:
        st.button("⬅️", on_click=prev_slide_action, key="prev_side_btn", help="Previous slide", use_container_width=True)

    with col_content:
        # Removed 'key' from st.markdown() call
        st.markdown(f""" 
        <div class="slide-display-container" key="html_div_key_slide_wrapper_{st.session_state.slide_index}"> 
            <div class="slide-image-wrapper">
                <img src="{current_slide_data['imgSrc']}" alt="{current_slide_data['title']}" class="slide-image">
            </div>
            <div class="slide-text-content">
                <h3>{current_slide_data['title']}</h3>
                <p>{current_slide_data['description']}</p>
                <a href="/{current_slide_data['cta_link']}" target="_self" class="slide-cta-button">
                    {current_slide_data['cta_button_text']}
                </a>
            </div>
        </div>
        """, unsafe_allow_html=True) 

    with col_next:
        st.button("➡️", on_click=next_slide_action, key="next_side_btn", help="Next slide", use_container_width=True)
else:
    st.warning("Slideshow data is currently unavailable.")

# --- Apply a wrapper for Part 2 content ---
st.markdown("<div class='part2-content-wrapper'>", unsafe_allow_html=True)

# --- Data-Driven "Discover India's Soul" Section ---
st.markdown('<p class="big-font">Discover India\'s Soul</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Curated insights into our vibrant heritage and how to experience it responsibly.</p>', unsafe_allow_html=True)

# --- Top Cultural States Section ---
st.subheader("Most Visited Cultural States")
st.markdown("Based on latest domestic tourism data analysis")
if top_states:
    state_cols = st.columns(len(top_states))
    for i, state_data in enumerate(top_states):
        with state_cols[i]:
            st.markdown(f"""
            <div class="feature-card">
                <img src="{state_data['image']}" alt="{state_data['state']}"><h3>{state_data['state']}</h3>
                <div class="stat">{state_data['visitors']} visitors (2023)</div><p>{state_data['description']}</p>
                <form action="{state_data['explore_url']}" target="_blank"><button type="submit">Explore {state_data['state']}</button></form>
            </div>""", unsafe_allow_html=True)
else: st.info("Top cultural states data is currently unavailable.")

# --- Featured Art Form Section ---
st.subheader("Featured GI-Tagged Art Form")
st.markdown("Geographical Indication protected traditional crafts")
if featured_art_form and featured_art_form.get("name") != "No Art Form Data":
    art_cols = st.columns([2, 3])
    with art_cols[0]: st.image(featured_art_form['image'], caption=featured_art_form['name'], use_container_width=True)
    with art_cols[1]:
        st.markdown(f"""
        <div class="data-card">
            <h4>{featured_art_form['name']}</h4><p class="stat">Region: {featured_art_form['region']}</p>
            <p class="description">{featured_art_form['description']}</p>
            <form action="{featured_art_form['learn_more_url']}" target="_blank"><button type="submit">Learn More</button></form>
        </div>""", unsafe_allow_html=True)
else: st.info("Featured art form data is currently unavailable or no art forms found.")

# --- Upcoming Festival Section ---
st.subheader("Upcoming Cultural Festival")
st.markdown("Plan your cultural immersion")
if upcoming_festival and upcoming_festival.get('name') != "No Upcoming Festivals Found":
    festival_cols = st.columns([3, 2])
    with festival_cols[0]:
        st.markdown(f"""
        <div class="data-card"><h4>{upcoming_festival['name']}</h4><p class="stat">{upcoming_festival['date']}</p>
            <p><strong>Location:</strong> {upcoming_festival['location']}</p><p class="description">{upcoming_festival['description']}</p>
        </div>""", unsafe_allow_html=True)
    with festival_cols[1]:
        if upcoming_festival.get('image'): st.image(upcoming_festival['image'], caption=upcoming_festival['name'], use_container_width=True)
        else: st.markdown("<p style='text-align:center;'>Image not available.</p>", unsafe_allow_html=True)
else: st.info("Upcoming festival data is currently unavailable or no festivals are found.")

# --- Tourism Trends Charts Section ---
st.subheader("Tourism Trends in India")
if not tourism_trends_df.empty:
    st.markdown("Historical data illustrating trends in domestic and foreign tourist visits, and their annual growth rates. Source: `CULTURE_HERITAGE.PUBLIC.TOURISM_TRENDS`")

    st.markdown("#### Annual Tourist Visits (in Millions)")
    visits_chart_df = tourism_trends_df.copy()
    if 'DOMESTIC_TOURIST_VISITS' in visits_chart_df.columns:
        visits_chart_df['DOMESTIC_TOURIST_VISITS_MILLIONS'] = visits_chart_df['DOMESTIC_TOURIST_VISITS'] / 1000000
    if 'FOREIGN_TOURIST_VISITS' in visits_chart_df.columns:
        visits_chart_df['FOREIGN_TOURIST_VISITS_MILLIONS'] = visits_chart_df['FOREIGN_TOURIST_VISITS'] / 1000000
    
    cols_to_plot_visits = [col for col in ['DOMESTIC_TOURIST_VISITS_MILLIONS', 'FOREIGN_TOURIST_VISITS_MILLIONS'] if col in visits_chart_df.columns]

    if cols_to_plot_visits:
        visits_to_plot = visits_chart_df.set_index('YEAR')[cols_to_plot_visits]
        st.line_chart(visits_to_plot)
        st.markdown("Note: Visits are displayed in millions.")
    else: st.caption("Visit data columns not found for plotting.")

    with st.expander("View Raw Visits Data (from Snowflake)"):
        st.dataframe(tourism_trends_df[['YEAR_NUM', 'DOMESTIC_TOURIST_VISITS', 'FOREIGN_TOURIST_VISITS']].rename(columns={'YEAR_NUM': 'Year'}))

    st.markdown("#### Annual Growth Rates (%)")
    cols_to_plot_growth = [col for col in ['ANNUAL_GROWTH_RATE_DOMESTIC', 'ANNUAL_GROWTH_RATE_FOREIGN'] if col in tourism_trends_df.columns]
        
    if cols_to_plot_growth:
        growth_to_plot = tourism_trends_df.set_index('YEAR')[cols_to_plot_growth]
        st.line_chart(growth_to_plot)
    else: st.caption("Growth rate data columns not found for plotting.")
        
    with st.expander("View Raw Growth Rate Data (from Snowflake)"):
        st.dataframe(tourism_trends_df[['YEAR_NUM', 'ANNUAL_GROWTH_RATE_DOMESTIC', 'ANNUAL_GROWTH_RATE_FOREIGN']].rename(columns={'YEAR_NUM': 'Year'}))
else:
    st.warning("Tourism trends data could not be loaded. Please check Snowflake connection and table `CULTURE_HERITAGE.PUBLIC.TOURISM_TRENDS`.")

# --- Call to Action Section ---
st.markdown("---")
st.markdown("<h2 style='text-align:center; color: #1a202c;'>Ready to Explore?</h2>", unsafe_allow_html=True)
st.markdown("""
<div style="display: flex; justify-content: space-around; flex-wrap: wrap; margin-top: 20px;">
    <a href="/Art_Forms_Explorer" target="_self" class="slide-cta-button" style="background-color: #007bff; margin: 5px;">Browse Traditional Art Forms</a>
    <a href="/Cultural_Hotspots_Map" target="_self" class="slide-cta-button" style="background-color: #28a745; margin: 5px;">Find Cultural Destinations</a>
    <a href="/Responsible_Tourism_Guide" target="_self" class="slide-cta-button" style="background-color: #ffc107; color: black !important; margin: 5px;">Learn About Responsible Tourism</a>
</div>
""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True) # End of part2-content-wrapper

# --- Footer ---
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px; font-size: 0.9rem; color: #555;">
    <p><strong>Cultural Canvas of India</strong>: A project dedicated to showcasing India's rich heritage and promoting responsible tourism through data-driven insights.</p>
    <p>Data sourced from public records including Ministry of Tourism, <a href="https://data.gov.in" target="_blank">data.gov.in</a>, artisan communities, and cultural archives.</p>
    <p>&copy; 2025 Cultural Canvas. Made with ❤️ and Streamlit.</p>
</div>
""", unsafe_allow_html=True)

# --- Autoplay Logic ---
if slides_data and len(slides_data) > 0:
    next_autoplay_event_time = st.session_state.last_user_action_time + AUTOPLAY_INTERVAL
    current_time = time.time()
    time_to_wait = next_autoplay_event_time - current_time

    if time_to_wait <= 0:
        st.session_state.slide_index = (st.session_state.slide_index + 1) % len(slides_data)
        st.session_state.last_user_action_time = time.time()
        st.rerun()
    else:
        time.sleep(0.1) 
        st.rerun()
else:
    if 'initial_load_done' not in st.session_state:
        st.session_state.initial_load_done = True
        if not slides_data: 
             st.rerun()