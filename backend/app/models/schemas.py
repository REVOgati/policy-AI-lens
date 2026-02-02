"""
Pydantic models for request/response validation.
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class PolicyData(BaseModel):
    """Extracted insurance policy data."""
    client_name: Optional[str] = Field(None, description="Name of the policy holder")
    policy_number: Optional[str] = Field(None, description="Unique policy identifier")
    insurer_name: Optional[str] = Field(None, description="Name of the insurance company")
    sum_insured: Optional[str] = Field(None, description="Coverage amount")
    start_date: Optional[str] = Field(None, description="Policy start date")
    expiry_date: Optional[str] = Field(None, description="Policy expiry date")
    premium_amount: Optional[str] = Field(None, description="Premium amount")
    policy_type: Optional[str] = Field(None, description="Type of insurance policy")


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
    total_fields: int = 8
    edited_fields_count: int = 0
