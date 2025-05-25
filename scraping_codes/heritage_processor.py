# import pandas as pd
# import os
# import glob
# import re
# from datetime import datetime
# import time

# # --- API Client Setup ---
# # Google Maps Client has been REMOVED.

# # Gemini API Client
# import google.generativeai as genai

# # !!! IMPORTANT: REPLACE THIS WITH YOUR ACTUAL GEMINI API KEY !!!
# # Example: GEMINI_API_KEY = "AIzaSyYourActualKeyGoesHere..."
# GEMINI_API_KEY = "AIzaSyBaTotk06zc3bGLACQ68l9sijkBjnTPp7w"

# gemini_model = None # Initialize as None

# # Check if the user has replaced the placeholder key
# # This check is performed BEFORE attempting to configure or use the API key.
# if GEMINI_API_KEY == "YOUR_ACTUAL_GEMINI_API_KEY_HERE" or not GEMINI_API_KEY:
#     print("CRITICAL WARNING: Your Gemini API Key is missing or is still the default placeholder value.")
#     print("                 Please replace 'YOUR_ACTUAL_GEMINI_API_KEY_HERE' at the top of the script with your valid Gemini API Key.")
#     print("                 All Gemini API features (latitude/longitude fetching, text generation) will be disabled.")
# else:
#     try:
#         print(f"INFO: Configuring Gemini API with key ending in: ...{GEMINI_API_KEY[-5:]}")
#         genai.configure(api_key=GEMINI_API_KEY)
        
#         # Using a standard 'flash' model. Change to 'gemini-2.0-flash' if that's specifically available to you.
#         # If 'gemini-2.0-flash' is incorrect, this line will likely cause an error.
#         MODEL_NAME = "gemini-1.5-flash-latest"
#         # MODEL_NAME = "gemini-2.0-flash" # Uncomment and use if you are sure about this model name
        
#         gemini_model = genai.GenerativeModel(MODEL_NAME)
#         print(f"INFO: Gemini client configured and model '{MODEL_NAME}' selected successfully.")
#         # Optional: A quick test to see if the model can be reached (can be commented out)
#         # try:
#         #     print("INFO: Performing a quick test call to Gemini model...")
#         #     test_response = gemini_model.generate_content("hello", generation_config=genai.types.GenerationConfig(candidate_count=1, max_output_tokens=5))
#         #     if test_response.text:
#         #         print("INFO: Gemini model test call successful.")
#         #     else:
#         #         print("WARNING: Gemini model test call did not return text. Check model status or API key permissions.")
#         # except Exception as test_e:
#         #     print(f"ERROR: Gemini model test call failed: {test_e}")
#         #     print("       This could indicate an issue with the API key, model name, or network access.")
#         #     gemini_model = None # Disable if test fails
            
#     except Exception as e:
#         print(f"ERROR initializing Gemini client or selecting model: {e}")
#         print("      Please ensure your Gemini API key is valid and the model name is correct for your access.")
#         print("      All Gemini API features will be disabled.")
#         gemini_model = None # Ensure it's None on any failure during setup


# # --- Configuration ---
# # INPUT_CSV_DIR = os.path.join("data", "CULTURE_HERITAGE_")
# # For debugging only - replace with your actual full path
# INPUT_CSV_DIR = r"C:\Users\yashg\Documents\hero_travel\data\CULTURE_HERITAGE_"
# file_pattern = os.path.join(INPUT_CSV_DIR, "*.csv")
# csv_files = glob.glob(file_pattern)
# OUTPUT_CSV_PATH = "final_heritage_data_gemini_only.csv"
# CURRENT_YEAR = datetime.now().year
# CITY_TO_STATE_MAPPING = {
#     "Thiruvananthapuram": "Kerala", "Bhubaneswar": "Odisha", "Saharanpur": "Uttar Pradesh",
#     "Namchi": "Sikkim", "RAIPUR": "Chhattisgarh", "Raipur": "Chhattisgarh",
#     "lucknow": "Uttar Pradesh", "Lucknow": "Uttar Pradesh", "Davanagere": "Karnataka",
#     "kakinada": "Andhra Pradesh", "Kakinada": "Andhra Pradesh", "Salem": "Tamil Nadu",
#     "TIRUPPUR": "Tamil Nadu", "Tiruppur": "Tamil Nadu", "VADODARA": "Gujarat",
#     "Vadodara": "Gujarat", "AURANGABAD": "Maharashtra", "Aurangabad": "Maharashtra",
#     "SRINAGAR": "Jammu and Kashmir", "Srinagar": "Jammu and Kashmir",
#     "BELAGAVI": "Karnataka", "Belagavi": "Karnataka", "PUDUCHERRY": "Puducherry",
#     "Puducherry": "Puducherry", "Hubballi-Dharwad": "Karnataka", "Hubballi": "Karnataka",
#     "Dharwad": "Karnataka", "SILVASSA": "Dadra and Nagar Haveli and Daman and Diu",
#     "Silvassa": "Dadra and Nagar Haveli and Daman and Diu", "PATNA": "Bihar", "Patna": "Bihar",
#     "KALYAN DOMBIVLI": "Maharashtra", "Kalyan Dombivli": "Maharashtra", "Kalyan": "Maharashtra",
#     "Dombivli": "Maharashtra", "GWALIOR": "Madhya Pradesh", "Gwalior": "Madhya Pradesh",
#     "TUMAKURU": "Karnataka", "Tumakuru": "Karnataka", "ATALNAGAR": "Chhattisgarh",
#     "Atal Nagar": "Chhattisgarh", "Nava Raipur": "Chhattisgarh", "ERODE": "Tamil Nadu",
#     "Erode": "Tamil Nadu", "shivamogga": "Karnataka", "Shivamogga": "Karnataka",
#     "BAREILLY": "Uttar Pradesh", "Bareilly": "Uttar Pradesh", "indore": "Madhya Pradesh",
#     "Indore": "Madhya Pradesh", "KalyanDombivli": "Maharashtra", "satna": "Madhya Pradesh",
#     "Satna": "Madhya Pradesh", "Thane": "Maharashtra", "AGARTALA": "Tripura",
#     "Agartala": "Tripura", "Thanjavur": "Tamil Nadu", "KOTA": "Rajasthan", "Kota": "Rajasthan",
#     "Pune": "Maharashtra", "KOHIMA": "Nagaland", "Kohima": "Nagaland",
# }

# # --- Helper Functions --- (extract_city_from_filename, get_state_for_city, determine_heritage_type, calculate_age, get_lat_lon_with_gemini, generate_heritage_info remain the same as previous version)

# def extract_city_from_filename(filename):
#     name = os.path.splitext(filename)[0]
#     patterns = [
#         re.compile(r"D\d+-CulturalHeritage_([A-Za-z]+)_.*", re.IGNORECASE),
#         re.compile(r"Cultural_Heritage_Data_([A-Za-z\s-]+)(?:_|\d{4})?", re.IGNORECASE),
#         re.compile(r"Cultural_Heritage_([A-Za-z\s-]+)_\d{4}", re.IGNORECASE),
#         re.compile(r"D\d+[_-]Cultural(?:_|-)Heritage(?:_updated)?(?:_?\d*_?\d*_?\d*_?)([A-Z_a-z-]+?)(?:_\d{4}|_?\d)?$", re.IGNORECASE),
#         re.compile(r"DS\d+-CulturalofHeritage_([A-Za-z]+)_\d{4}", re.IGNORECASE),
#         re.compile(r"([A-Za-z\s]+)_Cultural_Heritage_(\1)", re.IGNORECASE),
#         re.compile(r"Tourist_Places_\d{4}_\d_([A-Za-z]+)", re.IGNORECASE)
#     ]
#     for pattern in patterns:
#         match = pattern.search(name)
#         if match:
#             city = match.group(2) if pattern.pattern == r"([A-Za-z\s]+)_Cultural_Heritage_(\1)" else match.group(1)
#             city = city.replace('_', ' ').replace('-', ' ').strip()
#             return city.upper()
#     name = name.replace("Cultural_Heritage_Data_", "").replace("D31_Cultural_Heritage_", "") \
#         .replace("D31-CulturalHeritage_", "").replace("CulturalHeritage", "") \
#         .replace("Cultural_Heritage_", "").replace("Cultural_", "").replace("_updated", "")
#     name = re.sub(r"_\d{4}$", "", name)
#     name = re.sub(r"_\d(_\d)?(_\d)?$", "", name)
#     name = re.sub(r"^[A-Z\d]+?_([A-Z\d_]+?)_\d*_\d*_", "", name, flags=re.IGNORECASE)
#     name = name.replace('_', ' ').strip()
#     name = re.sub(r"^\d+\s?\d*\s?", "", name).strip()
#     return name.upper() if name else "UnknownCityFromFile"

# def get_state_for_city(city_name_from_csv):
#     city_key = str(city_name_from_csv).strip()
#     if city_key in CITY_TO_STATE_MAPPING: return CITY_TO_STATE_MAPPING[city_key]
#     if city_key.upper() in CITY_TO_STATE_MAPPING: return CITY_TO_STATE_MAPPING[city_key.upper()]
#     if city_key.title() in CITY_TO_STATE_MAPPING: return CITY_TO_STATE_MAPPING[city_key.title()]
#     return "UnknownState"

# def determine_heritage_type(name, nature_of_heritage, heritage_use):
#     name_lower, nature_lower, use_lower = str(name).lower(), str(nature_of_heritage).lower(), str(heritage_use).lower()
#     if any(k in nature_lower or k in use_lower for k in ["house", "housing", "residential"]): return None
#     if any(k in name_lower or k in nature_lower or k in use_lower for k in ["temple", "mandir", "kovil", "devalayam", "mosque", "masjid", "dargah", "khankah", "church", "basilica", "cathedral", "gurudwara", "takht", "prayer hall", "religious", "worship", "devasthan"]): return "religious/worship"
#     if any(k in name_lower or k in nature_lower or k in use_lower for k in ["palace", "mahal", "vilasam", "kothi", "rajbari", "wada"]): return "palace"
#     if any(k in use_lower for k in ["gate", "fort", "museum", "clock tower", "exhibition hall", "memorial", "govt office", "library", "gallery"]): return "monument"
#     if any(k in nature_lower or k in name_lower for k in ["monument", "ruins", "public national library", "fort gate", "archaeological site", "open space", "park", "maidan", "garden", "baag", "pillar", "statue", "stupa", "tomb", "minar", "cenotaph", "chhatri", "bawdi", "stepwell", "tank", "lakefront", "ghat", "fort", "garh", "gate", "darwaza", "museum", "tomb", "maqbara", "stupa", "minar", "library", "memorial", "pillar", "watch tower"]): return "monument"
#     if "building" in nature_lower and not any(k in nature_lower for k in ["house", "housing", "residential"]): return "monument"
#     return "Other"

# def calculate_age(age_str):
#     if pd.isna(age_str) or str(age_str).strip().upper() == "NA" or str(age_str).strip() == "": return "NA"
#     age_str = str(age_str).strip()
#     if age_str.isdigit(): return int(age_str)
#     year_match = re.fullmatch(r"(\d{4})", age_str)
#     if year_match:
#         y = int(year_match.group(1)); return CURRENT_YEAR - y if 1000 < y <= CURRENT_YEAR else "NA_InvalidYear"
#     year_ad_bc_match = re.match(r"c\.\s*(\d{3,4})\s*(?:AD|CE)", age_str, re.IGNORECASE)
#     if year_ad_bc_match: return CURRENT_YEAR - int(year_ad_bc_match.group(1))
#     year_range_match = re.match(r"(\d{4})-(\d{2,4})", age_str)
#     if year_range_match: return CURRENT_YEAR - int(year_range_match.group(1))
#     century_match = re.search(r"(\d{1,2})(?:st|nd|rd|th)?\s*century", age_str, re.IGNORECASE)
#     if century_match: return CURRENT_YEAR - ((int(century_match.group(1)) - 1) * 100 + 50)
#     roman_map = {"I":1, "II":2, "III":3, "IV":4, "V":5, "VI":6, "VII":7, "VIII":8, "IX":9, "X":10, "XI":11, "XII":12, "XIII":13, "XIV":14, "XV":15, "XVI":16, "XVII":17, "XVIII":18, "XIX":19, "XX":20, "XXI":21}
#     if "century" in age_str.lower():
#         p_roman = age_str.split(" ")[0].upper()
#         if p_roman in roman_map: return CURRENT_YEAR - ((roman_map[p_roman] - 1) * 100 + 50)
#     return "NA_FormatUnknown"

# def get_lat_lon_with_gemini(heritage_name, city, state):
#     if not gemini_model: return "NA (Gemini)", "NA (Gemini)"
#     prompt = (
#         f"What are the geographic coordinates (latitude and longitude) for '{heritage_name}' "
#         f"located in {city}, {state}? Please provide ONLY the latitude and longitude as "
#         f"comma-separated numerical values, like '12.9716, 77.5946'. "
#         f"If you cannot find the exact coordinates, please respond with only the words 'Not Found'."
#     )
#     try:
#         time.sleep(1.1) 
#         response = gemini_model.generate_content(prompt)
#         response_text = ""
#         if hasattr(response, 'parts') and response.parts: response_text = response.parts[0].text.strip()
#         elif hasattr(response, 'text') and response.text: response_text = response.text.strip()
#         if not response_text: return "NA (Gemini_Empty)", "NA (Gemini_Empty)"
#         if "not found" in response_text.lower(): return "NA (Gemini_NotFound)", "NA (Gemini_NotFound)"
#         match = re.search(r"^\s*(-?\d{1,3}(?:\.\d+)?)\s*,\s*(-?\d{1,3}(?:\.\d+)?)\s*$", response_text)
#         if not match: match = re.search(r"(-?\d{1,3}(?:\.\d+)?)\s*[,;\s]\s*(-?\d{1,3}(?:\.\d+)?)", response_text)
#         if match:
#             lat_str, lon_str = match.group(1), match.group(2)
#             try:
#                 lat, lon = float(lat_str), float(lon_str)
#                 if -90 <= lat <= 90 and -180 <= lon <= 180: return lat, lon
#                 return "NA (Gemini_InvalidRange)", "NA (Gemini_InvalidRange)"
#             except ValueError: return "NA (Gemini_ParseError)", "NA (Gemini_ParseError)"
#         return "NA (Gemini_NoMatch)", "NA (Gemini_NoMatch)"
#     except Exception as e:
#         print(f"    Error querying Gemini for lat/lon ({heritage_name}): {e}")
#         return "NA (Gemini_Error)", "NA (Gemini_Error)"

# def generate_heritage_info(heritage_name, city, state, info_type):
#     if not gemini_model: return f"NA (Gemini for {info_type})"
#     templates = {
#         "history": f"Provide a concise cultural history (around 50-100 words) of '{heritage_name}' located in {city}, {state}.",
#         "significance": f"Explain the historical and cultural significance (around 50-100 words) of '{heritage_name}' in {city}, {state}.",
#         "tourist_attraction": f"Describe what makes '{heritage_name}' in {city}, {state} a tourist attraction, highlighting unique features or information useful for visitors (around 50-100 words)."
#     }
#     prompt = templates.get(info_type)
#     if not prompt: return f"NA (Invalid info type for {info_type})"
#     try:
#         time.sleep(1.1) 
#         response = gemini_model.generate_content(prompt)
#         text_content = ""
#         if hasattr(response, 'parts') and response.parts: text_content = response.parts[0].text.strip().replace("\n", " ")
#         elif hasattr(response, 'text') and response.text: text_content = response.text.strip().replace("\n", " ")
#         return text_content if text_content else f"NA (Gemini_NoContent for {info_type})"
#     except Exception as e:
#         print(f"    Error generating {info_type} for {heritage_name} with Gemini: {e}")
#         return f"NA (Gemini_Error for {info_type})"

# # --- Main Processing Logic --- (process_csv_file function remains the same as previous)
# def process_csv_file(csv_filepath, city_from_filename_param):
#     processed_rows = []
#     try:
#         df = pd.read_csv(csv_filepath, on_bad_lines='skip')
#     except Exception as e:
#         print(f"Error reading {csv_filepath}: {e}"); return []

#     column_mapping = {
#         'City Name': 'City Name', 'City': 'City Name', 'CITY': 'City Name',
#         'Name of heritage': 'Name of heritage', 'NAME OF HERITAGE': 'Name of heritage', 'Heritage Structure': 'Name of heritage',
#         'Nature of heritage (open space, monuments, street etc.)': 'Nature of heritage',
#         'Nature of heritage': 'Nature of heritage', 'NATURE OF HERITAGE': 'Nature of heritage', 'Type of Structure': 'Nature of heritage',
#         'Heritage use': 'Heritage use', 'HERITAGE USE': 'Heritage use', 'Use of Structure': 'Heritage use',
#         'Age of heritage (in Years)': 'Age of heritage (in Years)',
#         'Age of heritage': 'Age of heritage (in Years)', 'AGE OF HERITAGE (IN YEARS)': 'Age of heritage (in Years)', 'Approx Age (Years)': 'Age of heritage (in Years)'
#     }
#     df.rename(columns=lambda c: column_mapping.get(c, c), inplace=True)
#     expected_cols = ['City Name', 'Name of heritage', 'Nature of heritage', 'Heritage use', 'Age of heritage (in Years)']
#     for col in expected_cols:
#         if col not in df.columns: df[col] = pd.NA

#     for index, row in df.iterrows():
#         city_name_csv = str(row.get('City Name', '')).strip()
#         city_name_to_use = city_from_filename_param if not city_name_csv or city_name_csv.lower() == 'na' else city_name_csv
        
#         city_lookup_key = city_name_to_use
#         if city_name_to_use.upper() in CITY_TO_STATE_MAPPING: city_lookup_key = city_name_to_use.upper()
#         elif city_name_to_use.title() in CITY_TO_STATE_MAPPING: city_lookup_key = city_name_to_use.title()
        
#         state = get_state_for_city(city_lookup_key)
#         heritage_name_csv = str(row.get('Name of heritage', '')).strip()
#         if not heritage_name_csv or heritage_name_csv.lower() == 'na':
#             continue
        
#         print(f"  Processing: {heritage_name_csv}, {city_name_to_use} ({state})") 
#         nature, use, age_input = row.get('Nature of heritage', pd.NA), row.get('Heritage use', pd.NA), row.get('Age of heritage (in Years)', pd.NA)
#         heritage_type = determine_heritage_type(heritage_name_csv, nature, use)
#         if heritage_type is None: 
#             continue
        
#         current_age_years = calculate_age(age_input)
#         latitude, longitude = get_lat_lon_with_gemini(heritage_name_csv, city_name_to_use, state)
#         culture_history = generate_heritage_info(heritage_name_csv, city_name_to_use, state, "history")
#         significance = generate_heritage_info(heritage_name_csv, city_name_to_use, state, "significance")
#         tourist_info = generate_heritage_info(heritage_name_csv, city_name_to_use, state, "tourist_attraction")

#         processed_rows.append({
#             'State': state, 'City': city_name_to_use, 'Latitude': latitude, 'Longitude': longitude,
#             'Name of heritage': heritage_name_csv, 'Type': heritage_type, 'Age of heritage (in Years)': current_age_years,
#             'Place culture history': culture_history, 'Significance': significance,
#             'Something more info which attract tourists': tourist_info
#         })
#     return processed_rows

# # --- Main function --- (main function remains the same as previous)
# def main():
#     all_heritage_data = []
#     if not os.path.exists(INPUT_CSV_DIR):
#         try:
#             os.makedirs(INPUT_CSV_DIR)
#             print(f"Created directory structure: '{INPUT_CSV_DIR}'.")
#             print(f"Please place your CSV files (e.g., D31-CulturalHeritage_5_PUDUCHERRY.csv) inside '{INPUT_CSV_DIR}'.")
#         except OSError as e:
#             print(f"Error: Could not create directory '{INPUT_CSV_DIR}'. Please create it manually. {e}")
#         return

#     file_pattern = os.path.join(INPUT_CSV_DIR, "*.csv")
#     csv_files = glob.glob(file_pattern)
    
#     if not csv_files:
#         print(f"No CSV files found in directory: '{INPUT_CSV_DIR}' (using pattern: '*.csv').")
#         print(f"Please ensure your script is run from the correct parent directory of '{INPUT_CSV_DIR.split(os.sep)[0]}',")
#         print(f"and that files like 'D31-CulturalHeritage_5_PUDUCHERRY.csv' are inside '{INPUT_CSV_DIR}'.")
#         return
           
#     print(f"Found {len(csv_files)} CSV files to process from '{INPUT_CSV_DIR}'.")

#     for csv_file_path in csv_files:
#         filename_only = os.path.basename(csv_file_path)
#         city_from_filename = extract_city_from_filename(filename_only)
#         print(f"\nProcessing file: {filename_only} (Detected City from filename: {city_from_filename})")
#         all_heritage_data.extend(process_csv_file(csv_file_path, city_from_filename))

#     if all_heritage_data:
#         final_df = pd.DataFrame(all_heritage_data)
#         try:
#             final_df.to_csv(OUTPUT_CSV_PATH, index=False, encoding='utf-8')
#             print(f"\nSuccessfully created consolidated CSV: {OUTPUT_CSV_PATH}")
#         except Exception as e: print(f"Error writing final CSV: {e}")
#     else: print("\nNo data processed. Final CSV not created.")


# if __name__ == "__main__":
#     # The check for GEMINI_API_KEY is now at the top, right after its definition.
#     # If gemini_model is None after the setup attempt, the functions using it will return "NA (Gemini)"
#     if not gemini_model: # A simpler check here, detailed warning is printed during initialization
#         print("Re-confirming: Gemini model was not initialized. API calls to Gemini will not be made.")
#     main()



import pandas as pd
import os
import glob
import re
from datetime import datetime
import time

# --- API Client Setup ---
import google.generativeai as genai

# !!! IMPORTANT: REPLACE THIS WITH YOUR ACTUAL GEMINI API KEY !!!
GEMINI_API_KEY = "AIzaSyBaTotk06zc3bGLACQ68l9sijkBjnTPp7w" # User provided this key as an example of their setup

gemini_model = None

if GEMINI_API_KEY == "YOUR_ACTUAL_GEMINI_API_KEY_HERE" or not GEMINI_API_KEY:
    print("CRITICAL WARNING: Your Gemini API Key is missing or is still the default placeholder value.")
    print("                 Please replace 'YOUR_ACTUAL_GEMINI_API_KEY_HERE' at the top of the script with your valid Gemini API Key.")
    print("                 All Gemini API features (latitude/longitude fetching, text generation) will be disabled.")
else:
    try:
        print(f"INFO: Configuring Gemini API with key ending in: ...{GEMINI_API_KEY[-5:]}")
        genai.configure(api_key=GEMINI_API_KEY)
        MODEL_NAME = "gemini-1.5-flash-latest"
        gemini_model = genai.GenerativeModel(MODEL_NAME)
        print(f"INFO: Gemini client configured and model '{MODEL_NAME}' selected successfully.")
    except Exception as e:
        print(f"ERROR initializing Gemini client or selecting model: {e}")
        print("      Please ensure your Gemini API key is valid and the model name is correct for your access.")
        print("      All Gemini API features will be disabled.")
        gemini_model = None


# --- Configuration ---
# INPUT_CSV_DIR = os.path.join("data", "CULTURE_HERITAGE_")
INPUT_CSV_DIR = r"C:\Users\yashg\Documents\hero_travel\data\CULTURE_HERITAGE_"
file_pattern = os.path.join(INPUT_CSV_DIR, "*.csv")
csv_files = glob.glob(file_pattern)
OUTPUT_CSV_PATH = "final_heritage_data_gemini_only.csv"
CURRENT_YEAR = datetime.now().year
CITY_TO_STATE_MAPPING = {
    "Thiruvananthapuram": "Kerala", "Bhubaneswar": "Odisha", "Saharanpur": "Uttar Pradesh",
    "Namchi": "Sikkim", "RAIPUR": "Chhattisgarh", "Raipur": "Chhattisgarh",
    "lucknow": "Uttar Pradesh", "Lucknow": "Uttar Pradesh", "Davanagere": "Karnataka",
    "kakinada": "Andhra Pradesh", "Kakinada": "Andhra Pradesh", "Salem": "Tamil Nadu",
    "TIRUPPUR": "Tamil Nadu", "Tiruppur": "Tamil Nadu", "VADODARA": "Gujarat",
    "Vadodara": "Gujarat", "AURANGABAD": "Maharashtra", "Aurangabad": "Maharashtra", # Sambhaji Nagar
    "SRINAGAR": "Jammu and Kashmir", "Srinagar": "Jammu and Kashmir",
    "BELAGAVI": "Karnataka", "Belagavi": "Karnataka", "PUDUCHERRY": "Puducherry",
    "Puducherry": "Puducherry", "Hubballi-Dharwad": "Karnataka", "Hubballi": "Karnataka",
    "Dharwad": "Karnataka", "SILVASSA": "Dadra and Nagar Haveli and Daman and Diu",
    "Silvassa": "Dadra and Nagar Haveli and Daman and Diu", "PATNA": "Bihar", "Patna": "Bihar",
    "KALYAN DOMBIVLI": "Maharashtra", "Kalyan Dombivli": "Maharashtra", "Kalyan": "Maharashtra",
    "Dombivli": "Maharashtra", "GWALIOR": "Madhya Pradesh", "Gwalior": "Madhya Pradesh",
    "TUMAKURU": "Karnataka", "Tumakuru": "Karnataka", "ATALNAGAR": "Chhattisgarh", # Nava Raipur
    "Atal Nagar": "Chhattisgarh", "Nava Raipur": "Chhattisgarh", "ERODE": "Tamil Nadu",
    "Erode": "Tamil Nadu", "shivamogga": "Karnataka", "Shivamogga": "Karnataka",
    "BAREILLY": "Uttar Pradesh", "Bareilly": "Uttar Pradesh", "indore": "Madhya Pradesh",
    "Indore": "Madhya Pradesh", "KalyanDombivli": "Maharashtra", "satna": "Madhya Pradesh",
    "Satna": "Madhya Pradesh", "Thane": "Maharashtra", "AGARTALA": "Tripura",
    "Agartala": "Tripura", "Thanjavur": "Tamil Nadu", "KOTA": "Rajasthan", "Kota": "Rajasthan",
    "Pune": "Maharashtra", "KOHIMA": "Nagaland", "Kohima": "Nagaland",
}

# --- Helper Functions ---

def extract_city_from_filename(filename):
    name = os.path.splitext(filename)[0]
    # More specific pattern first for filenames like "D31 - Cultural Heritage_0_0_RAIPUR"
    specific_pattern = re.compile(r"D\d+\s*-\s*Cultural\s*Heritage(?:_\d+)*_([A-Za-z\s-]+)", re.IGNORECASE)
    match_specific = specific_pattern.search(name)
    if match_specific:
        city = match_specific.group(1).replace('_', ' ').strip()
        return city.upper()

    patterns = [
        re.compile(r"D\d+-CulturalHeritage_([A-Za-z]+)_.*", re.IGNORECASE),
        re.compile(r"Cultural_Heritage_Data_([A-Za-z\s-]+)(?:_|\d{4})?", re.IGNORECASE),
        re.compile(r"Cultural_Heritage_([A-Za-z\s-]+)_\d{4}", re.IGNORECASE),
        re.compile(r"D\d+[_-]Cultural(?:_|-)Heritage(?:_updated)?(?:_?\d*_?\d*_?\d*_?)([A-Z_a-z-]+?)(?:_\d{4}|_?\d)?$", re.IGNORECASE),
        re.compile(r"DS\d+-CulturalofHeritage_([A-Za-z]+)_\d{4}", re.IGNORECASE),
        re.compile(r"([A-Za-z\s]+)_Cultural_Heritage_(\1)", re.IGNORECASE),
        re.compile(r"Tourist_Places_\d{4}_\d_([A-Za-z]+)", re.IGNORECASE)
    ]
    for pattern in patterns:
        match = pattern.search(name)
        if match:
            city = match.group(2) if pattern.pattern == r"([A-Za-z\s]+)_Cultural_Heritage_(\1)" else match.group(1)
            city = city.replace('_', ' ').replace('-', ' ').strip()
            return city.upper()
    # Fallback cleaning
    name = name.replace("Cultural_Heritage_Data_", "").replace("D31_Cultural_Heritage_", "") \
        .replace("D31-CulturalHeritage_", "").replace("CulturalHeritage", "") \
        .replace("Cultural_Heritage_", "").replace("Cultural_", "").replace("_updated", "")
    name = re.sub(r"_\d{4}$", "", name) # Remove trailing _YYYY
    name = re.sub(r"_\d(_\d)?(_\d)?$", "", name) # Remove trailing _1_1 or _1 etc.
    name = re.sub(r"^[A-Z\d]+?_([A-Z\d_]+?)_\d*_\d*_", "", name, flags=re.IGNORECASE) # D31_..._0_0_
    name = name.replace('_', ' ').strip()
    name = re.sub(r"^\d+\s?\d*\s?", "", name).strip() # Remove leading numbers/indices
    return name.upper() if name else "UnknownCityFromFile"

def get_state_for_city(city_name_from_csv):
    city_key = str(city_name_from_csv).strip()
    if city_key in CITY_TO_STATE_MAPPING: return CITY_TO_STATE_MAPPING[city_key]
    if city_key.upper() in CITY_TO_STATE_MAPPING: return CITY_TO_STATE_MAPPING[city_key.upper()]
    if city_key.title() in CITY_TO_STATE_MAPPING: return CITY_TO_STATE_MAPPING[city_key.title()]
    return "UnknownState"

def determine_heritage_type(name, nature_of_heritage, heritage_use):
    name_lower, nature_lower, use_lower = str(name).lower(), str(nature_of_heritage).lower(), str(heritage_use).lower()
    if any(k in nature_lower or k in use_lower for k in ["house", "housing", "residential"]): return None
    if any(k in name_lower or k in nature_lower or k in use_lower for k in ["temple", "mandir", "kovil", "devalayam", "mosque", "masjid", "dargah", "khankah", "church", "basilica", "cathedral", "gurudwara", "takht", "prayer hall", "religious", "worship", "devasthan"]): return "religious/worship"
    if any(k in name_lower or k in nature_lower or k in use_lower for k in ["palace", "mahal", "vilasam", "kothi", "rajbari", "wada"]): return "palace"
    if any(k in use_lower for k in ["gate", "fort", "museum", "clock tower", "exhibition hall", "memorial", "govt office", "library", "gallery"]): return "monument"
    if any(k in nature_lower or k in name_lower for k in ["monument", "ruins", "public national library", "fort gate", "archaeological site", "open space", "park", "maidan", "garden", "baag", "pillar", "statue", "stupa", "tomb", "minar", "cenotaph", "chhatri", "bawdi", "stepwell", "tank", "lakefront", "ghat", "fort", "garh", "gate", "darwaza", "museum", "tomb", "maqbara", "stupa", "minar", "library", "memorial", "pillar", "watch tower"]): return "monument"
    if "building" in nature_lower and not any(k in nature_lower for k in ["house", "housing", "residential"]): return "monument"
    return "Other"

def calculate_age(age_str):
    if pd.isna(age_str) or str(age_str).strip().upper() == "NA" or str(age_str).strip() == "": return "NA"
    age_str = str(age_str).strip()
    if age_str.isdigit(): return int(age_str)
    year_match = re.fullmatch(r"(\d{4})", age_str)
    if year_match:
        y = int(year_match.group(1)); return CURRENT_YEAR - y if 1000 < y <= CURRENT_YEAR else "NA_InvalidYear"
    year_ad_bc_match = re.match(r"c\.\s*(\d{3,4})\s*(?:AD|CE)", age_str, re.IGNORECASE)
    if year_ad_bc_match: return CURRENT_YEAR - int(year_ad_bc_match.group(1))
    year_range_match = re.match(r"(\d{4})-(\d{2,4})", age_str)
    if year_range_match: return CURRENT_YEAR - int(year_range_match.group(1))
    century_match = re.search(r"(\d{1,2})(?:st|nd|rd|th)?\s*century", age_str, re.IGNORECASE)
    if century_match: return CURRENT_YEAR - ((int(century_match.group(1)) - 1) * 100 + 50)
    roman_map = {"I":1, "II":2, "III":3, "IV":4, "V":5, "VI":6, "VII":7, "VIII":8, "IX":9, "X":10, "XI":11, "XII":12, "XIII":13, "XIV":14, "XV":15, "XVI":16, "XVII":17, "XVIII":18, "XIX":19, "XX":20, "XXI":21}
    if "century" in age_str.lower():
        p_roman = age_str.split(" ")[0].upper()
        if p_roman in roman_map: return CURRENT_YEAR - ((roman_map[p_roman] - 1) * 100 + 50)
    return "NA_FormatUnknown"

def get_lat_lon_with_gemini(heritage_name, city, state):
    if not gemini_model: return "NA (Gemini)", "NA (Gemini)"
    prompt = (
        f"What are the geographic coordinates (latitude and longitude) for '{heritage_name}' "
        f"located in {city}, {state}? Please provide ONLY the latitude and longitude as "
        f"comma-separated numerical values, like '12.9716, 77.5946'. "
        f"If you cannot find the exact coordinates, please respond with only the words 'Not Found'."
    )
    try:
        time.sleep(1.1) 
        response = gemini_model.generate_content(prompt)
        response_text = ""
        if hasattr(response, 'parts') and response.parts: response_text = response.parts[0].text.strip()
        elif hasattr(response, 'text') and response.text: response_text = response.text.strip()
        if not response_text: return "NA (Gemini_Empty)", "NA (Gemini_Empty)"
        if "not found" in response_text.lower(): return "NA (Gemini_NotFound)", "NA (Gemini_NotFound)"
        match = re.search(r"^\s*(-?\d{1,3}(?:\.\d+)?)\s*,\s*(-?\d{1,3}(?:\.\d+)?)\s*$", response_text)
        if not match: match = re.search(r"(-?\d{1,3}(?:\.\d+)?)\s*[,;\s]\s*(-?\d{1,3}(?:\.\d+)?)", response_text)
        if match:
            lat_str, lon_str = match.group(1), match.group(2)
            try:
                lat, lon = float(lat_str), float(lon_str)
                if -90 <= lat <= 90 and -180 <= lon <= 180: return lat, lon
                return "NA (Gemini_InvalidRange)", "NA (Gemini_InvalidRange)"
            except ValueError: return "NA (Gemini_ParseError)", "NA (Gemini_ParseError)"
        return "NA (Gemini_NoMatch)", "NA (Gemini_NoMatch)"
    except Exception as e:
        print(f"    Error querying Gemini for lat/lon ({heritage_name}): {e}")
        return "NA (Gemini_Error)", "NA (Gemini_Error)"

def generate_heritage_info(heritage_name, city, state, info_type):
    if not gemini_model: return f"NA (Gemini for {info_type})"
    templates = {
        "history": f"Provide a concise cultural history (around 50-100 words) of '{heritage_name}' located in {city}, {state}.",
        "significance": f"Explain the historical and cultural significance (around 50-100 words) of '{heritage_name}' in {city}, {state}.",
        "tourist_attraction": f"Describe what makes '{heritage_name}' in {city}, {state} a tourist attraction, highlighting unique features or information useful for visitors (around 50-100 words)."
    }
    prompt = templates.get(info_type)
    if not prompt: return f"NA (Invalid info type for {info_type})"
    try:
        time.sleep(1.1) 
        response = gemini_model.generate_content(prompt)
        text_content = ""
        if hasattr(response, 'parts') and response.parts: text_content = response.parts[0].text.strip().replace("\n", " ")
        elif hasattr(response, 'text') and response.text: text_content = response.text.strip().replace("\n", " ")
        return text_content if text_content else f"NA (Gemini_NoContent for {info_type})"
    except Exception as e:
        print(f"    Error generating {info_type} for {heritage_name} with Gemini: {e}")
        return f"NA (Gemini_Error for {info_type})"

# --- Main Processing Logic ---
def process_csv_file(csv_filepath, city_from_filename_param):
    processed_rows = []
    df = None
    encodings_to_try = ['utf-8', 'latin1', 'cp1252'] # Common encodings
    for encoding in encodings_to_try:
        try:
            df = pd.read_csv(csv_filepath, on_bad_lines='skip', encoding=encoding)
            print(f"Successfully read {os.path.basename(csv_filepath)} with encoding '{encoding}'.")
            break # Exit loop if successful
        except UnicodeDecodeError:
            print(f"Failed to read {os.path.basename(csv_filepath)} with encoding '{encoding}'. Trying next...")
        except Exception as e:
            print(f"Error reading {os.path.basename(csv_filepath)} with encoding '{encoding}': {e}")
            # If it's a general error not related to decoding, we might not want to try other encodings
            # For now, we'll let it try others, but this could be refined.
            
    if df is None:
        print(f"Could not read CSV file: {csv_filepath} after trying encodings: {encodings_to_try}")
        return [] # Skip this file

    column_mapping = {
        'City Name': 'City Name', 'City': 'City Name', 'CITY': 'City Name',
        'Name of heritage': 'Name of heritage', 'NAME OF HERITAGE': 'Name of heritage', 'Heritage Structure': 'Name of heritage',
        'Nature of heritage (open space, monuments, street etc.)': 'Nature of heritage',
        'Nature of heritage': 'Nature of heritage', 'NATURE OF HERITAGE': 'Nature of heritage', 'Type of Structure': 'Nature of heritage',
        'Heritage use': 'Heritage use', 'HERITAGE USE': 'Heritage use', 'Use of Structure': 'Heritage use',
        'Age of heritage (in Years)': 'Age of heritage (in Years)',
        'Age of heritage': 'Age of heritage (in Years)', 'AGE OF HERITAGE (IN YEARS)': 'Age of heritage (in Years)', 'Approx Age (Years)': 'Age of heritage (in Years)'
    }
    df.rename(columns=lambda c: column_mapping.get(c, c), inplace=True)
    expected_cols = ['City Name', 'Name of heritage', 'Nature of heritage', 'Heritage use', 'Age of heritage (in Years)']
    for col in expected_cols:
        if col not in df.columns: df[col] = pd.NA

    for index, row in df.iterrows():
        # Robust check for city_name_csv
        city_name_csv_val = row.get('City Name', pd.NA)
        if pd.isna(city_name_csv_val) or str(city_name_csv_val).strip().lower() == 'nan' or not str(city_name_csv_val).strip():
            city_name_to_use = city_from_filename_param
        else:
            city_name_to_use = str(city_name_csv_val).strip()
        
        # Robust check for heritage_name_csv
        heritage_name_csv_val = row.get('Name of heritage', pd.NA)
        if pd.isna(heritage_name_csv_val) or str(heritage_name_csv_val).strip().lower() == 'nan' or not str(heritage_name_csv_val).strip():
            # print(f"    Skipping row {index+2} in {os.path.basename(csv_filepath)} due to missing or 'nan' heritage name.")
            continue # Skip this row if heritage name is effectively missing
        else:
            heritage_name_csv = str(heritage_name_csv_val).strip()
        
        # If city_name_to_use itself became "nan" (e.g. from filename extraction for a badly named file AND CSV column was also nan)
        if city_name_to_use.lower() == 'nan':
            # print(f"    Skipping row {index+2} in {os.path.basename(csv_filepath)} due to 'nan' city name after all checks.")
            continue

        city_lookup_key = city_name_to_use
        if city_name_to_use.upper() in CITY_TO_STATE_MAPPING: city_lookup_key = city_name_to_use.upper()
        elif city_name_to_use.title() in CITY_TO_STATE_MAPPING: city_lookup_key = city_name_to_use.title()
        
        state = get_state_for_city(city_lookup_key)
        
        print(f"  Processing: {heritage_name_csv}, {city_name_to_use} ({state})") 
        nature, use, age_input = row.get('Nature of heritage', pd.NA), row.get('Heritage use', pd.NA), row.get('Age of heritage (in Years)', pd.NA)
        heritage_type = determine_heritage_type(heritage_name_csv, nature, use)
        if heritage_type is None: 
            continue
        
        current_age_years = calculate_age(age_input)
        latitude, longitude = get_lat_lon_with_gemini(heritage_name_csv, city_name_to_use, state)
        culture_history = generate_heritage_info(heritage_name_csv, city_name_to_use, state, "history")
        significance = generate_heritage_info(heritage_name_csv, city_name_to_use, state, "significance")
        tourist_info = generate_heritage_info(heritage_name_csv, city_name_to_use, state, "tourist_attraction")

        processed_rows.append({
            'State': state, 'City': city_name_to_use, 'Latitude': latitude, 'Longitude': longitude,
            'Name of heritage': heritage_name_csv, 'Type': heritage_type, 'Age of heritage (in Years)': current_age_years,
            'Place culture history': culture_history, 'Significance': significance,
            'Something more info which attract tourists': tourist_info
        })
    return processed_rows

# --- Main function ---
def main():
    all_heritage_data = []
    if not os.path.exists(INPUT_CSV_DIR):
        try:
            os.makedirs(INPUT_CSV_DIR)
            print(f"Created directory structure: '{INPUT_CSV_DIR}'.")
            print(f"Please place your CSV files (e.g., D31-CulturalHeritage_5_PUDUCHERRY.csv) inside '{INPUT_CSV_DIR}'.")
        except OSError as e:
            print(f"Error: Could not create directory '{INPUT_CSV_DIR}'. Please create it manually. {e}")
        return

    file_pattern = os.path.join(INPUT_CSV_DIR, "*.csv")
    csv_files = glob.glob(file_pattern)
    
    if not csv_files:
        print(f"No CSV files found in directory: '{INPUT_CSV_DIR}' (using pattern: '*.csv').")
        print(f"Please ensure your script is run from the correct parent directory of '{INPUT_CSV_DIR.split(os.sep)[0]}',")
        print(f"and that files like 'D31-CulturalHeritage_5_PUDUCHERRY.csv' are inside '{INPUT_CSV_DIR}'.")
        return
           
    print(f"Found {len(csv_files)} CSV files to process from '{INPUT_CSV_DIR}'.")

    for csv_file_path in csv_files:
        filename_only = os.path.basename(csv_file_path)
        city_from_filename = extract_city_from_filename(filename_only)
        print(f"\nProcessing file: {filename_only} (Detected City from filename: {city_from_filename})")
        all_heritage_data.extend(process_csv_file(csv_file_path, city_from_filename))

    if all_heritage_data:
        final_df = pd.DataFrame(all_heritage_data)
        try:
            final_df.to_csv(OUTPUT_CSV_PATH, index=False, encoding='utf-8')
            print(f"\nSuccessfully created consolidated CSV: {OUTPUT_CSV_PATH}")
        except Exception as e: print(f"Error writing final CSV: {e}")
    else: print("\nNo data processed. Final CSV not created.")


if __name__ == "__main__":
    if not gemini_model: 
        print("Re-confirming: Gemini model was not initialized. API calls to Gemini will not be made.")
    main()