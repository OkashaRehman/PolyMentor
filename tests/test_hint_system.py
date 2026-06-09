"""
Test Suite for Smart Hint & Skill Development System
======================================================

Tests for:
- Progressive hint generation
- Adaptive difficulty levels
- Hint effectiveness tracking
- Learner performance analytics
- Recommendation engine
"""

import sys
from pathlib import Path

# Add parent directory to path so we can import src
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.reasoning_engine.hint_system import HintSystem
from src.reasoning_engine.feedback_scorer import FeedbackScorer


class TestProgressiveHints:
    """Test progressive hint generation for different learner levels"""

    def test_beginner_gets_all_steps(self):
        """Beginner should get all 3 steps"""
        hs = HintSystem()
        hints = hs.get_hints("syntax_error", level="beginner")
        assert len(hints) == 3
        assert "Step 1:" in hints[0]
        assert "Step 2:" in hints[1]
        assert "Step 3:" in hints[2]

    def test_intermediate_gets_fewer_hints(self):
        """Intermediate should get steps 2-3 (less hand-holding)"""
        hs = HintSystem()
        hints = hs.get_hints("syntax_error", level="intermediate")
        assert len(hints) >= 1  # Gets middle steps
        assert any("Step" in h for h in hints)

    def test_advanced_gets_just_answer(self):
        """Advanced should get only the final answer"""
        hs = HintSystem()
        hints = hs.get_hints("syntax_error", level="advanced")
        assert len(hints) == 1
        assert isinstance(hints[0], str)

    def test_hint_progression_comparison_operators(self):
        """Test comparison operator hints"""
        hs = HintSystem()
        
        beginner_hints = hs.get_hints("comparison_operators", "beginner")
        intermediate_hints = hs.get_hints("comparison_operators", "intermediate")
        advanced_hints = hs.get_hints("comparison_operators", "advanced")
        
        assert len(beginner_hints) >= 3
        assert len(intermediate_hints) < len(beginner_hints)
        assert len(advanced_hints) == 1
        assert "==" in advanced_hints[0]

    def test_hint_progression_loop_boundaries(self):
        """Test loop boundary hints"""
        hs = HintSystem()
        
        hints = hs.get_hints("loop_boundaries", "beginner")
        assert len(hints) >= 3
        assert any("range" in h.lower() for h in hints)
        assert any("trace" in h.lower() for h in hints)


class TestAdaptiveGeneration:
    """Test hint generation with code context"""

    def test_generate_hints_with_code(self):
        """Generate hints based on actual code"""
        hs = HintSystem()
        
        error_code = "if x = 5: print(x)"
        context = {"level": "beginner"}
        
        hints = hs.generate_hints("assignment_in_condition", error_code, context)
        assert len(hints) >= 3
        assert any("==" in h for h in hints)

    def test_generate_hints_with_context(self):
        """Hints should adapt to provided context"""
        hs = HintSystem()
        
        context_beginner = {"level": "beginner"}
        context_advanced = {"level": "advanced"}
        
        hints_beginner = hs.generate_hints("infinite_loop", "", context_beginner)
        hints_advanced = hs.generate_hints("infinite_loop", "", context_advanced)
        
        assert len(hints_beginner) > len(hints_advanced)

    def test_first_hint_extraction(self):
        """Should extract first hint correctly"""
        hs = HintSystem()
        
        first_hint = hs.get_first_hint("type_error", "beginner")
        assert first_hint is not None
        assert len(first_hint) > 0
        assert "Step 1:" in first_hint or "Step" in first_hint


class TestFeedbackTracking:
    """Test feedback collection and performance tracking"""

    def test_score_helpful_feedback(self):
        """Helpful feedback should score high"""
        fs = FeedbackScorer()
        
        score = fs.score_feedback(
            hint_text="Use == instead of = for comparison",
            was_helpful=True,
            error_type="assignment_in_condition",
            user_level="beginner"
        )
        
        assert score > 70  # Helpful feedback scores high
        assert score <= 100

    def test_score_unhelpful_feedback(self):
        """Unhelpful feedback should score lower"""
        fs = FeedbackScorer()
        
        score = fs.score_feedback(
            hint_text="This doesn't help",
            was_helpful=False,
            error_type="syntax_error",
            user_level="intermediate"
        )
        
        assert score < 70  # Unhelpful feedback scores lower

    def test_hint_effectiveness_stats(self):
        """Track hint effectiveness statistics"""
        fs = FeedbackScorer()
        
        # Record multiple feedbacks
        fs.score_feedback("Hint 1", True, "syntax_error", "beginner")
        fs.score_feedback("Hint 2", True, "syntax_error", "beginner")
        fs.score_feedback("Hint 3", False, "syntax_error", "beginner")
        
        stats = fs.get_hint_effectiveness("syntax_error")
        
        assert stats["total_feedback_records"] == 3
        assert stats["helpful_count"] == 2
        assert stats["success_rate"] == round(2/3, 2)
        assert "recommendation" in stats

    def test_learner_session_tracking(self):
        """Track individual learner sessions"""
        fs = FeedbackScorer()
        
        fs.track_learner_session(
            learner_id="student_123",
            error_type="comparison_operators",
            level="beginner",
            hints_used=2,
            problem_solved=True
        )
        
        fs.track_learner_session(
            learner_id="student_123",
            error_type="loop_boundaries",
            level="beginner",
            hints_used=3,
            problem_solved=False
        )
        
        analytics = fs.get_learner_analytics("student_123")
        
        assert analytics["total_sessions"] == 2
        assert analytics["problems_solved"] == 1
        assert analytics["success_rate"] == 0.5
        assert len(analytics["error_types_encountered"]) == 2


class TestAdaptiveDifficulty:
    """Test adaptive difficulty recommendations"""

    def test_recommend_level_up_beginner(self):
        """Should recommend intermediate when beginner succeeds > 80%"""
        fs = FeedbackScorer()
        
        recommended = fs.recommend_difficulty_change(
            user_level="beginner",
            success_rate=0.85,
            errors_solved=5
        )
        
        assert recommended == "intermediate"

    def test_recommend_level_up_intermediate(self):
        """Should recommend advanced when intermediate succeeds > 85%"""
        fs = FeedbackScorer()
        
        recommended = fs.recommend_difficulty_change(
            user_level="intermediate",
            success_rate=0.9,
            errors_solved=10
        )
        
        assert recommended == "advanced"

    def test_recommend_level_down(self):
        """Should recommend lower level when success < 50%"""
        fs = FeedbackScorer()
        
        recommended = fs.recommend_difficulty_change(
            user_level="intermediate",
            success_rate=0.3,
            errors_solved=1
        )
        
        assert recommended == "beginner"

    def test_stay_same_level(self):
        """Should stay at same level with moderate performance"""
        fs = FeedbackScorer()
        
        recommended = fs.recommend_difficulty_change(
            user_level="intermediate",
            success_rate=0.6,
            errors_solved=3
        )
        
        assert recommended == "intermediate"


class TestHintQualityScoring:
    """Test hint quality assessment"""

    def test_hint_length_penalty_too_short(self):
        """Very short hints should be penalized"""
        fs = FeedbackScorer()
        
        short_hint = "Use =="
        score = fs.score_feedback(short_hint, True, "test", "beginner")
        
        # Even though helpful, short hint is penalized
        assert score < 80

    def test_hint_length_optimal(self):
        """Optimal length hints should score highest"""
        fs = FeedbackScorer()
        
        good_hint = "Step 1: Check if you used = instead of ==. Step 2: Replace = with == in your condition."
        score = fs.score_feedback(good_hint, True, "test", "beginner")
        
        # Optimal length gets good score
        assert score >= 80

    def test_hint_length_penalty_too_long(self):
        """Very long hints should be penalized"""
        fs = FeedbackScorer()
        
        long_hint = " ".join(["word"] * 150)  # Very long
        score = fs.score_feedback(long_hint, True, "test", "beginner")
        
        # Even though helpful, overly long hint is penalized
        assert score < 90


class TestErrorTypeHints:
    """Test hints for various error types"""

    def test_assignment_in_condition_hints(self):
        """Test hints for = vs == confusion"""
        hs = HintSystem()
        hints = hs.get_hints("assignment_in_condition", "beginner")
        
        assert any("==" in h for h in hints)
        assert any("compare" in h.lower() or "condition" in h.lower() for h in hints)

    def test_off_by_one_hints(self):
        """Test hints for off-by-one errors"""
        hs = HintSystem()
        hints = hs.get_hints("off_by_one", "beginner")
        
        assert any("range" in h.lower() or "0" in h for h in hints)
        assert any("trace" in h.lower() for h in hints)

    def test_infinite_loop_hints(self):
        """Test hints for infinite loops"""
        hs = HintSystem()
        hints = hs.get_hints("infinite_loop", "beginner")
        
        assert any("loop" in h.lower() for h in hints)
        assert any("stop" in h.lower() or "condition" in h.lower() for h in hints)

    def test_type_error_hints(self):
        """Test hints for type errors"""
        hs = HintSystem()
        hints = hs.get_hints("type_error", "beginner")
        
        assert any("type(" in h for h in hints) or any("convert" in h.lower() for h in hints)

    def test_null_safety_hints(self):
        """Test hints for None/null reference errors"""
        hs = HintSystem()
        hints = hs.get_hints("null_safety", "beginner")
        
        assert any("None" in h or "null" in h.lower() for h in hints)


class TestHintSystemIntegration:
    """Integration tests for complete hint system workflow"""

    def test_complete_learner_journey(self):
        """Test complete learning journey with adaptive hints"""
        hs = HintSystem()
        fs = FeedbackScorer()
        
        # Step 1: Beginner encounters syntax error
        beginner_hints = hs.get_hints("syntax_error", "beginner")
        assert len(beginner_hints) == 3
        
        # Step 2: Gets feedback on first hint
        score1 = fs.score_feedback(beginner_hints[0], True, "syntax_error", "beginner")
        assert score1 > 50
        
        # Step 3: Track performance
        fs.track_learner_session("learner1", "syntax_error", "beginner", 1, True)
        
        # Step 4: Check analytics
        analytics = fs.get_learner_analytics("learner1")
        assert analytics["problems_solved"] == 1
        
        # Step 5: Recommend difficulty after multiple sessions with high success
        for i in range(5):
            fs.track_learner_session("learner1", f"error_{i}", "beginner", 2, True)
        
        recommended = fs.recommend_difficulty_change("beginner", 0.85, 6)
        assert recommended == "intermediate"

    def test_hint_effectiveness_improves_recommendations(self):
        """Hints that are effective should influence recommendations"""
        fs = FeedbackScorer()
        
        # Record several successful hint sessions
        for i in range(5):
            fs.score_feedback(
                "Effective hint here",
                True,
                "loop_boundaries",
                "beginner"
            )
        
        stats = fs.get_hint_effectiveness("loop_boundaries")
        assert stats["success_rate"] == 1.0
        assert "Excellent" in stats["recommendation"]


if __name__ == "__main__":
    # Run tests
    test_progressive = TestProgressiveHints()
    test_progressive.test_beginner_gets_all_steps()
    test_progressive.test_intermediate_gets_fewer_hints()
    test_progressive.test_advanced_gets_just_answer()
    
    test_adaptive = TestAdaptiveGeneration()
    test_adaptive.test_generate_hints_with_code()
    test_adaptive.test_first_hint_extraction()
    
    test_feedback = TestFeedbackTracking()
    test_feedback.test_score_helpful_feedback()
    test_feedback.test_hint_effectiveness_stats()
    
    test_difficulty = TestAdaptiveDifficulty()
    test_difficulty.test_recommend_level_up_beginner()
    test_difficulty.test_recommend_level_down()
    
    test_errors = TestErrorTypeHints()
    test_errors.test_assignment_in_condition_hints()
    test_errors.test_infinite_loop_hints()
    
    test_integration = TestHintSystemIntegration()
    test_integration.test_complete_learner_journey()
    
    print("✅ All tests passed!")
