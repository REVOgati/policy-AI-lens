"""
Test PDF Text Extraction
"""
import fitz  # PyMuPDF
import os

# Find the uploaded PDF
upload_dir = "uploads"
if os.path.exists(upload_dir):
    pdfs = [f for f in os.listdir(upload_dir) if f.endswith('.pdf')]
    
    if pdfs:
        pdf_path = os.path.join(upload_dir, pdfs[0])
        print(f"Testing: {pdf_path}\n")
        print("=" * 70)
        
        try:
            doc = fitz.open(pdf_path)
            print(f"✅ PDF opened successfully")
            print(f"   Pages: {len(doc)}")
            
            for page_num, page in enumerate(doc):
                text = page.get_text()
                print(f"\n📄 Page {page_num + 1}:")
                print(f"   Characters: {len(text)}")
                print(f"   Text preview:\n{text[:500]}")
                
            doc.close()
            
        except Exception as e:
            print(f"❌ Error: {e}")
    else:
        print("❌ No PDFs found in uploads directory")
        print("Please upload a PDF first via Swagger UI")
else:
    print("❌ Uploads directory doesn't exist")
