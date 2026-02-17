/**
 * TypeScript interfaces for Policy AI Lens
 */

export interface PolicyData {
  policy_holder: string | null;
  policy_number: string | null;
  insurer_name: string | null;
  sum_insured: string | null;
  commencing_date: string | null;
  expiring_date: string | null;
  premium_amount: string | null;
  paid_amount: string | null;
  balance_amount: string | null;
  policy_type: string | null;
  registration_no: string | null;
  contact: string | null;
  vehicle_type: string | null;
}

export interface ExtractionResponse {
  success: boolean;
  message: string;
  data: PolicyData;
  extraction_id: string;
}

export interface UploadResponse {
  success: boolean;
  message: string;
  file_id: string;
  filename: string;
}

export interface VerificationRequest {
  extraction_id: string;
  verified_data: PolicyData;
  edited_fields: string[];
}

export interface VerificationResponse {
  success: boolean;
  message: string;
  accuracy_score: number;
  total_fields: number;
  edited_fields_count: number;
}
