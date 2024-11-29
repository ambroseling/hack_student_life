import os
import time
import json
import yaml
from pathlib import Path
from backend.level1_scraper import scrape_urls
from backend.level2_scraper import perform_level2_scraping
from flask import Flask, request,jsonify, send_from_directory
from backend.models import Events
from backend import create_app,db
from typing import List
import openai
application = create_app()
from flask import request  # Make sure to import request
from datetime import datetime
import dateparser

@application.after_request
def apply_cors(response):
    origin = request.headers.get('Origin')
    allowed_origins = [
        "http://localhost:8000",
        "http://localhost:3000",
        "http://localhost:5000",
        f"{os.getenv('AWS_URL')}"
    ]
    
    # Check if the origin is in our allowed list
    if origin in allowed_origins:
        # Set the specific origin that made the request
        response.headers["Access-Control-Allow-Origin"] = origin
    else:
        # For development, you might want to allow all origins (not recommended for production)
        response.headers["Access-Control-Allow-Origin"] = "*"
    
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response

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

def load_config(config_file):
    """Load configuration from YAML file"""
    try:
        with open(config_file, 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        raise Exception(f"Error loading config file: {str(e)}")


def process_urls(config):
    """Process URLs and store events in database"""
    results = []
    
    # Create data directories
    LEVEL1_DATA_DIR = "level_1_data"
    LEVEL2_DATA_DIR = "level_2_data" if config['level'] in [2, 3] else None
    Path(LEVEL1_DATA_DIR).mkdir(parents=True, exist_ok=True)
    if LEVEL2_DATA_DIR:
        Path(LEVEL2_DATA_DIR).mkdir(parents=True, exist_ok=True)

    if config['level'] in [1, 2]:
        urls = config.get('urls', [])
        for url in urls:
            try:
                # Perform scraping
                result = process_single_url(
                    url, 
                    config, 
                    LEVEL1_DATA_DIR, 
                    LEVEL2_DATA_DIR
                )
                
                if result:
                    # Store events in database
                    store_events(result)
                    results.append({
                        "url": url,
                        "status": "success",
                        "data": result
                    })
                    
            except Exception as e:
                results.append({
                    "url": url,
                    "status": "error",
                    "error": str(e)
                })
                
    return results

def store_events(scrape_result):
    """Store scraped events in database, avoiding duplicates"""
    events_data = scrape_result.get('events', [])
    
    for event_data in events_data:
        try:
            # Check for existing event with same title and date
            existing_event = Events.query.filter_by(
                title=event_data.get('Name', ''),
                date=event_data.get('Date'),
                location=event_data.get('Location', '')
            ).first()
            
            # Skip if event already exists
            if existing_event:
                print(f"Skipping duplicate event: {event_data.get('Name', '')}")
                continue
            
            # Create new Event object if no duplicate found
            event = Events(
                title=event_data.get('Name', ''),
                source_url=event_data.get('URL', ''),
                description=event_data.get('Description', ''),
                date=event_data.get('Date'),
                location=event_data.get('Location', ''),
                # Add other fields as needed
            )
            
            # Add to database
            db.session.add(event)
            
        except Exception as e:
            print(f"Error storing event: {str(e)}")
            continue
            
    # Commit all events
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Error committing events to database: {str(e)}")

def parse_date(date_string):
    """Parse various date formats to datetime object"""
    if not date_string:
        return None
        
    try:
        # Handle the specific format from your JSON: "November 30, 2024 8:00pm - 10:00pm"
        # Split on '-' and take the first part to get start time only
        start_time = date_string.split('-')[0].strip()
        return dateparser.parse(start_time, settings={
            'PREFER_DATES_FROM': 'future',
            'TIMEZONE': 'UTC',
            'RETURN_AS_TIMEZONE_AWARE': False
        })
    except Exception as e:
        print(f"Error parsing date '{date_string}': {str(e)}")
        return None

def parse_time(time_string):
    """Parse various time formats to datetime object"""
    if not time_string:
        return None
        
    try:
        openai.api_key = os.getenv('OPENAI_API_KEY')

        # Use GPT to parse and standardize the time format
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that parses dates and times. Return only the ISO format datetime. If it is a range, return the start time only."},
                {"role": "user", "content": f"Convert this time to ISO format (YYYY-MM-DD HH:MM:SS): {time_string}"}
            ],
            max_tokens=50,
            temperature=0.3
        )
        
        # Extract the parsed time from response
        parsed_time = response.choices[0].message.content.strip()
        
        # Convert to datetime object
        return datetime.strptime(parsed_time, '%Y-%m-%d %H:%M:%S')
        
    except Exception as e:
        print(f"Error parsing time '{time_string}' with GPT: {str(e)}")
        return None

    

def categorize_event(description: str, available_tags: List[str]) -> str:
    """
    Use OpenAI to categorize an event based on its description.
    
    Args:
        description (str): Event description
        available_tags (List[str]): List of possible tags to choose from
        
    Returns:
        str: The most appropriate tag from available_tags
    """
    try:
        # Ensure your API key is set
        openai.api_key = os.getenv('OPENAI_API_KEY')
        
        # Create the prompt
        prompt = f"""
        Given the following event description, choose the most appropriate categories (can be more than 1) from this list: {', '.join(available_tags)}
        
        Event description: {description}
        
        Return only the category names, separated by commas.
        """
        
        # Make API call
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that categorizes events. Respond only with the category name."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=50,
            temperature=0.3  # Lower temperature for more consistent results
        )
        
        # Extract the categories from response and convert to list
        suggested_tags = [
            tag.strip().lower() 
            for tag in response.choices[0].message.content.strip().split(',')
        ]
        
        # Validate each suggested tag is in our available tags
        valid_tags = [tag for tag in suggested_tags if tag in available_tags]
        
        # Return valid tags or default to ['other'] if none are valid
        return valid_tags if valid_tags else ['other']
            
    except Exception as e:
        print(f"Error categorizing event: {str(e)}")
        return 'other'  # Default fallback
    

@application.route('/api/delete-events', methods=['DELETE'])
def delete_events():
    """Delete all events from the database"""
    try:
        Events.query.delete()
        db.session.commit()
        return jsonify({"message": "All events deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@application.route('/api/import-events', methods=['GET'])
def import_events():
    """Import events from JSON file to database"""
    print("========================== CALLING IMPORT EVENTS ================================")

    try:
        # Read the JSON file
        with open('backend/events.json', 'r') as file:
            data = json.load(file)
        
        events_added = 0
        events_skipped = 0
        errors = []
        
        # Process each source
        for source in data:
            items = source.get('items', [])
            
            for item in items:
                detailed_info = item.get('detailed_info', {})
                date = detailed_info.get('date')
                
                # Handle date if it's a dictionary with start/end dates
                if isinstance(date, dict):
                    date = date.get('start')  # Use the start date for the event
                
                # Skip events without valid dates
                parsed_date = parse_time(date)

                # Check for existing event to avoid duplicates
                existing_event = Events.query.filter_by(
                    title=detailed_info.get('title', ''),
                    date=parsed_date,
                    location=detailed_info.get('location', '')
                ).first()
                
                if existing_event:
                    db.session.delete(existing_event)
                    db.session.commit()

                description = detailed_info.get('description', '')
                if len(description) > 200:
                    description = description[:200] + '...'
                # Create new event
                available_tags = ['music', 'general', 'sports', 'arts', 'academic', 'career', 'social', 'business','engineering','games','health','fitness','coding','other']
                try:
                    tags = categorize_event(description, available_tags)
                except Exception as e:
                    tags = []   

                try:
                    new_event = Events(
                        title=detailed_info.get('title', ''),
                        description=description,
                        date=parsed_date,
                        location=detailed_info.get('location', ''),
                        source_url=item.get('URL', ''),
                        tags=tags
                    )
                    
                    db.session.add(new_event)
                    events_added += 1
                    print(f"Added event '{detailed_info.get('title')}' with tags {tags} and time {parsed_date}")
                    # Commit in batches to avoid memory issues
                    if events_added % 100 == 0:
                        db.session.commit()
                except Exception as e:
                    errors.append(f"Error adding event '{detailed_info.get('title')}': {str(e)}")
                    continue
        
        # Final commit for remaining events
        db.session.commit()
        
        return jsonify({
            'success': True,
            'events_added': events_added,
            'events_skipped': events_skipped,
            'errors': errors,
            'message': f'Successfully imported {events_added} events ({events_skipped} duplicates skipped)'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to import events'
        }), 500

@application.route('/api/start_scraping', methods=['POST'])
def start_scraping():
    """
    Start scraping process with provided configuration
    Expected POST body: {
        "config_file": "path/to/config.yml"  // optional
        "urls": ["url1", "url2"],  // optional, override urls in config
        "level": 1,  // optional, default to 1
    }
    """
    try:
        data = request.get_json()
        config_file = data.get('config_file', 'config.yml')
        
        # Load and validate configuration
        config = load_config(config_file)
        if not config:
            return jsonify({"error": "Invalid configuration"}), 400
        # Override config with request data if provided
        if 'urls' in data:
            config['urls'] = data['urls']
        if 'level' in data:
            config['level'] = data['level']
            
        # Process URLs and store events
        results = process_urls(config)
        
        return jsonify({
            "message": "Scraping completed",
            "events_processed": len(results),
            "results": results
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500          



@application.route('/api/get-events', methods=['GET'])
def get_events():
    print("========================== CALLING GET EVENTS ================================")
    
    # Get search parameter from query string
    search_query = request.args.get('search', '')
    
    if search_query:
        # Use ts_vector for full-text search
        events = Events.query.filter(Events.ts_vector.match(search_query)).all()
    else:
        # If no search query, return all events
        events = Events.query.all()
    
    # Convert each event object to a dictionary
    events_list = [{
        'id': event.id,
        'title': event.title,
        'source_url': event.source_url,
        'description': event.description,
        'date': event.date,  
        'location': event.location,
        'tags': event.tags
    } for event in events]
    
    return jsonify(events_list)

@application.route("/api/events/<int:id>")
def get_event(id):
    event = Events.query.get(id)
    return jsonify(event)

@application.route("/api/create-events", methods=["POST"])
def create_events():
    data = request.json()
    new_event = Events(title=data["title"], description=data["description"], date=data["date"], location=data["location"], tags=data["tags"])
    db.session.add(new_event)
    db.session.commit()
    return jsonify(new_event)

@application.route('/api/scrape_website')
def scrape_website():
    return jsonify({"message": "Scraping website..."})


@application.route('/')
def serve_react_app():
    return send_from_directory('../frontend/hack_student_life_gui/build', 'index.html')

@application.route('/<path:path>')
def serve_static_files(path):
    return send_from_directory('../frontend/hack_student_life_gui/build', path)

if __name__ == "__main__":
    application.run(host='0.0.0.0', port=8000)