## Voice → Image (Masters_GenAI_Capstone2) — Copilot instructions

This repo is a small Streamlit app that converts spoken audio into an AI-generated image. The goal of these instructions is to give an AI coding agent the minimal, concrete context needed to be productive right away.

- Big picture
  - UI: `app.py` is a Streamlit front-end with a simple 3-step flow: upload/record audio → transcribe → generate LLM prompt → generate image and display.
  - Business logic should live in small modules referenced by `app.py`: speech-to-text (STT), prompt generation (LLM), and image generation (gen/image modules).
  - The app expects helper functions with these names (see examples below):
    - `transcribe_audio(audio_file) -> str`  (in `stt.py`)
    - `generate_image_prompt(transcript: str) -> str`  (in `llm.py`)
    - `generate_image(prompt: str) -> <image>`  (imported as `generate_image` from `gen` in `app.py`; the repo also contains `image_gen.py`)

- Key files (start here)
  - `app.py` — Streamlit UI and orchestration. This file shows the exact function names and the flow to implement.
  - `stt.py` — placeholder for speech-to-text. Implement `transcribe_audio` here.
  - `llm.py` — placeholder for LLM prompt logic. Implement `generate_image_prompt` here.
  - `image_gen.py` (present but empty) and note: `app.py` imports `generate_image` from `gen` — reconcile by creating/renaming `gen.py` or updating `app.py`.
  - `README.md` — minimal repo description; use for high-level notes.

- Project-specific conventions / patterns discovered
  - The app uses a tiny imperative Streamlit flow; keep UI logic in `app.py` and business logic in the module files listed above.
  - Logging: code uses Python `logging` with logger name `voice-to-image` (see `app.py`). Use the same logger name when adding logging to helper modules for consistent logs.
  - Return types: `generate_image` must return an object supported by `st.image` (PIL Image, URL, or bytes). `transcribe_audio` returns a plaintext string.

- Integration points & gotchas
  - Missing / inconsistent files: `app.py` imports `from gen import generate_image`, but there is no `gen.py` file in the repo; `image_gen.py` exists but is empty. Before running, either implement `gen.py` or update `app.py` to import from `image_gen`.
  - Many modules and `requirements.txt` are empty placeholders. Do not assume external packages — confirm with the maintainer or add a minimal `requirements.txt` (e.g., `streamlit`, model SDKs) when implementing.

- How to run (quick, discoverable workflow)
  - Typical local dev: ensure Python 3.x and Streamlit are available, then run:
    - `python -m pip install -r requirements.txt` (requirements currently empty; add packages as needed)
    - `streamlit run app.py`
  - When adding remote API keys (LLM/image SDKs), put them in environment variables and reference them in the helper modules; do not commit secrets.

- Helpful examples (taken from `app.py`)
  - The orchestration in `app.py`:
    - call `transcribe_audio(audio_file)` → show result in `st.text_area`
    - call `generate_image_prompt(transcript)` → display prompt via `st.code`
    - call `generate_image(prompt)` → display the returned image with `st.image`

- Quick tasks for an agent that lands here
  1. Reconcile the `gen` vs `image_gen.py` import mismatch. Create `gen.py` (or export `generate_image` from `image_gen.py`).
  2. Implement minimal, testable stubs:
     - `transcribe_audio` that returns a fixed string for local dev.
     - `generate_image_prompt` that returns a formatted prompt based on the transcript.
     - `generate_image` that returns a local test image (PIL or file path) so the Streamlit UI can be verified.
  3. Add required dependencies to `requirements.txt` (at minimum `streamlit`), then run `streamlit run app.py` to validate the end-to-end flow.

- Where to look next
  - Open `app.py` to follow the exact flow. Use the function names and logger name above as anchors.
  - Implement helper modules (`stt.py`, `llm.py`, and `gen.py` / `image_gen.py`) and add unit tests if desired.

If any part of the app's intended integrations (specific LLMs or image APIs) is missing or you want me to implement the minimal stubs and run the app locally, tell me which modules you'd like implemented first and whether you have preferred SDKs or API keys to wire in.
