"""
src/api/app.py
--------------
PolyMentor FastAPI application.

Works in two modes:
  - PRE-TRAINING mode: rule-based responses (no model needed) — works right now
  - POST-TRAINING mode: full ML pipeline (after best_mentor_model.pt is created)

The mode is selected automatically based on whether the model file exists.
"""

import ast
import os
import re
import time
from pathlib import Path
from typing import List, Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------------

app = FastAPI(
    title="PolyMentor API",
    description=(
        "AI-powered coding mentor. Submit code in any supported language "
        "and receive error explanations, hints, and quality feedback."
    ),
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Rule-based engine (works with zero ML, zero training)
# ---------------------------------------------------------------------------

ERROR_TO_CONCEPT = {
    "syntax_error": "Syntax Rules & Language Grammar",
    "logical_error": "Program Logic & Control Flow",
    "type_error": "Data Types & Type Casting",
    "off_by_one": "Loop Indexing & Array Boundaries",
    "infinite_loop": "Loop Termination Conditions",
    "null_reference": "Null Safety & Object Initialization",
    "division_by_zero": "Input Validation & Edge Cases",
    "bad_practice": "Clean Code & Readability",
    "structural_issue": "Function Design & Decomposition",
}

EXPLANATIONS = {
    "syntax_error": (
        "Your code has a syntax error — the language cannot parse its structure. "
        "This is often caused by:\n"
        "• Missing colon (:) after if/for/while/def statements\n"
        "• Using = (assignment) instead of == (comparison) in conditions\n"
        "• Unmatched brackets, quotes, or parentheses\n"
        "• Wrong indentation (especially in Python)\n"
        "• Missing semicolons (in JavaScript, C++, Java)\n\n"
        "Check the line number in the error message and review the syntax."
    ),
    "type_error": (
        "You are using a value of the wrong type. Common examples:\n"
        "• Adding a string and a number: '5' + 3\n"
        "• Calling a method that doesn't exist on that type\n"
        "• Trying to iterate over a non-iterable value\n"
        "• Passing the wrong type as a function argument\n\n"
        "Solution: Check the data types involved and convert as needed."
    ),
    "off_by_one": (
        "Your loop starts or ends one step too early or too late. "
        "This is extremely common with:\n"
        "• range(n) produces 0 to n-1, NOT 0 to n\n"
        "• Array indexing starts at 0 (or 1 in some languages)\n"
        "• <= vs < comparisons in loop conditions\n"
        "• Missing or extra +1 or -1 in range calculations\n\n"
        "Manually trace your loop with a small example to verify."
    ),
    "infinite_loop": (
        "Your loop's stopping condition is never reached. Debug by asking:\n"
        "• Does the loop condition ever become false?\n"
        "• Is the variable controlling the loop actually changing?\n"
        "• Is it changing in the right direction (increasing or decreasing)?\n"
        "• Are you modifying the counter inside the loop?\n\n"
        "Add print statements to see how the variable changes each iteration."
    ),
    "division_by_zero": (
        "Your code attempts to divide a number by zero, which is mathematically undefined. "
        "This causes a runtime error.\n\n"
        "Solution: Always check that the denominator is not zero before dividing:\n"
        "    if denominator != 0:\n"
        "        result = numerator / denominator\n"
        "    else:\n"
        "        result = float('inf')  # or handle the error appropriately"
    ),
    "logical_error": (
        "Your code runs without crashing but produces the wrong result. "
        "The algorithm logic does not match the intended behavior.\n\n"
        "Debugging steps:\n"
        "1. Add print statements to see intermediate values\n"
        "2. Trace through your logic step-by-step on paper\n"
        "3. Test with simple examples where you know the expected output\n"
        "4. Check edge cases (empty lists, single item, negative numbers, etc.)"
    ),
    "bad_practice": (
        "Your code works but uses patterns that make it hard to read or maintain:\n"
        "• Single-letter variable names (i, x, a) instead of descriptive names\n"
        "• Magic numbers (100, 42, 3.14) without explanation\n"
        "• Very long functions (100+ lines) that do multiple things\n"
        "• Missing comments or docstrings\n"
        "• Inconsistent spacing or naming conventions\n\n"
        "These issues make your code hard to understand and modify later."
    ),
    "null_reference": (
        "You are trying to use an object that is None/null/undefined. "
        "This is called a null reference error.\n\n"
        "Common causes:\n"
        "• Function returns None but you didn't check for it\n"
        "• Variable was declared but never initialized\n"
        "• Dictionary lookup returns None if the key doesn't exist\n\n"
        "Solution: Always check if an object is not None before using it:\n"
        "    if my_object is not None:\n"
        "        my_object.method()"
    ),
    "structural_issue": (
        "The overall structure of your code could be improved:\n"
        "• Code is deeply nested (more than 3-4 levels)\n"
        "• Function does too many different things\n"
        "• Lines are too long or hard to follow\n"
        "• Similar code is repeated in multiple places\n\n"
        "Solution: Break the code into smaller, well-named functions. "
        "Each function should do one thing and be under 20 lines."
    ),
}

HINTS = {
    "syntax_error": [
        "💡 Step 1: Find the line number in the error message and look at that exact line.",
        "💡 Step 2: Check for missing colons (:) after if, elif, while, def, for, class statements.",
        "💡 Step 3: Look for unmatched parentheses (), brackets [], or quotes (' or \").",
        "💡 Step 4: In Python, check that indentation is consistent (use spaces, not tabs).",
        "💡 Step 5: If using = in a condition, change it to == for comparison.",
    ],
    "type_error": [
        "💡 Step 1: Add print(type(variable)) for each value involved in the operation.",
        "💡 Step 2: Identify which type the operation expects vs what you have.",
        "💡 Step 3: Check function signatures to see what types they accept.",
        "💡 Step 4: Convert the value to the correct type: int(), str(), float(), list(), etc.",
        "💡 Step 5: Test your conversion with a simple example first.",
    ],
    "off_by_one": [
        "💡 Step 1: Write out the range values: range(5) gives [0, 1, 2, 3, 4], NOT [0, 1, 2, 3, 4, 5].",
        "💡 Step 2: Trace through your loop manually with 3 items on paper.",
        "💡 Step 3: Check: does your index start at 0 or 1? Where does it end?",
        "💡 Step 4: Try changing your range by +1 or -1 and re-trace. Does it match now?",
        "💡 Step 5: Consider using enumerate() in Python to avoid index mistakes.",
    ],
    "infinite_loop": [
        "💡 Step 1: Find your while or for loop. What is the condition that should stop it?",
        "💡 Step 2: Inside the loop, look at the variable that controls the condition.",
        "💡 Step 3: Add a print(variable) inside the loop to see if it's actually changing.",
        "💡 Step 4: Verify the stopping variable is being modified in the right direction.",
        "💡 Step 5: If you can't find the issue, create a simple version with fewer steps.",
    ],
    "division_by_zero": [
        "💡 Step 1: Find where division (/ or //) happens in your code.",
        "💡 Step 2: Ask: Can the denominator ever be 0 with the inputs you're using?",
        "💡 Step 3: Add a guard clause: if denominator != 0: before dividing.",
        "💡 Step 4: Decide what to do if denominator is 0 (return error, skip, use 0, etc.)",
        "💡 Step 5: Test with a zero denominator to make sure your fix works.",
    ],
    "logical_error": [
        "💡 Step 1: Add print() statements before and after each suspicious section.",
        "💡 Step 2: Write down the expected value vs what you actually got.",
        "💡 Step 3: Trace each step of your logic on paper using a simple test case.",
        "💡 Step 4: Check edge cases: empty lists, single items, negative numbers, etc.",
        "💡 Step 5: Compare your logic to a reference or working example.",
    ],
    "bad_practice": [
        "💡 Step 1: Replace single-letter variable names (i, x, a) with descriptive names.",
        "💡 Step 2: Replace magic numbers with named constants (e.g., MAX_USERS = 100).",
        "💡 Step 3: If a function is longer than 20 lines, break it into smaller helpers.",
        "💡 Step 4: Add comments or a docstring explaining what the code does.",
        "💡 Step 5: Check style: consistent spacing, naming conventions, proper formatting.",
    ],
    "null_reference": [
        "💡 Step 1: Find where a None value is assigned or returned.",
        "💡 Step 2: Add a guard clause: if obj is not None: before using it.",
        "💡 Step 3: Make sure the function that produces the value always returns something.",
        "💡 Step 4: Initialize variables before using them: x = some_function() if x is not None.",
        "💡 Step 5: Use defensive programming: check for None at function boundaries.",
    ],
    "structural_issue": [
        "💡 Step 1: Identify blocks of code that do one specific, logical thing.",
        "💡 Step 2: Extract each block into its own named function.",
        "💡 Step 3: Each function should ideally do one thing and be under 20 lines.",
        "💡 Step 4: Use clear, descriptive function names that explain what they do.",
        "💡 Step 5: Reduce nesting: if you have 4+ levels, extract inner blocks.",
    ],
}

DEFAULT_HINTS = [
    "Step 1: Re-read the code slowly, line by line.",
    "Step 2: Try running just the broken section in isolation.",
    "Step 3: Search the exact error message online.",
]


def detect_errors_rule_based(code: str, language: str) -> list:
    """Detect errors using syntax checking and pattern matching. No ML needed."""
    errors = []

    if language == "python":
        # Syntax check via Python's own parser
        try:
            ast.parse(code)
        except SyntaxError as e:
            errors.append("syntax_error")
            # If we have a syntax error, still try to detect other patterns
            # but we can return early since AST won't work

        # Pattern: = inside if/elif/while condition (common beginner mistake)
        if re.search(r"\b(if|elif|while)\b.*[^=!<>]=(?!=)", code):
            errors.append("syntax_error")

        # Try AST-based checks if syntax is valid
        try:
            tree = ast.parse(code)
            
            # Check for various error patterns
            for node in ast.walk(tree):
                # Division without zero check
                if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
                    errors.append("division_by_zero")

                # while True with no break
                if isinstance(node, ast.While):
                    if isinstance(node.test, ast.Constant) and node.test.value is True:
                        has_break = any(
                            isinstance(n, ast.Break) for n in ast.walk(node)
                        )
                        if not has_break:
                            errors.append("infinite_loop")

                # Uninitialized variable access (simple heuristic)
                if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                    if node.id in ("undefined", "null"):
                        errors.append("null_reference")

                # range(len(...) + 1) — classic off-by-one
                if isinstance(node, ast.Call):
                    if getattr(getattr(node, "func", None), "id", "") == "range":
                        if node.args and isinstance(node.args[0], ast.BinOp):
                            if isinstance(node.args[0].op, ast.Add):
                                errors.append("off_by_one")

                # Check for deeply nested blocks
                if isinstance(node, (ast.For, ast.While, ast.If)):
                    depth = 0
                    current = node
                    while hasattr(current, "body") or hasattr(current, "orelse"):
                        depth += 1
                        current = node
                    if depth > 5:
                        errors.append("structural_issue")

        except Exception:
            # If we can't parse, we already added syntax_error above
            pass

        # Pattern-based checks that don't require AST
        if "import" in code and len(re.findall(r"^\s*import\s+\*", code, re.MULTILINE)) > 0:
            errors.append("bad_practice")  # wildcard imports

    elif language == "javascript":
        # JS syntax pattern checks
        
        # Empty statements (while(); for();)
        if re.search(r"\b(while|for)\s*\([^)]*\)\s*;", code):
            errors.append("infinite_loop")
        
        # Assignment in condition (if(x = 5) instead of if(x == 5 || x === 5))
        if re.search(r"\b(if|while|else\s+if)\s*\([^)]*[^=!<>]=(?![=>])[^=]", code):
            errors.append("syntax_error")
        
        # Missing variable declaration
        if re.search(r"(?<!var\s|let\s|const\s)\w+\s*=", code) and "=" in code:
            # Heuristic: might be missing var/let/const
            pass  # This would be too many false positives
        
        # Semicolon at end of block
        if re.search(r"\}\s*;", code):
            errors.append("syntax_error")

    elif language == "cpp":
        # C++ specific error patterns
        
        # Missing semicolons (simplified heuristic)
        lines = code.split("\n")
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped and not stripped.startswith("//"):
                # Lines that should end with semicolon but don't
                if re.match(r".*[a-zA-Z0-9\)\]]$", stripped):
                    if not stripped.endswith((";", "{", "}", ":", "|", "\\", "*")):
                        if i < len(lines) - 1:
                            next_line = lines[i+1].strip()
                            if next_line and not next_line.startswith(("{", "}")):
                                errors.append("syntax_error")
                                break

    elif language == "java":
        # Java specific patterns
        
        # Missing semicolons
        if re.search(r"[a-zA-Z0-9\)]\s*\n\s*[a-z]", code):  # likely incomplete statement
            if ";" not in code.split("\n")[-1]:
                errors.append("syntax_error")

    # Universal checks
    
    # Deeply nested code (more than 4 levels of indentation)
    max_indent = (
        max(
            (len(line) - len(line.lstrip()))
            for line in code.split("\n")
            if line.strip()
        )
        if code.strip()
        else 0
    )
    # 4 spaces per level, so 16 spaces = 4 levels
    if max_indent >= 16:
        errors.append("structural_issue")

    # Very long lines (hard to read)
    long_lines = sum(1 for line in code.split("\n") if len(line) > 120)
    if long_lines >= 2:
        errors.append("bad_practice")

    # Check for TODO/FIXME comments (incomplete code)
    if re.search(r"(TODO|FIXME|XXX|HACK):", code, re.IGNORECASE):
        errors.append("bad_practice")

    if not errors:
        errors.append("bad_practice")

    return list(dict.fromkeys(errors))  # deduplicate, preserve order


def score_code(code: str) -> tuple[int, list]:
    """Score code quality 0-100 and return improvement suggestions."""
    score = 100
    suggestions = []
    lines = code.strip().split("\n")

    # Check for very long lines (hard to read)
    long_lines = [l for l in lines if len(l) > 100]
    if long_lines:
        score -= len(long_lines) * 3
        suggestions.append(
            f"Shorten {len(long_lines)} line(s) that exceed 100 characters."
        )

    # Check for deep nesting (hard to follow logic)
    deep = sum(1 for l in lines if l.startswith("    " * 4))
    if deep:
        score -= deep * 5
        suggestions.append(
            "Reduce deep nesting — consider extracting inner blocks into functions."
        )

    # Check for magic numbers
    magic = len(re.findall(r"\b(?<!\.)(?!0\b)\d{2,}\b", code))
    if magic:
        score -= magic * 2
        suggestions.append(f"Replace {magic} magic number(s) with named constants.")

    # Check for bad variable names (single letters except common loop counters)
    bad_vars = len(re.findall(r"\b(?![ijknxy])[a-wz]\b\s*=", code))
    if bad_vars:
        score -= bad_vars * 3
        suggestions.append("Use descriptive variable names instead of single letters.")

    # Check for missing documentation
    if len(lines) > 15 and '"""' not in code and "'''" not in code and "#" not in code:
        score -= 10
        suggestions.append("Add comments or docstrings to explain what the code does.")

    # Check for commented-out code (usually indicates unfinished work)
    commented = len(re.findall(r"^\s*#.*=|^\s*#.*\(", code, re.MULTILINE))
    if commented > 2:
        score -= commented
        suggestions.append("Remove or uncomment large blocks of commented-out code.")

    # Check for TODO/FIXME comments (incomplete code)
    todos = len(re.findall(r"(TODO|FIXME|XXX|HACK):", code, re.IGNORECASE))
    if todos:
        score -= todos * 5
        suggestions.append(f"Complete {todos} TODO/FIXME comment(s) in your code.")

    # Check for inconsistent indentation
    indents = [len(l) - len(l.lstrip()) for l in lines if l.strip()]
    if indents:
        # Check if all indentations are multiples of 4 (Python convention)
        non_multiple = sum(1 for i in indents if i > 0 and i % 4 != 0)
        if non_multiple > 0:
            score -= non_multiple * 2
            suggestions.append("Use consistent indentation (4 spaces per level in Python).")

    # Check for repeated code patterns (code duplication)
    code_lines = [l.strip() for l in lines if l.strip() and not l.strip().startswith("#")]
    if len(code_lines) > 5:
        # Simple heuristic: look for repeated lines
        from collections import Counter
        line_counts = Counter(code_lines)
        duplicates = sum(1 for count in line_counts.values() if count > 2)
        if duplicates > 0:
            score -= duplicates * 2
            suggestions.append("Reduce code duplication — extract repeated patterns into functions.")

    # Positive feedback if none of the above issues found
    if not suggestions:
        suggestions.append("Excellent code! Clean, readable, and well-structured.")

    return max(0, min(100, score)), suggestions


# ---------------------------------------------------------------------------
# ML pipeline (loaded only if model exists)
# ---------------------------------------------------------------------------

_pipeline = None
MODEL_PATH = os.environ.get(
    "POLYMENTOR_MODEL_PATH", "models_saved/best_mentor_model.pt"
)


@app.on_event("startup")
async def startup():
    global _pipeline
    if Path(MODEL_PATH).exists():
        try:
            # Only import heavy ML deps when model actually exists
            from src.inference.pipeline import PolyMentorPipeline

            _pipeline = PolyMentorPipeline.from_pretrained(MODEL_PATH)
            print(f"✅ ML pipeline loaded from {MODEL_PATH}")
        except Exception as e:
            print(f"⚠️  ML pipeline failed to load: {e}")
            print("   Falling back to rule-based mode.")
            _pipeline = None
    else:
        print("ℹ️  No trained model found — running in rule-based mode.")
        print(f"   Train a model with: bash scripts/train.sh")
        print(f"   Then restart the API.")


# ---------------------------------------------------------------------------
# Request / Response schemas
# ---------------------------------------------------------------------------


class AnalyzeRequest(BaseModel):
    code: str = Field(..., description="Source code to analyze.")
    language: str = Field("python", description="python | javascript | cpp | java")
    level: str = Field("beginner", description="beginner | intermediate | advanced")
    num_hints: int = Field(3, ge=1, le=5)


class AnalyzeResponse(BaseModel):
    status: str
    mode: str  # "ml" or "rule_based"
    error_type: Optional[str]
    error_types: List[str]
    explanation: str
    hint: str
    hints: List[str]
    concept_taught: str
    quality_score: int
    suggestions: List[str]
    language: str
    level: str
    elapsed_ms: float


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@app.get("/health")
async def health():
    """Health check."""
    return {
        "status": "ok",
        "mode": "ml" if _pipeline is not None else "rule_based",
        "model_loaded": _pipeline is not None,
        "model_path": MODEL_PATH,
    }


@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze(request: AnalyzeRequest):
    """Analyze a code snippet. Works in both rule-based and ML mode."""
    start = time.perf_counter()

    code = request.code.strip()
    language = request.language.lower()
    level = request.level.lower()

    if not code:
        return AnalyzeResponse(
            status="clean",
            mode="rule_based",
            error_type=None,
            error_types=[],
            explanation="No code provided.",
            hint="",
            hints=[],
            concept_taught="",
            quality_score=0,
            suggestions=["Paste your code to get feedback."],
            language=language,
            level=level,
            elapsed_ms=0.0,
        )

    # --- Use ML pipeline if available ---
    if _pipeline is not None:
        try:
            result = _pipeline.analyze(code=code, language=language, level=level)
            elapsed = (time.perf_counter() - start) * 1000
            return AnalyzeResponse(
                status=result.status,
                mode="ml",
                error_type=result.error_type,
                error_types=result.error_types,
                explanation=result.explanation,
                hint=result.hint,
                hints=result.hints,
                concept_taught=result.concept_taught,
                quality_score=result.quality_score,
                suggestions=getattr(result, "suggestions", []),
                language=language,
                level=level,
                elapsed_ms=round(elapsed, 2),
            )
        except Exception as e:
            print(f"ML pipeline error: {e}, falling back to rule-based")

    # --- Rule-based fallback ---
    error_types = detect_errors_rule_based(code, language)
    primary = error_types[0] if error_types else "bad_practice"

    explanation = EXPLANATIONS.get(primary, "An issue was detected in your code.")
    all_hints = HINTS.get(primary, DEFAULT_HINTS)

    # Adjust hints by level
    if level == "advanced":
        hints = all_hints[-1:]
    elif level == "intermediate":
        hints = all_hints[1:]
    else:
        hints = all_hints

    hints = hints[: request.num_hints]
    concept = ERROR_TO_CONCEPT.get(primary, "General Programming")
    quality, suggestions = score_code(code)
    elapsed = (time.perf_counter() - start) * 1000

    is_clean = error_types == ["bad_practice"] and quality >= 80

    return AnalyzeResponse(
        status="clean" if is_clean else "error_found",
        mode="rule_based",
        error_type=None if is_clean else primary,
        error_types=[] if is_clean else error_types,
        explanation=(
            "No errors detected! Code looks clean." if is_clean else explanation
        ),
        hint=hints[0] if hints else "",
        hints=hints,
        concept_taught="" if is_clean else concept,
        quality_score=quality,
        suggestions=suggestions,
        language=language,
        level=level,
        elapsed_ms=round(elapsed, 2),
    )


@app.get("/")
async def root():
    return {
        "message": "PolyMentor API is running!",
        "docs": "/docs",
        "health": "/health",
        "analyze": "POST /analyze",
        "mode": "ml" if _pipeline is not None else "rule_based",
    }
