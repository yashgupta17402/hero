# Cultural Canvas of India - YourStory Snowflake HERO Challenge Submission

**Live Streamlit App:** [https://srxbbgdabl9mnaqsu7unsc.streamlit.app/](https://srxbbgdabl9mnaqsu7unsc.streamlit.app/)

**GitHub Repository:** [https://github.com/yashgupta17402/hero/tree/main](https://github.com/yashgupta17402/hero/tree/main)


## 📜 Introduction

Cultural Canvas of India is a data-driven Streamlit application designed to showcase India's rich and diverse traditional art forms, uncover unique cultural experiences, and promote responsible tourism. Embark on a journey through India's artistic and cultural heritage, with insights and visualizations powered by data analysis, primarily managed through Snowflake.

This project aims to enrich the traveler's journey while contributing to the preservation of India's cultural treasures by providing a comprehensive, interactive platform.

## 🎯 Problem Statement

To design, develop, and produce a solution on Streamlit that showcases traditional art forms, uncovers cultural experiences offered across the country, and promotes responsible tourism. The project emphasizes a "data-first" approach, leveraging data from sources like `data.gov.in` and others to identify trends, seasonalities in tourism, and culturally rich yet "untouched" regions, all managed and queried via Snowflake.

## ✨ Features

* **Homepage:** An engaging overview with a dynamic slideshow, featured art forms, top cultural states, and upcoming festivals.
* **🎨 Art Forms Explorer:** Discover India's diverse traditional art forms (paintings, dances, crafts, textiles). Filter by state or art type, search, and view detailed information including origin, descriptions, and (where available) government support and artisan cooperatives. Data is sourced from Snowflake tables: `CRAFTS`, `PAINTING`, `DANCE`, and other curated lists.
* **🗺️ Cultural Hotspots Map:** An interactive map showcasing various cultural sites, monuments, and historical locations across India. Users can explore site details, including descriptions and (planned) tourism statistics.
* **🏛️ UNESCO World Heritage Sites Map:** An interactive map dedicated to exploring India's UNESCO World Heritage Sites with detailed information and links. Data sourced from a Snowflake table (`UNESCO_INDIA_SITES`).
* **Responsible Tourism Guide (Planned):** Information and guidelines on how to travel responsibly and support local communities and heritage preservation.

## 🛠️ Technology Stack

* **Frontend:** Streamlit
* **Backend/Data Processing:** Python
* **Data Storage & Warehousing:** Snowflake
* **Core Python Libraries:** Pandas (data manipulation), Folium & `streamlit-folium` (maps), Plotly Express (charts).

## 📊 Data Sources

The application utilizes data that can be sourced from:
* **Public Datasets:** [data.gov.in](https://www.data.gov.in) for government contributions, tourism statistics, heritage site information.
* **Official Bodies:** Ministry of Tourism, Ministry of Culture, Archaeological Survey of India (ASI), UNESCO.
* **State Tourism Websites:** For local art forms, festivals, and sites.
* **Curated Lists & Research:** For qualitative data, descriptions, and filling gaps.

All primary datasets for the application are intended to be stored and managed within **Snowflake** tables (e.g., `CRAFTS`, `PAINTING`, `DANCE`, `HERITAGE`, `UNESCO_INDIA_SITES`, `TOURISM_TRENDS`, etc.) within a database (e.g., `CULTURE_HERITAGE`) and schema (e.g., `PUBLIC`).


## 📂 File Descriptions

* **`.streamlit/secrets.toml`**: Configuration file for Streamlit to store sensitive information like API keys and database credentials (e.g., Snowflake). This file should be added to `.gitignore` to prevent accidental commits.
* **`assets/`**: (Optional) This directory can be used to store static assets like images, custom CSS files, or other resources used by the application.
* **`pages/`**: Contains the Python scripts for the different pages of the multi-page Streamlit application.
    * `1_🎨_Art_Forms_Explorer.py`: Script for the "Art Forms Explorer" page.
    * `2_🗺️_Cultural_Hotspots_Map.py`: Script for the "Cultural Hotspots Map" page.
    * `4_🏛️_UNESCO_Sites_Map.py`: Script for the "UNESCO Sites Map" page (ensure the filename matches your actual file).
    * *(Other page files)*: Placeholder for any additional pages in your application.
* **`home.py`**: The main script that serves as the landing page or homepage of your Streamlit application.
* **`README.md`**: This file, providing an overview of the project, setup instructions, and other relevant information.
* **`requirements.txt`**: Lists all Python package dependencies required to run the project. This file is used to recreate the project's environment (e.g., using `pip install -r requirements.txt`).




## 🚀 Setup and Installation

### Prerequisites

* Python 3.8 - 3.11
* pip (Python package installer)
* A Snowflake account with the necessary permissions to create databases, schemas, tables, and warehouses, or access to an existing setup.

### Steps

1.  **Clone the Repository (Optional):**
    If this project is hosted on Git:
    ```bash
    git clone <repository_url>
    cd cultural-canvas-india
    ```

2.  **Create a Virtual Environment (Recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install Dependencies:**
    Create a `requirements.txt` file with the following content (add other libraries as you use them):
    ```txt
    streamlit
    pandas
    folium
    streamlit-folium
    snowflake-connector-python
    plotly # For plotly.express and plotly.graph_objects
    ```
    Then install:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up Snowflake:**
    * Log in to your Snowflake account.
    * Create a database (e.g., `CULTURE_HERITAGE`) and a schema (e.g., `PUBLIC`).
    * Create a warehouse (e.g., `APP_WH`) and ensure your Snowflake user/role has `USAGE` rights on it.
    * Create the necessary tables (e.g., `CRAFTS`, `PAINTING`, `DANCE`, `HERITAGE`, `UNESCO_INDIA_SITES`, `TOURISM_TRENDS`, etc.) within your chosen database and schema. Refer to the column structures discussed or implied by the Python scripts.
    * Load data into these tables from your CSV files using `PUT` and `COPY INTO` commands or the Snowsight UI.

5.  **Configure Snowflake Credentials:**
    * Create a directory named `.streamlit` in the root of your project folder if it doesn't exist.
    * Inside `.streamlit`, create a file named `secrets.toml`.
    * Add your Snowflake connection details:
        ```toml
        [connections.snowflake]
        account = "YOUR_SNOWFLAKE_ACCOUNT_IDENTIFIER" # e.g., xy12345.region.cloud OR your_org-your_account
        user = "YOUR_SNOWFLAKE_USERNAME"
        password = "YOUR_SNOWFLAKE_PASSWORD"
        # If using browser-based/SSO auth, comment out password and uncomment authenticator:
        # authenticator = "externalbrowser"
        role = "YOUR_SNOWFLAKE_ROLE"
        warehouse = "YOUR_SNOWFLAKE_WAREHOUSE" # e.g., APP_WH
        database = "CULTURE_HERITAGE"          # Your database name
        schema = "PUBLIC"                      # Your schema name
        ```
    * **Important:** Add `.streamlit/secrets.toml` to your `.gitignore` file to prevent committing sensitive credentials.

## ▶️ Running the Application

Navigate to the root directory of the project in your terminal and run:

```bash
streamlit run home.py
```



Key Pages & Functionality
home.py (Main Page):

Provides an introduction to the "Cultural Canvas of India."
Features an automated slideshow highlighting key aspects of Indian culture and tourism.
Displays statistics on top cultural states (data from Snowflake).
Showcases a randomly selected GI-tagged art form (data from Snowflake).
Lists an upcoming major cultural festival (data from Snowflake).


pages/1_🎨_Art_Forms_Explorer.py:

Allows users to browse and explore a wide variety of Indian art forms (Paintings, Dances, Crafts, Textiles).
Data is primarily sourced from Snowflake tables (CRAFTS, PAINTING, DANCE) and supplemented by curated lists.
Features filters for State and Art Type, and a search bar.
Displays art forms in a card grid with images and short descriptions.
Provides a detailed view for each art form with comprehensive information, including its origin, description, GI tag status (if applicable), supporting government schemes, artisan cooperatives, and a map showing its region of origin.


pages/2_🗺️_Cultural_Hotspots_Map.py:

Presents an interactive Folium map marked with various cultural hotspots across India.
(Planned/In Progress) Users can click on markers to get more details about each site, including descriptions, images, and tourism statistics (domestic/foreign visitors, seasonality trends). Data to be sourced from Snowflake.
Includes layer controls to filter sites (e.g., UNESCO sites, ASI protected sites, high/low tourist traffic).


pages/4_🏛️_UNESCO_Sites_Map.py :

Dedicated page to explore India's UNESCO World Heritage Sites.
Data loaded from the UNESCO_INDIA_SITES table in Snowflake.
Interactive map with custom markers for each site.
Pop-ups provide names, locations, short descriptions, and links to official pages.
Search functionality to find specific UNESCO sites.


💡 Future Enhancements
User accounts and personalized recommendations.
Integration of real-time data where possible.
Community features for sharing experiences and tips.
More detailed data on local artisans and how to support them.
Expanded "Responsible Tourism Guide" with actionable advice.
Multi-language support.


🙏 Acknowledgements
Data sourced from data.gov.in, Ministry of Tourism, Ministry of Culture, UNESCO, and various public cultural archives.
Built using the wonderful Streamlit framework and Python libraries like Pandas, Folium, and Plotly.
Snowflake for robust data management.

Contributors:

Yash Gupta

Prasad Jore
