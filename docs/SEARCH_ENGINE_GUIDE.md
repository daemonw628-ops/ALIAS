# Enhanced Search Engine Integration for ALIAS

## Overview

ALIAS now supports **multiple free search engine APIs** with automatic fallback! This means better search results with zero costs and no mandatory API keys.

## 🔍 Supported Search Engines

### 1. **DuckDuckGo Instant Answer API** ⭐ (Always Available)
- **Status**: Built-in, always works
- **Cost**: 100% FREE forever
- **API Key**: Not required
- **Best For**: Facts, definitions, quick answers
- **Quality**: Excellent for encyclopedic information
- **Setup**: Zero setup required!

### 2. **SearchApi.io** (Optional Enhancement)
- **Status**: Optional, enhances results
- **Cost**: FREE tier - 100 searches/month
- **API Key**: Optional (no credit card required)
- **Best For**: Real-time Google SERPs, structured data
- **Quality**: Excellent for current information, news, trending topics
- **Setup**: Get free API key at https://www.searchapi.io/
- **Features**:
  - Answer boxes (featured snippets)
  - Knowledge graphs
  - Organic search results
  - Real-time data

### 3. **search-engines Library** (Optional Enhancement)
- **Status**: Optional Python library
- **Cost**: 100% FREE
- **API Key**: Not required
- **Best For**: Multi-source scraping (Google, Bing, Yahoo, etc.)
- **Quality**: Good for finding relevant links
- **Setup**: `pip install search-engines`
- **Features**:
  - Scrapes multiple search engines
  - Full control over results
  - No API limitations

## 📦 Installation

### Basic (DuckDuckGo Only - Always Works)
```bash
# Already installed! No extra setup needed
python alias.py
```

### Enhanced (Multi-Source Search)
```bash
# Optional: Install search-engines library for more sources
pip install search-engines

# Optional: Get SearchApi.io key for even better results
# Visit: https://www.searchapi.io/ (free, no credit card)
```

## 🚀 Usage

### Automatic (Recommended)
ALIAS automatically uses the best available search engine:

1. **First**: Tries SearchApi.io (if API key is set) - best quality
2. **Second**: Tries DuckDuckGo Instant Answer - very reliable
3. **Third**: Tries search-engines library (if installed) - scraping fallback
4. **Result**: You always get an answer!

### Manual Configuration

#### Enable SearchApi.io (Optional):
```python
from ai_engine import FreeAIEngine

# Initialize ALIAS AI
ai = FreeAIEngine()

# Set your free SearchApi.io key
ai.search_tool.set_searchapi_key('your-free-api-key-here')

# Now you get 100 enhanced searches per month!
```

#### Check Available Engines:
```python
# See what search engines are currently active
engines = ai.search_tool.get_available_engines()
print(engines)
# Output: ['SearchApi.io (100 free searches/month)', 
#          'DuckDuckGo Instant Answer (always free)',
#          'Multi-Engine Scraper (Google, Bing, Yahoo)']
```

## 💡 Features & Benefits

### Auto-Fallback System
If one search engine fails, ALIAS automatically tries the next one:
```
SearchApi.io → DuckDuckGo → search-engines library → Success!
```

### Quality Results
- **Answer Boxes**: Featured snippets from Google
- **Knowledge Graphs**: Structured information cards
- **Instant Answers**: Direct facts and definitions
- **Source Links**: Always provides sources

### Zero Cost
- DuckDuckGo: Always free, unlimited
- SearchApi.io: 100 free searches/month
- search-engines: Unlimited free scraping

## 📊 Comparison Table

| Feature | DuckDuckGo | SearchApi.io | search-engines |
|---------|-----------|--------------|----------------|
| **Cost** | Free ∞ | Free 100/mo | Free ∞ |
| **API Key** | No | Optional | No |
| **Setup** | None | 2 minutes | `pip install` |
| **Quality** | Excellent | Excellent++ | Good |
| **Speed** | Fast | Fast | Medium |
| **Best For** | Facts, definitions | Current info, news | Link discovery |
| **Limitations** | No real-time data | 100/month free | Scraping-dependent |

## 🎯 Recommended Setup

### For Most Users (Zero Setup):
✅ Use DuckDuckGo (built-in)
- Already works
- Great results
- Zero configuration

### For Power Users:
✅ Add SearchApi.io API key
✅ Install search-engines library

```bash
# Get better results with zero cost
pip install search-engines

# Then in Python:
from ai_engine import FreeAIEngine
ai = FreeAIEngine()
ai.search_tool.set_searchapi_key('your-key')  # Optional but recommended
```

## 🔧 Advanced Usage

### Direct Search API
```python
from search_engines_api import FreeSearchEngine

# Create search engine
search = FreeSearchEngine()

# Simple search (formatted string)
result = search.search_and_format("who was Albert Einstein")
print(result)

# Structured search (dictionary)
data = search.search("capital of France")
print(data['answer'])    # "Paris is the capital..."
print(data['source'])    # URL source
print(data['engine'])    # Which engine was used

# Check available engines
engines = search.get_available_engines()
print(engines)
```

### Enable SearchApi.io
```python
# Set API key to enable SearchApi.io
search.set_searchapi_key('your-free-api-key')

# Now SearchApi.io will be tried first!
```

## 🆓 Getting Free API Keys

### SearchApi.io (Recommended):
1. Visit https://www.searchapi.io/
2. Sign up (no credit card required)
3. Get 100 free searches per month
4. Copy your API key
5. Use: `ai.search_tool.set_searchapi_key('your-key')`

That's it! Enjoy enhanced search with zero cost.

## 📈 Performance Tips

1. **Use DuckDuckGo for**: Encyclopedia facts, definitions, historical information
2. **Use SearchApi.io for**: Current events, news, trending topics, real-time data
3. **Use search-engines for**: Finding multiple sources, link discovery

## 🐛 Troubleshooting

### "search-engines library not installed"
```bash
pip install search-engines
```

### "SearchApi.io key not working"
- Check your key is correct
- Verify you haven't exceeded 100 searches/month
- Get a new key at https://www.searchapi.io/

### "No search results"
- DuckDuckGo always works as fallback
- Try rephrasing your query
- Check your internet connection

## 📝 Examples

### Basic Search:
```python
from ai_engine import FreeAIEngine

ai = FreeAIEngine()
response = ai.get_response("who was the first president", mode="Assistant")
print(response)
# Uses web search automatically if needed
```

### Direct Web Search:
```python
from search_engines_api import search_web

result = search_web("what is photosynthesis")
print(result)
# [Web Search via DuckDuckGo Instant Answer]
# Photosynthesis is the process by which green plants...
# Source: https://...
```

## 🎉 Summary

You now have **3 free search engines** working together:
1. ✅ **DuckDuckGo** - Always works, zero setup
2. ✅ **SearchApi.io** - 100 free searches/month (optional)
3. ✅ **search-engines** - Unlimited scraping (optional)

**Total cost: $0.00** 💰

All sources are completely free, no credit card ever required!
