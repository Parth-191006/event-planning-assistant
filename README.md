\# 🎓 Event Planning Assistant



A multi-agent AI system that automates college event planning.



\## ✨ Features

\- 🔍 \*\*Research Agent\*\*: AI-powered venue/vendor discovery via Tavily web search

\- 🎨 \*\*Design Agent\*\*: Visual theme generation with color palettes + layout suggestions  

\- ✍️ \*\*Copy Agent\*\*: Automated invitation, script, and social media content

\- 📦 \*\*Packaging Agent\*\*: Professional report assembly with budget breakdown + checklist

\- 🌐 \*\*Streamlit UI\*\*: One-click web interface with downloadable outputs



\## 🤖 AI Integration

\- Primary: Google Gemini 2.0 Flash (function calling + JSON output)

\- Fallback: Graceful mock-data mode when API quota is exhausted

\- Architecture: Agentic loop with tool calling, retry logic, and error isolation



\## 🛠️ Tech Stack

\- Python 3.10+

\- Streamlit (web UI)

\- google-genai (Gemini API client)

\- Tavily (AI-optimized web search)

\- python-dotenv (secure config)



\## ▶️ How to Run

1\. `python -m venv venv`

2\. `.\\venv\\Scripts\\Activate.ps1` (Windows PowerShell)

3\. `pip install -r requirements.txt`

4\. Create `.env` with:

