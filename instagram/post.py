from apify_client import ApifyClient
from dotenv import load_dotenv
import os
import json
from datetime import datetime
import time

def get_instagram_posts(username_list, results_limit=3):
    # Load environment variables
    load_dotenv()
    
    # Initialize the ApifyClient with API token from .env
    client = ApifyClient(os.getenv('APIFY_API_KEY'))
    
    accounts_data = {}  # Dictionary to store all accounts and their posts
    for username in username_list:
        start_time_account = time.time()
        # Prepare the Actor input
        run_input = {
            "username": [username.strip()],
            "resultsLimit": results_limit,
        }
        
        # Run the Actor and wait for it to finish
        run = client.actor("nH2AHrwxeTRJoN5hX").call(run_input=run_input)
        
        # Fetch posts for this account
        posts = list(client.dataset(run["defaultDatasetId"]).iterate_items())
        
        # Store in dictionary with account as key and posts in a nested dictionary
        accounts_data[username] = {
            "posts": posts
        }
        elapsed_time = time.time() - start_time_account
        print(f"Processed account: {username} (took {elapsed_time:.2f} seconds)")
    
    return accounts_data

def read_accounts_from_file(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file if line.strip()]

def save_to_json(data, filename):
    # Create a timestamp for the filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'instagram_data_{timestamp}.json'
    
    # Save the data to a JSON file
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"Data saved to {filename}")

def main():
    start_time = time.time()
    
    accounts_file = "instagram_accounts.txt"
    accounts = read_accounts_from_file(accounts_file)
    accounts_data = get_instagram_posts(accounts)
    results = {}
    
    # Process and print results
    for account, data in accounts_data.items():
        print(f"\nAccount: {account}")
        print(f"Number of posts: {len(data['posts'])}")
        results[account] = data['posts']
    
    # Save results to JSON file
    save_to_json(results, 'instagram_data.json')
    
    # Calculate and print total execution time
    total_time = time.time() - start_time
    minutes = int(total_time // 60)
    seconds = total_time % 60
    print(f"\nTotal execution time: {minutes} minutes and {seconds:.2f} seconds")
    
    print(f"These are the results: ")
    import ipdb; ipdb.set_trace();
    print(results)

if __name__ == "__main__":
    main()

    