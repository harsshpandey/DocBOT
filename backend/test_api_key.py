"""
Test script to verify Google API key is working.
Run this to check if your API key is valid.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
backend_dir = Path(__file__).parent
env_path = backend_dir / ".env"

if env_path.exists():
    load_dotenv(env_path, override=True)
    print(f"✓ Loaded .env file from: {env_path}\n")
else:
    print(f"✗ .env file not found at {env_path}\n")
    print("Please create .env file first!")
    exit(1)

# Get API key
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("✗ GOOGLE_API_KEY not found in environment variables")
    print("\nPlease check your .env file contains:")
    print("GOOGLE_API_KEY=your-actual-api-key-here")
    exit(1)

print(f"✓ Found API key: {api_key[:10]}...{api_key[-5:]}\n")

# Test 1: Test Google Generative AI (Gemini) API
print("Testing Google Generative AI (Gemini) API...")
try:
    import google.generativeai as genai
    
    genai.configure(api_key=api_key)
    
    # Try to list models (simple API call)
    models = genai.list_models()
    model_names = [m.name for m in models]
    
    print(f"✓ Gemini API connection successful!")
    print(f"  Available models: {len(model_names)} models found")
    
    # Check for specific models we need
    embedding_model = os.getenv("GOOGLE_EMBEDDING_MODEL", "models/embedding-001")
    llm_model = os.getenv("GOOGLE_LLM_MODEL", "gemini-2.0-flash-lite")
    
    if embedding_model in model_names:
        print(f"  ✓ Embedding model '{embedding_model}' is available")
    else:
        print(f"  ⚠ Embedding model '{embedding_model}' not found in available models")
    
    if llm_model in model_names:
        print(f"  ✓ LLM model '{llm_model}' is available")
    else:
        print(f"  ⚠ LLM model '{llm_model}' not found in available models")
        print(f"  Available Gemini models: {[m for m in model_names if 'gemini' in m.lower()][:5]}")
    
    # Try a simple generation test
    print("\n  Testing text generation...")
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content("Say 'Hello' in one word.")
    print(f"  ✓ Generation test successful: {response.text.strip()}")
    
except ImportError:
    print("  ⚠ google-generativeai package not installed")
    print("  Install with: pip install google-generativeai")
except Exception as e:
    print(f"  ✗ Gemini API test failed: {e}")
    print(f"  Error type: {type(e).__name__}")
    if "API_KEY_INVALID" in str(e) or "invalid" in str(e).lower():
        print("\n  ⚠ Your API key appears to be invalid!")
        print("  Please check:")
        print("  1. The key is correct (no extra spaces or quotes)")
        print("  2. The key has the right permissions")
        print("  3. You're using a valid Google AI Studio API key")

# Test 2: Test with LangChain Google GenAI (what the app actually uses)
print("\n" + "="*50)
print("Testing LangChain Google GenAI integration...")
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    
    llm = ChatGoogleGenerativeAI(
        model=os.getenv("GOOGLE_LLM_MODEL", "gemini-pro"),
        google_api_key=api_key,
        temperature=0.3,
    )
    
    response = llm.invoke("Say 'test' in one word.")
    print(f"✓ LangChain ChatGoogleGenerativeAI test successful!")
    print(f"  Response: {response.content}")
    
except ImportError:
    print("  ⚠ langchain-google-genai package not installed")
except Exception as e:
    print(f"  ✗ LangChain test failed: {e}")
    print(f"  Error type: {type(e).__name__}")

# Test 3: Test Embeddings API
print("\n" + "="*50)
print("Testing Google Embeddings API...")
try:
    from langchain_google_genai import GoogleGenerativeAIEmbeddings
    
    embeddings = GoogleGenerativeAIEmbeddings(
        model=os.getenv("GOOGLE_EMBEDDING_MODEL", "models/embedding-001"),
        google_api_key=api_key,
    )
    
    # Test embedding generation
    test_text = "This is a test"
    result = embeddings.embed_query(test_text)
    print(f"✓ Embeddings API test successful!")
    print(f"  Generated embedding vector of length: {len(result)}")
    
except ImportError:
    print("  ⚠ langchain-google-genai package not installed")
except Exception as e:
    print(f"  ✗ Embeddings API test failed: {e}")
    print(f"  Error type: {type(e).__name__}")
    if "API_KEY_INVALID" in str(e) or "invalid" in str(e).lower():
        print("\n  ⚠ Your API key appears to be invalid for embeddings!")

print("\n" + "="*50)
print("Test complete!")
print("\nIf all tests passed (✓), your API key is working correctly.")
print("If any tests failed (✗), check the error messages above.")

