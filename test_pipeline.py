# test_pipeline.py - Simple test of Research → Design flow
from agents.research_agent import search_venues
from agents.design_agent import generate_theme
import json

print("🚀 Testing Agent Pipeline: Research → Design\n")

# Step 1: Research venues
print("🔍 Step 1: Researching venues...")
venues = search_venues(
    event_type="college tech fest",
    location="Austin, TX",
    budget=3000
)
print(f"✅ Found {len(venues)} venues\n")

# Step 2: Generate theme based on research
print("🎨 Step 2: Generating theme...")
theme = generate_theme(
    venue_data=venues,
    event_type="college tech fest",
    theme_preference="cyberpunk"
)

# Step 3: Show combined output
print("\n📦 Combined Output:")
output = {
    "venues": venues,
    "theme": theme
}
print(json.dumps(output, indent=2))

print("\n✅ Pipeline test complete!")