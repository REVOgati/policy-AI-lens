from fastapi import Response
# Keepalive endpoint
@router.get("/keepalive")
async def keepalive():
    return Response(content="OK", status_code=200)
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from datetime import datetime
from fpdf import FPDF
import io
import os

router = APIRouter()

class ReceiptData(BaseModel):
    policy_number: str
    policy_holder: str
    policy_type: str
    commencing_date: str
    expiring_date: str
    premium_amount: str
    paid_amount: str
    balance_amount: str
    registration_no: str
    vehicle_type: str

@router.post("/generate", response_class=StreamingResponse)
async def generate_receipt(data: ReceiptData):
    try:
        pdf = FPDF()
        pdf.add_page()
        # Logo
        logo_path = os.path.join("app", "static", "logo.png")
        if os.path.exists(logo_path):
            pdf.image(logo_path, x=10, y=8, w=33)
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 40, "", ln=1)  # Space below logo

        # Title and date
        pdf.cell(0, 10, "Insurance Payment Receipt", ln=1, align="C")
        pdf.set_font("Arial", "", 12)
        pdf.cell(0, 10, f"Date: {datetime.now().strftime('%d/%m/%Y')}", ln=1, align="C")
        pdf.ln(10)

        # Receipt fields
        fields = [
            ("Policy Number", data.policy_number),
            ("Policy Holder", data.policy_holder),
            ("Policy Type", data.policy_type),
            ("Commencing Date", data.commencing_date),
            ("Expiring Date", data.expiring_date),
            ("Premium Amount (Kshs.)", data.premium_amount),
            ("Paid Amount (Kshs.)", data.paid_amount),
            ("Balance Amount (Kshs.)", data.balance_amount),
            ("Registration No", data.registration_no),
            ("Vehicle Type", data.vehicle_type),
        ]
        for label, value in fields:
            pdf.set_font("Arial", "B", 12)
            pdf.cell(60, 10, f"{label}:", border=0)
            pdf.set_font("Arial", "", 12)
            pdf.cell(0, 10, value, ln=1, border=0)

        # Space before signature section
        pdf.ln(10)

        # Kind Regards and Signatory
        pdf.set_font("Arial", "", 12)
        pdf.cell(0, 10, "Kind Regards,", ln=1)
        pdf.cell(0, 8, "George K. Tirop", ln=1)

        # Signature image
        signature_path = os.path.join("app", "static", "mainSignature.png")
        if os.path.exists(signature_path):
            # Place signature, resize to fit as signature (width ~40, keep aspect)
            y_before = pdf.get_y()
            pdf.image(signature_path, x=10, y=y_before, w=40)
            pdf.ln(22)  # Space after signature
        else:
            pdf.ln(18)

        # Thank you message (bold, centered)
        pdf.set_font("Arial", "B", 13)
        pdf.cell(0, 16, "Thank you for Choosing Totality Insurance Agency!", ln=1, align="C")

        # Output PDF to bytes
        pdf_bytes = pdf.output(dest="S").encode("latin1")
        return StreamingResponse(io.BytesIO(pdf_bytes), media_type="application/pdf", headers={
            "Content-Disposition": f"attachment; filename=receipt_{data.policy_number}.pdf"
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate receipt: {str(e)}")
