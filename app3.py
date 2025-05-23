import streamlit as st
import time
import streamlit.components.v1 as components

# 0. --- Page Configuration ---
st.set_page_config(
    page_title="Cultural Canvas India: Explore, Experience, Preserve", # More descriptive title
    layout="wide",
    initial_sidebar_state="auto",
    page_icon="🎨" # Changed icon for variety
)

# 1. --- Enhanced Slide Data (Simulating data that could come from Snowflake) ---
# Consider adding a 'theme' or 'category' to link slides to app sections
slides_data = [
    {
        "imgSrc": "https://raw.githubusercontent.com/yashgupta17402/hero/main/kathakali.PNG", # Placeholder (e.g., vibrant festival)
        "title": "Vibrant Traditions: A Tapestry of Art",
        "description": "India's artistic heritage is a kaleidoscope of color, skill, and ancient wisdom. From intricate paintings to mesmerizing dance forms, discover the soul of a nation expressed through its art.",
        "cta_button_text": "Explore Art Forms", # Call to action
        "cta_link": "Art_Forms_Explorer" # Target page (using Streamlit page naming convention)
    },
    {
        "imgSrc": "https://raw.githubusercontent.com/yashgupta17402/hero/main/AGRA_FORT.PNG", # Placeholder (e.g., serene monument)
        "title": "Journey Through Time: Uncover Cultural Hotspots",
        "description": "Explore majestic forts, ancient temples, and bustling cultural hubs. Find popular destinations and unearth hidden gems waiting to share their stories.",
        "cta_button_text": "Discover Destinations",
        "cta_link": "Cultural_Hotspots_Map"
    },
    {
        "imgSrc": "https://raw.githubusercontent.com/yashgupta17402/hero/main/handloom.PNG", # Placeholder (e.g., artisan hands at work)
        "title": "Travel with Purpose: Embrace Responsible Tourism",
        "description": "Be a part of preserving India's cultural treasures. Learn how your travels can support local communities, protect heritage, and ensure these traditions thrive for generations.",
        "cta_button_text": "Learn About Responsible Travel",
        "cta_link": "Responsible_Tourism_Guide"
    }
]

# 2. --- Session State Initialization ---
# if 'slide_index' not in st.session_state:
#     st.session_state.slide_index = 0
# autoplay_interval = 5 # Slightly increased interval

# 2. --- Session State Initialization ---
if 'slide_index' not in st.session_state:
    st.session_state.slide_index = 0

autoplay_interval = 5 # You can adjust this

if 'last_user_action_time' not in st.session_state:
    # Initialize to allow the first autoplay to occur after 'autoplay_interval'
    st.session_state.last_user_action_time = time.time() - autoplay_interval

autoplay_interval = 5

# 3. --- Combined Custom CSS Injection (Your existing CSS - no changes needed here for now) ---
# Ensure your CSS from the original post is here. I'm omitting it for brevity.
# For example: st.markdown(f"""<style> ... YOUR CSS ... </style>""", unsafe_allow_html=True)
# IMPORTANT: For the new buttons in the slideshow, you might want to add specific styling.
# Example for slideshow CTA button (add to your CSS):
# .slide-cta-button {{
#   background-color: #FF4B4B; /* Example color */
#   color: white;
#   padding: 10px 20px;
#   border-radius: 5px;
#   text-decoration: none;
#   font-weight: bold;
#   margin-top: 15px;
#   display: inline-block;
# }}
# .slide-cta-button:hover {{
#   background-color: #E04040; /* Darker shade on hover */
# }}

st.markdown(f"""
<style>
/* --- Global Page Styling (White Background & Default Black Text) --- */
html, body {{
    min-height: 100vh;
    background-color: white !important;
    color: #000000 !important; /* Default all text to black */
}}
div[data-testid="stAppViewContainer"], .stApp {{
    background-color: white !important;
    color: #000000 !important; /* Default text in Streamlit container to black */
}}
body {{
    display: flex;
    flex-direction: column;
    align-items: center;
    padding-top: 1rem;
}}

/* --- Part 1: Slideshow Specific Styling (Ensure its colors are preserved) --- */
.slide-display-container {{
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
}}
@keyframes fadeInAnimation {{
  from {{ opacity: 0.6; transform: translateY(10px); }}
  to {{ opacity: 1; transform: translateY(0); }}
}}
.slide-image-wrapper {{
    width: 100%;
    margin-bottom: 30px;
    display: flex;
    justify-content: center;
    align-items: center;
}}
.slide-image {{
    width: 100%;
    max-width: 100%;
    max-height: 60vh; /* Adjusted for potentially more text */
    object-fit: cover; /* Changed to cover for better aesthetics if aspect ratios vary */
    border-radius: 18px;
}}
.slide-text-content {{
    text-align: center;
}}
.slide-text-content h3 {{
    font-size: 2.8rem; /* Slightly reduced for balance */
    font-weight: 700;
    color: #1a202c !important; /* Slideshow title color with !important */
    margin-bottom: 15px; /* Adjusted margin */
}}
.slide-text-content p {{
    font-size: 1.4rem; /* Slightly reduced */
    color: #4a5568 !important; /* Slideshow description color with !important */
    line-height: 1.7;
    margin-bottom: 20px; /* Added margin for button spacing */
}}

/* CTA Button for Slideshow - Add this */
.slide-cta-button {{
  background-color: #FF6347; /* Tomato color - adjust as needed */
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
}}
.slide-cta-button:hover {{
  background-color: #E5533D; /* Darker tomato */
}}


@media (min-width: 768px) {{
    .slide-display-container {{
        flex-direction: row;
        align-items: center;
        padding: 50px;
    }}
    .slide-image-wrapper {{
        flex: 0 0 50%; /* Adjusted flex basis */
        padding-right: 40px;
        margin-bottom: 0;
    }}
    .slide-text-content {{
        flex: 1;
        padding-left: 0;
        text-align: left;
    }}
    .slide-text-content h3 {{
        font-size: 3rem; /* Adjusted */
    }}
    .slide-text-content p {{
        font-size: 1.6rem; /* Adjusted */
    }}
}}

/* Slideshow Navigation Buttons (Your existing styles) */
div[data-testid="stButton-prev_side_btn"] > button,
div[data-testid="stButton-next_side_btn"] > button {{
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
    color: #2d3748 !important; /* Nav button icon color with !important */
    transition: background-color 0.2s ease, transform 0.2s ease, box-shadow 0.2s ease;
}}
div[data-testid="stButton-prev_side_btn"] > button:hover,
div[data-testid="stButton-next_side_btn"] > button:hover {{
    background-color: #f8f9fa !important;
    transform: translateY(-2px) scale(1.08);
    border-color: #ced4da !important;
    box-shadow: 0 8px 20px rgba(0,0,0,0.15) !important;
}}
div[data-testid="stButton-prev_side_btn"] > button:active,
div[data-testid="stButton-next_side_btn"] > button:active {{
    transform: translateY(0px) scale(1);
    box-shadow: 0 3px 10px rgba(0,0,0,0.1) !important;
}}


/* --- Part 2: General Content Styling (Your existing styles) --- */
/* NOTE: Make sure this CSS is loaded. For brevity, I'm not repeating all of it. */
/* Key changes for "Discover India's Soul" cards might be needed here if you want custom card styling */
.part2-content-wrapper {{
    padding: 1rem 1rem; /* Adjusted padding */
    width: 100%;
    max-width: 2000px;
    margin: 0 auto;
    color: #000000 !important;
}}

.part2-content-wrapper .big-font {{
    font-size: 2.8rem !important; /* Adjusted */
    font-weight: 600;
    color: #000000 !important;
    margin-bottom: 0.5rem;
    margin-top: 2rem; /* Increased top margin */
    text-align: center; /* Centered this title */
}}
.part2-content-wrapper .subtitle {{
    font-size: 1.6rem !important; /* Adjusted */
    color: #333333 !important; /* Slightly softer black */
    margin-bottom: 2.5rem; /* Increased margin */
    text-align: center; /* Centered this subtitle */
}}

/* Styling for the new cards in "Discover India's Soul" */
.feature-card {{
    background-color: #f9f9f9;
    border-radius: 10px;
    padding: 20px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    height: 100%; /* Ensure cards in a row are same height */
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}}
.feature-card:hover {{
    transform: translateY(-5px);
    box-shadow: 0 6px 12px rgba(0,0,0,0.15);
}}
.feature-card img {{
    width: 100%;
    height: 200px; /* Fixed height for images in cards */
    object-fit: cover;
    border-radius: 8px;
    margin-bottom: 15px;
}}
.feature-card h3 {{
    font-size: 1.5rem;
    color: #000000 !important; /* Black */
    margin-bottom: 10px;
}}
.feature-card p {{
    font-size: 1rem;
    color: #333333 !important; /* Dark Gray */
    line-height: 1.6;
    flex-grow: 1; /* Allows paragraph to take available space */
}}
.feature-card .stButton button {{ /* Targeting Streamlit buttons inside cards */
    width: 100%;
    background-color: #FF6347; /* Tomato color */
    color: white !important;
    border: none;
    border-radius: 5px;
    padding: 10px 0; /* Adjusted padding */
    transition: background-color 0.3s ease;
    margin-top: 15px; /* Space above button */
}}
.feature-card .stButton button:hover {{
    background-color: #E5533D; /* Darker tomato */
    transform: none; /* Override general button hover if needed */
    box-shadow: none; /* Override general button shadow if needed */
}}

/* Your other .part2-content-wrapper styles like h1, h2, inputs etc. would go here */
/* For brevity, I am not repeating them from your original prompt but they should be included. */
.part2-content-wrapper h1,
.part2-content-wrapper h2,
.part2-content-wrapper .stMarkdown h1,
.part2-content-wrapper .stMarkdown h2
{{
    color: #000000 !important; /* BLACK text for all headings */
    font-weight: 600;
    margin-top: 1.5rem;
    text-align: center; /* Center section headings */
}}
/* ... include all your other .part2-content-wrapper styles ... */

</style>
""", unsafe_allow_html=True)


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


# 4. --- Navigation Functions ---
def next_slide_action():
    st.session_state.slide_index = (st.session_state.slide_index + 1) % len(slides_data)
    st.session_state.last_user_action_time = time.time() # Record this user action

def prev_slide_action():
    st.session_state.slide_index = (st.session_state.slide_index - 1 + len(slides_data)) % len(slides_data)
    st.session_state.last_user_action_time = time.time() # Record this user action



# Helper function to switch pages (useful for the slideshow CTA buttons)
def go_to_page(page_name):
    # This is a conceptual function. Actual page switching in Streamlit multipage apps
    # happens when the user clicks on the navigation in the sidebar.
    # For buttons, you typically use them to set a state or trigger an action,
    # and then the user would navigate via sidebar.
    # However, you can "simulate" a redirect-like experience if pages are functions,
    # or by using st.experimental_set_query_params and checking them.
    # For now, we'll just print, assuming sidebar navigation will be used.
    st.info(f"Navigate to: {page_name} (using sidebar)")
    # If you create pages like `pages/Art_Forms_Explorer.py`, Streamlit handles navigation.
    # This function is more for if you were building a single-page app with sections.


# 5. --- Display Current Slide and Side Navigation ---
current_slide_data = slides_data[st.session_state.slide_index]
slide_display_key = f"slide_container_content_{st.session_state.slide_index}" # Unique key for re-render

col_prev, col_content, col_next = st.columns([1, 20, 1], vertical_alignment="center")

with col_prev:
    st.button("⬅️", on_click=prev_slide_action, key="prev_side_btn", help="Previous slide", use_container_width=True)

with col_content:
    # Using st.markdown with a unique key for the container to ensure it re-renders on slide change
    # This is an alternative to st.empty() or st.experimental_rerun() directly after button clicks
    # The main rerun will be triggered by the autoplay logic.
    st.markdown(f"""
    <div class="slide-display-container" key="{slide_display_key}">
        <div class="slide-image-wrapper">
            <img src="{current_slide_data['imgSrc']}" alt="{current_slide_data['title']}" class="slide-image">
        </div>
        <div class="slide-text-content">
            <h3>{current_slide_data['title']}</h3>
            <p>{current_slide_data['description']}</p>
            <a href="#{current_slide_data['cta_link'].lower().replace(' ', '_')}" class="slide-cta-button" target="_self" style="display:none;">
                {current_slide_data['cta_button_text']}
            </a>
            </div>
    </div>
    """, unsafe_allow_html=True)
    # For newer Streamlit versions (1.28+), you could use st.page_link more effectively inside the slideshow
    # Example:
    # if "cta_link_page" in current_slide_data: # Assuming cta_link_page is the path to the page file
    # st.page_link(current_slide_data["cta_link_page"], label=current_slide_data["cta_button_text"], icon="➡️")


with col_next:
    st.button("➡️", on_click=next_slide_action, key="next_side_btn", help="Next slide", use_container_width=True)


# --- Apply a wrapper for Part 2 content to scope its styles ---
st.markdown("<div class='part2-content-wrapper'>", unsafe_allow_html=True)

# --- Part 2: Enhanced "Discover India's Soul" Section ---
st.markdown('<p class="big-font">Discover India\'s Soul</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Curated insights into our vibrant heritage and how to experience it responsibly.</p>', unsafe_allow_html=True)

# Placeholder data for the feature cards - this would come from Snowflake eventually
# For example, "Art Form of the Month", "Undiscovered Gem", "Responsible Tip"
features = [
    {
        "image": "https://raw.githubusercontent.com/yashgupta17402/hero/main/madhubani.PNG", # Your Madhubani image
        "title": "Spotlight: Madhubani Painting",
        "description": "Delve into the intricate patterns and vibrant narratives of Madhubani art, a cherished tradition from the Mithila region. Each stroke tells a story of culture and nature.",
        "button_text": "Explore Art Forms",
        "button_action_page": "Art_Forms_Explorer" # Conceptual page link
    },
    {
        "image": "https://raw.githubusercontent.com/yashgupta17402/hero/main/orcha_mp.jpeg", # Placeholder for a lesser-known fort or village
        "title": "Cultural Gem: Orchha, Madhya Pradesh",
        "description": "Step back in time in Orchha, a hidden town filled with magnificent palaces, temples, and cenotaphs along the Betwa River, offering a serene cultural experience.",
        "button_text": "Discover Destinations",
        "button_action_page": "Cultural_Hotspots_Map"
    },
    {
        "image": "https://raw.githubusercontent.com/yashgupta17402/hero/main/handicraft_1.PNG", # Placeholder for responsible tourism visual
        "title": "Travel Responsibly: Support Local Artisans",
        "description": "When you purchase authentic, locally made handicrafts directly from artisans or recognized cooperatives, you empower communities and help keep traditional skills alive.",
        "button_text": "Responsible Travel Tips",
        "button_action_page": "Responsible_Tourism_Guide"
    }
]

cols = st.columns(len(features)) # Create columns based on number of features

for i, feature in enumerate(features):
    with cols[i]:
        st.markdown(f"""
        <div class="feature-card">
            <img src="{feature['image']}" alt="{feature['title']}">
            <h3>{feature['title']}</h3>
            <p>{feature['description']}</p>
        </div>
        """, unsafe_allow_html=True)
        # The button needs to be an actual Streamlit button to trigger page navigation
        # if st.button(feature["button_text"], key=f"feature_btn_{i}"):
        #    go_to_page(feature["button_action_page"]) # This is conceptual
        # For actual multipage app, you'd expect users to use the sidebar after being inspired.
        # Or use st.page_link if your Streamlit version supports it well in this context.
        st.markdown(f"<a href='#' class='stButton'><button style='width:100%; background-color: #FF6347; color: white; border:none; border-radius:5px; padding:10px 0; cursor:pointer; margin-top:15px;'>{feature['button_text']}</button></a>", unsafe_allow_html=True)
        # The above button is styled to look like other buttons but is a simple link for now.
        # To make it functional for page switching, you'll use Streamlit's multipage navigation via sidebar.
        # Or, for Streamlit 1.28+, you can use:
        # st.page_link(f"pages/{feature['button_action_page']}.py", label=feature["button_text"])
        # Ensure your page files are named correctly, e.g., "Art_Forms_Explorer.py" in a "pages" folder.


# --- Call to Action Section ---
st.markdown("---") # Visual separator
st.markdown("<h2 style='text-align:center; color: #1a202c;'>Ready to Explore?</h2>", unsafe_allow_html=True)

cta_cols = st.columns([1,1,1])
with cta_cols[0]:
    if st.button("Browse Traditional Art Forms", use_container_width=True, key="cta_art"):
        st.info("Navigate to 'Art Forms Explorer' via the sidebar.") # Placeholder action
        # In a real multipage app, user clicks sidebar. Or use st.switch_page (newer versions)
with cta_cols[1]:
    if st.button("Find Cultural Destinations", use_container_width=True, key="cta_dest"):
        st.info("Navigate to 'Cultural Hotspots Map' via the sidebar.") # Placeholder action
with cta_cols[2]:
    if st.button("Learn About Responsible Tourism", use_container_width=True, key="cta_resp"):
        st.info("Navigate to 'Responsible Tourism Guide' via the sidebar.") # Placeholder action

st.markdown("</div>", unsafe_allow_html=True) # End of part2-content-wrapper


# --- Footer ---
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px; font-size: 0.9rem; color: #555;">
    <p><strong>Cultural Canvas of India</strong>: A project dedicated to showcasing India's rich heritage and promoting responsible tourism through data-driven insights.</p>
    <p>Data sourced from public records including <a href="https://data.gov.in" target="_blank">data.gov.in</a>, artisan communities, and cultural archives.</p>
    <p>&copy; 2026 Bruteforce. Made with ❤️ and Streamlit.</p>
</div>
""", unsafe_allow_html=True)


# 6. --- Autoplay Logic (REFINED - place at the VERY END of your script) ---

# Calculate when the next autoplay event is due based on the last action (user or auto)
# Assumes 'autoplay_interval' is defined (e.g., autoplay_interval = 5)
# Assumes 'st.session_state.last_user_action_time' is initialized and updated correctly

next_autoplay_event_time = st.session_state.last_user_action_time + autoplay_interval
current_time = time.time()

time_to_wait = next_autoplay_event_time - current_time

if time_to_wait <= 0:
    # It's time (or past time) for an automatic slide change.
    st.session_state.slide_index = (st.session_state.slide_index + 1) % len(slides_data)
    # Update last_user_action_time to *this* autoplay event's time.
    # This ensures the next autoplay waits for the full interval from now.
    st.session_state.last_user_action_time = time.time()
    st.rerun() # Rerun to display the new slide and reset timers.
else:
    # It's not yet time for an automatic slide change.
    # We need to make the script wait for the remaining duration and then rerun to re-evaluate.
    time.sleep(time_to_wait)
    st.rerun() # Rerun to re-check conditions after sleeping.