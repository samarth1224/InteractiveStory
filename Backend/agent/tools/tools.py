"""
Agent tools for state management.

Provides tool functions that LLM agents can invoke during their
execution to read or modify session state variables.
"""



from google.adk.tools import ToolContext
from typing import Annotated

import requests

url = "https://api.siliconflow.com/v1/images/generations"


from app import config

async def generate_image(prompt: str,
                        context: ToolContext | None = None):
    """
    Generate an image using the SiliconFlow API.

    This tool sends a request to the SiliconFlow image generation endpoint
    using the provided text prompt. It returns the URL of the generated image.

    Args:
        prompt (str): A detailed text description of the image to generate.

    Returns:
        str: The URL of the generated image if successful, or an empty string if it fails.
    """
    payload = {
        "model": "black-forest-labs/FLUX.1-schnell",
        "prompt": prompt,
        "image_size": "512x512"
    }
    headers = {
        "Authorization": f"Bearer {config.SILICONFLOW_API_KEY}",
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.ok:
        data = response.json()
        if "images" in data and len(data["images"]) > 0:
            return data["images"][0]["url"]
        if "data" in data and len(data["data"]) > 0:
            return data["data"][0]["url"]
    return "failed"

