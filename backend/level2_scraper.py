from scrapegraphai.graphs import SmartScraperGraph
import json
import time
from pathlib import Path
import os


def perform_level2_scraping(level1_data, level2_prompt, output_dir):
    """
    Perform Level 2 scraping based on Level 1 results
    
    Args:
        level1_data: Dictionary containing Level 1 results with 'events' list
        level2_prompt: Prompt for Level 2 scraping
        output_dir: Directory to save results
    """
    print("\n=== Starting Level 2 Scraping ===")
    
    # Configure the scraper
    graph_config = {
        "llm": {
            "api_key": os.getenv('OPENAI_API_KEY'),
            "model": "openai/gpt-4o-mini",
            "temperature": 0,
            "streaming": True
        },
        "headless": True,
        "verbose": True
    }
    # import ipdb; ipdb.set_trace()
    # Extract items dynamically from level1_data
    keys = list(level1_data.keys())
    if len(keys) < 2:
        print("Invalid Level 1 data structure: missing items key")
        print(f"these are the keys: {keys}")
        return None
        
    items_key = keys[1]  # Get the second key (first is usually 'source_url')
    items = level1_data.get(items_key, [])
    
    source_url = level1_data.get('source_url', '')
    
    if not items:
        print(f"No items found in Level 1 data under '{items_key}' key")
        return None
    
    all_results = []
    total_items = len(items)
    
    print(f"\nProcessing {total_items} items from {source_url}...")
    
    for index, item in enumerate(items, 1):
        item_url = item.get('URL', '')  # Note: Using 'URL' with capital letters
        item_name = item.get('Name', f'Item {index}')  # Note: Using 'Name' with capital letter
        
        if not item_url:
            print(f"Skipping {item_name}: No URL found")
            continue
            
        print(f"\n[{index}/{total_items}] Processing: {item_name}")
        print(f"URL: {item_url}")
        
        try:
            # Create scraper for this item
            level2_scraper = SmartScraperGraph(
                prompt=level2_prompt,
                source=item_url,
                config=graph_config
            )
            
            # Get detailed information
            detailed_info = level2_scraper.run()
            
            # Combine Level 1 and Level 2 data
            combined_result = {
                "Name": item_name,  # Keep original Name
                "URL": item_url,    # Keep original URL
                "detailed_info": detailed_info  # Add detailed info from Level 2
            }
            
            all_results.append(combined_result)
            
            # Save progress periodically
            if index % 10 == 0:
                save_progress(all_results, index, output_dir)
                
            # Small delay between requests
            time.sleep(2)
            
        except Exception as e:
            print(f"Error processing {item_name}: {str(e)}")
            continue
    
    # Save final results
    final_result = save_final_results(all_results, source_url, output_dir)
    return final_result

def save_progress(results, count, output_dir):
    """Save intermediate results"""
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"saving_progress_{count}_{timestamp}.json"
    filepath = Path(output_dir) / filename
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(results, indent=2, ensure_ascii=False, fp=f)
    
    print(f"\nProgress saved to: {filepath}")

def save_final_results(results, source_url, output_dir):
    """Save final combined results"""
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    source_identifier = Path(source_url).stem
    filename = f"level2_final_{source_identifier}_{timestamp}.json"
    filepath = Path(output_dir) / filename
    
    final_result = {
        "source_url": source_url,
        "total_items": len(results),
        "items": results
    }
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(final_result, indent=2, ensure_ascii=False, fp=f)
    
    print(f"\nFinal results saved to: {filepath}")
    return final_result

# Remove the main() function since it's now integrated with main.py