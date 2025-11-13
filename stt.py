from openai import OpenAI
import logging
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
logger = logging.getLogger("voice-to-image")

def transcribe_audio(file_path: str) -> str:
    """
    Takes a file path to WAV audio and sends to OpenAI whisper.
    """

    try:
        logger.info("Sending audio to OpenAI Whisper...")

        with open(file_path, "rb") as f:
            result = client.audio.transcriptions.create(
                model="gpt-4o-transcribe",
                file=f,
                language="en",                         # user speaks English
                prompt="The speaker is talking in English. Return clean English text."
            )

        transcript = result.text
        logger.info(f"Transcription successful: {transcript}")
        return transcript

    except Exception as e:
        logger.error(f"Transcription error: {e}")
        raise RuntimeError("Failed to transcribe audio")