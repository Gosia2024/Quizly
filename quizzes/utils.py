import os
import re
import json
import tempfile
import logging

import yt_dlp
import whisper
from google import genai


# ================= LOGGING =================

logger = logging.getLogger(__name__)


# ================= LOAD MODELS ONLY ONCE =================

# Whisper model (VERY heavy -> load once)
whisper_model = whisper.load_model("base")

# Gemini client
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("Missing GEMINI_API_KEY in environment variables")

gemini_client = genai.Client(api_key=GEMINI_API_KEY)


# ========== 1. Normalize YouTube URL ==========

def normalize_youtube_url(url: str) -> str:
    """
    Extracts YouTube video ID and returns normalized watch URL.
    """

    match = re.search(r"(?:v=|youtu\.be/)([\w-]{11})", url)

    if not match:
        raise ValueError("Invalid YouTube URL")

    video_id = match.group(1)

    return f"https://www.youtube.com/watch?v={video_id}"


# ========== 2. Download audio using yt_dlp ==========

def download_audio(url: str) -> str:
    """
    Downloads YouTube audio and returns path to temp mp3 file.
    """

    try:
        tmp_dir = tempfile.mkdtemp()
        tmp_filename = os.path.join(tmp_dir, "audio")

        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": tmp_filename,
            "quiet": True,
            "noplaylist": True,
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3"
            }]
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return tmp_filename + ".mp3"

    except Exception as e:
        logger.error(f"Audio download failed: {e}")
        raise RuntimeError("Failed to download audio")


# ========== 3. Transcribe using Whisper ==========

def transcribe_audio(audio_path: str) -> str:
    """
    Transcribes audio file to text using Whisper.
    """

    try:
        result = whisper_model.transcribe(audio_path)
        return result["text"]

    except Exception as e:
        logger.error(f"Transcription failed: {e}")
        raise RuntimeError("Whisper transcription failed")


# ========== 4. Build Gemini Prompt ==========

def build_prompt(transcript: str) -> str:
    """
    Builds prompt for Gemini quiz generation.
    """

    return f"""
Based on the following transcript, generate a quiz in valid JSON format.

The quiz must follow this EXACT structure:

{{
  "title": "Create a concise quiz title based on the transcript topic.",
  "description": "Summarize the transcript in no more than 150 characters.",
  "questions": [
    {{
      "question_title": "The question goes here.",
      "question_options": ["Option A", "Option B", "Option C", "Option D"],
      "answer": "The correct answer"
    }}
  ]
}}

STRICT REQUIREMENTS:
- Generate EXACTLY 10 questions
- Each question must have exactly 4 options
- Only ONE correct answer
- Output MUST be valid JSON
- Do NOT include markdown
- Do NOT include explanations
- Return JSON only

Transcript:
{transcript}
"""


# ========== 5. Ask Gemini ==========

def generate_quiz_json(prompt: str) -> dict:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Missing GEMINI_API_KEY in environment variables")

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )

    raw_text = response.text
    raw_text = raw_text.replace("```json", "").replace("```", "").strip()

    return json.loads(raw_text)

