# 🧠 AI Interview Assessment – Django NLP & FastAPI Audio Transcription Project

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Django](https://img.shields.io/badge/django-4.2+-green.svg)](https://djangoproject.com/)
[![FastAPI](https://img.shields.io/badge/fastapi-0.104+-red.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This project demonstrates two AI-powered microservices showcasing modern web development and machine learning integration:

1. 🎧 **Audio Transcription with Speaker Diarization** (FastAPI + Whisper + PyAnnote)
2. 📝 **Blog Post Title Suggestions using NLP** (Django + Fine-tuned GPT-2)

## 🎯 Project Overview

This assessment project demonstrates proficiency in:

- **Backend Development**: Django REST Framework and FastAPI
- **Machine Learning**: Audio processing, NLP, and transformer models
- **API Design**: RESTful endpoints with proper error handling
- **Microservices Architecture**: Separate services for different functionalities
- **AI Integration**: Real-world application of pre-trained models

---

## 📁 Project Structure

```
assessment-project/
├── 📁 blogai/                    # Django project for NLP features
│   ├── 📁 blogai/               # Project settings
│   ├── 📁 titles/               # Blog title suggestion app
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── models.py
│   └── manage.py
├── 📁 feature1_transcription/    # FastAPI audio transcription service
│   ├── app.py                   # Main FastAPI application
│   ├── requirements.txt         # Service-specific dependencies
│   └── 📁 uploads/             # Temporary audio file storage
├── requirements.txt             # Global dependencies
├── .env.example                 # Environment variables template
├── .gitignore
└── README.md
```

---

## ✨ Features

### 🎧 Feature 1: Audio Transcription with Speaker Diarization

**Technology Stack**: FastAPI, OpenAI Whisper, PyAnnote.audio, FFmpeg

Transform audio files into structured, speaker-separated transcripts with timestamps.

#### 📍 API Endpoint

```http
POST /api/transcribe/
Content-Type: multipart/form-data
```

#### 📤 Request

- **File**: Audio file (`.wav`, `.mp3`, `.m4a`, `.flac`)
- **Max size**: 25MB
- **Supported formats**: All common audio formats

#### 📥 Response

```json
{
  "status": "success",
  "duration": 12.45,
  "speakers_detected": 2,
  "transcription": [
    {
      "speaker": "SPEAKER_00",
      "start": 0.59,
      "end": 0.91,
      "text": "Hi there!"
    },
    {
      "speaker": "SPEAKER_01",
      "start": 1.95,
      "end": 3.44,
      "text": "How are you doing today?"
    }
  ]
}
```

#### 🧪 Example Usage

```bash
# cURL
curl -X POST "http://127.0.0.1:8000/api/transcribe/" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@sample_audio.wav"

# Python requests
import requests

with open("sample_audio.wav", "rb") as audio_file:
    response = requests.post(
        "http://127.0.0.1:8000/api/transcribe/",
        files={"file": audio_file}
    )
print(response.json())
```

---

### 📝 Feature 2: Blog Post Title Suggestions

**Technology Stack**: Django, Transformers, Fine-tuned GPT-2

Generate creative, SEO-friendly blog post titles using advanced NLP techniques.

#### 📍 API Endpoint

```http
POST /api/titles/suggest/
Content-Type: application/json
```

#### 📤 Request

```json
{
  "content": "This blog explores how AI agents are transforming productivity and workflow automation in modern software teams, discussing implementation strategies and real-world case studies.",
  "count": 3,
  "style": "creative"
}
```

#### 📥 Response

```json
{
  "status": "success",
  "suggestions": [
    "AI Agents: The Future of Team Productivity",
    "Transforming Workflows with Intelligent Automation",
    "From Manual to Magical: AI-Powered Team Efficiency"
  ],
  "generated_at": "2024-12-09T10:30:00Z"
}
```

#### 🧪 Example Usage

```bash
# cURL
curl -X POST "http://127.0.0.1:8000/api/titles/suggest/" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Machine learning is revolutionizing healthcare diagnosis and treatment recommendations."
  }'

# Python requests
import requests

response = requests.post(
    "http://127.0.0.1:8000/api/titles/suggest/",
    json={"content": "Your blog content here"}
)
print(response.json())
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- FFmpeg (for audio processing)
- Git
- 4GB+ RAM (for ML models)

### 1. Clone & Setup

```bash
git clone https://github.com/<your-username>/ai-interview-assessment.git
cd ai-interview-assessment
```

### 2. Environment Setup

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Variables

Create `.env` file in the root directory:

```ini
# Required for PyAnnote speaker diarization
HUGGINGFACE_TOKEN=your_hf_token_here

# Optional: Database configuration
DATABASE_URL=sqlite:///db.sqlite3

# Optional: Logging level
LOG_LEVEL=INFO
```

**🔑 Getting HuggingFace Token:**

1. Visit [huggingface.co](https://huggingface.co)
2. Create account and go to Settings → Access Tokens
3. Create new token with "Read" permissions
4. Accept PyAnnote model terms at `pyannote/speaker-diarization-3.1`

### 4. Install FFmpeg

```bash
# Ubuntu/Debian
sudo apt update && sudo apt install ffmpeg

# macOS
brew install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
```

### 5. Run Services

#### Django Service (Blog Titles)

```bash
cd blogai
python manage.py migrate
python manage.py runserver
# Access at: http://127.0.0.1:8000/
```

#### FastAPI Service (Audio Transcription)

```bash
cd feature1_transcription
uvicorn app:app --reload --port 8001
# Access at: http://127.0.0.1:8001/docs
```

---

## 🧪 Testing

### Automated Tests

```bash
# Run Django tests
cd blogai
python manage.py test

# Run FastAPI tests
cd feature1_transcription
pytest tests/
```

### Manual Testing

1. **Audio Transcription**: Use the interactive docs at `http://127.0.0.1:8001/docs`
2. **Title Generation**: Send POST requests to `http://127.0.0.1:8000/api/titles/suggest/`

### Sample Test Files

- `test_audio.wav` - 30-second sample conversation
- `test_content.json` - Sample blog content for title generation

---

## 📊 Performance & Limitations

### Audio Transcription

- **Processing Time**: ~2-3x audio duration
- **Memory Usage**: 2-4GB during processing
- **File Size Limit**: 25MB per upload
- **Accuracy**: 90-95% for clear English speech

### Title Generation

- **Response Time**: 1-3 seconds
- **Memory Usage**: 500MB-1GB
- **Input Limit**: 2000 characters
- **Languages**: Primarily English

---

## 🛠️ Development

### Adding New Features

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

### Code Style

- Follow PEP 8 for Python code
- Use type hints where applicable
- Add docstrings for functions and classes
- Format with Black: `black .`

---

## 🔧 Troubleshooting

### Common Issues

**1. HuggingFace Authentication Error**

```
Solution: Ensure HUGGINGFACE_TOKEN is set and you've accepted model terms
```

**2. FFmpeg Not Found**

```
Solution: Install FFmpeg and ensure it's in your system PATH
```

**3. Out of Memory Errors**

```
Solution: Reduce audio file size or increase system RAM
```

**4. Model Download Failures**

```
Solution: Check internet connection, may need to download models manually
```

### Getting Help

- Contact: [rithikmotupalli@gmail.com](rithikmotupalli@gmail.com)

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **OpenAI Whisper** - Speech recognition model
- **PyAnnote.audio** - Speaker diarization toolkit
- **Hugging Face** - Transformer models and hosting
- **FastAPI** - Modern web framework for APIs
- **Django** - Robust web framework for Python

---

_Built with ❤️ by Rithik Sai Motupalli_
