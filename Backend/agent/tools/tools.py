"""
Agent tools for state management.

Provides tool functions that LLM agents can invoke during their
execution to read or modify session state variables.
"""



from google.adk.tools import ToolContext
from typing import Annotated

import requests

url = "https://api.siliconflow.com/v1/images/generations"


import os
import uuid
import boto3

def upload_to_s3(image_url: str) -> str:
    bucket_name = os.getenv("AWS_S3_BUCKET")
    if not bucket_name:
        return image_url

    try:
        img_resp = requests.get(image_url)
        if not img_resp.ok:
            return image_url
            
        s3_client = boto3.client(
            's3',
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION", "us-east-1")
        )
        
        filename = f"generated_images/{uuid.uuid4().hex}.png"
        s3_client.put_object(
            Bucket=bucket_name,
            Key=filename,
            Body=img_resp.content,
            ContentType='image/png'
        )
        region = os.getenv("AWS_REGION", "eu-north-1")
        return f"https://{bucket_name}.s3.{region}.amazonaws.com/{filename}"
    except Exception as e:
        print(f"Error uploading to S3: {e}")
        return image_url

async def generate_image(prompt: str,
                        context: ToolContext | None = None):
    """
    Generate an image using the SiliconFlow API and upload to S3.

    This tool sends a request to the SiliconFlow image generation endpoint
    using the provided text prompt. It downloads the image, uploads it to an S3 bucket,
    and returns the S3 URL of the generated image.

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
        "Authorization": f"Bearer {os.getenv('SILICONFLOW_API_KEY', '')}",
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.ok:
        data = response.json()
        image_url = None
        if "images" in data and len(data["images"]) > 0:
            image_url = data["images"][0]["url"]
        elif "data" in data and len(data["data"]) > 0:
            image_url = data["data"][0]["url"]
            
        if image_url:
            return upload_to_s3(image_url)
            
    return "failed"

