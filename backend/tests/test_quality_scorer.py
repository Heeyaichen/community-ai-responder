import pytest
from unittest.mock import patch, from app.services.quality_scorer import QualityScorer


class TestQualityScorer:
    def test_score_empty_text(self):
        scorer = QualityScorer()
        score = scorer.score("")
        assert score == 0.0

    
    def test_score_short_text(self):
        scorer = QualityScorer()
        score = scorer.score("hi")
        assert score == 0.0
    
    def test_score_with_question(self):
        scorer = QualityScorer()
        score = scorer.score("This is a test response?")
        assert score >= 1.0
    
    def test_score_with_specific_content(self):
        scorer = QualityScorer()
        score = scorer.score("First, check if the API key is correct. Second, verify the connection.")
        assert score >= 2.0
    
    def test_generic_phrase_detection(self):
        scorer = QualityScorer()
        score = scorer.score("I hope this helps! Let me know if you have any questions.")
        assert score < 3.0
    
    def test_passes_threshold(self):
        scorer = QualityScorer(threshold=3.0)
        assert scorer.passes("This is a good response with specific content?")
        assert not scorer.passes("I hope this helps!")
