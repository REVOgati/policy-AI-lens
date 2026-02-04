"""
POPPLER INSTALLATION GUIDE FOR WINDOWS
=======================================

OPTION 1: Manual Download (Recommended)
----------------------------------------
1. Download poppler for Windows:
   https://github.com/oschwartz10612/poppler-windows/releases/latest

   Download file: Release-XX.XX.X-X.zip (latest version)

2. Extract the ZIP file to:
   C:\\Program Files\\poppler\

   After extraction, you should see:
   C:\\Program Files\\poppler\\Library\bin\

3. Add to System PATH:
   - Press Win + X → System
   - Click "Advanced system settings"
   - Click "Environment Variables"
   - Under "System variables", find "Path"
   - Click "Edit"
   - Click "New"
   - Add: C:\\Program Files\\poppler\\Library\bin
   - Click OK on all windows

4. Restart terminal/VS Code


OPTION 2: Quick Test Without Installation
------------------------------------------
If you just want to test with text-based PDFs (like our sample),
you DON'T need poppler right now.

The PyMuPDF method should work for text-based PDFs.


VERIFY INSTALLATION:
-------------------
After installing, open a NEW terminal and run:
> pdftoppm -v

Should show version info if installed correctly.


WHAT POPPLER IS NEEDED FOR:
---------------------------
- Scanned insurance policies (images, not text)
- PDFs without embedded text
- When PyMuPDF can't extract text

For now, text-based PDFs work without poppler!
"""

import os
print(__doc__)

# Quick test
poppler_path = r"C:\Program Files\poppler\Library\bin"
if os.path.exists(poppler_path):
    print("✅ Poppler found at:", poppler_path)
else:
    print("⚠️  Poppler not installed yet")
    print("\nFor testing, you can continue without poppler.")
    print("PyMuPDF will handle text-based PDFs.")
