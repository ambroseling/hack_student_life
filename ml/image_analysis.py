from openai import OpenAI
from dotenv import load_dotenv
import os
import boto3
import requests
import json
# ec2 = boto3.client('ec2', 
#     region_name='us-east-2',
#     aws_access_key_id='ASIA2NK3X7FNVGUBM6CX',
#     aws_secret_access_key='cPIR8mLbhhiY7M/WelpBmnt+YMJetOvsO3AIFgMa'
# )
# Load environment variables from the .env file
load_dotenv()

# Get the API key from the environment
api_key = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI client correctly
client = OpenAI(api_key=api_key)

# Initialize Rekognition client (not EC2)
rekognition = boto3.client('rekognition',
    region_name='us-west-2',  # Make sure this matches your intended region
    aws_access_key_id='ASIA2NK3X7FNW5UD7MQA',
    aws_secret_access_key='+gp6p2r5C05u8pnTpuBu+0wyeQCdRqj/Y22IAmb3',
    aws_session_token='IQoJb3JpZ2luX2VjENL//////////wEaCXVzLWVhc3QtMiJIMEYCIQDHlFZ34i8t1Ov6EFy1CaK8HFMu56hNl+Bzcr7UYtC/hgIhAPlF4ALLwdRamqePUJWeGDpDw4B1kQNavccoJ0sAuTICKvICCHsQABoMNzE1ODQxMzM3NjkxIgxQZd3O8cxyFArUkfEqzwIoU12EE1V3WyuXCqxShe98e5hdKrA9b8eQFykSY1J0oZpxmkNW/Wb7FzLEBe1BM9Bpg7iKjOMIj0KdocAMQ97qmDXevTDP7uIgRmC18YXHPEjSQge3saYm+H4b5hQ2wAzQai2C/K67qklExCCA8LoyTy4pv4SHmtXv+sTDbaLDWcnO/oNMrIvZ9qGdKoGdqMkQYqyMdQsar9uTZOLttXYXNcrzxiEkpA00cMYcKOOAsFhdBymbxx02H8Y+jW1kv4bYsJPSDfCGTb6ahWXDa4xy9oWP58NgvwaZGq0DKln01kYt+NiBjf+EBQB12gqTyA8R16yn2VuaOwpI9uWpFDXeMItWVRfj5wC410FCbG9T1LEkM73AkLXkhrRNIpp5PiE08RmIu0LNekmsTfqd2ul4Wc3Hqs4glwPLkmmu+840wMGoESUt7X6j79kB/AOhQDDlgai6BjqmAWK00g95TziBSbSdqJiEQUXEXhw3p8szCSgHQp21MLKpuN29csuKiQ+yuH1Rd6ATXUrqGd8TE6kPLa+Jyiamx9YZizxDCpSUWgQIXMIU9wQumqU4U+u1vMAO2cSpsyZc3nnPA7xm1L5KDOHPRw4tRGVJvly+5YwUTisGD9BAq39OzDOAuOEI+Y6mRWjOTnXne+7DtnwnwEZTL3T5vfCCLpUJfRH6vBo='
)

# Open and read the JSON file
with open('all_insta_data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

available_tags = ['music', 'general', 'sports', 'arts', 'academic', 'career', 'social', 
                 'business', 'engineering', 'games', 'health', 'fitness', 'coding', 'other']

processed_data = {}  # New dictionary for filtered results

for account in data:
    print(f"\n=== Processing account: {account} ===")
    processed_data[account] = []
    
    for post in data[account]:
        print("\n--- Processing new post ---")
        url = post.get('displayUrl')
        
        if not url:
            print("Skipping post - Missing URL")
            continue
            
        caption = post.get('caption', '')
        print(f"Caption found: {caption[:100]}...")  # Print first 100 chars of caption

        try:
            print("Fetching image...")
            response = requests.get(url)
            image_bytes = response.content
            print("Image fetched successfully")

            print("Detecting text in image...")
            text_response = rekognition.detect_text(
                Image={'Bytes': image_bytes}
            )

            detected_text = []
            for text_detection in text_response['TextDetections']:
                detected_text.append(text_detection['DetectedText'])
            
            print(f"Detected text: {' '.join(detected_text)[:100]}...")  # Print first 100 chars
            combined_text = f"Image text: {' '.join(detected_text)}\nCaption: {caption}"

            print("Checking if post is an event...")
            event_classification = client.chat.completions.create(
                model="gpt-4o-mini",  # Changed to correct model name
                messages=[
                    {"role": "system", "content": "Analyze the following text and determine if it's advertising an event. Respond with only 'yes' or 'no'."},
                    {"role": "user", "content": combined_text}
                ]
            )

            event_response = event_classification.choices[0].message.content.lower().strip()
            print(f"Event classification response: {event_response}")
            is_event = event_response == 'yes'

            if is_event:
                print("Post classified as event, extracting details...")
                event_analysis = client.chat.completions.create(
                    model="gpt-4o-mini",  # Changed to correct model name
                    messages=[
                        {"role": "system", 
                         "content": f"""Extract the following information from the text and respond ONLY with a valid JSON object.
                         Required information:
                         1. Event Title
                         2. Event Date
                         3. Event Description
                         4. Tags (choose only from this list: {', '.join(available_tags)})
                         
                         Respond with EXACTLY this format (no additional text):
                         {{"title": "Event Name", "date": "Event Date", "description": "Event Description", "tags": ["tag1", "tag2"]}}"""
                        },
                        {"role": "user", "content": combined_text}
                    ]
                )
                
                try:
                    response_content = event_analysis.choices[0].message.content.strip()
                    print(f"Raw GPT response: {response_content}")
                    
                    # Try to clean the response if it's not proper JSON
                    if not response_content.startswith('{'):
                        response_content = response_content[response_content.find('{'):]
                    if not response_content.endswith('}'):
                        response_content = response_content[:response_content.rfind('}')+1]
                    
                    event_info = json.loads(response_content)
                    print("Successfully parsed JSON response")
                    
                    # Validate required fields
                    required_fields = ['title', 'date', 'description', 'tags']
                    if not all(field in event_info for field in required_fields):
                        raise ValueError("Missing required fields in JSON response")
                    
                    # Create updated post with event information
                    post_with_event = post.copy()
                    post_with_event.update({
                        'is_event': True,
                        'event_title': event_info['title'],
                        'event_date': event_info['date'],
                        'event_description': event_info['description'],
                        'event_tags': event_info['tags']
                    })
                    
                    processed_data[account].append(post_with_event)
                    print(f"Successfully added event: {event_info['title']}")
                    
                except json.JSONDecodeError as je:
                    print(f"JSON parsing error: {str(je)}")
                    print(f"Problematic response: {response_content}")
                    continue
                except Exception as e:
                    print(f"Error processing event info: {str(e)}")
                    continue
                
        except Exception as e:
            print(f"Error processing post: {str(e)}")
            continue

    if not processed_data[account]:
        print(f"No events found for account {account}, removing from processed data")
        del processed_data[account]

print("\nSaving results to file...")
with open('instagram-events-only.json', 'w', encoding='utf-8') as file:
    json.dump(processed_data, file, indent=4, ensure_ascii=False)
print("Processing complete!")