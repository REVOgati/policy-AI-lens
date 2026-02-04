"""
Results storage service - tracks extraction accuracy for analytics.
"""
import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from app.models.schemas import PolicyData


class ResultsStorage:
    """Simple JSON-based storage for extraction results."""

    def __init__(self, storage_file: str = "results.json"):
        """Initialize storage with file path."""
        self.storage_file = Path(storage_file)
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Create storage file if it doesn't exist."""
        if not self.storage_file.exists():
            self.storage_file.write_text("[]")

    def _read_results(self) -> List[dict]:
        """Read all results from storage."""
        try:
            with open(self.storage_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _write_results(self, results: List[dict]):
        """Write results to storage."""
        with open(self.storage_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

    def save_result(
        self,
        extraction_id: str,
        policy_number: Optional[str],
        accuracy_score: float,
        edited_fields: List[str]
    ):
        """
        Save a verification result.

        Args:
            extraction_id: Unique extraction identifier
            policy_number: Policy number from the document
            accuracy_score: Accuracy percentage (0-100)
            edited_fields: List of field names that were edited
        """
        results = self._read_results()

        result_entry = {
            "extraction_id": extraction_id,
            "policy_number": policy_number or "N/A",
            "accuracy_score": round(accuracy_score, 2),
            "edited_fields": edited_fields,
            "timestamp": datetime.now().isoformat(),
        }

        results.append(result_entry)
        self._write_results(results)

        print(f"✅ Result saved: {extraction_id} - Accuracy: {accuracy_score}%")

    def get_all_results(self) -> List[dict]:
        """Retrieve all stored results."""
        return self._read_results()

    def get_average_accuracy(self) -> float:
        """Calculate average accuracy across all results."""
        results = self._read_results()
        if not results:
            return 0.0

        total = sum(r.get("accuracy_score", 0) for r in results)
        return round(total / len(results), 2)

    def get_result_by_id(self, extraction_id: str) -> Optional[dict]:
        """Get a specific result by extraction ID."""
        results = self._read_results()
        for result in results:
            if result.get("extraction_id") == extraction_id:
                return result
        return None


# Singleton instance
_storage = None


def get_results_storage() -> ResultsStorage:
    """Get or create the results storage instance."""
    global _storage
    if _storage is None:
        # Store in backend root directory
        storage_path = Path(__file__).parent.parent.parent / "results.json"
        _storage = ResultsStorage(str(storage_path))
    return _storage
