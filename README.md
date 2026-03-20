# 🧠 MeetingMind Agent

A Streamlit app that analyses meeting transcripts through a 5-step AI pipeline powered by Groq (`llama-3.3-70b-versatile`). Paste a transcript, click a button, get a structured report with summaries, action items, decisions, and section breakdowns.

[![Deploy to Streamlit Cloud](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/deploy)

---

## Prerequisites

- Python 3.9+
- A free Groq API key → [console.groq.com](https://console.groq.com)

---

## Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/your-username/Meeting-Agent.git
cd Meeting-Agent
```

### 2. Install dependencies

```bash
cd meetingmind
pip install -r requirements.txt
```

> Tip: use a virtual environment to keep things tidy:
> ```bash
> python -m venv .venv
> source .venv/bin/activate   # Windows: .venv\Scripts\activate
> pip install -r requirements.txt
> ```

### 3. Add your Groq API key

```bash
cp .env.example .env
```

Open `.env` and replace the placeholder:

```
GROQ_API_KEY=gsk_your_actual_key_here
```

### 4. Run the app

```bash
streamlit run app.py
```

The app opens automatically at **http://localhost:8501**.

---

## Using the App

1. Paste your meeting transcript into the text area.
2. Enter your Groq API key in the sidebar (auto-filled if set in `.env`).
3. Click **Analyse Meeting**.
4. Watch the 5 pipeline nodes complete one by one.
5. Read the generated report on screen, then hit **Download Report** to save it as a `.md` file.

---

## What the Pipeline Produces

| Section | Contents |
|---------|----------|
| **Meeting Summary** | High-level narrative overview |
| **Action Items** | Table of tasks with owner and deadline |
| **Decisions Made** | Table of decisions with decision-maker |
| **Section Breakdowns** | 2-3 sentence summary per topic |

---

## Project Structure

```
meetingmind/
├── app.py              # Streamlit UI and pipeline orchestration
├── nodes.py            # One function per pipeline node
├── prompts.py          # All LLM prompt templates
├── requirements.txt    # Python dependencies
├── .env.example        # API key template
└── .streamlit/
    └── secrets.toml    # Streamlit Cloud secrets template
```

---

## Deploying to Streamlit Cloud

1. Push this repo to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**.
3. Set **Main file path** to `meetingmind/app.py`.
4. Open **Advanced settings → Secrets** and add:
   ```toml
   GROQ_API_KEY = "gsk_your_key_here"
   ```
5. Click **Deploy** — no other configuration needed.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` from inside `meetingmind/` |
| `AuthenticationError` | Check your Groq API key is correct and has not expired |
| Blank report / JSON error | The model occasionally returns malformed JSON — retry the analysis |
| Port 8501 already in use | Run `streamlit run app.py --server.port 8502` |
