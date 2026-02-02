"""
Find Poppler Installation Path
"""
import os
import glob

print("=" * 70)
print("SEARCHING FOR POPPLER INSTALLATION")
print("=" * 70)

# Check common paths
search_paths = [
    r"C:\ProgramData\chocolatey\lib\poppler",
    r"C:\Program Files\poppler",
    r"C:\poppler",
]

for base_path in search_paths:
    if os.path.exists(base_path):
        print(f"\n✅ Found base path: {base_path}")
        
        # Search for bin directories
        for root, dirs, files in os.walk(base_path):
            if 'bin' in dirs:
                bin_path = os.path.join(root, 'bin')
                # Check if pdftoppm.exe exists
                pdftoppm = os.path.join(bin_path, 'pdftoppm.exe')
                if os.path.exists(pdftoppm):
                    print(f"   ✅ FOUND WORKING PATH: {bin_path}")
                    print(f"      pdftoppm.exe exists: {pdftoppm}")
                else:
                    print(f"   ⚠️  Found bin dir but no pdftoppm.exe: {bin_path}")

print("\n" + "=" * 70)
print("RECOMMENDED ACTION:")
print("=" * 70)

# Try to find any pdftoppm.exe
print("\nSearching entire chocolatey folder for pdftoppm.exe...")
choco_base = r"C:\ProgramData\chocolatey"
if os.path.exists(choco_base):
    for root, dirs, files in os.walk(choco_base):
        if 'pdftoppm.exe' in files:
            print(f"✅ FOUND: {os.path.join(root, 'pdftoppm.exe')}")
            print(f"   Use this directory: {root}")
            break
else:
    print("❌ Chocolatey directory not found")
