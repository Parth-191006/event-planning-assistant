# Task Decomposition & Specs

## 1. Research Agent
- **Input:** Event type, location, budget.
- **Tool:** Tavily Search API.
- **Output:** JSON list of venues.

## 2. Design Agent
- **Input:** Venue data, theme preference.
- **Tool:** Gemini API.
- **Output:** JSON with theme name, color palette, and layout.

## 3. Copy Agent
- **Input:** Theme data, guest count.
- **Tool:** Gemini API.
- **Output:** JSON with invitation, MC script, and social posts.

## 4. Packaging Agent
- **Input:** All agent outputs.
- **Output:** Final Markdown report with budget breakdown.

## 5. Judge Agent (LLM-as-Judge)
- **Input:** Final report.
- **Tool:** Gemini API.
- **Output:** Quality score (1-10) and feedback based on completeness, creativity, and clarity.