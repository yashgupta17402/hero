import requests
from bs4 import BeautifulSoup
import pandas as pd
import time # For adding delays
from urllib.parse import urljoin # For handling relative URLs in pagination
import re # For more flexible text searching in pagination

base_url = "https://www.craftscouncilofindia.in/indian-crafts-map/"

# --- State and UT slugs based on the user-provided image and corrections ---
state_slugs_from_image = [
    "andhra-pradesh", "arunachal-pradesh", "assam", "bihar", "chhattisgarh",
    "goa", "gujarat", "haryana", "himachal-pradesh", "jammu-kashmir",
    "jharkhand", "karnataka", "kerala", "madhya-pradesh", "maharashtra",
    "manipur", "meghalaya", "mizoram", "nagaland", "orissa",
    "punjab", "rajasthan", "sikkim", "tamil-nadu", "tripura",
    "uttarakhand-formerly-uttaranchal", # Corrected slug for Uttarakhand
    "uttar-pradesh", "west-bengal"
]
ut_slugs_from_image = [
    "chandigarh", "dadar-nagar-haveli",
    "daman-diu",
    "delhi", "pondicherry"
]

locations = state_slugs_from_image + ut_slugs_from_image
# locations = ["mizoram", "sikkim", "uttarakhand-formerly-uttaranchal"] # For targeted testing

all_crafts_data = []

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

for location_slug in locations:
    current_url = base_url + location_slug + "/"
    page_number = 1

    while current_url:
        print(f"Scraping page {page_number} for {location_slug}: {current_url}")
        try:
            response = requests.get(current_url, headers=headers, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            data_table = None
            all_tables = soup.find_all('table')
            if not all_tables:
                print(f"No tables found on {current_url} for {location_slug}.")
            
            for table_idx, table_candidate in enumerate(all_tables):
                header_row = table_candidate.find('tr') # Assuming first row could be header
                if header_row:
                    # Get text from all cells (th or td) in this potential header row
                    header_texts = [cell.get_text(strip=True).upper() for cell in header_row.find_all(['th', 'td'])]
                    
                    # --- DEBUG PRINT for problematic locations ---
                    if location_slug in ["mizoram", "sikkim"] and data_table is None: # Only print if table not yet found
                        print(f"DEBUG: For {location_slug}, table candidate {table_idx}, found potential headers: {header_texts}")

                    # Check if all expected header components are present
                    # Making the "VILLAGE/SUB DISTRICT" check slightly more robust to variations like "VILLAGE / SUB DISTRICT"
                    # by checking for key components.
                    has_district = "DISTRICT" in header_texts
                    has_craft = "CRAFT" in header_texts
                    # Check for "VILLAGE" and "SUB" and "DISTRICT" for the third column header
                    has_village_sub_district = any(
                        ("VILLAGE" in h and "SUB" in h and "DISTRICT" in h) or h == "VILLAGE/SUB DISTRICT"
                        for h in header_texts
                    )
                    
                    if has_district and has_craft and has_village_sub_district:
                        # Ensure these keywords are likely in separate columns for a basic sanity check
                        # This is a heuristic: if all three keywords appear in the *same* header cell text, it's probably not the right layout.
                        # A better check would be to find the indices of these headers.
                        # For now, we assume if they are all present in the list of header texts, it's good.
                        
                        # Let's try to find the specific "VILLAGE/SUB DISTRICT" string as per image.
                        # The original check was "VILLAGE/SUB DISTRICT" in header_texts.
                        # The images show "Village/Sub District", which uppercased is "VILLAGE/SUB DISTRICT".
                        if "VILLAGE/SUB DISTRICT" in header_texts:
                             data_table = table_candidate
                             print(f"Found a matching table for {location_slug} (idx {table_idx}) based on exact headers.")
                             break
                        elif has_village_sub_district: # Fallback if the exact string with slash isn't found but components are
                             data_table = table_candidate
                             print(f"Found a matching table for {location_slug} (idx {table_idx}) based on flexible 'Village/Sub District' header components.")
                             break
            
            if data_table:
                table_body = data_table.find('tbody') if data_table.find('tbody') else data_table
                rows = table_body.find_all('tr')

                header_is_first_row_of_body = False
                if rows: # Check if the first row of the (selected or full) table is actually a header
                    first_row_cells = rows[0].find_all(['th', 'td'])
                    first_row_texts = [cell.get_text(strip=True).upper() for cell in first_row_cells]
                    if "DISTRICT" in first_row_texts and "CRAFT" in first_row_texts and \
                       ("VILLAGE/SUB DISTRICT" in first_row_texts or any(("VILLAGE" in h and "SUB" in h and "DISTRICT" in h) for h in first_row_texts)):
                        # print(f"Identified first data row as header for {location_slug}, skipping it.")
                        rows = rows[1:]
                        header_is_first_row_of_body = True


                if not rows:
                    print(f"No data rows found in the identified table on {current_url} for {location_slug} (after potential header skip).")

                for i, row in enumerate(rows):
                    cols = row.find_all('td')
                    if len(cols) == 3:
                        district = cols[0].get_text(strip=True)
                        craft = cols[1].get_text(strip=True)
                        village = cols[2].get_text(strip=True)
                        
                        if not village.strip(): 
                            village = district

                        if not district and not craft and not village and not (district == village): # if all are empty, or only district copied to village is there
                            if not district and not craft : # if original district and craft were empty
                                print(f"Skipping perceived empty row for {location_slug} - D:'{district}' C:'{craft}' V:'{village}'")
                                continue

                        all_crafts_data.append({
                            "State/UT": location_slug.replace('-', ' ').title(),
                            "District": district,
                            "Craft": craft,
                            "Village/Sub District": village
                        })
                    elif cols: # If there are data cells but not 3
                        # print(f"Row with {len(cols)} cells (expected 3) in {location_slug} page {page_number}: {[c.get_text(strip=True) for c in cols]}. Skipping.")
                        pass
            else:
                print(f"Data table with expected headers not found on {current_url} for {location_slug}.")

            # --- Pagination Logic ---
            next_page_tag = None
            # Try to find Avia pagination first as seen in previous logs (?avia-element-paging=2)
            avia_paging_links = soup.select('a.avia-button.avia- τότε-button') # This selector might need adjustment
            # More specific: links that contain '?avia-element-paging='
            avia_page_links = soup.find_all('a', href=lambda href: href and '?avia-element-paging=' in href)
            
            current_page_num_from_url = page_number # Default to current page_number
            if '?avia-element-paging=' in current_url:
                try:
                    current_page_num_from_url = int(current_url.split('?avia-element-paging=')[-1])
                except ValueError:
                    pass
            
            highest_avia_page_found = 0
            potential_next_avia_link = None

            for avia_link in avia_page_links:
                try:
                    page_val_str = avia_link['href'].split('?avia-element-paging=')[-1]
                    page_val = int(page_val_str)
                    if page_val > current_page_num_from_url: # Found a link to a higher page number
                        if potential_next_avia_link is None or page_val < highest_avia_page_found : # find the smallest next page
                             potential_next_avia_link = avia_link['href']
                             highest_avia_page_found = page_val # this logic is a bit off for finding *next* page.

                except (ValueError, KeyError):
                    continue
            
            # Corrected logic for finding the immediate next Avia page link
            next_avia_page_num_expected = current_page_num_from_url + 1
            found_specific_next_avia = None
            for avia_link in avia_page_links:
                 href_val = avia_link.get('href')
                 if href_val and f'?avia-element-paging={next_avia_page_num_expected}' in href_val:
                     found_specific_next_avia = href_val
                     break
            
            if found_specific_next_avia:
                next_page_tag_href = found_specific_next_avia
            elif potential_next_avia_link and highest_avia_page_found > current_page_num_from_url : # Fallback if direct next not found but higher pages exist
                # This fallback is tricky, as direct next is better. The above specific check is preferred.
                # For now, if specific next is not found, we'll rely on other methods.
                # next_page_tag_href = potential_next_avia_link
                pass


            if found_specific_next_avia:
                 next_page_tag = {'href': found_specific_next_avia} # Create a mock tag for simplicity
            else: # Fallback to general pagination link finding if Avia specific not found or no more Avia pages
                current_page_span = soup.find('span', class_='page-numbers current')
                if current_page_span:
                    next_sibling = current_page_span.find_next_sibling('a', class_='page-numbers')
                    if next_sibling and next_sibling.has_attr('href'):
                        next_page_tag = next_sibling
                
                if not next_page_tag:
                    possible_next_links = soup.find_all('a', string=re.compile(r'Next|»|>', re.IGNORECASE))
                    if not possible_next_links:
                        possible_next_links = soup.select('a.next, a.pagination-next, a.next_page, a[rel="next"], .nav-next a, .pagination .next a')

                    for link_tag_candidate in possible_next_links:
                        if link_tag_candidate.has_attr('href'):
                            href_val = link_tag_candidate['href'].strip()
                            if href_val and href_val != "#" and not href_val.lower().startswith('javascript:'):
                                next_page_tag = link_tag_candidate
                                break
            
            if next_page_tag and next_page_tag.get('href'): # Use .get('href') for the mock tag too
                next_href = next_page_tag.get('href').strip()
                if next_href and next_href != "#" and not (hasattr(next_page_tag, 'get') and next_page_tag.get('disabled')) and not next_href.lower().startswith('javascript:'): # check original tag for disabled
                    new_potential_url = urljoin(current_url, next_href)
                    if new_potential_url == current_url or new_potential_url == response.url:
                        current_url = None
                    else:
                        current_url = new_potential_url
                        page_number += 1
                else:
                    current_url = None
            else:
                current_url = None

        except requests.exceptions.RequestException as e:
            print(f"Error fetching {current_url if current_url else base_url + location_slug + '/'}: {e}")
            current_url = None
        
        time.sleep(1.5)

df = pd.DataFrame(all_crafts_data)

if not df.empty:
    print("\n--- Sample of Scraped Data ---")
    print(df.head())
    print(f"\nTotal records scraped: {len(df)}")
    try:
        df.to_csv("indian_crafts_data_v4.csv", index=False, encoding='utf-8-sig')
        print("Data saved to indian_crafts_data_v4.csv")
    except Exception as e:
        print(f"Error saving to CSV: {e}")
else:
    print("\nNo data was scraped. The DataFrame is empty.")
    print("Please verify issues for any locations reporting errors.")

