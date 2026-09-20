# Intelligent Text Correction System

An NLP-oriented text correction web application built with Python and Flask.

## Resume-aligned project scope

- Grammar and spelling correction
- Python and Flask backend
- Input validation
- Backend API processing
- Simple browser interface

## Features

- Corrects common spelling and grammar mistakes
- Returns the original and corrected text
- Shows individual changes
- REST API endpoint
- Input validation and 5000-character limit
- Automated tests with pytest
- No external API key required

## Project structure

```text
Intelligent-Text-Correction-System/
├── app/
│   ├── __init__.py
│   ├── corrector.py
│   └── routes.py
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
├── tests/
│   ├── test_api.py
│   └── test_corrector.py
├── requirements.txt
└── run.py
```

## Run locally

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

Open `http://127.0.0.1:5000` in a browser.

## Test

```bash
pytest
```

## Free hosting

This is a Flask application, so GitHub Pages cannot host the working API. To deploy it free on Render, create a new Web Service from this repository. Render will use `render.yaml`, install the dependencies, run Gunicorn, and use `/api/health` for health checks. The free service may sleep after inactivity and take a few seconds to wake.

## API

### Health

`GET /api/health`

### Correct text

`POST /api/correct`

Example JSON:

```json
{
  "text": "I definately recieve teh email."
}
```

Example response:

```json
{
  "original_text": "I definately recieve teh email.",
  "corrected_text": "I definitely receive the email.",
  "changes": [
    {"original": "definately", "corrected": "definitely", "type": "spelling/grammar"},
    {"original": "recieve", "corrected": "receive", "type": "spelling/grammar"},
    {"original": "teh", "corrected": "the", "type": "spelling/grammar"}
  ],
  "change_count": 3
}
```

## Note

This implementation uses a lightweight local correction dictionary and punctuation rules so it can be run and demonstrated without third-party API credentials. The resume describes the project as an NLP-based grammar and spelling correction system using Python and Flask.
