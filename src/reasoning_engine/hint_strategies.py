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
    "comparison_operators": [
        "Step 1: Look for = or == in your code.",
        "Step 2: Remember: = assigns a value, == compares two values.",
        "Step 3: In if statements, use == to compare. Use = when assigning.",
    ],
    "loop_boundaries": [
        "Step 1: Think about how many times your loop should run.",
        "Step 2: Check your range or condition: range(n) goes from 0 to n-1.",
        "Step 3: Trace through your loop with a small example to verify it's correct.",
    ],
    "null_safety": [
        "Step 1: Find where you access an object without checking if it's None.",
        "Step 2: Ask: can this variable ever be None?",
        "Step 3: Add a check: if variable is not None: before using it.",
    ],
    "type_safety": [
        "Step 1: Check what type of data each variable holds.",
        "Step 2: Can you perform the operation on that type?",
        "Step 3: Convert to the correct type if needed.",
    ],
    "best_practice": [
        "Step 1: This works, but there's a cleaner way.",
        "Step 2: Look for built-in functions or methods that do this.",
        "Step 3: Refactor to use the better approach.",
    ],
    "performance_issue": [
        "Step 1: This code is inefficient. How many times does it run?",
        "Step 2: Can you reduce the number of iterations or calculations?",
        "Step 3: Use a more efficient data structure or algorithm.",
    ],
    "security_issue": [
        "Step 1: This could be a security risk. Why?",
        "Step 2: Think about what happens if someone provides malicious input.",
        "Step 3: Add validation and sanitization.",
    ],
}

DEFAULT_HINTS = [
    "Step 1: Re-read the code slowly, line by line.",
    "Step 2: Try running just the broken section in isolation.",
    "Step 3: Search for the error message online — you're likely not the first to see it.",
]


class BaseHintStrategy:
    """Base strategy for generating hints"""
    def generate(self, code: str, context: dict) -> list:
        error_type = context.get("error_label", "")
        return HINT_TEMPLATES.get(error_type, DEFAULT_HINTS)


class AssignmentInConditionStrategy(BaseHintStrategy):
    """Hints for confusing = and == operators"""
    def generate(self, code: str, context: dict) -> list:
        return [
            "Step 1: Look at the condition inside your if statement",
            "Step 2: Check if you are assigning a value (=) instead of comparing (==)",
            "Step 3: Use '==' for comparison in conditions",
            "Answer: if x == 5: is the correct way to check if x equals 5"
        ]


class OffByOneStrategy(BaseHintStrategy):
    """Hints for off-by-one errors in loops"""
    def generate(self, code: str, context: dict) -> list:
        return [
            "Step 1: Check the loop range boundaries",
            "Step 2: Remember: range(n) goes from 0 to n-1, not 0 to n",
            "Step 3: Trace through with a small example (3-5 items) to verify",
            "Answer: If you have 5 items, use range(5) for indices 0-4"
        ]


class InfiniteLoopStrategy(BaseHintStrategy):
    """Hints for infinite loop detection"""
    def generate(self, code: str, context: dict) -> list:
        level = context.get("level", "beginner")
        
        if level == "beginner":
            return [
                "Step 1: Find your while loop and identify the stopping condition",
                "Step 2: Trace through: Is that condition ever reached?",
                "Step 3: Add a print statement inside to debug",
                "Answer: Make sure your loop variable changes each iteration"
            ]
        elif level == "intermediate":
            return [
                "Step 1: Verify the loop termination condition can be reached",
                "Step 2: Check that loop variables are being modified",
                "Step 3: Consider adding max iterations as safeguard"
            ]
        else:  # advanced
            return [
                "Answer: Ensure loop variable updates and condition eventually becomes false"
            ]


class TypeErrorStrategy(BaseHintStrategy):
    """Hints for type-related errors"""
    def generate(self, code: str, context: dict) -> list:
        return [
            "Step 1: Print the type of the problematic variable using type()",
            "Step 2: Check what type the function expects",
            "Step 3: Convert if needed: int(), str(), float(), etc.",
            "Answer: Cannot add string and int; convert one of them first"
        ]


class NullSafetyStrategy(BaseHintStrategy):
    """Hints for null/None reference errors"""
    def generate(self, code: str, context: dict) -> list:
        return [
            "Step 1: Find where you use the variable without checking if it's None",
            "Step 2: Ask: Can this be None?",
            "Step 3: Add a guard: if var is not None: before using it",
            "Answer: Defensive programming prevents NoneType errors"
        ]


class DivisionByZeroStrategy(BaseHintStrategy):
    """Hints for division by zero errors"""
    def generate(self, code: str, context: dict) -> list:
        return [
            "Step 1: Find the division operation",
            "Step 2: Can the divisor ever be 0?",
            "Step 3: Add a check before dividing",
            "Answer: if denominator != 0: result = numerator / denominator"
        ]


def get_hint_strategy(error_type: str) -> BaseHintStrategy:
    """
    Get the appropriate hint strategy for an error type.
    
    Supports:
    - assignment_in_condition
    - off_by_one
    - infinite_loop
    - type_error
    - null_safety
    - division_by_zero
    - comparison_operators (from templates)
    - loop_boundaries (from templates)
    - And all others via template lookup
    """
    if not error_type:
        return BaseHintStrategy()
    
    error_type = error_type.lower().strip()
    
    # Map specific strategies
    mapping = {
        "assignment_in_condition": AssignmentInConditionStrategy(),
        "off_by_one": OffByOneStrategy(),
        "infinite_loop": InfiniteLoopStrategy(),
        "type_error": TypeErrorStrategy(),
        "null_safety": NullSafetyStrategy(),
        "division_by_zero": DivisionByZeroStrategy(),
    }
    
    if error_type in mapping:
        return mapping[error_type]
    
    # Fall back to template-based strategy
    return BaseHintStrategy()