"""
Tests for 04_guardrails_validator.py
Tests PIIDetector and JSONFormatter without requiring API calls.
"""

import pytest
import sys
import importlib
from pathlib import Path

root = Path(__file__).parent.parent
sys.path.insert(0, str(root))

guardrails_module = importlib.import_module("04_guardrails_validator")
PIIDetector = guardrails_module.PIIDetector
JSONFormatter = guardrails_module.JSONFormatter

from guardrails import Guard
from guardrails.validator_base import OnFailAction


class TestPIIDetector:
    """Test PII detection and redaction patterns."""

    def _guard(self):
        return Guard().use(PIIDetector(on_fail=OnFailAction.FIX))

    def test_email_detection(self):
        guard = self._guard()
        result = guard.validate("Contact John at john.doe@example.com for details.")
        assert result.validation_passed is True
        assert "[EMAIL_REDACTED]" in result.validated_output
        assert "john.doe@example.com" not in result.validated_output

    def test_email_with_subdomains(self):
        guard = self._guard()
        result = guard.validate("Reach us at admin@mail.company.co.uk.")
        assert result.validation_passed is True
        assert "[EMAIL_REDACTED]" in result.validated_output
        assert "admin@mail.company.co.uk" not in result.validated_output

    def test_phone_parentheses_format(self):
        guard = self._guard()
        result = guard.validate("Call our support line at (555) 867-5309.")
        assert result.validation_passed is True
        assert "[PHONE_REDACTED]" in result.validated_output
        assert "867-5309" not in result.validated_output

    def test_phone_dashes_format(self):
        guard = self._guard()
        result = guard.validate("Phone: 555-123-4567")
        assert result.validation_passed is True
        assert "[PHONE_REDACTED]" in result.validated_output
        assert "555-123-4567" not in result.validated_output

    def test_phone_international_format(self):
        guard = self._guard()
        result = guard.validate("Call +1-555-987-6543 for assistance.")
        assert result.validation_passed is True
        assert "[PHONE_REDACTED]" in result.validated_output
        assert "555-987-6543" not in result.validated_output

    def test_ssn_detection(self):
        guard = self._guard()
        result = guard.validate("Patient SSN is 123-45-6789 on file.")
        assert result.validation_passed is True
        assert "[SSN_REDACTED]" in result.validated_output
        assert "123-45-6789" not in result.validated_output

    def test_credit_card_spaces(self):
        guard = self._guard()
        result = guard.validate("Payment made with card 4532 1234 5678 9010.")
        assert result.validation_passed is True
        assert "[CREDIT_CARD_REDACTED]" in result.validated_output
        assert "4532 1234 5678 9010" not in result.validated_output

    def test_credit_card_dashes(self):
        guard = self._guard()
        result = guard.validate("Card: 4532-1234-5678-9010")
        assert result.validation_passed is True
        assert "[CREDIT_CARD_REDACTED]" in result.validated_output
        assert "4532-1234-5678-9010" not in result.validated_output

    def test_credit_card_no_separator(self):
        guard = self._guard()
        result = guard.validate("Card: 1111 2222 3333 4444")
        assert result.validation_passed is True
        assert "[CREDIT_CARD_REDACTED]" in result.validated_output
        assert "1111 2222 3333 4444" not in result.validated_output

    def test_multiple_pii_types(self):
        guard = self._guard()
        result = guard.validate("Email: alice@example.com, Phone: 555-123-4567")
        assert result.validation_passed is True
        assert "[EMAIL_REDACTED]" in result.validated_output
        assert "[PHONE_REDACTED]" in result.validated_output
        assert "alice@example.com" not in result.validated_output
        assert "555-123-4567" not in result.validated_output

    def test_clean_text_no_pii(self):
        guard = self._guard()
        result = guard.validate("No sensitive information in this text.")
        assert result.validation_passed is True
        assert result.validated_output == "No sensitive information in this text."

    def test_empty_text(self):
        guard = self._guard()
        result = guard.validate("")
        assert result.validation_passed is False
        assert result.validated_output is None or result.validated_output == ""

    def test_pii_preserves_surrounding_text(self):
        guard = self._guard()
        result = guard.validate("User alice@example.com has ID 12345.")
        assert result.validation_passed is True
        assert "User [EMAIL_REDACTED] has ID 12345." in result.validated_output


class TestJSONFormatter:
    """Test JSON validation and auto-repair patterns."""

    def _guard(self):
        return Guard().use(JSONFormatter(on_fail=OnFailAction.FIX))

    def test_valid_json(self):
        guard = self._guard()
        result = guard.validate('{"name": "Alice", "age": 30}')
        assert result.validation_passed is True
        assert '"name": "Alice"' in result.validated_output
        assert '"age": 30' in result.validated_output

    def test_markdown_fences_json(self):
        guard = self._guard()
        result = guard.validate('```json\n{"name": "Bob"}\n```')
        assert result.validation_passed is True
        assert '"name": "Bob"' in result.validated_output
        assert "```" not in result.validated_output

    def test_markdown_fences_no_lang(self):
        guard = self._guard()
        result = guard.validate('```\n{"status": "ok"}\n```')
        assert result.validation_passed is True
        assert '"status": "ok"' in result.validated_output
        assert "```" not in result.validated_output

    def test_single_quotes_converted(self):
        guard = self._guard()
        result = guard.validate("{'name': 'Charlie', 'score': 95}")
        assert result.validation_passed is True
        assert '"name": "Charlie"' in result.validated_output
        assert "'" not in result.validated_output

    def test_trailing_comma_removed(self):
        guard = self._guard()
        result = guard.validate('{"key": "value",}')
        assert result.validation_passed is True
        assert '"key": "value"' in result.validated_output
        assert ",}" not in result.validated_output

    def test_trailing_comma_in_array(self):
        guard = self._guard()
        result = guard.validate('["a", "b", "c",]')
        assert result.validation_passed is True
        assert '"a"' in result.validated_output
        assert ",]" not in result.validated_output

    def test_nested_structure_repaired(self):
        guard = self._guard()
        result = guard.validate("{'user': {'name': 'Test', 'active': true,},}")
        assert result.validation_passed is True
        assert '"user"' in result.validated_output
        assert ",}" not in result.validated_output

    def test_truly_invalid_json_fails_cleanly(self):
        guard = self._guard()
        result = guard.validate("This is not JSON at all: ??? {]")
        assert result.validation_passed is False
        assert result.validated_output is None

    def test_whitespace_only_surrounding(self):
        guard = self._guard()
        result = guard.validate('  {"clean": true}  ')
        assert result.validation_passed is True
        assert '"clean": true' in result.validated_output

    def test_invalid_json_preserves_original_on_failure(self):
        guard = self._guard()
        original = "definitely not json {"
        result = guard.validate(original)
        assert result.validation_passed is False
        assert result.validated_output is None
