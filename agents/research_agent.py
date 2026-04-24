import json
import os
from dotenv import load_dotenv
from tavily import TavilyClient

# Load API keys from .env file
load_dotenv()
TAVILY_KEY = os.getenv("TAVILY_API_KEY")

def search_venues(event_type, location, budget):
    """
    Search for venues using Tavily web search.
    """
    tavily = TavilyClient(api_key=TAVILY_KEY)
    
    # Build a smart search query
    query = f"best event venues in {location} for {event_type} under ${budget} budget"
    
    print(f"🔍 Searching: {query}")
    
    # Run the search
    results = tavily.search(query, max_results=5)
    
    # Clean up and return useful info
    venues = []
    for result in results.get("results", []):
        venues.append({
            "title": result.get("title", "No title"),
            "url": result.get("url", ""),
            "snippet": result.get("content", "")[:200] + "..."
        })
    
    return venues
# Quick test when we run this file directly
if __name__ == "__main__":
    import json  # Add this at the top of the file too if not already there
    
    print("🧪 Testing Research Agent...")
    results = search_venues(
        event_type="college tech fest",
        location="Austin, TX",
        budget=3000
    )
    
    # Output as JSON (machine-readable format)
    output = {
        "query": "best event venues in Austin, TX for college tech fest under $3000 budget",
        "count": len(results),
        "venues": results
    }
    
    print("\n📦 JSON Output (for other agents):")
    print(json.dumps(output, indent=2))    
    print(f"\n✅ Found {len(results)} venue suggestions:\n")
    for i, venue in enumerate(results, 1):
        print(f"{i}. {venue['title']}")
        print(f"   {venue['snippet']}")
        print(f"   🔗 {venue['url']}\n")