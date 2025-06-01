import streamlit as st
import pandas as pd

# --- Page Configuration ---
st.set_page_config(
    page_title="Cultural Canvas India | Festivals",
    layout="wide",
    initial_sidebar_state="auto",
    page_icon="🎉"
)
def get_snowflake_connection():
    return st.connection("snowflake")
# --- Function to fetch festivals from Snowflake ---
def get_festivals_from_snowflake():
    """Fetch festival data from Snowflake FESTIVALS_FINAL table."""
    try:
        conn = get_snowflake_connection()  # Ensure this is defined elsewhere
        query = """
        SELECT
            "STATE",
            "FESTIVAL_NAME",
            "TIME_OF_YEAR",
            "SHORT_DESCRIPTION",
            "IMAGE_URL"
        FROM
            "CULTURE_HERITAGE"."PUBLIC"."FESTIVALS_FINAL";
        """
        df = conn.query(query, ttl=3600)
        return df
    except Exception as e:
        st.error(f"Error fetching festivals from Snowflake: {e}")
        return pd.DataFrame()

# --- Load data from Snowflake ---
df = get_festivals_from_snowflake()

# --- Page Content ---
st.title("🌟 Discover Indian Festivals")
st.subheader("Explore vibrant local celebrations from every corner of India")

# --- Festival Cards Layout ---
if not df.empty:
    col1, col2 = st.columns(2)

    for i, row in df.iterrows():
        with (col1 if i % 2 == 0 else col2):
            with st.container():
                st.markdown(f"### {row['FESTIVAL_NAME']}")
                st.markdown(f"**State:** {row['STATE']}")
                st.markdown(f"**Time of Year:** {row['TIME_OF_YEAR']}")
                st.markdown(row['SHORT_DESCRIPTION'])
                if pd.notna(row['IMAGE_URL']):
                    st.image(row['IMAGE_URL'], use_container_width=True)
                st.markdown("---")
else:
    st.warning("No festival data available.")
