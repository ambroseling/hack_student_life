import json
from datetime import datetime, timedelta
import random

def generate_future_date():
    current_date = datetime.now()
    days_to_add = random.randint(1, 180)
    future_date = current_date + timedelta(days=days_to_add)
    return future_date.strftime('%Y-%m-%d')

def update_event_dates():
    # Read the JSON file
    with open('instagram-events-only.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # Update dates for all events
    for account in data:
        for event in data[account]:
            # Replace event_date with new future date
            if 'event_date' in event:
                event['date'] = generate_future_date()
                del event['event_date']
            elif 'date' in event:
                event['date'] = generate_future_date()
    
    # Save updated data
    with open('UPDATED_instagram-events-updated.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    update_event_dates()
    print("Dates updated successfully!")