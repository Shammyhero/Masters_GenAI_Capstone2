from openai import OpenAI
import logging
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
logger = logging.getLogger("voice-to-image")


def generate_image_prompt(transcript: str) -> str:
    """
    Takes transcript text → uses LLM to convert into
    a clean, descriptive image prompt for image generation.
    """

    try:
        logger.info("Sending transcript to LLM for prompt generation...")

        system_msg = (
            "You are an expert prompt engineer. "
            "Convert the user's spoken request into a highly detailed, vivid, "
            "and visually descriptive prompt suitable for an AI image generator. "
            "Keep it concise but descriptive. Do NOT include disclaimers, "
            "chats, or quotes. Output ONLY the final prompt."
        )

        user_msg = f"User voice transcript: {transcript}"

        response = client.responses.create(
            model="gpt-4o-mini",
            input=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_msg}
            ]
        )

        prompt = response.output_text.strip()
        logger.info(f"Generated Image Prompt: {prompt}")

        return prompt

    except Exception as e:
        logger.error(f"LLM prompt generation error: {e}")
        return "Error generating image prompt."