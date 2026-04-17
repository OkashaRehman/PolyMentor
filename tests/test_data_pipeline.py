import pytest
from src.data_pipeline.cleaner import DataCleaner


def test_cleaner_removes_missing_fields():
    cleaner = DataCleaner()
    samples = [{"id": "1", "code": "x = 1"}]  # Missing required fields
    result = cleaner.clean(samples)
    assert len(result) == 0


def test_cleaner_keeps_valid_sample():
    cleaner = DataCleaner()
    sample = {
        "id": "1",
        "code": "x = 1",
        "language": "python",
        "error_types": ["syntax_error"],
        "difficulty": "beginner",
        "explanation": "Test",
        "hint_steps": ["Step 1"],
        "concept_taught": "Variables",
    }
    result = cleaner.clean([sample])
    assert len(result) == 1
