import streamlit as st
import pandas as pd
import random

# --- Page Configuration ---
st.set_page_config(
    page_title="Responsible Tourism Guide | Cultural Canvas India",
    layout="wide",
    initial_sidebar_state="auto",
    page_icon="🌱"
)

# --- Simulated Database Functions ---
def get_responsible_tourism_tips():
    """Fetch responsible tourism tips (simulated)"""
    return pd.DataFrame({
        'tip_id': range(1, 16),
        'category': [
            'Cultural Respect', 'Cultural Respect', 'Cultural Respect',
            'Environmental', 'Environmental', 'Environmental',
            'Economic Impact', 'Economic Impact', 'Economic Impact',
            'Photography', 'Photography',
            'Accommodation', 'Accommodation',
            'Transportation', 'Transportation'
        ],
        'tip': [
            'Research local customs and traditions before your visit to show respect and avoid unintentional offense.',
            'Dress appropriately when visiting religious sites - cover shoulders, knees, and sometimes head.',
            'Ask permission before participating in religious ceremonies or cultural rituals.',
            'Minimize plastic waste by carrying a reusable water bottle, bag, and utensils.',
            'Stay on designated paths at natural and heritage sites to prevent erosion and damage.',
            'Choose eco-friendly tour operators who prioritize sustainability and conservation.',
            'Buy directly from local artisans to ensure they receive fair compensation for their work.',
            'Learn the basics of bargaining respectfully without aggressive haggling that devalues craftsmanship.',
            'Support community-based tourism initiatives that reinvest in local development.',
            'Always ask permission before photographing people, especially in rural and tribal areas.',
            'Be mindful about photographing religious ceremonies - some may prohibit photography.',
            'Choose locally-owned accommodations that employ local staff and use local products.',
            'Consider homestays for a more authentic experience that directly benefits families.',
            'Use public transportation or shared vehicles when possible to reduce carbon footprint.',
            'Consider carbon offset programs for long-distance travel to India.'
        ],
        'impact': [
            'Promotes cultural understanding and prevents misunderstandings.',
            'Shows respect for local beliefs and traditions.',
            'Ensures authentic participation without disrupting sacred practices.',
            'Reduces pollution in areas with limited waste management infrastructure.',
            'Preserves natural and cultural sites for future generations.',
            'Supports businesses committed to sustainable practices.',
            'Ensures artisans receive fair compensation and preserves traditional crafts.',
            'Maintains dignity of artisans while supporting fair economic exchange.',
            'Helps distribute tourism benefits throughout the community.',
            'Respects privacy and dignity, especially in communities unaccustomed to tourism.',
            'Preserves the sanctity of religious practices.',
            'Keeps tourism revenue within local economies.',
            'Provides cultural exchange opportunities and direct economic benefits.',
            'Reduces carbon emissions and supports local transportation systems.',
            'Mitigates environmental impact of long-distance travel.'
        ]
    })

def get_government_initiatives():
    """Fetch government initiatives data (simulated)"""
    return pd.DataFrame({
        'initiative_id': range(1, 11),
        'name': [
            'Swadesh Darshan Scheme',
            'PRASAD (Pilgrimage Rejuvenation and Spiritual Augmentation Drive)',
            'Incredible India 2.0 Campaign',
            'Adopt a Heritage Project',
            'National Mission on Cultural Mapping',
            'Hunar Se Rozgar Tak',
            'Rural Tourism Scheme',
            'Dekho Apna Desh Initiative',
            'Buddhist Circuit Development',
            'Heritage City Development and Augmentation Yojana (HRIDAY)'
        ],
        'focus_area': [
            'Infrastructure Development',
            'Religious Tourism',
            'Promotion',
            'Heritage Conservation',
            'Cultural Mapping',
            'Skill Development',
            'Rural Development',
            'Domestic Tourism',
            'Thematic Circuit',
            'Urban Heritage'
        ],
        'description': [
            'Develops theme-based tourist circuits across India, including cultural circuits, to enhance tourist experience and generate employment.',
            'Focuses on developing and beautifying religious destinations, improving tourist amenities, and preserving local culture and heritage.',
            'Promotes India\'s cultural richness and diversity through digital marketing, social media, and international campaigns.',
            'Encourages public and private companies to "adopt" heritage sites and develop tourist amenities while ensuring responsible tourism.',
            'Documents and preserves various cultural assets and resources across the country, including traditional art forms.',
            'Provides hospitality training to youth, creating skilled workforce for the tourism industry while preserving traditional knowledge.',
            'Promotes tourism in rural areas to showcase traditional life, art, culture, and heritage, benefiting local communities.',
            'Encourages Indians to explore domestic destinations, promoting awareness of India\'s rich cultural heritage.',
            'Develops sites related to Buddha\'s life for pilgrimage and cultural tourism, connecting India with other Buddhist countries.',
            'Focuses on holistic development of heritage cities, preserving character while creating tourist-friendly infrastructure.'
        ],
        'impact': [
            'Created integrated tourism circuits, improved infrastructure, and generated employment in cultural tourism.',
            'Enhanced pilgrim experience while preserving religious heritage and supporting local communities.',
            'Increased international awareness of India\'s cultural diversity and heritage tourism opportunities.',
            'Improved maintenance of monuments while creating public-private partnerships for heritage conservation.',
            'Documented thousands of artists and cultural practices, creating digital repository of India\'s cultural heritage.',
            'Trained thousands of youth in hospitality skills, creating employment while preserving traditional knowledge.',
            'Generated alternative livelihoods in rural areas and preserved traditional cultural practices.',
            'Increased domestic tourism to cultural sites and raised awareness about India\'s heritage among citizens.',
            'Connected Buddhist heritage sites, improved infrastructure, and increased international Buddhist tourism.',
            'Revitalized urban heritage areas while improving quality of life for residents and experience for tourists.'
        ],
        'website': [
            'https://tourism.gov.in/swadesh-darshan-scheme',
            'https://tourism.gov.in/prasad-scheme',
            'https://www.incredibleindia.org',
            'https://adoptaheritage.in',
            'https://nmcm.gov.in',
            'https://tourism.gov.in/hunar-se-rozgar-tak',
            'https://tourism.gov.in/rural-tourism',
            'https://dekhopanadesh.gov.in',
            'https://tourism.gov.in/buddhist-circuit',
            'https://mohua.gov.in/hriday'
        ]
    })

def get_impact_stories():
    """Fetch impact stories data (simulated)"""
    return pd.DataFrame({
        'story_id': range(1, 6),
        'title': [
            'Madhubani Art Revival in Bihar',
            'Responsible Tourism in Khonoma, Nagaland',
            'Shekhawati Haveli Restoration Project',
            'Women Artisans of Kutch',
            'Spiti Valley Eco-Tourism Initiative'
        ],
        'location': [
            'Madhubani, Bihar',
            'Khonoma, Nagaland',
            'Shekhawati Region, Rajasthan',
            'Kutch, Gujarat',
            'Spiti Valley, Himachal Pradesh'
        ],
        'story': [
            'Once facing decline, Madhubani painting has experienced a remarkable revival through responsible tourism. Visitors now participate in workshops led by master artists, learning the traditional techniques while providing direct income to artists. The Mithila Art Institute has trained over 500 young artists, preserving this ancient art form while creating sustainable livelihoods. Tourism has created market linkages, with visitors purchasing authentic artwork directly from creators.',
            'Khonoma, Asia\'s first green village, has pioneered community-based tourism where the entire village participates in and benefits from tourism. Visitors stay in traditional Angami Naga homes, learning about indigenous conservation practices that have protected the Khonoma Nature Conservation and Tragopan Sanctuary. The community has banned hunting, established forest protection protocols, and shares traditional ecological knowledge with visitors, creating a model of tourism that supports both cultural and environmental conservation.',
            'The ornate havelis (mansions) of Shekhawati were falling into disrepair until a community-led restoration project, supported by responsible tourism, began revitalizing them. Several havelis have been converted into heritage hotels and museums, with restoration work employing local craftspeople using traditional techniques. Tourism revenue now funds ongoing conservation, while visitors learn about the region\'s unique fresco art traditions from local guides trained in cultural interpretation.',
            'In the aftermath of the 2001 earthquake, women artisans in Kutch faced economic hardship as traditional crafts declined. Through responsible tourism initiatives, these women now showcase their embroidery, bandhani (tie-dye), and other textile arts directly to visitors. Self-help groups like Shrujan and Kala Raksha have connected over 4,000 women artisans to markets, while tourism has created appreciation for the cultural significance of these crafts. Visitors participate in craft workshops, supporting intergenerational knowledge transfer.',
            'The fragile ecosystem of Spiti Valley faced threats from unregulated tourism until local monasteries and communities established the Spiti Ecosphere initiative. This program trains local youth as eco-guides, develops homestay networks that follow strict environmental guidelines, and educates visitors about the region\'s unique Buddhist culture and high-altitude ecology. Tourism now funds solar energy projects, greenhouse farming, and snow leopard conservation, demonstrating how responsible tourism can support both cultural and environmental sustainability in vulnerable regions.'
        ],
        'impact_metrics': [
            '500+ artists trained, 35% increase in household income, 12 villages benefiting from art tourism',
            '80% reduction in hunting, 45 homestays established, 60% of village households benefiting from tourism',
            '28 havelis restored, 120 local craftspeople employed, 40% increase in visitor numbers',
            '4,000+ women artisans supported, 22 villages participating, 30% increase in craft valuation',
            '65 homestays established, 40% reduction in waste, 85% of tourism revenue remaining in local economy'
        ],
        'image_url': [
            'https://raw.githubusercontent.com/yashgupta17402/hero/main/madhubani_impact.jpg',
            'https://raw.githubusercontent.com/yashgupta17402/hero/main/khonoma_impact.jpg',
            'https://raw.githubusercontent.com/yashgupta17402/hero/main/shekhawati_impact.jpg',
            'https://raw.githubusercontent.com/yashgupta17402/hero/main/kutch_impact.jpg',
            'https://raw.githubusercontent.com/yashgupta17402/hero/main/spiti_impact.jpg'
        ]
    })

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

/* Tip Card Styling */
.tip-card {
    background-color: #f8f9fa;
    border-radius: 10px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    border-left: 5px solid #3498db;
    transition: transform 0.3s ease;
}
.tip-card:hover {
    transform: translateY(-5px);
}
.tip-card-title {
    font-size: 1.2rem;
    font-weight: 600;
    color: #2c3e50;
    margin-bottom: 0.5rem;
}
.tip-card-content {
    font-size: 1rem;
    color: #555;
    line-height: 1.5;
    margin-bottom: 0.5rem;
}
.tip-card-impact {
    font-size: 0.9rem;
    color: #7f8c8d;
    font-style: italic;
}

/* Initiative Card Styling */
.initiative-card {
    background-color: white;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    margin-bottom: 1.5rem;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    border: 1px solid #e0e0e0;
}
.initiative-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 16px rgba(0,0,0,0.15);
}
.initiative-card-header {
    background-color: #3498db;
    color: white;
    padding: 1rem 1.5rem;
}
.initiative-card-title {
    font-size: 1.3rem;
    font-weight: 600;
    margin-bottom: 0.3rem;
}
.initiative-card-subtitle {
    font-size: 0.9rem;
    opacity: 0.9;
}
.initiative-card-body {
    padding: 1.5rem;
}
.initiative-card-description {
    font-size: 1rem;
    color: #555;
    line-height: 1.5;
    margin-bottom: 1rem;
}
.initiative-card-impact {
    font-size: 0.95rem;
    color: #2c3e50;
    background-color: #f8f9fa;
    padding: 0.8rem;
    border-radius: 5px;
    margin-bottom: 1rem;
}
.initiative-card-link {
    display: inline-block;
    color: #3498db;
    text-decoration: none;
    font-weight: 500;
}
.initiative-card-link:hover {
    text-decoration: underline;
}

/* Impact Story Styling */
.impact-story {
    background-color: white;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    margin-bottom: 2rem;
}
.impact-story-image {
    width: 100%;
    height: 250px;
    object-fit: cover;
}
.impact-story-content {
    padding: 1.5rem;
}
.impact-story-title {
    font-size: 1.5rem;
    font-weight: 600;
    color: #2c3e50;
    margin-bottom: 0.5rem;
}
.impact-story-location {
    font-size: 1rem;
    color: #7f8c8d;
    margin-bottom: 1rem;
}
.impact-story-text {
    font-size: 1rem;
    color: #555;
    line-height: 1.6;
    margin-bottom: 1rem;
}
.impact-metrics {
    background-color: #f8f9fa;
    padding: 1rem;
    border-radius: 5px;
    margin-top: 1rem;
}
.impact-metrics-title {
    font-size: 1.1rem;
    font-weight: 600;
    color: #2c3e50;
    margin-bottom: 0.5rem;
}
.impact-metrics-list {
    list-style-type: none;
    padding: 0;
    margin: 0;
}
.impact-metrics-list li {
    padding-left: 1.5rem;
    position: relative;
    margin-bottom: 0.5rem;
    font-size: 0.95rem;
    color: #555;
}
.impact-metrics-list li:before {
    content: "✓";
    position: absolute;
    left: 0;
    color: #2ecc71;
    font-weight: bold;
}

/* Pledge Styling */
.pledge-container {
    background-color: #f0f9ff;
    border-radius: 10px;
    padding: 2rem;
    margin-top: 2rem;
    border: 1px solid #d1e7ff;
}
.pledge-title {
    font-size: 1.5rem;
    font-weight: 600;
    color: #2c3e50;
    margin-bottom: 1rem;
    text-align: center;
}
.pledge-subtitle {
    font-size: 1.1rem;
    color: #555;
    margin-bottom: 1.5rem;
    text-align: center;
}
.pledge-item {
    display: flex;
    align-items: flex-start;
    margin-bottom: 1rem;
}
.pledge-checkbox {
    margin-right: 1rem;
    margin-top: 0.2rem;
}
.pledge-text {
    font-size: 1rem;
    color: #2c3e50;
}
.pledge-button {
    background-color: #3498db;
    color: white;
    border: none;
    padding: 0.8rem 2rem;
    border-radius: 5px;
    font-size: 1.1rem;
    font-weight: 500;
    cursor: pointer;
    transition: background-color 0.3s ease;
    display: block;
    margin: 1.5rem auto 0;
}
.pledge-button:hover {
    background-color: #2980b9;
}
.pledge-confirmation {
    background-color: #d4edda;
    color: #155724;
    padding: 1rem;
    border-radius: 5px;
    margin-top: 1rem;
    text-align: center;
    font-weight: 500;
}

/* Category Badge */
.category-badge {
    display: inline-block;
    padding: 0.3rem 0.6rem;
    border-radius: 4px;
    font-size: 0.8rem;
    font-weight: 500;
    margin-right: 0.5rem;
    margin-bottom: 0.5rem;
}
.badge-cultural {
    background-color: #3498db;
    color: white;
}
.badge-environmental {
    background-color: #2ecc71;
    color: white;
}
.badge-economic {
    background-color: #f39c12;
    color: white;
}
.badge-photography {
    background-color: #9b59b6;
    color: white;
}
.badge-accommodation {
    background-color: #e74c3c;
    color: white;
}
.badge-transportation {
    background-color: #1abc9c;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("""
<div class="header">
    <h1>🌱 Responsible Tourism Guide</h1>
    <p>Learn how to travel responsibly in India, supporting local communities, preserving cultural heritage, and minimizing environmental impact. Your choices as a traveler can make a positive difference.</p>
</div>
""", unsafe_allow_html=True)

# --- Load Data ---
tips_df = get_responsible_tourism_tips()
initiatives_df = get_government_initiatives()
stories_df = get_impact_stories()

# --- Responsible Tourism Tips ---
st.markdown('<div class="section-container">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Responsible Tourism Tips</div>', unsafe_allow_html=True)
st.markdown('<div class="section-subtitle">Practical ways to make a positive impact during your travels in India</div>', unsafe_allow_html=True)

# Category filter
categories = ['All Categories'] + sorted(tips_df['category'].unique().tolist())
selected_category = st.selectbox("Filter by Category", categories)

# Filter tips by category
if selected_category != 'All Categories':
    filtered_tips = tips_df[tips_df['category'] == selected_category]
else:
    filtered_tips = tips_df

# Display tips
for _, tip in filtered_tips.iterrows():
    # Determine badge color based on category
    badge_class = ""
    if tip['category'] == 'Cultural Respect':
        badge_class = "badge-cultural"
    elif tip['category'] == 'Environmental':
        badge_class = "badge-environmental"
    elif tip['category'] == 'Economic Impact':
        badge_class = "badge-economic"
    elif tip['category'] == 'Photography':
        badge_class = "badge-photography"
    elif tip['category'] == 'Accommodation':
        badge_class = "badge-accommodation"
    elif tip['category'] == 'Transportation':
        badge_class = "badge-transportation"
    
    st.markdown(f"""
    <div class="tip-card">
        <span class="category-badge {badge_class}">{tip['category']}</span>
        <div class="tip-card-title">{tip['tip']}</div>
        <div class="tip-card-impact"><strong>Impact:</strong> {tip['impact']}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# --- Government & NGO Initiatives ---
st.markdown('<div class="section-container">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Government & NGO Initiatives</div>', unsafe_allow_html=True)
st.markdown('<div class="section-subtitle">Programs and policies promoting sustainable tourism and cultural preservation</div>', unsafe_allow_html=True)

# Focus area filter
focus_areas = ['All Areas'] + sorted(initiatives_df['focus_area'].unique().tolist())
selected_focus = st.selectbox("Filter by Focus Area", focus_areas)

# Filter initiatives by focus area
if selected_focus != 'All Areas':
    filtered_initiatives = initiatives_df[initiatives_df['focus_area'] == selected_focus]
else:
    filtered_initiatives = initiatives_df

# Display initiatives
for _, initiative in filtered_initiatives.iterrows():
    st.markdown(f"""
    <div class="initiative-card">
        <div class="initiative-card-header">
            <div class="initiative-card-title">{initiative['name']}</div>
            <div class="initiative-card-subtitle">Focus: {initiative['focus_area']}</div>
        </div>
        <div class="initiative-card-body">
            <div class="initiative-card-description">{initiative['description']}</div>
            <div class="initiative-card-impact"><strong>Impact:</strong> {initiative['impact']}</div>
            <a href="{initiative['website']}" target="_blank" class="initiative-card-link">Learn More →</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# --- Impact Stories ---
st.markdown('<div class="section-container">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Impact Stories</div>', unsafe_allow_html=True)
st.markdown('<div class="section-subtitle">Real examples of how responsible tourism has benefited communities and preserved cultural heritage</div>', unsafe_allow_html=True)

# Display impact stories
for _, story in stories_df.iterrows():
    st.markdown(f"""
    <div class="impact-story">
        <img src="{story['image_url']}" alt="{story['title']}" class="impact-story-image">
        <div class="impact-story-content">
            <div class="impact-story-title">{story['title']}</div>
            <div class="impact-story-location">{story['location']}</div>
            <div class="impact-story-text">{story['story']}</div>
            <div class="impact-metrics">
                <div class="impact-metrics-title">Impact Metrics</div>
                <ul class="impact-metrics-list">
                    {' '.join([f'<li>{metric.strip()}</li>' for metric in story['impact_metrics'].split(',')])}
                </ul>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# --- Responsible Traveler's Pledge ---
st.markdown('<div class="section-container">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Responsible Traveler\'s Pledge</div>', unsafe_allow_html=True)
st.markdown('<div class="section-subtitle">Commit to traveling responsibly and making a positive impact</div>', unsafe_allow_html=True)

st.markdown('<div class="pledge-container">', unsafe_allow_html=True)
st.markdown('<div class="pledge-title">I Pledge to Travel Responsibly in India</div>', unsafe_allow_html=True)
st.markdown('<div class="pledge-subtitle">By taking this pledge, you commit to being a responsible traveler who respects local cultures, supports communities, and preserves heritage.</div>', unsafe_allow_html=True)

# Pledge items
pledge_items = [
    "I will respect local customs, traditions, and dress codes.",
    "I will support local artisans by purchasing authentic handicrafts.",
    "I will minimize my environmental footprint by reducing waste and conserving resources.",
    "I will ask permission before photographing people or participating in cultural activities.",
    "I will learn about the places I visit and share accurate information about India's culture.",
    "I will choose accommodations and tour operators that practice sustainability.",
    "I will be mindful of my impact on local communities and heritage sites."
]

# Create checkboxes for each pledge item
pledge_checks = []
for item in pledge_items:
    check = st.checkbox(item)
    pledge_checks.append(check)

# Take pledge button
if st.button("Take the Pledge", key="pledge_button"):
    if all(pledge_checks):
        st.markdown('<div class="pledge-confirmation">Thank you for taking the Responsible Traveler\'s Pledge! Your commitment helps preserve India\'s cultural heritage for future generations.</div>', unsafe_allow_html=True)
    else:
        st.warning("Please check all items to complete the pledge.")

st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# --- Resources Section ---
st.markdown('<div class="section-container">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Additional Resources</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Recommended Reading")
    st.markdown("""
    - [Incredible India Official Website](https://www.incredibleindia.org)
    - [Responsible Tourism India](https://responsibletourismindia.com)
    - [UNESCO World Heritage Sites in India](https://whc.unesco.org/en/statesparties/in)
    - [India's GI Tagged Products](https://ipindia.gov.in/registered-gls.htm)
    - [Ministry of Tourism Guidelines](https://tourism.gov.in)
    """)

with col2:
    st.subheader("Responsible Tourism Organizations")
    st.markdown("""
    <p>Recommended Organizations:</p>
    <ul>
        <li><a href="https://www.thetravelfoundation.org.uk">The Travel Foundation</a></li>
        <li><a href="https://www.gstcouncil.org">Global Sustainable Tourism Council</a></li>
        <li><a href="https://www.ecotourismsocietyofindia.org">Ecotourism Society of India</a></li>
        <li><a href="https://rtsindia.org">Responsible Tourism Society of India</a></li>
    </ul>
""", unsafe_allow_html=True)