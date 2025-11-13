from openai import OpenAI
import base64
from io import BytesIO
from PIL import Image
import logging
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
logger = logging.getLogger("voice-to-image")


def generate_image(prompt: str):
    """
    Sends the generated prompt to OpenAI image model and returns
    a PIL image that Streamlit can show directly.
    """

    try:
        logger.info("Sending prompt to OpenAI Image Model...")

        response = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size="1024x1024"
        )

        # Extract Base64 image
        image_base64 = response.data[0].b64_json
        image_bytes = base64.b64decode(image_base64)

        # Convert to PIL image
        image = Image.open(BytesIO(image_bytes))

        logger.info("Image generated successfully.")
        return image

    except Exception as e:
        logger.error(f"Image generation error: {e}")
        return None