#!/usr/bin/env python3
"""
ALIAS Search Engine Integration Test Suite
Tests all available search engines and demonstrates usage
"""

from search_engines_api import FreeSearchEngine, INSTALL_INSTRUCTIONS
import sys

def test_basic_functionality():
    """Test basic search engine setup"""
    print("="*60)
    print("🔍 ALIAS Multi-Source Search Engine Test")
    print("="*60)
    print()
    
    # Initialize
    engine = FreeSearchEngine()
    
    # Show available engines
    print("📊 Available Search Engines:")
    for i, eng in enumerate(engine.get_available_engines(), 1):
        print(f"  {i}. {eng}")
    print()
    
    return engine

def test_search_queries(engine):
    """Test various search queries"""
    print("="*60)
    print("🧪 Testing Search Queries")
    print("="*60)
    print()
    
    test_queries = [
        "what is Python",
        "who invented the telephone",
        "capital of Japan",
        "what is artificial intelligence",
        "Albert Einstein"
    ]
    
    for query in test_queries:
        print(f"📝 Query: {query}")
        result = engine.search(query)
        
        if result.get('answer'):
            print(f"   ✅ Found answer via {result.get('engine', 'Unknown')}")
            print(f"   📄 Answer: {result['answer'][:100]}...")
            if result.get('source'):
                print(f"   🔗 Source: {result['source']}")
        else:
            print(f"   ⚠️  No results (may be rate limited)")
        print()

def test_structured_vs_formatted():
    """Test structured vs formatted output"""
    print("="*60)
    print("📦 Structured vs Formatted Output")
    print("="*60)
    print()
    
    engine = FreeSearchEngine()
    query = "what is machine learning"
    
    print("🔹 Structured Output (dictionary):")
    structured = engine.search(query)
    print(f"   Type: {type(structured)}")
    print(f"   Keys: {list(structured.keys())}")
    print()
    
    print("🔹 Formatted Output (string):")
    formatted = engine.search_and_format(query)
    if formatted:
        print(f"   {formatted[:200]}...")
    else:
        print("   (No results - may be rate limited)")
    print()

def test_searchapi_integration():
    """Test SearchApi.io integration (if key is available)"""
    print("="*60)
    print("🔑 SearchApi.io Integration Test")
    print("="*60)
    print()
    
    engine = FreeSearchEngine()
    
    # Try setting a dummy key to test the interface
    print("ℹ️  SearchApi.io requires a free API key")
    print("   Get yours at: https://www.searchapi.io/")
    print("   Usage: engine.set_searchapi_key('your-key-here')")
    print()
    
    # Check if user wants to test with their key
    print("💡 To test with your free API key, set it in this script")
    print("   or use: engine.set_searchapi_key('YOUR_KEY')")
    print()

def show_installation_guide():
    """Show installation instructions"""
    print("="*60)
    print("📚 Installation Guide")
    print("="*60)
    print()
    print(INSTALL_INSTRUCTIONS)

def main():
    """Run all tests"""
    print()
    print("╔" + "="*58 + "╗")
    print("║" + " "*10 + "ALIAS SEARCH ENGINE TEST SUITE" + " "*18 + "║")
    print("╚" + "="*58 + "╝")
    print()
    
    try:
        # Test 1: Basic functionality
        engine = test_basic_functionality()
        
        # Test 2: Search queries
        test_search_queries(engine)
        
        # Test 3: Output formats
        test_structured_vs_formatted()
        
        # Test 4: SearchApi.io
        test_searchapi_integration()
        
        # Show installation guide
        show_installation_guide()
        
        print("="*60)
        print("✅ Test suite completed!")
        print("="*60)
        print()
        print("💡 Tips:")
        print("  • DuckDuckGo may rate limit - this is normal")
        print("  • Install 'search-engines' for more sources")
        print("  • Get free SearchApi.io key for best results")
        print()
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
