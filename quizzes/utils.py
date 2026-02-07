import os
import re
import json
import tempfile
import yt_dlp
import subprocess
import whisper
from google import genai


# ========== 1. Normalizacja YouTube URL ==========
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
    Downloads YouTube audio and returns path to temp audio file.
    """
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


# ========== 3. Transcribe using Whisper ==========
def transcribe_audio(audio_path: str) -> str:
    """
    Transcribes audio file to text using Whisper.
    """
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    return result["text"]


# ========== 4. Build Gemini Prompt ==========
def build_prompt(transcript: str) -> str:
    """
    Builds prompt for Gemini quiz generation.
    """
    return f"""
Based on the following transcript, generate a quiz in valid JSON format.

The quiz must follow this exact structure:

{{
  "title": "Create a concise quiz title based on the topic of the transcript.",
  "description": "Summarize the transcript in no more than 150 characters.",
  "questions": [
    {{
      "question_title": "The question goes here.",
      "question_options": ["Option A", "Option B", "Option C", "Option D"],
      "answer": "The correct answer from the above options"
    }}
    (exactly 10 questions)
  ]
}}

Requirements:
- Output valid JSON only.
- No extra text.
- One correct answer per question.

Transcript:
{transcript}
"""


# ========== 5. Ask Gemini ==========
def generate_quiz_json(prompt: str) -> dict:
    """
    Calls Gemini Flash API and returns parsed JSON quiz.
    """
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt
    )

    raw_text = response.text

    # Remove markdown code blocks if present
    raw_text = raw_text.replace("```json", "").replace("```", "").strip()

    return json.loads(raw_text)
