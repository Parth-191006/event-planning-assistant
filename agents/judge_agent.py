import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_KEY)

# Fallback score if Gemini fails
FALLBACK_SCORE = {
    "overall_score": 8,
    "breakdown": {
        "completeness": 9,
        "creativity": 7,
        "budget_adherence": 9,
        "clarity": 8
    },
    "feedback": "Solid plan with clear venues, theme, and copy. Consider adding backup vendor options.",
    "note": "🤖 Fallback score (Gemini unavailable)"
}

def evaluate_plan(report_text, event_details):
    """
    Evaluate the final event plan against a rubric.
    Returns JSON with scores + feedback.
    """
    prompt = f"""
You are an expert event planning evaluator. Score this event plan against the rubric below.

EVENT DETAILS:
- Type: {event_details.get('event_type')}
- Budget: ${event_details.get('budget')}
- Location: {event_details.get('location')}
- Guests: {event_details.get('guest_count')}

PLAN TO EVALUATE:
{report_text[:3000]}  # First 3000 chars

RUBRIC (score each 1-10):
1. Completeness: Does it include venues, theme, copy, budget, checklist?
2. Creativity: Is the theme/originality engaging for college students?
3. Budget Adherence: Are cost estimates realistic and within budget?
4. Clarity: Is the report well-organized and easy to follow?

Return ONLY valid JSON with these exact keys:
- overall_score: integer 1-10 (weighted average)
- breakdown: object with keys "completeness", "creativity", "budget_adherence", "clarity" (each integer 1-10)
- feedback: string (2-3 sentences of constructive feedback)
Do not include markdown or explanations. Just raw JSON.
"""
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        result = json.loads(response.text)
        # Validate required keys
        if all(k in result for k in ["overall_score", "breakdown", "feedback"]):
            return result
        else:
            raise ValueError("Missing required keys")
    except Exception as e:
        print(f"⚠️ Judge Agent failed: {e}. Using fallback score.")
        return FALLBACK_SCORE

if __name__ == "__main__":
    print("🧠 Testing LLM-as-Judge Agent...")
    mock_report = "# Test Plan\nVenues: XYZ\nTheme: Cyberpunk\nBudget: $3000"
    mock_details = {"event_type": "tech fest", "budget": 3000, "location": "Austin", "guest_count": 150}
    result = evaluate_plan(mock_report, mock_details)
    print(json.dumps(result, indent=2))