import agentql
from playwright.sync_api import sync_playwright
import json
import time
import os
from pathlib import Path
from dotenv import load_dotenv
import math

def scrape_urls(urls, output_dir="level_1_data", level1_query=None):
    """
    Scrape multiple URLs and save results to specified directory
    """
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    all_results = []
    for url in urls:
        try:
            result = perform_level1_scraping(url, output_dir, level1_query)
            if result:
                all_results.append(result)
        except Exception as e:
            print(f"Error processing {url}: {str(e)}")
            continue
    
    return all_results

def perform_level1_scraping(url, output_dir, level1_query):
    """Process a single URL"""
    print(f"\n=== Starting Level 1 Scraping for {url} ===")
    
    agentql.configure(api_key=os.getenv('AGENTQL_API_KEY'))
    
    PAGINATION_QUERY = """
    {
        pagination_controls {
            next_page_button(button or link with text containing "Next" or "→" or number for next page. Dont click Calendar buttons)
        }
    }
    """
    
    all_items = []
    page_number = 1
    collection_key = None
    
    try:
        with sync_playwright() as p:
            # if you want to see the browser, set headless=False
            browser = p.chromium.launch(headless=True)
            page = agentql.wrap(browser.new_page())
            
            print(f"\nNavigating to: {url}")
            page.goto(url)
            page.wait_for_page_ready_state()
            
            # First, check for pagination
            pagination = page.query_elements(PAGINATION_QUERY)
            has_pagination = bool(pagination and pagination.pagination_controls.next_page_button)
            
            if has_pagination:
                print("Detected pagination controls - using page navigation")
                previous_page_data = None  # Store previous page data
                
                while True:
                    page.wait_for_page_ready_state()
                    page.wait_for_timeout(2000)
                    
                    print(f"\nExtracting items from page {page_number}...")
                    results = page.query_data(level1_query)
                    
                    if results and len(results.keys()) > 0:
                        # Get collection key if we haven't already
                        if not collection_key:
                            collection_key = list(results.keys())[0]
                        current_page_items = results[collection_key]
                        
                        # Check if current page data is same as previous page
                        if previous_page_data == current_page_items:
                            print("Detected pagination loop - same data as previous page")
                            break
                            
                        previous_page_data = current_page_items  # Store current page data
                        all_items.extend(current_page_items)
                        print(f"Found {len(current_page_items)} items on page {page_number}")
                    
                    pagination = page.query_elements(PAGINATION_QUERY)
                    if not pagination or not pagination.pagination_controls.next_page_button:
                        print("\nNo more pages available")
                        break
                    
                    print(f"Moving to page {page_number + 1}...")
                    try:
                        pagination.pagination_controls.next_page_button.click()
                    except Exception as e:
                        print(f"Failed to click 'Next' button: {str(e)}")
                        break
                    page.wait_for_timeout(2000)
                    page_number += 1
            else:
                print("No pagination detected - using infinite scroll")
                # import ipdb; ipdb.set_trace()
                # First phase: Scroll through entire page
                print("\nScrolling through entire page...")
                handle_infinite_scroll(page)
                
                # Second phase: Extract all data at once
                print("\nExtracting all items...")
                results = page.query_data(level1_query)
                if results and len(results.keys()) > 0:
                    collection_key = list(results.keys())[0]
                    all_items = results[collection_key]
                    print(f"Found {len(all_items)} items in total")
            
            browser.close()
            
            # Save results
            result = {
                "source_url": url,
                collection_key: all_items
            }
            save_results(result, url, output_dir)
            return result
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

def save_results(results, url, output_dir):
    """Save the scraped results to a JSON file in the specified directory"""
    # Create a safe filename by replacing invalid characters
    safe_url = url.replace('https://', '').replace('http://', '')
    safe_url = safe_url.replace('?', '_').replace('=', '_').replace('&', '_').replace('/', '_')
    filename = f"events_{time.strftime('%Y%m%d_%H%M%S')}_{safe_url}.json"
    filepath = os.path.join(output_dir, filename)
    
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(results, indent=2, ensure_ascii=False, fp=f)
        
        print(f"\nResults saved to: {filepath}")
        print(f"Found total {len(results.get('events', []))} events")
    except Exception as e:
        print(f"Error saving results: {str(e)}")

def handle_infinite_scroll(page):
    """Handle infinite scroll pages by simulating continuous scrolling and button checks"""
    while True:
        viewport_height = page.evaluate("window.innerHeight")
        last_height = page.evaluate("document.body.scrollHeight")
        
        # Scroll down
        print("Scrolling down...")
        page.mouse.wheel(delta_x=0, delta_y=10 * viewport_height)
        page.wait_for_timeout(1000)
        
        # Check if we've reached the bottom
        new_height = page.evaluate("document.body.scrollHeight")
        if new_height == last_height:
            print("Reached the bottom of the page, checking for 'Load More' button...")
            
            # Try to find and click load more button
            load_more_query = """
            {
                load_more_button(button or element with text "Load More" or "Show More")
            }
            """
            button = page.query_elements(load_more_query)
            
            if button and button.load_more_button:
                print("Found 'Load More' button, attempting to click...")
                try:
                    button.load_more_button.click()
                    page.wait_for_timeout(1000)
                    
                    # Check if clicking actually loaded more content
                    after_click_height = page.evaluate("document.body.scrollHeight")
                    if after_click_height == new_height:
                        print("No new content loaded after clicking button. Scrolling complete.")
                        return
                    print("Successfully loaded more content, continuing to scroll...")
                except Exception as e:
                    print(f"Failed to click 'Load More' button: {str(e)}")
                    return
            else:
                print("No 'Load More' button found. Scrolling complete.")
                return

def find_pagination_buttons(page):
    """Find pagination buttons while excluding calendar elements"""
    # First check if there's a calendar on the page
    calendar_check = page.query_selector('div[class*="calendar"], table[class*="calendar"]')
    
    if calendar_check:
        # If calendar exists, use a more specific selector that excludes the calendar area
        pagination_query = """
        {
            pagination_number(
                button:has-text(/^[0-9]+$/) >> 
                :not(:has-ancestor(div[class*="calendar"], table[class*="calendar"]))
            )
        }
        """
    else:
        # If no calendar, use simple number button selector
        pagination_query = """
        {
            pagination_number(button:has-text(/^[0-9]+$/))
        }
        """
    
    return page.query_elements(pagination_query)