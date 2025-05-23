import streamlit as st
import time
import pandas as pd
import random
from datetime import datetime

# --- Page Configuration ---
st.set_page_config(
    page_title="Cultural Canvas India: Explore, Experience, Preserve",
    layout="wide",
    initial_sidebar_state="auto",
    page_icon="🎨"
)

# --- Simulated Database Functions (to be replaced with Snowflake connections) ---
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
    """Fetch top 3 most visited cultural states (simulated)"""
    return [
        {
            "state": "Rajasthan",
            "visitors": "10.5M",
            "image": "https://raw.githubusercontent.com/yashgupta17402/hero/main/rajasthan.jpg",
            "description": "Known for its majestic forts, vibrant festivals, and rich cultural heritage."
        },
        {
            "state": "Tamil Nadu",
            "visitors": "8.7M",
            "image": "https://raw.githubusercontent.com/yashgupta17402/hero/main/tamil_nadu.jpg",
            "description": "Home to magnificent temples, classical dance forms, and ancient Dravidian culture."
        },
        {
            "state": "Uttar Pradesh",
            "visitors": "7.2M",
            "image": "https://raw.githubusercontent.com/yashgupta17402/hero/main/uttar_pradesh.jpg",
            "description": "Featuring iconic monuments like the Taj Mahal and the spiritual city of Varanasi."
        }
    ]

def get_random_gi_art_form():
    """Fetch a randomly selected GI-tagged art form (simulated)"""
    gi_art_forms = [
        {
            "name": "Madhubani Painting",
            "region": "Bihar",
            "image": "https://raw.githubusercontent.com/yashgupta17402/hero/main/madhubani.PNG",
            "description": "Characterized by geometric patterns and nature motifs, this ancient art form has been practiced for centuries."
        },
        {
            "name": "Pashmina Shawls",
            "region": "Kashmir",
            "image": "https://raw.githubusercontent.com/yashgupta17402/hero/main/pashmina.jpg",
            "description": "Exquisite handwoven shawls made from the finest cashmere wool, known for their warmth and intricate embroidery."
        },
        {
            "name": "Banarasi Silk",
            "region": "Uttar Pradesh",
            "image": "https://raw.githubusercontent.com/yashgupta17402/hero/main/banarasi.jpg",
            "description": "Luxurious silk textiles woven with intricate gold and silver brocade, traditionally used for wedding attire."
        }
    ]
    return random.choice(gi_art_forms)

def get_upcoming_festival():
    """Fetch a major upcoming festival (simulated)"""
    # In a real app, this would calculate based on current date
    current_month = datetime.now().month
    
    festivals = [
        {
            "name": "Diwali",
            "date": "November 12, 2023",
            "location": "Nationwide",
            "image": "https://raw.githubusercontent.com/yashgupta17402/hero/main/diwali.jpg",
            "description": "The festival of lights celebrates the victory of light over darkness with lamps, fireworks, and family gatherings."
        },
        {
            "name": "Holi",
            "date": "March 25, 2024",
            "location": "Nationwide",
            "image": "https://raw.githubusercontent.com/yashgupta17402/hero/main/holi.jpg",
            "description": "The colorful spring festival where people throw colored powders and water at each other in joyful celebration."
        },
        {
            "name": "Pongal",
            "date": "January 15, 2024",
            "location": "Tamil Nadu",
            "image": "https://raw.githubusercontent.com/yashgupta17402/hero/main/pongal.jpg",
            "description": "A harvest festival dedicated to the Sun God, featuring elaborate kolam designs and special rice dishes."
        }
    ]
    
    # Simple logic to pick a festival based on current month
    if current_month >= 9:  # September onwards
        return festivals[0]  # Diwali
    elif current_month >= 2:  # February onwards
        return festivals[1]  # Holi
    else:
        return festivals[2]  # Pongal

# --- CSS Styling ---
st.markdown("""
<style>
/* Global Page Styling */
html, body {
    min-height: 100vh;
    background-color: white !important;
    color: #000000 !important;
}
div[data-testid="stAppViewContainer"], .stApp {
    background-color: white !important;
    color: #000000 !important;
}
body {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding-top: 1rem;
}

/* Slideshow Styling */
.slide-display-container {
    background-color: white;
    border-radius: 22px;
    box-shadow: 0 20px 45px rgba(0, 0, 0, 0.2);
    padding: 40px;
    width: 100%;
    max-width: 2000px;
    margin: 10px auto 30px auto;
    animation: fadeInAnimation 0.8s ease-in-out;
    display: flex;
    flex-direction: column;
}
@keyframes fadeInAnimation {
  from { opacity: 0.6; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
.slide-image-wrapper {
    width: 100%;
    margin-bottom: 30px;
    display: flex;
    justify-content: center;
    align-items: center;
}
.slide-image {
    width: 100%;
    max-width: 100%;
    max-height: 60vh;
    object-fit: cover;
    border-radius: 18px;
}
.slide-text-content {
    text-align: center;
}
.slide-text-content h3 {
    font-size: 2.8rem;
    font-weight: 700;
    color: #1a202c !important;
    margin-bottom: 15px;
}
.slide-text-content p {
    font-size: 1.4rem;
    color: #4a5568 !important;
    line-height: 1.7;
    margin-bottom: 20px;
}

/* CTA Button for Slideshow */
.slide-cta-button {
  background-color: #FF6347;
  color: white !important;
  padding: 12px 25px;
  border-radius: 8px;
  text-decoration: none;
  font-weight: bold;
  margin-top: 10px;
  display: inline-block;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s ease;
}
.slide-cta-button:hover {
  background-color: #E5533D;
}

/* Responsive Slideshow */
@media (min-width: 768px) {
    .slide-display-container {
        flex-direction: row;
        align-items: center;
        padding: 50px;
    }
    .slide-image-wrapper {
        flex: 0 0 50%;
        padding-right: 40px;
        margin-bottom: 0;
    }
    .slide-text-content {
        flex: 1;
        padding-left: 0;
        text-align: left;
    }
    .slide-text-content h3 {
        font-size: 3rem;
    }
    .slide-text-content p {
        font-size: 1.6rem;
    }
}

/* Slideshow Navigation Buttons */
div[data-testid="stButton-prev_side_btn"] > button,
div[data-testid="stButton-next_side_btn"] > button {
    border-radius: 50% !important;
    width: 50px !important;
    height: 50px !important;
    min-width: 50px !important;
    padding: 0 !important;
    font-size: 1.5rem !important;
    line-height: 50px !important;
    text-align: center !important;
    background-color: #fff !important;
    box-shadow: 0 5px 15px rgba(0,0,0,0.12) !important;
    border: 1px solid #dde1e6 !important;
    color: #2d3748 !important;
    transition: background-color 0.2s ease, transform 0.2s ease, box-shadow 0.2s ease;
}
div[data-testid="stButton-prev_side_btn"] > button:hover,
div[data-testid="stButton-next_side_btn"] > button:hover {
    background-color: #f8f9fa !important;
    transform: translateY(-2px) scale(1.08);
    border-color: #ced4da !important;
    box-shadow: 0 8px 20px rgba(0,0,0,0.15) !important;
}
div[data-testid="stButton-prev_side_btn"] > button:active,
div[data-testid="stButton-next_side_btn"] > button:active {
    transform: translateY(0px) scale(1);
    box-shadow: 0 3px 10px rgba(0,0,0,0.1) !important;
}

/* Content Styling */
.part2-content-wrapper {
    padding: 1rem 1rem;
    width: 100%;
    max-width: 2000px;
    margin: 0 auto;
    color: #000000 !important;
}

.part2-content-wrapper .big-font {
    font-size: 2.8rem !important;
    font-weight: 600;
    color: #000000 !important;
    margin-bottom: 0.5rem;
    margin-top: 2rem;
    text-align: center;
}
.part2-content-wrapper .subtitle {
    font-size: 1.6rem !important;
    color: #333333 !important;
    margin-bottom: 2.5rem;
    text-align: center;
}

/* Feature Cards */
.feature-card {
    background-color: #f9f9f9;
    border-radius: 10px;
    padding: 20px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}
.feature-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 6px 12px rgba(0,0,0,0.15);
}
.feature-card img {
    width: 100%;
    height: 200px;
    object-fit: cover;
    border-radius: 8px;
    margin-bottom: 15px;
}
.feature-card h3 {
    font-size: 1.5rem;
    color: #000000 !important;
    margin-bottom: 10px;
}
.feature-card p {
    font-size: 1rem;
    color: #333333 !important;
    line-height: 1.6;
    flex-grow: 1;
}
.feature-card .stButton button {
    width: 100%;
    background-color: #FF6347;
    color: white !important;
    border: none;
    border-radius: 5px;
    padding: 10px 0;
    transition: background-color 0.3s ease;
    margin-top: 15px;
}
.feature-card .stButton button:hover {
    background-color: #E5533D;
    transform: none;
    box-shadow: none;
}

/* Section Headings */
.part2-content-wrapper h1,
.part2-content-wrapper h2,
.part2-content-wrapper .stMarkdown h1,
.part2-content-wrapper .stMarkdown h2 {
    color: #000000 !important;
    font-weight: 600;
    margin-top: 1.5rem;
    text-align: center;
}

/* Data-driven section styling */
.data-card {
    background-color: #ffffff;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    padding: 20px;
    margin-bottom: 20px;
    transition: transform 0.3s ease;
    border-left: 5px solid #FF6347;
}
.data-card:hover {
    transform: translateY(-5px);
}
.data-card h4 {
    color: #1a202c;
    font-size: 1.3rem;
    margin-bottom: 10px;
}
.data-card .stat {
    font-size: 2rem;
    font-weight: bold;
    color: #FF6347;
    margin: 10px 0;
}
.data-card .description {
    color: #4a5568;
    font-size: 0.95rem;
}
</style>
""", unsafe_allow_html=True)

# --- Session State Initialization ---
if 'slide_index' not in st.session_state:
    st.session_state.slide_index = 0

if 'last_user_action_time' not in st.session_state:
    st.session_state.last_user_action_time = time.time() - 5  # 5 seconds autoplay interval

autoplay_interval = 5

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

# --- Navigation Functions ---
def next_slide_action():
    st.session_state.slide_index = (st.session_state.slide_index + 1) % len(slides_data)
    st.session_state.last_user_action_time = time.time()

def prev_slide_action():
    st.session_state.slide_index = (st.session_state.slide_index - 1 + len(slides_data)) % len(slides_data)
    st.session_state.last_user_action_time = time.time()

# --- Fetch Data (Simulated) ---
slides_data = get_slideshow_data()
top_states = get_top_cultural_states()
featured_art_form = get_random_gi_art_form()
upcoming_festival = get_upcoming_festival()

# --- Display Current Slide and Side Navigation ---
current_slide_data = slides_data[st.session_state.slide_index]
slide_display_key = f"slide_container_content_{st.session_state.slide_index}"

col_prev, col_content, col_next = st.columns([1, 20, 1], vertical_alignment="center")

with col_prev:
    st.button("⬅️", on_click=prev_slide_action, key="prev_side_btn", help="Previous slide", use_container_width=True)

with col_content:
    st.markdown(f"""
    <div class="slide-display-container" key="{slide_display_key}">
        <div class="slide-image-wrapper">
            <img src="{current_slide_data['imgSrc']}" alt="{current_slide_data['title']}" class="slide-image">
        </div>
        <div class="slide-text-content">
            <h3>{current_slide_data['title']}</h3>
            <p>{current_slide_data['description']}</p>
            <a href="/{current_slide_data['cta_link']}" class="slide-cta-button">
                {current_slide_data['cta_button_text']}
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_next:
    st.button("➡️", on_click=next_slide_action, key="next_side_btn", help="Next slide", use_container_width=True)

# --- Apply a wrapper for Part 2 content ---
st.markdown("<div class='part2-content-wrapper'>", unsafe_allow_html=True)

# --- Data-Driven "Discover India's Soul" Section ---
st.markdown('<p class="big-font">Discover India\'s Soul</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Curated insights into our vibrant heritage and how to experience it responsibly.</p>', unsafe_allow_html=True)

# --- Top Cultural States Section ---
st.subheader("Most Visited Cultural States")
st.markdown("Based on latest tourism data analysis")

state_cols = st.columns(len(top_states))
for i, state in enumerate(top_states):
    with state_cols[i]:
        st.markdown(f"""
        <div class="feature-card">
            <img src="{state['image']}" alt="{state['state']}">
            <h3>{state['state']}</h3>
            <div class="stat">{state['visitors']} visitors</div>
            <p>{state['description']}</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"Explore {state['state']}", key=f"state_btn_{i}"):
            st.session_state.selected_state = state['state']
            # In a real app, this would navigate to the state's page

# --- Featured Art Form Section ---
st.subheader("Featured GI-Tagged Art Form")
st.markdown("Geographical Indication protected traditional crafts")

art_cols = st.columns([2, 3])
with art_cols[0]:
    st.image(featured_art_form['image'], caption=featured_art_form['name'], width=300)

with art_cols[1]:
    st.markdown(f"""
    <div class="data-card">
        <h4>{featured_art_form['name']}</h4>
        <p class="stat">Region: {featured_art_form['region']}</p>
        <p class="description">{featured_art_form['description']}</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Learn More About This Art Form"):
        # In a real app, this would navigate to the art form's page
        pass

# --- Upcoming Festival Section ---
st.subheader("Upcoming Cultural Festival")
st.markdown("Plan your cultural immersion")

festival_cols = st.columns([3, 2])
with festival_cols[0]:
    st.markdown(f"""
    <div class="data-card">
        <h4>{upcoming_festival['name']}</h4>
        <p class="stat">{upcoming_festival['date']}</p>
        <p>Location: {upcoming_festival['location']}</p>
        <p class="description">{upcoming_festival['description']}</p>
    </div>
    """, unsafe_allow_html=True)

with festival_cols[1]:
    st.image(upcoming_festival['image'], caption=upcoming_festival['name'], width=300)

# --- Call to Action Section ---
st.markdown("---")
st.markdown("<h2 style='text-align:center; color: #1a202c;'>Ready to Explore?</h2>", unsafe_allow_html=True)

cta_cols = st.columns([1,1,1])
with cta_cols[0]:
    if st.button("Browse Traditional Art Forms", use_container_width=True, key="cta_art"):
        # In a real app, this would navigate to the Art Forms Explorer page
        pass
with cta_cols[1]:
    if st.button("Find Cultural Destinations", use_container_width=True, key="cta_dest"):
        # In a real app, this would navigate to the Cultural Hotspots Map page
        pass
with cta_cols[2]:
    if st.button("Learn About Responsible Tourism", use_container_width=True, key="cta_resp"):
        # In a real app, this would navigate to the Responsible Tourism Guide page
        pass

st.markdown("</div>", unsafe_allow_html=True)

# --- Footer ---
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px; font-size: 0.9rem; color: #555;">
    <p><strong>Cultural Canvas of India</strong>: A project dedicated to showcasing India's rich heritage and promoting responsible tourism through data-driven insights.</p>
    <p>Data sourced from public records including <a href="https://data.gov.in" target="_blank">data.gov.in</a>, artisan communities, and cultural archives.</p>
    <p>&copy; 2026 Bruteforce. Made with ❤️ and Streamlit.</p>
</div>
""", unsafe_allow_html=True)

# --- Autoplay Logic ---
next_autoplay_event_time = st.session_state.last_user_action_time + autoplay_interval
current_time = time.time()
time_to_wait = next_autoplay_event_time - current_time

if time_to_wait <= 0:
    st.session_state.slide_index = (st.session_state.slide_index + 1) % len(slides_data)
    st.session_state.last_user_action_time = time.time()
    st.rerun()
else:
    time.sleep(time_to_wait)
    st.rerun()