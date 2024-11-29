import os
from pathlib import Path
import yaml
from level1_scraper import scrape_urls
from level2_scraper import perform_level2_scraping
from dotenv import load_dotenv
import json
import time

load_dotenv()

def load_config(config_file):
    """Load configuration from YAML file"""
    try:
        with open(config_file, 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Error loading config file: {str(e)}")
        return None

def load_urls(url_file):
    """Load URLs from specified file"""
    try:
        with open(url_file, 'r') as f:
            return yaml.safe_load(f).get('urls', [])
    except Exception as e:
        print(f"Error loading URL file: {str(e)}")
        return None

def load_level3_data(file_path):
    """Load existing Level 1 data for Level 3 processing"""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            if isinstance(data, dict):
                # Return the data structure as is
                return data
            elif isinstance(data, list):
                # If it's a list, wrap it in a standard structure
                return {
                    "source_url": file_path,  # Use file path as source
                    "items": data  # Keep the original list of items
                }
            else:
                print(f"Unexpected data format in {file_path}")
                return None
    except Exception as e:
        print(f"Error loading Level 3 data: {str(e)}")
        return None

def process_single_url(url, config, level1_dir, level2_dir=None):
    """Process a single URL through level 1 and optionally level 2 scraping"""
    print(f"\n=== Processing URL: {url} ===")
    
    # Level 1 Scraping
    if config['level'] in [1, 2]:
        print("Starting Level 1 Scraping...")
        level1_result = scrape_urls([url], level1_dir, config['level1_query'])
        
        if not level1_result:
            print(f"No Level 1 results for {url}")
            return None
        
        # If only level 1, we're done
        if config['level'] == 1:
            return level1_result[0]
    
    # Level 2 Scraping (for both level 2 and 3)
    if level2_dir and config.get('level2_prompt'):
        # import ipdb; ipdb.set_trace()
        print("Starting Level 2 Scraping...")
        try:
            if config['level'] == 2:
                # Use Level 1 results for Level 2
                level2_result = perform_level2_scraping(
                    level1_result[0], 
                    config['level2_prompt'], 
                    level2_dir
                )
            else:  # Level 3
                # Direct Level 2 processing
                # load in the data for level 3:
                level3_data = load_level3_data(config['file_with_linksLvl3'])
                level2_result = perform_level2_scraping(
                    level3_data, 
                    config['level2_prompt'], 
                    level2_dir
                )
            return level2_result
        except Exception as e:
            print(f"Error in Level 2 scraping for {url}: {str(e)}")
            return None
    
    return None

def main(config_file='config.yml'):
    # Load configuration
    config = load_config(config_file)
    if not config:
        return
    
    # Validate configuration based on level
    if config['level'] in [1]:
        required_fields = ['level', 'url_file', 'level1_query']
    elif config['level'] in [2]:
        required_fields = ['level', 'url_file', 'level1_query', 'level2_prompt']
    else:  # Level 3
        required_fields = ['level', 'file_with_linksLvl3', 'level2_prompt']
    
    if not all(field in config for field in required_fields):
        print("Missing required fields in config file")
        return
    
    # Create data directories
    LEVEL1_DATA_DIR = "level_1_data"
    LEVEL2_DATA_DIR = "level_2_data" if config['level'] in [2, 3] else None
    FINAL_DATA_DIR = "Final_Processed_Data"
    
    # Create all necessary directories
    Path(LEVEL1_DATA_DIR).mkdir(parents=True, exist_ok=True)
    if LEVEL2_DATA_DIR:
        Path(LEVEL2_DATA_DIR).mkdir(parents=True, exist_ok=True)
    Path(FINAL_DATA_DIR).mkdir(parents=True, exist_ok=True)
    
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    
    # Load URLs based on level
    if config['level'] in [1, 2]:
        urls = load_urls(config['url_file'])
        
        # Process each URL independently for Level 1 and 2
        results = []
        for url in urls:
            start_time_url = time.time()  # Start timing this URL
            print(f"\n=== Processing URL: {url} ===")
            try:
                result = process_single_url(
                    url, 
                    config, 
                    LEVEL1_DATA_DIR, 
                    LEVEL2_DATA_DIR
                )
                time_taken = time.time() - start_time_url  # Calculate time taken
                
                if result:
                    results.append(result)
                    print(f"Successfully processed {url} (Time taken: {round(time_taken, 2)} seconds)")
                else:
                    print(f"Failed to process {url} (Time taken: {round(time_taken, 2)} seconds)")
            except Exception as e:
                time_taken = time.time() - start_time_url
                print(f"Error processing {url}: {str(e)} (Time taken: {round(time_taken, 2)} seconds)")
                continue
        
        # Save final results for Level 1/2
        if results:
            final_filename = f"level{config['level']}_final_results_{timestamp}.json"
            final_filepath = Path(FINAL_DATA_DIR) / final_filename
            with open(final_filepath, 'w', encoding='utf-8') as f:
                json.dump({
                    "level": config['level'],
                    "total_processed": len(results),
                    "timestamp": timestamp,
                    "results": results
                }, f, indent=2, ensure_ascii=False)
            print(f"\nFinal results saved to: {final_filepath}")
        
        print(f"\nScraping completed! Processed {len(results)} out of {len(urls)} URLs")
        
    else:  # Level 3
        # For Level 3, process everything in one go
        try:
            result = process_single_url(
                config['file_with_linksLvl3'],  # Pass the file path
                config, 
                LEVEL1_DATA_DIR, 
                LEVEL2_DATA_DIR
            )
            if result:
                # Save final results for Level 3
                final_filename = f"level3_final_results_{timestamp}.json"
                final_filepath = Path(FINAL_DATA_DIR) / final_filename
                with open(final_filepath, 'w', encoding='utf-8') as f:
                    json.dump({
                        "level": 3,
                        "source_file": config['file_with_linksLvl3'],
                        "timestamp": timestamp,
                        "results": result
                    }, f, indent=2, ensure_ascii=False)
                print(f"\nFinal results saved to: {final_filepath}")
                print("Successfully processed Level 3 data")
            else:
                print("Failed to process Level 3 data")
        except Exception as e:
            print(f"Error processing Level 3 data: {str(e)}")

if __name__ == "__main__":
    if not os.getenv('AGENTQL_API_KEY'):
        print("Error: AGENTQL_API_KEY not found in .env file")
    if not os.getenv('OPENAI_API_KEY'):
        print("Error: OPENAI_API_KEY not found in .env file")
    else:
        import argparse
        parser = argparse.ArgumentParser(description='Web scraping script')
        parser.add_argument('--config', default='config.yml', help='Path to configuration file')
        args = parser.parse_args()
        main(args.config)