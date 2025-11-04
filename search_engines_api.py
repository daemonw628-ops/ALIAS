"""
Multi-Source Free Search Engine API Integration for ALIAS
Supports: SearchApi.io, search-engines library, DuckDuckGo, and more
All completely FREE with no API keys required for basic usage
"""

import requests
from urllib.parse import quote
from html import unescape
from typing import Dict, List, Optional
import logging
import json

logger = logging.getLogger(__name__)


class FreeSearchEngine:
    """
    Unified interface for multiple free search engine APIs
    Auto-fallback system: Tries each API in order until one succeeds
    """
    
    def __init__(self):
        """Initialize all available search engines"""
        self.headers = {
            'User-Agent': 'ALIAS/1.0 (Educational AI Assistant; https://github.com/daemonw628-ops/ALIAS)'
        }
        
        # SearchApi.io - Free tier available (optional API key for more requests)
        self.searchapi_key = None  # Set to enable SearchApi.io
        
        # Check if search-engines library is available
        self.search_engines_available = False
        try:
            import search_engines as se
            self.search_engines = se
            self.search_engines_available = True
            logger.info("search-engines library detected - multi-engine support enabled")
        except ImportError:
            logger.info("search-engines library not installed (optional)")
        
        # Available search engines in priority order
        self.engines = [
            'duckduckgo',      # Free, no API key, instant answers
            'searchapi',       # Free tier, structured results
            'search_engines',  # Library-based scraping
        ]
        
    def search(self, query: str, max_results: int = 1) -> Dict[str, any]:
        """
        Search using the best available engine
        Returns structured result with answer, source, and metadata
        """
        
        # Try each engine in order
        for engine in self.engines:
            try:
                if engine == 'duckduckgo':
                    result = self._search_duckduckgo(query)
                    if result.get('answer'):
                        result['engine'] = 'DuckDuckGo Instant Answer'
                        return result
                
                elif engine == 'searchapi' and self.searchapi_key:
                    result = self._search_searchapi(query, max_results)
                    if result.get('answer'):
                        result['engine'] = 'SearchApi.io'
                        return result
                
                elif engine == 'search_engines' and self.search_engines_available:
                    result = self._search_with_library(query, max_results)
                    if result.get('answer'):
                        result['engine'] = 'Multi-Engine Scraper'
                        return result
                        
            except Exception as e:
                logger.warning(f"Search engine {engine} failed: {e}")
                continue
        
        # No results from any engine
        return {
            'answer': '',
            'error': 'No search results available',
            'engine': 'none'
        }
    
    def _search_duckduckgo(self, query: str) -> Dict[str, str]:
        """
        DuckDuckGo Instant Answer API
        Free, no API key, excellent for facts and definitions
        """
        try:
            api_url = f"https://api.duckduckgo.com/?q={quote(query)}&format=json&no_html=1&skip_disambig=1"
            response = requests.get(api_url, headers=self.headers, timeout=5)
            
            if response.status_code != 200:
                return {'answer': ''}
            
            data = response.json()
            
            # Try Abstract (best for informational queries)
            if data.get('Abstract'):
                return {
                    'answer': unescape(data['Abstract']),
                    'source': data.get('AbstractURL', ''),
                    'title': data.get('Heading', query)
                }
            
            # Try Answer (for quick facts)
            if data.get('Answer'):
                answer_text = unescape(data['Answer'])
                return {
                    'answer': answer_text,
                    'source': data.get('AbstractURL', ''),
                    'title': query
                }
            
            # Try Definition
            if data.get('Definition'):
                return {
                    'answer': data['Definition'],
                    'source': data.get('DefinitionURL', ''),
                    'title': query
                }
            
            # Try RelatedTopics
            if data.get('RelatedTopics') and len(data['RelatedTopics']) > 0:
                first_topic = data['RelatedTopics'][0]
                if isinstance(first_topic, dict) and first_topic.get('Text'):
                    return {
                        'answer': first_topic['Text'],
                        'source': first_topic.get('FirstURL', ''),
                        'title': query
                    }
            
        except Exception as e:
            logger.error(f"DuckDuckGo search error: {e}")
            return {'answer': '', 'error': str(e)}
        
        return {'answer': ''}
    
    def _search_searchapi(self, query: str, max_results: int = 1) -> Dict[str, str]:
        """
        SearchApi.io - Real-time Google SERP API
        Free tier: 100 searches/month without credit card
        Returns structured JSON results
        """
        if not self.searchapi_key:
            return {'answer': ''}
        
        try:
            # SearchApi.io endpoint for Google search
            api_url = "https://www.searchapi.io/api/v1/search"
            params = {
                'engine': 'google',
                'q': query,
                'api_key': self.searchapi_key,
                'num': max_results
            }
            
            response = requests.get(api_url, params=params, timeout=10)
            
            if response.status_code != 200:
                return {'answer': ''}
            
            data = response.json()
            
            # Try answer box (featured snippet)
            if data.get('answer_box'):
                box = data['answer_box']
                answer = box.get('answer') or box.get('snippet')
                if answer:
                    return {
                        'answer': answer,
                        'source': box.get('link', ''),
                        'title': box.get('title', query)
                    }
            
            # Try knowledge graph
            if data.get('knowledge_graph'):
                kg = data['knowledge_graph']
                description = kg.get('description')
                if description:
                    return {
                        'answer': description,
                        'source': kg.get('source', {}).get('link', ''),
                        'title': kg.get('title', query)
                    }
            
            # Try organic results
            if data.get('organic_results') and len(data['organic_results']) > 0:
                first = data['organic_results'][0]
                return {
                    'answer': first.get('snippet', ''),
                    'source': first.get('link', ''),
                    'title': first.get('title', query)
                }
                
        except Exception as e:
            logger.error(f"SearchApi.io error: {e}")
            return {'answer': '', 'error': str(e)}
        
        return {'answer': ''}
    
    def _search_with_library(self, query: str, max_results: int = 1) -> Dict[str, str]:
        """
        search-engines library - Multi-engine scraping
        Tries Google, Bing, Yahoo, etc. in sequence
        DIY scraping with full control
        """
        if not self.search_engines_available:
            return {'answer': ''}
        
        try:
            # Try Google first (most reliable)
            google = self.search_engines.Google()
            results = google.search(query, pages=1)
            links = list(results.links())
            
            if links:
                # Get the first result and fetch its content
                # Note: We can't easily extract snippets without additional parsing
                # So we return the URL and let the user know
                return {
                    'answer': f"Found relevant information at: {links[0]}",
                    'source': links[0],
                    'title': query,
                    'note': 'Visit the link for full details'
                }
            
            # Fallback to Bing
            bing = self.search_engines.Bing()
            results = bing.search(query, pages=1)
            links = list(results.links())
            
            if links:
                return {
                    'answer': f"Found relevant information at: {links[0]}",
                    'source': links[0],
                    'title': query,
                    'note': 'Visit the link for full details'
                }
                
        except Exception as e:
            logger.error(f"search-engines library error: {e}")
            return {'answer': '', 'error': str(e)}
        
        return {'answer': ''}
    
    def search_and_format(self, query: str) -> str:
        """
        Search and return a nicely formatted response
        This is the main method to use from ALIAS
        """
        result = self.search(query)
        
        if not result.get('answer'):
            return ""
        
        # Format the response
        output = f"[Web Search via {result.get('engine', 'Unknown')}]\n\n"
        output += f"{result['answer']}"
        
        if result.get('source'):
            output += f"\n\nSource: {result['source']}"
        
        if result.get('note'):
            output += f"\n\n💡 {result['note']}"
        
        return output
    
    def set_searchapi_key(self, api_key: str):
        """
        Set SearchApi.io API key to enable enhanced search
        Free tier: 100 searches/month, no credit card required
        Get your key at: https://www.searchapi.io/
        """
        self.searchapi_key = api_key
        if api_key:
            # Move searchapi higher in priority if key is set
            if 'searchapi' in self.engines:
                self.engines.remove('searchapi')
                self.engines.insert(0, 'searchapi')
            logger.info("SearchApi.io enabled with API key")
    
    def get_available_engines(self) -> List[str]:
        """Return list of currently available search engines"""
        available = []
        
        # DuckDuckGo is always available
        available.append('DuckDuckGo Instant Answer (always free)')
        
        # SearchApi.io if key is set
        if self.searchapi_key:
            available.append('SearchApi.io (100 free searches/month)')
        
        # search-engines library if installed
        if self.search_engines_available:
            available.append('Multi-Engine Scraper (Google, Bing, Yahoo)')
        
        return available


# Convenience functions for easy integration
def search_web(query: str) -> str:
    """Quick search function - returns formatted string"""
    engine = FreeSearchEngine()
    return engine.search_and_format(query)


def search_web_structured(query: str) -> Dict:
    """Search and return structured data"""
    engine = FreeSearchEngine()
    return engine.search(query)


# Installation instructions
INSTALL_INSTRUCTIONS = """
🔍 Enhanced Search Engine Setup for ALIAS

Current Status:
✅ DuckDuckGo Instant Answer - Always available (free, no setup)

Optional Enhancements:

1️⃣ SearchApi.io (Recommended)
   • Free tier: 100 searches/month, no credit card
   • Get API key: https://www.searchapi.io/
   • Setup: engine.set_searchapi_key('your-key-here')
   • Benefit: Real-time Google SERPs, structured results

2️⃣ search-engines Library
   • Install: pip install search-engines
   • No API key needed
   • Benefit: Multi-engine scraping (Google, Bing, Yahoo)

All options remain completely FREE!
"""

if __name__ == "__main__":
    # Demo and testing
    print("🔍 ALIAS Free Search Engine API Demo\n")
    
    engine = FreeSearchEngine()
    print(f"Available engines: {', '.join(engine.get_available_engines())}\n")
    
    # Test search
    test_query = "who was Albert Einstein"
    print(f"Testing search: '{test_query}'\n")
    
    result = engine.search_and_format(test_query)
    if result:
        print(result)
    else:
        print("No results found")
    
    print("\n" + "="*60)
    print(INSTALL_INSTRUCTIONS)
