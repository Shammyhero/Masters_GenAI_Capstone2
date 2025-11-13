import streamlit as st
from streamlit_mic_recorder import mic_recorder
import logging
from stt import transcribe_audio
from llm import generate_image_prompt
from image_gen import generate_image
import tempfile
import os 
import time

os.environ["FFMPEG_BINARY"] = "/opt/homebrew/bin/ffmpeg"  
os.environ["FFPROBE_BINARY"] = "/opt/homebrew/bin/ffprobe"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("voice-to-image")

st.title("🎤 Voice → Image Generator")
st.write("Record your voice → check it → generate an image")

# -------------------------
# SESSION STATE INIT (very important)
# -------------------------
if "recording" not in st.session_state:
    st.session_state["recording"] = False
if "start_time" not in st.session_state:
    st.session_state["start_time"] = None
if "temp_audio_file" not in st.session_state:
    st.session_state["temp_audio_file"] = None

# -------------------------
# Recording UI (works with mic_recorder)
# -------------------------
st.subheader("🎙️ Record")
timer_placeholder = st.empty()

if not st.session_state["recording"]:
    if st.button("🎤 Start Recording by clicking this button and button below"):
        st.session_state["recording"] = True
        st.session_state["start_time"] = time.time()
        st.session_state["temp_audio_file"] = None
        st.rerun()

# mic_recorder will handle start/stop; return bytes when finished
audio_data = mic_recorder(start_prompt="Recording...", stop_prompt="Stop Recording", just_once=True, format="wav")

# timer while recording
if st.session_state["recording"] and audio_data is None:
    elapsed = int(time.time() - st.session_state["start_time"])
    timer_placeholder.markdown(f"### ⏱️ Recording: **{elapsed} s**")
    time.sleep(0.1)
    st.rerun()

# when recording finishes
if audio_data and st.session_state["recording"]:
    st.session_state["recording"] = False
    # save temp wav and keep path in session_state
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(audio_data["bytes"])
        st.session_state["temp_audio_file"] = tmp.name
    st.audio(audio_data["bytes"])
    st.success("Recording complete — now press Submit to process.")

# -------------------------
# Submit block (safe checks)
# -------------------------
if st.session_state["temp_audio_file"] is None:
    st.info("Please submit a recording first (Start Recording).")
else:
    if st.button("Submit to Agent"):
        audio_path = st.session_state["temp_audio_file"]

        # Transcribe
        try:
            transcript = transcribe_audio(audio_path)
        except Exception as e:
            st.error("❌ Transcription failed: " + str(e))
            st.stop()

        st.subheader("📝 Transcript")
        st.text_area("Transcript", transcript, height=150)

        # Prompt generation
        try:
            prompt = generate_image_prompt(transcript)
        except Exception as e:
            st.error("❌ Prompt generation failed: " + str(e))
            st.stop()

        st.subheader("✨ Prompt")
        st.code(prompt)

        # Image generation
        try:
            image = generate_image(prompt)
        except Exception as e:
            st.error("❌ Image generation failed: " + str(e))
            st.stop()

        if image:
            st.subheader("🎨 Generated image")
            st.image(image)