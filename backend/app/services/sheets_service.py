"""
Google Sheets service for storing policy extraction results.
Uses service account authentication to write verified data to Google Sheets.
"""
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
import logging

from app.config import get_settings

logger = logging.getLogger(__name__)


class GoogleSheetsService:
    """Service for writing policy data to Google Sheets."""
    
    def __init__(self):
        """Initialize Google Sheets service with credentials."""
        self.settings = get_settings()
        self.client: Optional[gspread.Client] = None
        self.spreadsheet: Optional[gspread.Spreadsheet] = None
        self.worksheet: Optional[gspread.Worksheet] = None
        
    def _get_credentials(self) -> Credentials:
        """Load service account credentials from JSON file."""
        credentials_path = Path(self.settings.google_sheets_credentials_file)
        
        if not credentials_path.exists():
            raise FileNotFoundError(
                f"Google Sheets credentials file not found: {credentials_path}"
            )
        
        # Define the required scopes
        scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive.file'
        ]
        
        credentials = Credentials.from_service_account_file(
            str(credentials_path),
            scopes=scopes
        )
        
        return credentials
    
    def connect(self) -> bool:
        """
        Connect to Google Sheets and open the target spreadsheet.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            # Get credentials and authorize client
            credentials = self._get_credentials()
            self.client = gspread.authorize(credentials)
            
            # Open spreadsheet by ID
            self.spreadsheet = self.client.open_by_key(self.settings.google_sheet_id)
            
            # Get or create the worksheet
            worksheet_name = self.settings.google_sheet_name
            
            try:
                self.worksheet = self.spreadsheet.worksheet(worksheet_name)
                logger.info(f"Connected to existing worksheet: {worksheet_name}")
            except gspread.exceptions.WorksheetNotFound:
                # Create worksheet if it doesn't exist
                self.worksheet = self.spreadsheet.add_worksheet(
                    title=worksheet_name,
                    rows=1000,
                    cols=15
                )
                self._initialize_headers()
                logger.info(f"Created new worksheet: {worksheet_name}")
            
            # Ensure headers exist
            if self.worksheet.row_values(1) == []:
                self._initialize_headers()
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to connect to Google Sheets: {e}")
            return False
    
    def _initialize_headers(self):
        """Initialize the worksheet with column headers."""
        headers = [
            'Timestamp',
            'Extraction ID',
            'Policy Number',
            'Policy Holder',
            'Insurer Name',
            'Policy Type',
            'Sum Insured',
            'Commencing Date',
            'Expiring Date',
            'Premium Amount',
            'Paid Amount',
            'Balance Amount',
            'Accuracy Score (%)',
            'Edited Fields',
            'Status'
        ]
        
        self.worksheet.update('A1:O1', [headers])
        
        # Format header row (bold)
        self.worksheet.format('A1:O1', {
            'textFormat': {'bold': True},
            'horizontalAlignment': 'CENTER',
            'backgroundColor': {'red': 0.9, 'green': 0.9, 'blue': 0.9}
        })
        
        logger.info("Initialized worksheet headers")
    
    def append_policy_data(
        self,
        extraction_id: str,
        policy_data: Dict[str, Any],
        accuracy_score: float,
        edited_fields: list,
        status: str = "Verified"
    ) -> bool:
        """
        Append a new row of policy data to the sheet.
        
        Args:
            extraction_id: Unique extraction identifier
            policy_data: Dictionary containing all policy fields
            accuracy_score: AI extraction accuracy percentage
            edited_fields: List of fields that were manually edited
            status: Status of the record (e.g., "Verified", "Pending")
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if not self.worksheet:
                if not self.connect():
                    return False
            
            # Prepare row data
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            edited_fields_str = ", ".join(edited_fields) if edited_fields else "None"
            
            row_data = [
                timestamp,
                extraction_id,
                policy_data.get('policy_number', ''),
                policy_data.get('policy_holder', ''),
                policy_data.get('insurer_name', ''),
                policy_data.get('policy_type', ''),
                policy_data.get('sum_insured', ''),
                policy_data.get('commencing_date', ''),
                policy_data.get('expiring_date', ''),
                policy_data.get('premium_amount', ''),
                policy_data.get('paid_amount', ''),
                policy_data.get('balance_amount', ''),
                f"{accuracy_score:.1f}",
                edited_fields_str,
                status
            ]
            
            # Append row to sheet
            self.worksheet.append_row(row_data, value_input_option='USER_ENTERED')
            
            logger.info(f"Successfully appended policy data: {extraction_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to append policy data to Google Sheets: {e}")
            return False
    
    def get_record_count(self) -> int:
        """
        Get the total number of records (excluding header).
        
        Returns:
            int: Number of records
        """
        try:
            if not self.worksheet:
                if not self.connect():
                    return 0
            
            # Get all values and subtract header row
            all_values = self.worksheet.get_all_values()
            return len(all_values) - 1 if len(all_values) > 0 else 0
            
        except Exception as e:
            logger.error(f"Failed to get record count: {e}")
            return 0
    
    def get_average_accuracy(self) -> float:
        """
        Calculate average accuracy score from all records.
        
        Returns:
            float: Average accuracy percentage
        """
        try:
            if not self.worksheet:
                if not self.connect():
                    return 0.0
            
            # Get all accuracy scores (column M, index 13)
            accuracy_col = self.worksheet.col_values(13)[1:]  # Skip header
            
            if not accuracy_col:
                return 0.0
            
            # Convert to floats and calculate average
            scores = [float(score) for score in accuracy_col if score]
            return sum(scores) / len(scores) if scores else 0.0
            
        except Exception as e:
            logger.error(f"Failed to calculate average accuracy: {e}")
            return 0.0


# Singleton instance
_sheets_service: Optional[GoogleSheetsService] = None


def get_sheets_service() -> GoogleSheetsService:
    """
    Get or create the Google Sheets service singleton.
    
    Returns:
        GoogleSheetsService: Initialized service instance
    """
    global _sheets_service
    
    if _sheets_service is None:
        _sheets_service = GoogleSheetsService()
    
    return _sheets_service
