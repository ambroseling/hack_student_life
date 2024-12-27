from enum import Enum
from llama_index.core.tools import FunctionTool
from llama_index.core.tools.types import BaseTool

class ActionStatus(Enum):
    SUCCESS = "success"
    FAILURE = "failure"

def navigate_to_instagram_account(username: str):
    print(f"Navigating to {username}'s Instagram account.")
    
    return ActionStatus.SUCCESS

def scrape_instagram_posts(username: str)->ActionStatus:
    print(f"Scraping {username}'s Instagram posts.")
    return ActionStatus.SUCCESS

def scrape_instagram_comments(username: str)->ActionStatus:
    print(f"Scraping {username}'s Instagram comments.")
    return ActionStatus.SUCCESS