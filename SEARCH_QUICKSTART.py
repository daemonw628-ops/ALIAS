#!/usr/bin/env python3
"""
Quick Start Guide: Using Free Search Engine APIs in ALIAS
Demonstrates all three search options with examples
"""

print("""
╔══════════════════════════════════════════════════════════════════════╗
║          ALIAS - Multi-Source Free Search Engine Integration         ║
║                        Quick Start Guide                              ║
╚══════════════════════════════════════════════════════════════════════╝

You now have THREE free search engines integrated into ALIAS!

┌──────────────────────────────────────────────────────────────────────┐
│ 1️⃣  DuckDuckGo Instant Answer API (Built-in)                         │
├──────────────────────────────────────────────────────────────────────┤
│ • Status: ✅ Always available                                        │
│ • Cost: 🆓 100% FREE forever                                         │
│ • Setup: ❌ None needed                                              │
│ • Best for: Facts, definitions, encyclopedic info                    │
│ • Limits: Rate limiting may occur (normal for free API)              │
└──────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────┐
│ 2️⃣  SearchApi.io (Optional Enhancement)                              │
├──────────────────────────────────────────────────────────────────────┤
│ • Status: 🔓 Optional                                                │
│ • Cost: 🆓 100 searches/month FREE                                   │
│ • Setup: ⚡ 2 minutes                                                │
│ • Best for: Real-time Google SERPs, news, current events             │
│ • Get key: https://www.searchapi.io/ (no credit card)               │
└──────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────┐
│ 3️⃣  search-engines Library (Optional Enhancement)                    │
├──────────────────────────────────────────────────────────────────────┤
│ • Status: 🔓 Optional                                                │
│ • Cost: 🆓 100% FREE forever                                         │
│ • Setup: pip install search-engines                                  │
│ • Best for: Multi-source scraping (Google, Bing, Yahoo, etc.)        │
│ • Limits: None - scraping based                                      │
└──────────────────────────────────────────────────────────────────────┘

════════════════════════════════════════════════════════════════════════
                            USAGE EXAMPLES
════════════════════════════════════════════════════════════════════════

📝 Example 1: Basic Usage (Already Works!)
─────────────────────────────────────────────────────────────────────────
""")

print("""
from ai_engine import FreeAIEngine

# Initialize ALIAS
ai = FreeAIEngine()

# Ask a question - search happens automatically!
response = ai.get_response("who was Albert Einstein", mode="Assistant")
print(response)

# Search is already integrated into ALIAS's knowledge system!
""")

print("""
────────────────────────────────────────────────────────────────────────

📝 Example 2: Direct Web Search
─────────────────────────────────────────────────────────────────────────
""")

print("""
from search_engines_api import search_web

# Quick search - returns formatted string
result = search_web("what is Python programming")
print(result)

# Output:
# [Web Search via DuckDuckGo Instant Answer]
# Python is a high-level programming language...
# Source: https://...
""")

print("""
────────────────────────────────────────────────────────────────────────

📝 Example 3: Enable SearchApi.io (100 free searches/month)
─────────────────────────────────────────────────────────────────────────
""")

print("""
from ai_engine import FreeAIEngine

# Initialize ALIAS
ai = FreeAIEngine()

# Enable SearchApi.io with your free key
ai.search_tool.set_searchapi_key('your-free-api-key-here')

# Now you get enhanced results!
# SearchApi.io will be tried first, then DuckDuckGo as fallback

print("Available engines:", ai.search_tool.get_available_engines())
# Output: ['SearchApi.io (100 free searches/month)', 
#          'DuckDuckGo Instant Answer (always free)']
""")

print("""
────────────────────────────────────────────────────────────────────────

📝 Example 4: Install search-engines Library (More Sources)
─────────────────────────────────────────────────────────────────────────
""")

print("""
# In terminal:
$ pip install search-engines

# In Python:
from ai_engine import FreeAIEngine

ai = FreeAIEngine()
print("Available engines:", ai.search_tool.get_available_engines())

# Output: ['DuckDuckGo Instant Answer (always free)',
#          'Multi-Engine Scraper (Google, Bing, Yahoo)']

# Now ALIAS can scrape multiple search engines!
""")

print("""
────────────────────────────────────────────────────────────────────────

📝 Example 5: Advanced - Using FreeSearchEngine Directly
─────────────────────────────────────────────────────────────────────────
""")

print("""
from search_engines_api import FreeSearchEngine

# Create search engine instance
search = FreeSearchEngine()

# Get structured results (dictionary)
result = search.search("capital of France")
print(f"Answer: {result['answer']}")
print(f"Source: {result['source']}")
print(f"Engine: {result['engine']}")

# Get formatted results (string)
formatted = search.search_and_format("capital of France")
print(formatted)

# Check available engines
engines = search.get_available_engines()
for eng in engines:
    print(f"  • {eng}")
""")

print("""
════════════════════════════════════════════════════════════════════════
                         INSTALLATION STEPS
════════════════════════════════════════════════════════════════════════

✅ OPTION A: Basic (Already Works - No Setup!)
   Just use ALIAS as normal - DuckDuckGo is built-in
   
🚀 OPTION B: Enhanced with SearchApi.io (Recommended)
   1. Visit https://www.searchapi.io/
   2. Sign up (free, no credit card)
   3. Copy your API key
   4. In Python:
      from ai_engine import FreeAIEngine
      ai = FreeAIEngine()
      ai.search_tool.set_searchapi_key('your-key')
   5. Done! Now you have 100 enhanced searches per month
   
⚡ OPTION C: Maximum Power (All Sources)
   1. Install search-engines library:
      $ pip install search-engines
   2. Get SearchApi.io key (steps above)
   3. Set the key in ALIAS
   4. Now you have ALL THREE engines working together!

════════════════════════════════════════════════════════════════════════
                            COMPARISON
════════════════════════════════════════════════════════════════════════

┌─────────────────┬─────────────┬──────────────┬─────────────────┐
│ Feature         │ DuckDuckGo  │ SearchApi.io │ search-engines  │
├─────────────────┼─────────────┼──────────────┼─────────────────┤
│ Cost            │ Free ∞      │ Free 100/mo  │ Free ∞          │
│ API Key         │ No          │ Yes (free)   │ No              │
│ Setup Time      │ 0 min       │ 2 min        │ 1 min           │
│ Quality         │ Excellent   │ Excellent++  │ Good            │
│ Best For        │ Facts       │ Current info │ Link discovery  │
│ Speed           │ Fast        │ Fast         │ Medium          │
│ Real-time Data  │ No          │ Limited      │ Limited         │
│ Always Works    │ Yes         │ 100/month    │ Yes             │
└─────────────────┴─────────────┴──────────────┴─────────────────┘

════════════════════════════════════════════════════════════════════════
                          TROUBLESHOOTING
════════════════════════════════════════════════════════════════════════

❓ "No search results found"
   → DuckDuckGo may be rate limiting (normal)
   → Try again in a few seconds
   → Install search-engines for more sources
   → Get SearchApi.io key for better reliability

❓ "search-engines library not found"
   → Install it: pip install search-engines
   → Restart ALIAS
   → Now you have multi-engine support

❓ "SearchApi.io key not working"
   → Check you copied the full key
   → Verify you haven't used 100 searches this month
   → Key resets monthly - get a new one free at searchapi.io

❓ "How do I know which engine was used?"
   → Search results show the engine name
   → Example: [Web Search via DuckDuckGo Instant Answer]

════════════════════════════════════════════════════════════════════════
                            MORE INFO
════════════════════════════════════════════════════════════════════════

📚 Full Documentation: docs/SEARCH_ENGINE_GUIDE.md
🧪 Test Suite: python test_search_engines.py
💻 Source Code: search_engines_api.py
🤖 Integration: ai_engine.py (WebSearchTool class)

════════════════════════════════════════════════════════════════════════

🎉 SUMMARY

You now have a sophisticated multi-source search system that:
  ✅ Works immediately (DuckDuckGo built-in)
  ✅ Can be enhanced with SearchApi.io (100 free/month)
  ✅ Can scrape multiple engines (search-engines library)
  ✅ Auto-fallback (tries each source until success)
  ✅ ALL COMPLETELY FREE - no credit card ever required!

Total cost: $0.00 forever! 💰

════════════════════════════════════════════════════════════════════════

Ready to try it? Just run:
  python alias.py

Or test the search engines:
  python test_search_engines.py

Enjoy your enhanced ALIAS! 🚀
""")
