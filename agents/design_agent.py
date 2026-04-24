import os
import json
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_KEY)

MODEL_NAME = "gemini-2.0-flash"  # ✅ Only free-tier model available

FALLBACK_THEME = {
    "theme_name": "Modern College Event",
    "description": "Clean, professional, and student-friendly design",
    "color_palette": ["#2563EB", "#7C3AED", "#0F172A"],
    "mood_keywords": ["professional", "engaging", "memorable"],
    "layout_suggestion": "Stage at front, seating in rows, photo zone at back",
    "note": "🤖 Fallback theme (Gemini quota limit reached)"
}

def generate_theme(venue_data, event_type, theme_preference="modern"):
    prompt = f"""
You are an expert event designer. Create a visual theme for a '{event_type}' with a '{theme_preference}' style.
Return ONLY valid JSON with these exact keys:
- theme_name: string
- description: string (2-3 sentences)
- color_palette: list of exactly 3 hex color codes
- mood_keywords: list of exactly 3 adjectives
- layout_suggestion: string (1 sentence)
Do not include markdown or explanations. Just raw JSON.
"""
    # Try up to 2 times with a short wait if quota is hit
    for attempt in range(2):
        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt
            )
            result = json.loads(response.text)
            if all(k in result for k in ["theme_name", "color_palette", "description"]):
                return result
        except Exception as e:
            if "429" in str(e) and attempt == 0:
                print("⏳ Quota limit hit. Waiting 60s for reset...")
                time.sleep(60)  # Wait for quota to refresh
                continue
            print(f"⚠️ Gemini Design failed: {e}. Using fallback.")
            return FALLBACK_THEME
    return FALLBACK_THEME

if __name__ == "__main__":
    print("🎨 Testing AI Design Agent...")
    result = generate_theme([], "college tech fest", "cyberpunk")
    print(json.dumps(result, indent=2))