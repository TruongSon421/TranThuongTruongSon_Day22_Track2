"""
Tests for config.py and qa_pairs.py
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


class TestConfig:
    """Test configuration module."""

    def test_config_module_loads(self):
        """Config module should load without errors."""
        import config
        assert config is not None

    def test_openai_config_present(self):
        from config import OPENAI_API_KEY, OPENAI_BASE_URL
        assert OPENAI_BASE_URL == "https://api.openai.com/v1"
        assert isinstance(OPENAI_API_KEY, str)

    def test_langsmith_config_present(self):
        from config import LANGSMITH_API_KEY, LANGSMITH_PROJECT, LANGSMITH_TRACING_V2
        assert LANGSMITH_PROJECT == "day22-langsmith-lab"
        assert LANGSMITH_TRACING_V2 == "true"
        assert isinstance(LANGSMITH_API_KEY, str)

    def test_get_llm_returns_chatopenai(self):
        from config import get_llm
        llm = get_llm(model="gpt-4o-mini", temperature=0.0)
        assert llm.model == "gpt-4o-mini"
        assert llm.temperature == 0.0

    def test_get_embeddings_returns_embeddings(self):
        from config import get_embeddings
        emb = get_embeddings(model="text-embedding-3-small")
        assert emb.model == "text-embedding-3-small"

    def test_verify_config_returns_bool(self):
        from config import verify_config
        result = verify_config()
        assert isinstance(result, bool)


class TestQAPairs:
    """Test QA pairs module."""

    def test_qa_pairs_module_loads(self):
        from qa_pairs import QA_PAIRS
        assert QA_PAIRS is not None

    def test_qa_pairs_count(self):
        from qa_pairs import QA_PAIRS
        assert len(QA_PAIRS) == 50, f"Expected 50 QA pairs, got {len(QA_PAIRS)}"

    def test_each_qa_has_question_and_reference(self):
        from qa_pairs import QA_PAIRS
        for qa in QA_PAIRS:
            assert "question" in qa, "Missing 'question' key"
            assert "reference" in qa, "Missing 'reference' key"
            assert isinstance(qa["question"], str)
            assert isinstance(qa["reference"], str)
            assert len(qa["question"]) > 0
            assert len(qa["reference"]) > 0

    def test_all_questions_are_unique(self):
        from qa_pairs import QA_PAIRS
        questions = [qa["question"] for qa in QA_PAIRS]
        assert len(questions) == len(set(questions)), "Duplicate questions found"

    def test_first_and_last_qa_pairs(self):
        from qa_pairs import QA_PAIRS
        assert "machine learning" in QA_PAIRS[0]["question"].lower()
        assert "ai safety" in QA_PAIRS[-1]["question"].lower()
