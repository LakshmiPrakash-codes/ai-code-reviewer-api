# AI Code Reviewer API

A REST API that takes a code snippet and returns a structured review — quality score, bugs with line numbers, security issues, improvement suggestions, complexity analysis, and a clean rewrite.

Built with FastAPI and Groq (Llama 3.3 70B). Reviews are stored in PostgreSQL so you can pull history later.

---

## Endpoints

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/health` | Check if the server is up |
| POST | `/review` | Submit code for review |
| GET | `/history` | List past reviews |
| GET | `/history/{id}` | Full detail of a specific review |
| GET | `/docs` | Swagger UI |

---

## Quick start

**1. Clone and set up**
```bash
git clone https://github.com/LakshmiPrakash-codes/ai-code-reviewer-api.git
cd ai-code-reviewer-api
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux
pip install -r requirements.txt
```

**2. Add your Groq API key**

Get a free key at [console.groq.com](https://console.groq.com) — no credit card needed.

```bash
cp .env.example .env
# open .env and set GROQ_API_KEY=your_key_here
```

**3. Run**
```bash
uvicorn app.main:app --reload
```

Open `http://localhost:8000/docs` to try it in the browser.

---

## Example

**Request**
```bash
POST /review
{
  "code": "def divide(a, b):\n    return a / b",
  "language": "python"
}
```

**Response**
```json
{
  "id": 1,
  "language": "python",
  "review": {
    "quality_score": 4,
    "summary": "Simple division function with no input validation or error handling.",
    "bugs": [
      {
        "line_number": 2,
        "description": "ZeroDivisionError if b is 0",
        "severity": "high"
      }
    ],
    "security_issues": [],
    "suggestions": [
      "Add a check for b == 0 before dividing",
      "Add type hints",
      "Consider raising a meaningful exception instead of crashing"
    ],
    "complexity": {
      "time_complexity": "O(1)",
      "space_complexity": "O(1)",
      "explanation": "Single arithmetic operation, constant time and space."
    },
    "rewritten_code": "def divide(a: float, b: float) -> float:\n    if b == 0:\n        raise ValueError(\"Cannot divide by zero\")\n    return a / b"
  },
  "created_at": "2026-06-08T10:00:00"
}
```

---

## Supported languages

- Python
- JavaScript
- SQL

---

## Stack

- **FastAPI** — API framework
- **Groq + Llama 3.3 70B** — AI model (free tier)
- **SQLAlchemy** — ORM
- **PostgreSQL** — production database (SQLite for local dev)
- **Pydantic v2** — request/response validation
- **Render** — deployment

---

## Deploy to Render

The `render.yaml` in this repo sets everything up automatically — web service + PostgreSQL. Just connect the repo in your Render dashboard and add `GROQ_API_KEY` as an environment variable.

---

## Run tests

```bash
python test_api.py
```

Starts hitting all endpoints and reports pass/fail. The `/review` test requires `GROQ_API_KEY` to be set.
