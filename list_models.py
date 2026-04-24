import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

print("🔍 Listing available Gemini models for your key...\n")
try:
    models = client.models.list()
    for m in models:
        if "generateContent" in m.supported_generation_methods:
            print(f"✅ {m.name}  (supports text generation)")
except Exception as e:
    print(f"❌ Error listing models: {e}")
    print("\n💡 Trying common model names manually...")
    common_models = [
        "gemini-pro",
        "gemini-1.5-pro-001", 
        "gemini-1.5-flash-001",
        "gemini-2.0-flash-exp"
    ]
    for model_name in common_models:
        try:
            resp = client.models.generate_content(
                model=model_name,
                contents="test",
                config={"response_mime_type": "text/plain"}
            )
            print(f"✅ {model_name} WORKS!")
            break
        except Exception as e:
            print(f"❌ {model_name}: {str(e)[:60]}...")