# Rule-based explanation generator (used before the fine-tuned model is ready)
EXPLANATIONS = {
    "syntax_error": (
        "Your code has a syntax error — the language cannot understand its structure. "
        "This usually means a missing colon, bracket, quote, or wrong indentation."
    ),
    "logical_error": (
        "Your code runs without crashing, but produces the wrong result. "
        "The logic of your algorithm doesn't match what you intended it to do."
    ),
    "off_by_one": (
        "You have an off-by-one error. Your loop starts or ends one step too early or too late, "
        "which is very common when working with arrays or ranges."
    ),
    "infinite_loop": (
        "Your loop never terminates because its stopping condition is never reached. "
        "The variable that should end the loop isn't changing correctly."
    ),
    "type_error": (
        "You passed the wrong data type to a function or operation. "
        "For example, trying to add a string and a number without converting one of them."
    ),
    "division_by_zero": (
        "Your code attempts to divide a number by zero, which is mathematically undefined "
        "and causes a runtime crash."
    ),
    "bad_practice": (
        "Your code works, but uses patterns that make it hard to read, maintain, or extend. "
        "Consider naming variables descriptively and avoiding magic numbers."
    ),
}

DEFAULT_EXPLANATION = (
    "An error was detected in your code. Review the flagged section carefully "
    "and compare it against the expected behavior."
)


class ExplanationGenerator:
    """Provides human-readable explanations for detected errors."""

    def explain(self, error_label: str) -> str:
        return EXPLANATIONS.get(error_label, DEFAULT_EXPLANATION)

    def explain_all(self, error_labels: list) -> list:
        return [self.explain(label) for label in error_labels]
