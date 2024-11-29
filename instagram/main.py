import json
import re

def extract_instagram_usernames(input_file, usernames_file):
    # Load the JSON data from the input file
    with open(input_file, 'r', encoding='utf-8') as f:
        clubs = json.load(f)
    
    # Extract usernames
    usernames = []
    pattern = r'instagram\.com/([^/?]+)'
    
    for club in clubs:
        instagram_url = club['detailed_info']['social_media_links'].get('Instagram')
        if instagram_url and instagram_url != "NA":
            match = re.search(pattern, instagram_url)
            if match:
                username = match.group(1)
                usernames.append(username)
    
    # Write usernames to text file
    with open(usernames_file, 'w', encoding='utf-8') as f:
        for username in usernames:
            f.write(f"{username}\n")
    
    print(f"Extracted {len(usernames)} usernames to {usernames_file}")

# Run the function
if __name__ == "__main__":
    extract_instagram_usernames('All_UofT_club_info.json', 'instagram_usernames.txt')
    