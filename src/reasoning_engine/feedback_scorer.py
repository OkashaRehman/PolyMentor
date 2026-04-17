import ast
import re


class FeedbackScorer:
    """
    Scores code quality on a 0–100 scale.
    Checks readability, complexity, and clean code principles.
    """

    def score(self, code: str, language: str = "python") -> int:
        score = 100

        lines = code.strip().split("\n")

        # Penalize very long lines
        long_lines = sum(1 for l in lines if len(l) > 100)
        score -= long_lines * 3

        # Penalize deeply nested code (4+ levels of indentation)
        deep_nesting = sum(1 for l in lines if l.startswith("    " * 4))
        score -= deep_nesting * 5

        # Penalize magic numbers
        magic_numbers = len(re.findall(r"\b(?<!\.)\d{2,}\b", code))
        score -= magic_numbers * 2

        # Penalize very short variable names (single char, excluding i/j/k/n/x/y)
        bad_vars = len(re.findall(r"\b(?![ijknxy])[a-wz]\b\s*=", code))
        score -= bad_vars * 3

        # Penalize no comments/docstrings in longer functions
        if len(lines) > 15 and '"""' not in code and "#" not in code:
            score -= 10

        return max(0, min(100, score))
