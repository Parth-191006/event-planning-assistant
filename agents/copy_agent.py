import os
import json
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_KEY)

MODEL_NAME = "gemini-2.0-flash"  # ✅ Only free-tier model available

FALLBACK_COPY = {
    "invitation": "🎉 You're invited to our upcoming college event! Join us for an unforgettable experience.",
    "mc_script": "[Opening] Welcome everyone! We're thrilled to have you here. [Closing] Thank you for coming!",
    "social_posts": {
        "instagram": "🔥 Event coming soon! Stay tuned. #CollegeLife",
        "twitter": "Get ready for an amazing campus event! 🚀",
        "linkedin": "Excited to announce our upcoming college event celebrating student innovation."
    },
    "tone": "energetic, professional, inclusive",
    "note": "🤖 Fallback copy (Gemini quota limit reached)"
}

def generate_copy(venue_data, theme_data, event_type, guest_count):
    venue_name = venue_data[0]['title'] if venue_data else "TBD"
    theme_name = theme_data.get('theme_name', 'Awesome Event')
    
    prompt = f"""
You are a professional event copywriter. Write content for a '{event_type}'.
Details:
- Venue: {venue_name}
- Theme: {theme_name}
- Expected Guests: {guest_count}

Return ONLY valid JSON with these exact keys:
- invitation: string (enthusiastic 3-4 line invite)
- mc_script: string (short opening + closing lines)
- social_posts: object with keys "instagram", "twitter", "linkedin"
Do not include markdown or explanations. Just raw JSON.
"""
    for attempt in range(2):
        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt
            )
            result = json.loads(response.text)
            if all(k in result for k in ["invitation", "mc_script", "social_posts"]):
                return result
        except Exception as e:
            if "429" in str(e) and attempt == 0:
                print("⏳ Quota limit hit. Waiting 60s for reset...")
                time.sleep(60)
                continue
            print(f"⚠️ Gemini Copy failed: {e}. Using fallback.")
            return FALLBACK_COPY
    return FALLBACK_COPY

if __name__ == "__main__":
    print("✍️ Testing AI Copy Agent...")
    result = generate_copy(
        [{"title": "Campus Hall A"}],
        {"theme_name": "Tech Fusion"},
        "college tech fest",
        150
    )
    print(json.dumps(result, indent=2))