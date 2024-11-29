from openai import OpenAI
from dotenv import load_dotenv
import os
import boto3
import requests
import json

load_dotenv()

# Get the API key from the environment
api_key = os.getenv("OPENAI_API_KEY")

# Set the API key for OpenAI
OpenAI.api_key = api_key

client = OpenAI()


# Open and read the JSON file
with open('site-data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

titles_and_descriptions = [
    {"title": event["title"]}
    for event in data
]

titles_list_str = "\n".join(f"- {item['title']}" for item in titles_and_descriptions)

#print(titles_list_str)

def search_bar(input, titles_list_str):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant who matches user search queries to event titles."
            },
            {
                "role": "user",
                "content": f"The user is searching for: '{input}'.\n\nHere are the available events:\n{titles_list_str}\n\nOnly return the top 5 most relevant events. If there are no relevant events then return nothing"
            }
        ]
    )
    return completion.choices[0].message.content

# Example usage
response = search_bar("jazz", titles_list_str)
print(response)

