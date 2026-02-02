"""
Manual Poppler Installation Script
This will download and set up poppler properly
"""
import urllib.request
import zipfile
import os
import shutil

print("=" * 70)
print("POPPLER MANUAL INSTALLATION")
print("=" * 70)

# Download URL (latest Windows release)
POPPLER_URL = "https://github.com/oschwartz10612/poppler-windows/releases/download/v24.08.0-0/Release-24.08.0-0.zip"
DOWNLOAD_PATH = "poppler-windows.zip"
EXTRACT_TO = r"C:\Program Files\poppler"

print("\n1. Downloading poppler for Windows...")
print(f"   URL: {POPPLER_URL}")

try:
    urllib.request.urlretrieve(POPPLER_URL, DOWNLOAD_PATH)
    print(f"   ✅ Downloaded to: {DOWNLOAD_PATH}")
    
    print("\n2. Extracting...")
    print(f"   Target: {EXTRACT_TO}")
    
    # Create directory if it doesn't exist
    os.makedirs(EXTRACT_TO, exist_ok=True)
    
    # Extract zip
    with zipfile.ZipFile(DOWNLOAD_PATH, 'r') as zip_ref:
        zip_ref.extractall(EXTRACT_TO)
    
    print("   ✅ Extracted successfully")
    
    # Find bin directory
    print("\n3. Locating binaries...")
    for root, dirs, files in os.walk(EXTRACT_TO):
        if 'pdftoppm.exe' in files:
            print(f"   ✅ Found pdftoppm.exe at: {root}")
            print(f"\n   Use this path in your code:")
            print(f"   {root}")
            break
    
    # Cleanup
    os.remove(DOWNLOAD_PATH)
    print("\n✅ Installation complete!")
    
except PermissionError:
    print("\n❌ Permission denied!")
    print("   Please run this script as Administrator")
    print("   Or extract to a different location (e.g., project directory)")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\n   ALTERNATIVE: Manual installation")
    print("   1. Download: https://github.com/oschwartz10612/poppler-windows/releases")
    print("   2. Extract to: C:\\Program Files\\poppler")
    print("   3. The bin folder should contain pdftoppm.exe")
