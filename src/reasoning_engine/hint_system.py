# Maps error type → progressive hint steps
HINT_TEMPLATES = {
    "syntax_error": [
        "Step 1: Read the error message carefully — it usually tells you the exact line.",
        "Step 2: Look at the line mentioned. Check for missing colons, brackets, or quotes.",
        "Step 3: Compare your syntax against a working example of the same construct.",
    ],
    "off_by_one": [
        "Step 1: Trace through your loop manually with a small example (e.g., 3 items).",
        "Step 2: Check: does your index start at 0 or 1? Where does it end?",
        "Step 3: Try changing your range by ±1 and re-trace. Does the output match now?",
    ],
    "logical_error": [
        "Step 1: Add print statements before and after the suspicious section to see values.",
        "Step 2: Write down the expected value vs. what you actually got.",
        "Step 3: Trace each step of your logic on paper for a simple test case.",
    ],
    "infinite_loop": [
        "Step 1: Find your loop. What condition makes it stop?",
        "Step 2: Is that condition ever actually reached during execution?",
        "Step 3: Add a print inside the loop to see if the stopping variable changes each iteration.",
    ],
    "type_error": [
        "Step 1: Print the type of the variable causing the error using type().",
        "Step 2: Check what type the function or operation expects as input.",
        "Step 3: Convert the variable to the correct type before using it.",
    ],
    "division_by_zero": [
        "Step 1: Find where division happens in your code.",
        "Step 2: Can the denominator ever be 0? What inputs would cause that?",
        "Step 3: Add a check: if denominator != 0: before dividing.",
    ],
}

DEFAULT_HINTS = [
    "Step 1: Re-read the code slowly, line by line.",
    "Step 2: Try running just the broken section in isolation.",
    "Step 3: Search for the error message online — you're likely not the first to see it.",
]


class HintSystem:
    """Generates progressive, step-by-step hints for a detected error."""

    def get_hints(self, error_label: str, level: str = "beginner") -> list:
        hints = HINT_TEMPLATES.get(error_label, DEFAULT_HINTS)

        # For advanced users, return fewer leading hints
        if level == "advanced":
            return hints[-1:]
        elif level == "intermediate":
            return hints[1:]
        return hints  # beginner gets all steps

    def get_first_hint(self, error_label: str, level: str = "beginner") -> str:
        hints = self.get_hints(error_label, level)
        return hints[0] if hints else DEFAULT_HINTS[0]
