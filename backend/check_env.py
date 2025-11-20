"""
Quick script to check what's in your .env file (without showing the actual key value).
"""
from pathlib import Path
from dotenv import load_dotenv
import os

backend_dir = Path(__file__).parent
env_path = backend_dir / ".env"

print(f"Checking .env file at: {env_path}\n")

if not env_path.exists():
    print("✗ .env file does not exist!")
    print(f"Create it by copying env.example:")
    print(f"  copy {backend_dir / 'env.example'} {env_path}")
    exit(1)

print("✓ .env file exists\n")

# Read the file to check format
with open(env_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("Checking .env file contents:\n")
found_api_key = False
for i, line in enumerate(lines, 1):
    line = line.strip()
    
    # Skip empty lines and comments
    if not line or line.startswith('#'):
        continue
    
    # Check for GOOGLE_API_KEY
    if 'GOOGLE_API_KEY' in line.upper():
        found_api_key = True
        if '=' in line:
            parts = line.split('=', 1)
            key_name = parts[0].strip()
            value = parts[1].strip() if len(parts) > 1 else ""
            
            print(f"Line {i}: Found GOOGLE_API_KEY")
            print(f"  Key name: '{key_name}'")
            
            if not value:
                print(f"  ✗ ERROR: Value is empty!")
            elif value == "your-google-api-key-here":
                print(f"  ✗ ERROR: Still has placeholder value!")
                print(f"  Please replace with your actual API key")
            elif len(value) < 20:
                print(f"  ⚠ WARNING: Value seems too short ({len(value)} chars)")
                print(f"  Google API keys are usually 39+ characters")
            else:
                print(f"  ✓ Value is set (length: {len(value)} chars)")
                print(f"  First 10 chars: {value[:10]}...")
                print(f"  Last 5 chars: ...{value[-5:]}")
                
            # Check for common issues
            if value.startswith('"') and value.endswith('"'):
                print(f"  ⚠ WARNING: Value has quotes - remove them!")
            if value.startswith("'") and value.endswith("'"):
                print(f"  ⚠ WARNING: Value has single quotes - remove them!")
            if ' ' in key_name:
                print(f"  ⚠ WARNING: Key name has spaces!")
        else:
            print(f"  ✗ ERROR: No '=' sign found in line")
    else:
        # Show other variables (but not their values if they look like keys)
        if '=' in line:
            key = line.split('=')[0].strip()
            if 'KEY' in key.upper() or 'SECRET' in key.upper() or 'PASSWORD' in key.upper():
                print(f"Line {i}: {key}=***hidden***")
            else:
                print(f"Line {i}: {line[:60]}...")

if not found_api_key:
    print("\n✗ GOOGLE_API_KEY not found in .env file!")
    print("\nYour .env file should contain a line like:")
    print("GOOGLE_API_KEY=AIzaSy...your-actual-key...")
    print("\nMake sure:")
    print("1. The line starts with GOOGLE_API_KEY")
    print("2. There's an = sign")
    print("3. Your actual API key is after the = sign")
    print("4. No quotes around the value")
    print("5. No spaces around the = sign")

print("\n" + "="*60)
print("Now testing if environment variable loads correctly...\n")

load_dotenv(env_path, override=True)
api_key = os.getenv("GOOGLE_API_KEY")

if api_key:
    print(f"✓ Environment variable loaded successfully!")
    print(f"  Length: {len(api_key)} characters")
else:
    print("✗ Environment variable not loaded")
    print("\nPossible issues:")
    print("1. Variable name mismatch (case sensitivity)")
    print("2. Value is empty")
    print("3. File encoding issue")

