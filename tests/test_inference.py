from src.reasoning_engine.error_classifier import ErrorClassifier
from src.reasoning_engine.hint_system import HintSystem
from src.reasoning_engine.feedback_scorer import FeedbackScorer


def test_error_classifier_decode():
    clf = ErrorClassifier()
    binary = [1, 0, 0, 0, 0, 0, 0, 0, 0]
    labels = clf.decode(binary)
    assert "syntax_error" in labels


def test_hint_system_returns_steps():
    hs = HintSystem()
    hints = hs.get_hints("syntax_error", "beginner")
    assert len(hints) > 0
    assert "Step" in hints[0]


def test_feedback_scorer_range():
    scorer = FeedbackScorer()
    code = "x = 1\nprint(x)"
    score = scorer.score(code)
    assert 0 <= score <= 100
