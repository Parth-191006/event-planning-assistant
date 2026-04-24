import os
from dotenv import load_dotenv
from pathlib import Path

# Get the exact path to your project folder
project_folder = Path(r"C:\Users\parth\event-planning-assistant")
env_path = project_folder / ".env"

print(f"🔍 Looking for .env at: {env_path}")
print(f"🔍 Does .env file exist there? {env_path.exists()}")

# Load using the exact path
load_dotenv(dotenv_path=env_path)

# Now check the keys
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
TAVILY_KEY = os.getenv("TAVILY_API_KEY")

print(f"\n✅ GEMINI_API_KEY found: {'Yes' if GEMINI_KEY else 'No'}")
print(f"✅ TAVILY_API_KEY found: {'Yes' if TAVILY_KEY else 'No'}")

if not GEMINI_KEY or not TAVILY_KEY:
    print("\n❌ API keys missing. Let's debug:")
    print(f"GEMINI value: {GEMINI_KEY}")
    print(f"TAVILY value: {TAVILY_KEY}")
    exit()

print("\n🎉 Both keys found! Testing connections...")

# Test Gemini
try:
    from google import genai
    client = genai.Client(api_key=GEMINI_KEY)
    resp = client.models.generate_content(
        model="gemini-2.0-flash",
        contents="Say: OK"
    )
    print("✅ Gemini connected!")
except Exception as e:
    print(f"❌ Gemini error: {e}")

# Test Tavily
try:
    from tavily import TavilyClient
    tavily = TavilyClient(api_key=TAVILY_KEY)
    result = tavily.search("test", max_results=1)
    print("✅ Tavily connected!")
except Exception as e:
    print(f"❌ Tavily error: {e}")

print("\n🎉 Phase 0 Complete!")