import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import random

# --- Page Configuration ---
st.set_page_config(
    page_title="Art Forms Explorer | Cultural Canvas India",
    layout="wide",
    initial_sidebar_state="auto",
    page_icon="🎨"
)

# --- Simulated Database Functions ---
def get_art_forms():
    """Fetch art forms data (simulated)"""
    return pd.DataFrame({
        'name': [
            'Madhubani Painting', 'Kathakali', 'Bharatanatyam', 'Pashmina Shawls',
            'Banarasi Silk', 'Pattachitra', 'Warli Painting', 'Phulkari',
            'Chikankari', 'Kantha', 'Kalamkari', 'Bidriware',
            'Dhokra', 'Tanjore Painting', 'Gond Art'
        ],
        'type': [
            'Painting', 'Dance', 'Dance', 'Textile',
            'Textile', 'Painting', 'Painting', 'Textile',
            'Textile', 'Textile', 'Painting', 'Craft',
            'Craft', 'Painting', 'Painting'
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
            25.4, 10.8, 13.1, 34.1,
            25.3, 20.3, 19.2, 31.1,
            26.8, 22.6, 16.5, 17.9,
            21.3, 10.8, 23.2
        ],
        'longitude': [
            85.4, 76.3, 80.3, 74.8,
            83.0, 85.8, 73.2, 75.3,
            80.9, 88.4, 80.6, 77.5,
            81.6, 79.1, 77.4
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

def get_state_coordinates():
    """Get approximate coordinates for Indian states (simplified)"""
    return {
        'Andhra Pradesh': [16.5, 80.6],
        'Bihar': [25.4, 85.4],
        'Chhattisgarh': [21.3, 81.6],
        'Gujarat': [22.3, 72.6],
        'Jammu & Kashmir': [34.1, 74.8],
        'Karnataka': [15.3, 75.7],
        'Kerala': [10.8, 76.3],
        'Madhya Pradesh': [23.2, 77.4],
        'Maharashtra': [19.2, 73.2],
        'Odisha': [20.3, 85.8],
        'Punjab': [31.1, 75.3],
        'Rajasthan': [27.0, 74.2],
        'Tamil Nadu': [11.1, 78.7],
        'Uttar Pradesh': [26.8, 80.9],
        'West Bengal': [22.6, 88.4]
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
}
.art-card-footer {
    margin-top: 1rem;
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
art_forms_df = get_art_forms()
state_coords = get_state_coordinates()

# --- Filters ---
st.markdown('<div class="filter-section">', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    selected_state = st.selectbox(
        "Filter by State",
        ["All States"] + sorted(art_forms_df['state'].unique().tolist())
    )

with col2:
    selected_type = st.selectbox(
        "Filter by Art Type",
        ["All Types"] + sorted(art_forms_df['type'].unique().tolist())
    )

with col3:
    search_term = st.text_input("Search Art Forms", "")

st.markdown('</div>', unsafe_allow_html=True)

# --- Apply Filters ---
filtered_df = art_forms_df.copy()

if selected_state != "All States":
    filtered_df = filtered_df[filtered_df['state'] == selected_state]

if selected_type != "All Types":
    filtered_df = filtered_df[filtered_df['type'] == selected_type]

if search_term:
    filtered_df = filtered_df[filtered_df['name'].str.contains(search_term, case=False) | 
                             filtered_df['description'].str.contains(search_term, case=False)]

# --- Display Art Forms Grid ---
if filtered_df.empty:
    st.info("No art forms match your filters. Try adjusting your criteria.")
else:
    # Create rows of 3 cards each
    for i in range(0, len(filtered_df), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(filtered_df):
                art = filtered_df.iloc[i + j]
                with cols[j]:
                    st.markdown(f"""
                    <div class="art-card">
                        <img src="{art['image_url']}" class="art-card-image" alt="{art['name']}">
                        <div class="art-card-content">
                            <div class="art-card-title">{art['name']}</div>
                            <div class="art-card-subtitle">{art['type']} • {art['state']}</div>
                            <div class="art-card-description">{art['description'][:100]}...</div>
                            <div class="art-card-footer">
                                {f'<span class="gi-tag">GI Tagged</span>' if art['gi_tag'] else ''}
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"View Details: {art['name']}", key=f"view_{i+j}"):
                        st.session_state.selected_art = art['name']

# --- Detailed View ---
if 'selected_art' in st.session_state:
    art = art_forms_df[art_forms_df['name'] == st.session_state.selected_art].iloc[0]
    
    st.markdown('<div class="detail-container">', unsafe_allow_html=True)
    
    # Back button
    if st.button("← Back to Art Forms"):
        del st.session_state.selected_art
        st.rerun()
    
    # Header with title and GI tag
    st.markdown(f"""
    <div class="detail-header">
        <div class="detail-title">{art['name']}</div>
        {f'<span class="gi-tag">GI Tagged</span>' if art['gi_tag'] else ''}
    </div>
    """, unsafe_allow_html=True)
    
    # Main image
    st.image(art['image_url'], use_column_width=True, caption=f"{art['name']} - {art['type']} from {art['state']}")
    
    # Description
    st.markdown(f"### About {art['name']}")
    st.write(art['description'])
    
    # Info cards
    st.markdown("### Details")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="info-card">
            <h4>Origin</h4>
            <p>{art['state']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="info-card">
            <h4>Government Support</h4>
            <p>Scheme: {art['govt_scheme']}<br>Allocation: {art['allocation_amount']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="info-card">
            <h4>Art Type</h4>
            <p>{art['type']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="info-card">
            <h4>Artisan Cooperative</h4>
            <p>{art['artisan_cooperative']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Data Story
    st.markdown("### Data Story")
    st.write(f"""
    This art form originates from {art['state']}. Government initiatives like {art['govt_scheme']} have allocated {art['allocation_amount']} for its promotion. 
    It has a GI Tag: {"Yes" if art['gi_tag'] else "No"}.
    
    Supporting local artisans through {art['artisan_cooperative']} helps preserve this cultural heritage and provides sustainable livelihoods.
    """)
    
    # Map showing region
    st.markdown("### Where to Find")
    m = folium.Map(location=[art['latitude'], art['longitude']], zoom_start=7)
    folium.Marker(
        [art['latitude'], art['longitude']], 
        popup=f"{art['name']}<br>{art['state']}",
        tooltip=art['name'],
        icon=folium.Icon(color="red", icon="palette", prefix="fa")
    ).add_to(m)
    
    # Add a circle to show the general region
    folium.Circle(
        [art['latitude'], art['longitude']],
        radius=50000,  # 50km radius
        color="#FF6347",
        fill=True,
        fill_color="#FF6347",
        fill_opacity=0.2
    ).add_to(m)
    
    folium_static(m)
    
    st.markdown("</div>", unsafe_allow_html=True)