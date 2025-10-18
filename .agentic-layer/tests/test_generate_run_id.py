"""Unit tests for generate_run_id module."""
import string
from generate_run_id import generate_run_id


def test_generate_run_id_returns_string():
    """Test that generate_run_id returns a string."""
    result = generate_run_id()
    assert isinstance(result, str)


def test_generate_run_id_length():
    """Test that generate_run_id returns exactly 10 characters."""
    result = generate_run_id()
    assert len(result) == 10


def test_generate_run_id_valid_characters():
    """Test that generate_run_id uses only alphanumeric characters."""
    result = generate_run_id()
    valid_chars = set(string.ascii_letters + string.digits)
    assert all(c in valid_chars for c in result)


def test_generate_run_id_alphanumeric_only():
    """Test that generate_run_id output is alphanumeric with no special chars."""
    result = generate_run_id()
    assert result.isalnum()


def test_generate_run_id_uniqueness():
    """Test that multiple calls generate different IDs (probabilistic)."""
    # Generate multiple IDs
    ids = [generate_run_id() for _ in range(100)]
    # Verify all are unique (extremely high probability with 10-char random strings)
    assert len(set(ids)) == len(ids), "Generated IDs should be unique"


def test_generate_run_id_no_spaces():
    """Test that generate_run_id does not include spaces."""
    result = generate_run_id()
    assert ' ' not in result
