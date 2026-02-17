"""
Pydantic models for request/response validation.
"""
from typing import Optional

from pydantic import BaseModel, Field


class PolicyData(BaseModel):
    """Extracted insurance policy data."""
    policy_holder: Optional[str] = Field(
        None, description="Name of the policy holder")
    policy_number: Optional[str] = Field(
        None, description="Unique policy identifier")
    insurer_name: Optional[str] = Field(
        None, description="Name of the insurance company")
    sum_insured: Optional[str] = Field(None, description="Coverage amount")
    commencing_date: Optional[str] = Field(
        None, description="Policy commencing date (YYYY-MM-DD)")
    expiring_date: Optional[str] = Field(
        None, description="Policy expiring date (YYYY-MM-DD)")
    premium_amount: Optional[str] = Field(None, description="Premium amount")
    paid_amount: Optional[str] = Field(None, description="Amount paid by client")
    balance_amount: Optional[str] = Field(None, description="Balance amount due")
    policy_type: Optional[str] = Field(
        None, description="Type of insurance policy")
    registration_no: Optional[str] = Field(
        None, description="Vehicle registration number (NTSA Kenya)")
    contact: Optional[str] = Field(
        None, description="Contact information")
    vehicle_type: Optional[str] = Field(
        None, description="Type of vehicle (e.g., commercial, private, motorcycle)")


class ExtractionResponse(BaseModel):
    """Response from the extraction endpoint."""
    success: bool
    message: str
    data: Optional[PolicyData] = None
    extraction_id: Optional[str] = None


class VerificationRequest(BaseModel):
    """Request to verify and save policy data."""
    extraction_id: str
    verified_data: PolicyData
    edited_fields: list[str] = Field(default_factory=list)


class VerificationResponse(BaseModel):
    """Response from verification endpoint."""
    success: bool
    message: str
    accuracy_score: Optional[float] = None
    total_fields: int = 8  # Varies: 7 for non-COMP, 8 for COMP
    edited_fields_count: int = 0
