from openai import OpenAI
from dotenv import load_dotenv
import os
import boto3
import requests
import json



# Load environment variables from the .env file
"""load_dotenv()

# Get the API key from the environment
api_key = os.getenv("OPENAI_API_KEY")

# Set the API key for OpenAI
OpenAI.api_key = api_key

client = OpenAI()

# Initialize Rekognition client
rekognition = boto3.client('rekognition', region_name='us-west-2')  # e.g., 'us-west-2'

# Open and read the JSON file
with open('instagram-data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

usersearch = "USER: soccer intermurals"
for account in data:
    for post in data[account]:
        url = post['displayUrl']
    
        # Fetch the image
        response = requests.get(url)

        # The content of the image in bytes
        image_bytes = response.content

        response = rekognition.detect_text(
            Image={'Bytes': image_bytes}
        )

        # Parse and print detected text
        detected_text = []
        for text_detection in response['TextDetections']:
            detected_text.append(text_detection['DetectedText'])

        result = ' '.join(detected_text)

search = []
search.append(result)
search.append(usersearch)
print(search)
completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", 
        "content": "You will be presented with text from instagram posts and your job is to pick which event is the most relevant to the user's search which will be the second list element"
        },
        {
            "role": "user",
            "content": result
        }
    ]
)

print(completion.choices[0].message)"""

