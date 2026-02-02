"""
Manual Poppler Path Finder - Step by Step
"""
import os

print("=" * 70)
print("MANUAL POPPLER DIAGNOSTIC")
print("=" * 70)

# Step 1: Check base directory
base = r"C:\ProgramData\chocolatey\lib\poppler\tools"
print(f"\n1. Checking base directory: {base}")
if os.path.exists(base):
    print("   ✅ Base directory EXISTS")
    
    # Step 2: List contents
    print("\n2. Contents of base directory:")
    try:
        contents = os.listdir(base)
        for item in contents:
            full_path = os.path.join(base, item)
            item_type = "DIR" if os.path.isdir(full_path) else "FILE"
            print(f"   - {item} ({item_type})")
    except Exception as e:
        print(f"   ❌ Error listing directory: {e}")
    
    # Step 3: Search recursively for any .exe files
    print("\n3. Searching for ALL .exe files:")
    for root, dirs, files in os.walk(base):
        exe_files = [f for f in files if f.endswith('.exe')]
        if exe_files:
            print(f"\n   📁 {root}")
            for exe in exe_files:
                print(f"      - {exe}")
    
    # Step 4: Specifically look for pdftoppm.exe
    print("\n4. Searching specifically for pdftoppm.exe:")
    found = False
    for root, dirs, files in os.walk(base):
        if 'pdftoppm.exe' in files:
            found = True
            pdftoppm_path = os.path.join(root, 'pdftoppm.exe')
            print(f"   ✅ FOUND: {pdftoppm_path}")
            print(f"   📂 Directory to use: {root}")
            
            # Test if file is accessible
            if os.path.exists(pdftoppm_path):
                print(f"   ✅ File is accessible")
                size = os.path.getsize(pdftoppm_path)
                print(f"   📊 File size: {size:,} bytes")
            break
    
    if not found:
        print("   ❌ pdftoppm.exe NOT FOUND in entire directory tree")
        print("\n   This means poppler was not properly extracted.")
        print("   Solution: Manually download and extract poppler")
        print("   URL: https://github.com/oschwartz10612/poppler-windows/releases")
    
else:
    print("   ❌ Base directory DOES NOT EXIST")
    print("   Poppler is not installed via Chocolatey")

# Step 5: Check alternative locations
print("\n5. Checking alternative locations:")
alt_paths = [
    r"C:\Program Files\poppler",
    r"C:\poppler",
]

for path in alt_paths:
    if os.path.exists(path):
        print(f"   ✅ Found: {path}")
    else:
        print(f"   ❌ Not found: {path}")

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
