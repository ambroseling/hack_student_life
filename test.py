import json
from scrapegraphai.graphs import SmartScraperGraph

# Define the configuration for the scraping pipeline
graph_config = {
    "llm": {
        "api_key": "YOUR_OPENAI_APIKEY",
        "model": "openai/gpt-4o-mini",
    },
    "verbose": True,
    "headless": False,
}

# Create the SmartScraperGraph instance
smart_scraper_graph = SmartScraperGraph(
    prompt="Find some information about what does the company do, the name and a contact email.",
    source="https://scrapegraphai.com/",
    config=graph_config
)

# Run the pipeline
result = smart_scraper_graph.run()
print(json.dumps(result, indent=4))