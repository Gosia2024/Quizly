# 🚀 Quizly Backend

Quizly is a Django REST API that automatically generates quizzes from YouTube videos using AI.

The system downloads audio from a YouTube video, transcribes it with Whisper AI, and generates a structured quiz using Google Gemini Flash.

---

# 📚 Table of Contents

- [About The Project](#about-the-project)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Quickstart](#quickstart)
- [Installation (Windows)](#installation-windows)
- [FFmpeg Requirement](#ffmpeg-requirement)
- [Environment Variables](#environment-variables)
- [Running The Project](#running-the-project)
- [Authentication](#authentication)
- [API Endpoints](#api-endpoints)
- [Project Structure](#project-structure)
- [Clean Code Principles](#clean-code-principles)

---

# 📖 About The Project

Quizly allows users to generate quizzes automatically from YouTube videos.

### AI Flow:

1. Download video audio using **yt-dlp**
2. Convert audio with **FFmpeg**
3. Transcribe audio using **OpenAI Whisper**
4. Generate quiz JSON with **Google Gemini Flash**
5. Store quizzes and questions in the database

---

# ✨ Features

- JWT Authentication with HTTP-only cookies
- Secure login & logout with token blacklist
- AI-generated quizzes
- REST API architecture
- User-specific quiz management
- Edit quiz metadata
- Permanent quiz deletion
- Fully tested endpoints

---

# 🛠 Tech Stack

- Python  
- Django  
- Django REST Framework  
- SimpleJWT  
- yt-dlp  
- OpenAI Whisper  
- Google Gemini Flash  
- FFmpeg  

---

# ⚡ Quickstart

If you want to run the project quickly:

```bash
git clone https://github.com/YOUR_USERNAME/quizly.git
cd quizly

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

python manage.py migrate
python manage.py runserve
```
👉 Don’t forget to install FFmpeg (see below).
💻 Installation (Windows)
1️⃣ Clone repository
```bash
git clone https://github.com/Gosia2024/quizly.git
cd quizly
```
2️⃣ Create virtual environment
```bash
python -m venv venv
```
Activate:
```bash
venv\Scripts\activate
```
3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```
❗ FFmpeg Requirement

⚠️ FFmpeg MUST be installed globally.

Whisper will fail without it.

Install via winget:

```bash
winget install --id Gyan.FFmpeg -e
```
Verify:
```bash
ffmpeg -version
```
If version info appears → ready ✅
🔑 Environment Variables

Create a .env file:
```bash
GEMINI_API_KEY=your_api_key_here
```
Get your key:

👉 https://ai.google.dev/

▶️ Running The Project

Apply migrations:
```bash
python manage.py migrate
```
🔐 Authentication

Quizly uses JWT stored in HTTP-only cookies.

This protects tokens from JavaScript attacks.
Register
```bash
POST /api/register/
```
Login
```bash
POST /api/login/
```
- Returns cookies:

- access_token

- refresh_token

Logout
```bash
POST /api/logout/
```

Refresh tokens are blacklisted.
Refresh Access Token
```bash
POST /api/token/refresh/
```
📡 API Endpoints
✅ Create Quiz
```bash
POST /api/createQuiz/
```
Body:
```bash
{
  "url": "https://www.youtube.com/watch?v=VIDEO_ID"
}
```
✅ Get User Quizzes
```bash
GET /api/quizzes/
```
✅ Get Quiz Detail
```bash
GET /api/quizzes/{id}/
```
✅ Update Quiz
```bash
PATCH /api/quizzes/{id}/
```
Example:
```bash
{
  "title": "Updated title"
}
```
✅ Delete Quiz
```bash
DELETE /api/quizzes/{id}/
```
Returns:
```bash
204 No Content
```
⚠️ Deletion is permanent.
📂 Project Structure
```bash
quizly/
│
├── accounts/        → authentication
├── quizzes/        → quiz logic
├── quizly_backend/ → settings
```
🧼 Clean Code Principles
This project follows:

✅ snake_case naming
✅ single responsibility functions
✅ REST conventions
✅ modular architecture
✅ PEP-8