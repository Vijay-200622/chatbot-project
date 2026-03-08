# 📚 Padhai Buddy — NCERT AI Tutor

A Hinglish/Tanglish AI-powered doubt-clearing chatbot for NCERT Class 9–10 students. Built with FastAPI + Streamlit + HuggingFace.

## Features

- **💬 Codemixed AI Chat** — Ask doubts in Hinglish, Tanglish, or English
- **🔊 Voice Explanations** — Listen to explanations via text-to-speech
- **📈 Adaptive Difficulty** — Repeated questions get simpler explanations
- **📝 Practice Questions** — Easy/Medium/Hard questions per topic
- **🗺️ Concept Maps** — Visual concept relationship diagrams
- **🔍 Mistake Analyzer** — Paste wrong answers for AI analysis
- **🔥 Study Streaks** — Gamified daily streak tracker (3 questions/day)
- **👨‍🏫 Teacher Dashboard** — Analytics with topic frequency charts

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | Streamlit |
| Backend | FastAPI |
| AI Model | HuggingFace Inference API (Mistral 7B / Llama 3 8B) |
| Database | SQLite |
| Voice | gTTS (Google Text-to-Speech) |
| Visualization | Graphviz |
| Analytics | Pandas |

## Prerequisites

- **Python 3.10+**
- **Graphviz** system binary (for concept maps)
- **HuggingFace account** (free) with API token

### Install Graphviz

**Windows:**
```bash
# Download from https://graphviz.org/download/
# Or use winget:
winget install graphviz
```

**macOS:**
```bash
brew install graphviz
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install graphviz
```

## Setup

### 1. Clone / Navigate to project
```bash
cd ncert_ai_tutor
```

### 2. Create virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment
```bash
# Copy example env file
copy .env.example .env   # Windows
cp .env.example .env     # macOS/Linux

# Edit .env and add your HuggingFace API token
# Get your free token at: https://huggingface.co/settings/tokens
```

### 5. Run the application
```bash
python run.py
```

This starts both services:
- **Backend API:** http://127.0.0.1:8000/docs (Swagger UI)
- **Frontend UI:** http://127.0.0.1:8501

## Project Structure

```
ncert_ai_tutor/
├── frontend/
│   ├── app.py                         # Streamlit entry point
│   ├── pages/
│   │   ├── 1_Student_Chat.py          # AI chat interface
│   │   ├── 2_Practice.py              # Practice questions & mistake analyzer
│   │   ├── 3_Streaks.py               # Study streak dashboard
│   │   └── 4_Teacher_Dashboard.py     # Teacher analytics (login-gated)
│   └── assets/style.css
├── backend/
│   ├── main.py                        # FastAPI app
│   ├── config.py                      # Settings from .env
│   ├── routers/
│   │   ├── chat.py                    # /api/chat endpoints
│   │   ├── practice.py                # /api/practice endpoint
│   │   ├── concept_map.py             # /api/concept-map endpoint
│   │   ├── mistakes.py                # /api/analyze-mistake endpoint
│   │   ├── streaks.py                 # /api/streaks endpoints
│   │   ├── analytics.py               # /api/analytics endpoints
│   │   └── auth.py                    # /api/auth/login endpoint
│   ├── services/
│   │   ├── llm_engine.py              # HuggingFace API wrapper
│   │   ├── adaptive_engine.py         # Difficulty adaptation
│   │   ├── practice_generator.py      # Question generation
│   │   ├── concept_map.py             # Graphviz concept maps
│   │   ├── mistake_analyzer.py        # Answer analysis
│   │   ├── voice_engine.py            # gTTS text-to-speech
│   │   └── topic_filter.py            # NCERT syllabus filter
│   └── models/schemas.py              # Pydantic models
├── database/
│   ├── db.py                          # SQLite connection
│   ├── models.py                      # Table definitions
│   └── crud.py                        # CRUD operations
├── data/
│   ├── ncert_topics.json              # 55+ NCERT topics (Class 9-10)
│   └── system_prompts.py              # AI prompt templates
├── tests/
├── requirements.txt
├── .env.example
├── run.py                             # Launch both servers
└── README.md
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/chat` | Send question, get AI response |
| POST | `/api/chat/voice` | Get MP3 audio of text |
| POST | `/api/practice` | Generate practice questions |
| POST | `/api/concept-map` | Generate concept map SVG |
| POST | `/api/analyze-mistake` | Analyze incorrect answer |
| GET | `/api/streaks/{username}` | Get streak data |
| POST | `/api/auth/login` | Teacher login |
| GET | `/api/analytics/weekly-topics` | Top topics this week |
| GET | `/api/analytics/confused-topics` | Most repeated topics |
| GET | `/api/analytics/daily-counts` | Daily question frequency |

## Default Credentials

| Role | Username | Password |
|------|----------|----------|
| Teacher | `teacher` | `teach123` |
| Student | *(any name)* | *(none needed)* |

## Usage Examples

### Student Chat
```
"bhaiya photosynthesis samajh nahi aaya"
"anna, Newton's law explain pannu"
"What is the difference between speed and velocity?"
```

### Out-of-Syllabus Detection
```
"Explain quantum mechanics" → "Ye topic NCERT class 9-10 syllabus mein nahi hai!"
```

## Future Upgrades

- Azure deployment (App Service / Container Apps)
- JWT-based authentication
- RAG with actual NCERT textbook PDFs
- WebSocket streaming for real-time responses
- Redis caching for frequently asked topics
- Multi-language UI (Hindi, Tamil, English)

## License

MIT
