"""
Create a sample insurance policy PDF for testing
"""
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
except ImportError:
    print("Installing reportlab for PDF generation...")
    import subprocess
    subprocess.check_call(['pip', 'install', 'reportlab'])
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas

def create_sample_policy():
    filename = "sample_insurance_policy.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    
    # Title
    c.setFont("Helvetica-Bold", 20)
    c.drawString(200, 750, "Insurance Policy Document")
    
    # Policy Details
    c.setFont("Helvetica", 12)
    y = 700
    
    details = [
        "",
        "Client Name: John Doe",
        "Policy Number: POL-2024-987654",
        "Insurer Name: SafeGuard Insurance Company",
        "Sum Insured: $500,000",
        "Start Date: 2024-01-15",
        "Expiry Date: 2025-01-14",
        "Premium Amount: $2,500",
        "Policy Type: Life Insurance",
        "",
        "Terms and Conditions:",
        "This policy provides comprehensive life insurance coverage",
        "subject to the terms outlined in this document.",
    ]
    
    for line in details:
        c.drawString(100, y, line)
        y -= 20
    
    c.save()
    print(f"✅ Sample PDF created: {filename}")
    return filename

if __name__ == "__main__":
    create_sample_policy()
    print("\nYou can now run: python test_full_workflow.py")
    print("And use: sample_insurance_policy.pdf")
