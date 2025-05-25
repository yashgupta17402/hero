import requests
import json
import csv

# URL that directly serves JSON data
url = "https://techedumike.online/all_scheme_public/Allied_Cultural_Activities.php"
# https://techedumike.online/all_scheme_public/repertory_grant_scheme.php

# Output CSV file name
output_csv_file = 'Allied_Cultural_Activities.csv'

try:
    # 1. Fetch the JSON content directly
    print(f"Fetching JSON content from {url}...")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
    
    # The response text is the JSON string itself
    json_string = response.text
    print("JSON content fetched successfully.")
    # print("Raw JSON string (first 200 chars):", json_string[:200]) # For debugging

    # 2. Parse the JSON string
    try:
        print("Parsing JSON string...")
        parsed_json_data = json.loads(json_string)
        print("JSON data parsed successfully.")
        # print("Sample of parsed data (first item):", parsed_json_data[0] if parsed_json_data else "No data")

        # 3. Convert JSON to CSV
        if parsed_json_data and isinstance(parsed_json_data, list) and len(parsed_json_data) > 0:
            if isinstance(parsed_json_data[0], dict):
                # Get headers from the keys of the first dictionary in the list
                headers = parsed_json_data[0].keys()

                print(f"Writing data to {output_csv_file}...")
                with open(output_csv_file, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=headers)
                    writer.writeheader()  # Write the header row
                    writer.writerows(parsed_json_data) # Write all data rows
                print(f"Data successfully converted to {output_csv_file}")
            else:
                print("Error: The parsed JSON data is a list, but its elements are not dictionaries.")
        elif isinstance(parsed_json_data, list) and len(parsed_json_data) == 0:
            print("The JSON data is an empty list. No CSV file will be created.")
        else:
            print("Error: The parsed JSON data is not in the expected format (a list of dictionaries).")

    except json.JSONDecodeError as e:
        print(f"Error parsing JSON string: {e}")
        print(f"Problematic JSON string (first 500 chars):\n{json_string[:500]}")
    except IOError as e:
        print(f"Error writing CSV file: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during JSON processing or CSV conversion: {e}")

except requests.exceptions.RequestException as e:
    print(f"Error fetching URL: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")