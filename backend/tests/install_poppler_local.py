"""
Install Poppler in Project Directory (No Admin Required)
"""
import urllib.request
import zipfile
import os

print("=" * 70)
print("INSTALLING POPPLER IN PROJECT DIRECTORY")
print("=" * 70)

# Download URL
POPPLER_URL = "https://github.com/oschwartz10612/poppler-windows/releases/download/v24.08.0-0/Release-24.08.0-0.zip"
DOWNLOAD_PATH = "poppler-windows.zip"
EXTRACT_TO = "poppler"  # Local directory

print("\n1. Downloading poppler...")
try:
    print(f"   Downloading from GitHub... (this may take a minute)")
    urllib.request.urlretrieve(POPPLER_URL, DOWNLOAD_PATH)
    print(f"   ✅ Downloaded: {DOWNLOAD_PATH}")

    print("\n2. Extracting to project directory...")
    with zipfile.ZipFile(DOWNLOAD_PATH, 'r') as zip_ref:
        zip_ref.extractall(EXTRACT_TO)
    print(f"   ✅ Extracted to: {os.path.abspath(EXTRACT_TO)}")

    print("\n3. Finding binaries...")
    for root, dirs, files in os.walk(EXTRACT_TO):
        if 'pdftoppm.exe' in files:
            bin_path = root
            print(f"   ✅ Binaries found at: {os.path.abspath(bin_path)}")
            print(f"\n   Full path to use: {os.path.abspath(bin_path)}")
            break

    # Cleanup
    os.remove(DOWNLOAD_PATH)
    print("\n✅ Installation complete!")
    print("\n📝 The OCR service will automatically detect this installation.")

except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
