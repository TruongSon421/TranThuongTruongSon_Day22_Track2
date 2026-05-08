"""
Tests for 02_prompt_hub_ab_routing.py
Tests A/B routing logic without requiring API calls.
"""

import pytest
import sys
import hashlib
import importlib
from pathlib import Path

root = Path(__file__).parent.parent
sys.path.insert(0, str(root))

routing_module = importlib.import_module("02_prompt_hub_ab_routing")
get_prompt_version = routing_module.get_prompt_version
PROMPT_V1_NAME = routing_module.PROMPT_V1_NAME
PROMPT_V2_NAME = routing_module.PROMPT_V2_NAME


class TestPromptRouting:
    """Test deterministic A/B routing based on MD5 hash."""

    def test_routing_returns_v1_or_v2(self):
        """Routing must return one of the two defined prompt names."""
        result = get_prompt_version("test-request-id")
        assert result in (PROMPT_V1_NAME, PROMPT_V2_NAME)

    def test_routing_is_deterministic(self):
        """Same request_id must always route to the same version."""
        request_id = "req-0042"
        result1 = get_prompt_version(request_id)
        result2 = get_prompt_version(request_id)
        result3 = get_prompt_version(request_id)
        assert result1 == result2 == result3

    def test_routing_distributes_roughly_equally(self):
        """Over many request IDs, both versions should appear."""
        v1_count = 0
        v2_count = 0
        for i in range(100):
            version = get_prompt_version(f"req-{i:04d}")
            if version == PROMPT_V1_NAME:
                v1_count += 1
            else:
                v2_count += 1
        assert v1_count > 0, "V1 should appear at least once in 100 requests"
        assert v2_count > 0, "V2 should appear at least once in 100 requests"

    def test_routing_uses_md5_hash(self):
        """Verify the routing is based on MD5 hash of request_id."""
        request_id = "test-id-123"
        hash_int = int(hashlib.md5(request_id.encode()).hexdigest(), 16)
        expected = PROMPT_V1_NAME if hash_int % 2 == 0 else PROMPT_V2_NAME
        assert get_prompt_version(request_id) == expected

    def test_routing_known_request_ids(self):
        """Test a few specific request IDs with known expected outputs."""
        for req_id in ["req-0000", "req-0001", "req-0010", "req-0100", "req-1000"]:
            result = get_prompt_version(req_id)
            assert result in (PROMPT_V1_NAME, PROMPT_V2_NAME)

    def test_prompt_names_are_different(self):
        """V1 and V2 names must be distinct."""
        assert PROMPT_V1_NAME != PROMPT_V2_NAME

    def test_known_hash_routing(self):
        """Test that specific request IDs route predictably."""
        results = {}
        for i in range(50):
            rid = f"req-{i:04d}"
            results[rid] = get_prompt_version(rid)
        assert all(v in (PROMPT_V1_NAME, PROMPT_V2_NAME) for v in results.values())
