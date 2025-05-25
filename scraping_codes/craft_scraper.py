import google.generativeai as genai
import pandas as pd
import time # To handle potential rate limits

# --- Configuration ---
# 1. Configure your API key
#    (Store it securely, e.g., as an environment variable, not hardcoded)
GOOGLE_API_KEY = "use you api" # Replace with your actual API key
genai.configure(api_key=GOOGLE_API_KEY)

# 2. Initialize the Gemini Model
#    Choose a model that suits your needs (e.g., 'gemini-1.5-flash', 'gemini-1.5-pro')
#    Check the Gemini documentation for the latest model names and capabilities.
model = genai.GenerativeModel('gemini-1.5-flash-latest') # Or 'gemini-1.5-pro-latest'

# 3. Load your CSV data
#    Replace 'indian_crafts_data_v4.csv' with the actual path to your file.
try:
    df_crafts = pd.read_csv('indian_crafts_data_v4.csv')
    # To prevent issues with NaN values in string columns:
    df_crafts = df_crafts.fillna('')
except FileNotFoundError:
    print("Error: The CSV file was not found. Please check the file path.")
    exit()
except Exception as e:
    print(f"Error loading CSV: {e}")
    exit()

# --- Helper Function to Get Craft Details ---
def get_craft_info_from_gemini(craft_name, state, district, village):
    """
    Generates a prompt and queries the Gemini API for craft details.
    Attempts to get structured output.
    """
    prompt = f"""
    For the Indian craft named "{craft_name}" from {state} (District: {district}, Village/Sub District: {village}), provide the following information:

    1.  **Details**: A brief description of what the craft is, the materials used, and the process involved in making it.
    2.  **Historic Details**: Information about its origins, historical significance, evolution over time, and any traditional communities associated with it.
    3.  **Uniqueness to Attract Consumers**: What makes this craft special and appealing to consumers? Highlight its unique selling points, cultural value, aesthetics, or rarity.

    Please structure your response clearly with these three headings.
    For example:

    Details:
    [Information here]

    Historic Details:
    [Information here]

    Uniqueness to Attract Consumers:
    [Information here]
    """

    try:
        response = model.generate_content(prompt)
        if response.parts:
            return response.text
        else:
            if response.prompt_feedback and response.prompt_feedback.block_reason:
                return f"Blocked: {response.prompt_feedback.block_reason_message}"
            return "No content generated or response structure not as expected."
    except Exception as e:
        print(f"Error calling Gemini API for '{craft_name}': {e}")
        return "Error generating details."

# --- Main Processing Loop ---
# Create new columns in your DataFrame
df_crafts['Generated_Details'] = ""
df_crafts['Generated_Historic_Details'] = ""
df_crafts['Generated_Uniqueness'] = "" # <-- MODIFIED HERE

# Process a subset for testing, or the whole DataFrame
# For testing, you might want to process only the first few rows:
# for index, row in df_crafts.head(5).iterrows():
for index, row in df_crafts.iterrows():
    craft_name = row['Craft']
    state = row['State/UT']
    district = row['District']
    village = row['Village/Sub District']

    print(f"Processing craft: {craft_name} from {state}...")

    generated_text = get_craft_info_from_gemini(craft_name, state, district, village)

    # --- Basic Parsing Logic (you might need to make this more robust) ---
    details_text = "Not found"
    historic_text = "Not found"
    uniqueness_text = "Not found"

    if "Error generating details." not in generated_text and "Blocked:" not in generated_text and "No content generated" not in generated_text:
        parts = generated_text.split("Historic Details:")
        if len(parts) > 0:
            details_part = parts[0].replace("Details:", "").strip()
            details_text = details_part

        if len(parts) > 1:
            historic_uniqueness_parts = parts[1].split("Uniqueness to Attract Consumers:") # Prompt still asks for this heading
            if len(historic_uniqueness_parts) > 0:
                historic_text = historic_uniqueness_parts[0].strip()
            if len(historic_uniqueness_parts) > 1:
                uniqueness_text = historic_uniqueness_parts[1].strip()
        else:
            parts_alt = generated_text.split("Uniqueness to Attract Consumers:") # Prompt still asks for this heading
            if len(parts_alt) > 0 and "Details:" in parts_alt[0]:
                 details_historic_part = parts_alt[0].replace("Details:", "").strip()
                 if not details_text or details_text == "Not found":
                     details_text = details_historic_part
            if len(parts_alt) > 1:
                uniqueness_text = parts_alt[1].strip()


    df_crafts.at[index, 'Generated_Details'] = details_text
    df_crafts.at[index, 'Generated_Historic_Details'] = historic_text
    df_crafts.at[index, 'Generated_Uniqueness'] = uniqueness_text # <-- MODIFIED HERE

    print(f"Finished processing: {craft_name}")
    print("-" * 20)
    print(f"Details: {details_text[:100]}...")
    print(f"Historic: {historic_text[:100]}...")
    print(f"Uniqueness: {uniqueness_text[:100]}...") # <-- MODIFIED HERE
    print("-" * 40)

    time.sleep(1)

# --- Save the Enriched DataFrame ---
try:
    output_filename = 'indian_crafts_data_v4_enriched.csv'
    df_crafts.to_csv(output_filename, index=False)
    print(f"\nEnriched data saved to {output_filename}")
except Exception as e:
    print(f"Error saving CSV: {e}")
