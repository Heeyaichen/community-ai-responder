import re
from typing import List


class QualityScorer:
    GENERIC_PHRASES = [
        r"as an ai",
        r"i understand",
        r"i hope this helps",
        r"let me know if",
        r"feel free to",
        r"don't hesitate",
        r"please let me know",
        r"i'm here to help",
        r"happy to assist",
    ]

    def __init__(self, threshold: float = 3.0):
        self.threshold = threshold

    def score(self, text: str) -> float:
        score = 0.0

        if len(text) > 50:
            score += 1.0

        if "?" in text:
            score += 1.0

        if not self._contains_generic(text):
            score += 2.0

        if self._is_specific(text):
            score += 1.0

        return score

    def passes(self, text: str) -> bool:
        return self.score(text) >= self.threshold

    def _contains_generic(self, text: str) -> bool:
        lower_text = text.lower()
        for phrase in self.GENERIC_PHRASES:
            if phrase in lower_text:
                return True
        return False

    def _is_specific(self, text: str) -> bool:
        specific_indicators = [
            r"step 1",
            r"step 2",
            r"first,",
            r"second,",
            r"try this",
            r"check the",
            r"make sure",
            r"specifically",
        ]
        lower_text = text.lower()
        return any(indicator in lower_text for indicator in specific_indicators)
