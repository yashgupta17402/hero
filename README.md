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

## 📁 Project Structure
