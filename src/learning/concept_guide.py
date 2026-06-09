"""
src/learning/concept_guide.py
-----------------------------

Concept teaching system - provides human-like explanations of programming concepts
and learning paths for different skill levels.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum


class ConceptDifficulty(Enum):
    """Concept difficulty levels"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


@dataclass
class CodeExample:
    """A code example with explanation"""
    title: str
    wrong_code: str
    right_code: str
    language: str
    explanation: str
    key_learning: str


@dataclass
class ConceptExplanation:
    """Complete concept explanation for teaching"""
    concept_name: str
    difficulty: ConceptDifficulty
    
    # Human-like explanation
    simple_explanation: str
    detailed_explanation: str
    
    # Related concepts
    prerequisites: List[str]  # Concepts to learn first
    related_concepts: List[str]  # Concepts to learn next
    
    # Examples
    examples: List[CodeExample]
    
    # Learning tips
    common_mistakes: List[str]
    tips_for_mastery: List[str]
    
    # Resources
    learning_resources: List[Dict[str, str]]  # [{"title": "...", "url": "..."}]


# ============================================================================
# CONCEPT DEFINITIONS
# ============================================================================

CONCEPT_LIBRARY: Dict[str, ConceptExplanation] = {
    "comparison_operators": ConceptExplanation(
        concept_name="Comparison Operators",
        difficulty=ConceptDifficulty.BEGINNER,
        simple_explanation=(
            "Comparison operators are symbols that let you check if two values are "
            "the same, different, or in a certain order. They always give you a "
            "yes/no answer (True or False)."
        ),
        detailed_explanation=(
            "When you need to make a decision in your code, you ask questions like "
            "'Is x bigger than 5?' or 'Are these two values equal?' Comparison operators "
            "answer these questions.\n\n"
            "Python has six main comparison operators:\n"
            "• == checks if two values are equal (they have the same value)\n"
            "• != checks if two values are NOT equal\n"
            "• < checks if the left value is smaller than the right\n"
            "• > checks if the left value is bigger than the right\n"
            "• <= checks if the left value is smaller OR equal to the right\n"
            "• >= checks if the left value is bigger OR equal to the right\n\n"
            "Important: Do NOT confuse = (assignment) with == (comparison). "
            "One creates a variable, the other asks a question."
        ),
        prerequisites=["variables", "data_types"],
        related_concepts=["logical_operators", "conditional_statements"],
        examples=[
            CodeExample(
                title="Checking Equality",
                wrong_code="if x = 5:\n    print('x is 5')",
                right_code="if x == 5:\n    print('x is 5')",
                language="python",
                explanation="= assigns a value, == compares values. In an if statement, we always need ==",
                key_learning="Assignment vs Comparison"
            ),
            CodeExample(
                title="Range Checking",
                wrong_code="if age > 18 and age < 65:\n    print('working age')",
                right_code="if 18 < age < 65:\n    print('working age')",
                language="python",
                explanation="Python allows chained comparisons for cleaner code",
                key_learning="Chaining Comparisons"
            ),
        ],
        common_mistakes=[
            "Using = instead of == in conditions",
            "Forgetting that == is needed for string comparisons",
            "Mixing up < and <= (off-by-one errors)",
            "Comparing strings without understanding string comparison rules",
        ],
        tips_for_mastery=[
            "Remember: = is for making, == is for checking",
            "Always test your conditions with specific values first",
            "Read comparisons out loud: 'if x is greater than 5'",
            "Practice writing conditions before using them in real code",
        ],
        learning_resources=[
            {"title": "Python Comparison Operators", "url": "https://www.w3schools.com/python/python_operators.asp"},
            {"title": "If Statements and Conditions", "url": "https://www.w3schools.com/python/python_conditions.asp"},
        ]
    ),
    
    "loop_boundaries": ConceptExplanation(
        concept_name="Loop Boundaries & Off-by-One Errors",
        difficulty=ConceptDifficulty.BEGINNER,
        simple_explanation=(
            "Loops repeat code multiple times. The boundary is where the loop starts and stops. "
            "Off-by-one means your loop starts or stops one step too early or too late."
        ),
        detailed_explanation=(
            "One of the most common bugs in programming is getting loop boundaries wrong. "
            "This happens because different languages count differently:\n\n"
            "In Python:\n"
            "• range(5) gives you 0, 1, 2, 3, 4 (NOT 5)\n"
            "• Lists are indexed 0, 1, 2... (the first item is 0, not 1)\n"
            "• range(1, 6) gives you 1, 2, 3, 4, 5 (starts at 1, stops BEFORE 6)\n\n"
            "Why this matters:\n"
            "If you have a list with 5 items and you accidentally try to access item 5, "
            "you'll get an 'index out of range' error because the items are numbered 0-4.\n\n"
            "How to avoid it:\n"
            "1. Always test with small examples (list of 3 items)\n"
            "2. Trace through manually: what numbers does my range produce?\n"
            "3. Remember: range(n) goes FROM 0 TO n-1, not FROM 0 TO n"
        ),
        prerequisites=["loops", "arrays_lists"],
        related_concepts=["arrays", "string_indexing", "array_slicing"],
        examples=[
            CodeExample(
                title="Correct List Access",
                wrong_code="items = ['a', 'b', 'c']\nfor i in range(len(items)):\n    print(items[i])  # What if i = 3?",
                right_code="items = ['a', 'b', 'c']\nfor i in range(len(items)):  # i is 0, 1, 2\n    print(items[i])  # Safe - never tries 3",
                language="python",
                explanation="range(3) gives 0, 1, 2 - exactly the valid indices",
                key_learning="range(n) means 0 through n-1"
            ),
            CodeExample(
                title="Using Enumerate Instead",
                wrong_code="for i in range(len(items)):\n    item = items[i]",
                right_code="for i, item in enumerate(items):\n    print(f'{i}: {item}')",
                language="python",
                explanation="enumerate() is safer and cleaner - it handles indexing for you",
                key_learning="Prefer enumerate() for loops"
            ),
        ],
        common_mistakes=[
            "Forgetting that range(n) stops at n-1, not n",
            "Using <= when you should use <",
            "Starting at 1 instead of 0 when accessing arrays",
            "Adding +1 or -1 without thinking through the logic",
        ],
        tips_for_mastery=[
            "Always manually trace your loop with pen and paper",
            "Test with a 3-item list to make sure your boundaries work",
            "Use enumerate() instead of range(len()) - it's safer",
            "When in doubt, print out the values to see what's happening",
        ],
        learning_resources=[
            {"title": "Python range() Function", "url": "https://www.w3schools.com/python/ref_func_range.asp"},
            {"title": "Array Indexing", "url": "https://www.w3schools.com/python/python_lists.asp"},
        ]
    ),
    
    "type_safety": ConceptExplanation(
        concept_name="Type Safety & Type Errors",
        difficulty=ConceptDifficulty.BEGINNER,
        simple_explanation=(
            "Every value in programming has a type: numbers, text, true/false, lists, etc. "
            "Type errors happen when you try to do something that doesn't work with that type."
        ),
        detailed_explanation=(
            "Think of types like boxes:\n"
            "• A number box can hold 42\n"
            "• A text box can hold 'hello'\n"
            "• A list box can hold [1, 2, 3]\n\n"
            "You can't put a text box into a number operation. For example, "
            "you CAN'T do: '5' + 3 (text five plus number three)\n\n"
            "Common type errors:\n"
            "• Adding strings and numbers: '5' + 3\n"
            "• Using .upper() on a number\n"
            "• Calling .append() on something that's not a list\n"
            "• Trying to loop over a number\n\n"
            "How to fix it:\n"
            "1. Convert the value to the right type\n"
            "2. Check what type something is with type(x)\n"
            "3. Read error messages carefully - they tell you what went wrong"
        ),
        prerequisites=["variables", "data_types"],
        related_concepts=["type_conversion", "error_handling"],
        examples=[
            CodeExample(
                title="String and Number Addition",
                wrong_code="age = 25\nmessage = 'I am ' + age + ' years old'\nprint(message)",
                right_code="age = 25\nmessage = f'I am {age} years old'\nprint(message)",
                language="python",
                explanation="Can't add string and number. Use f-strings or str() to convert",
                key_learning="Convert types when mixing them"
            ),
            CodeExample(
                title="Method on Wrong Type",
                wrong_code="number = 42\ntext = number.upper()  # numbers don't have .upper()",
                right_code="number = 42\ntext = str(number).upper()  # Convert to text first",
                language="python",
                explanation="Methods only work on their correct type",
                key_learning="Check the type before using methods"
            ),
        ],
        common_mistakes=[
            "Forgetting to convert user input from string to number",
            "Trying to use string methods on numbers",
            "Not realizing that '5' and 5 are different types",
            "Mixing lists and single values",
        ],
        tips_for_mastery=[
            "Use type(x) to check what something is",
            "Read error messages - they tell you the actual and expected types",
            "Remember: 'hello' is text, 42 is a number, [1,2,3] is a list",
            "When taking user input, remember it's always a string at first",
        ],
        learning_resources=[
            {"title": "Python Data Types", "url": "https://www.w3schools.com/python/python_datatypes.asp"},
            {"title": "Type Conversion", "url": "https://www.w3schools.com/python/python_type_casting.asp"},
        ]
    ),
    
    "null_safety": ConceptExplanation(
        concept_name="Null/None Safety - Checking Before Using",
        difficulty=ConceptDifficulty.INTERMEDIATE,
        simple_explanation=(
            "None (or null in other languages) means 'nothing' or 'no value'. "
            "Many bugs happen when code tries to use None as if it has a value."
        ),
        detailed_explanation=(
            "Sometimes a variable doesn't have a value - it's None. This is NOT the same "
            "as 0 or an empty string. It means the variable is empty.\n\n"
            "Why do null pointer exceptions happen?\n"
            "You try to use None like it has a value. For example:\n"
            "• Calling a method on None: result.upper() when result is None\n"
            "• Accessing a property of None: obj.name when obj is None\n"
            "• Indexing into None: items[0] when items is None\n\n"
            "How to prevent it:\n"
            "1. Always check if something is None before using it\n"
            "2. Use 'if value is not None:' or 'if value:'\n"
            "3. Use default values: value = result or default_value\n"
            "4. Use .get() on dictionaries instead of direct access"
        ),
        prerequisites=["variables", "conditional_statements"],
        related_concepts=["error_handling", "defensive_programming"],
        examples=[
            CodeExample(
                title="Dangerous: No Null Check",
                wrong_code="result = find_user(user_id)\nprint(result.name)  # What if result is None?",
                right_code="result = find_user(user_id)\nif result is not None:\n    print(result.name)\nelse:\n    print('User not found')",
                language="python",
                explanation="Always check before accessing properties",
                key_learning="Check for None before using"
            ),
            CodeExample(
                title="Safe Dictionary Access",
                wrong_code="user = {'name': 'John'}\nage = user['age']  # Key might not exist",
                right_code="user = {'name': 'John'}\nage = user.get('age', 18)  # Default to 18 if not found",
                language="python",
                explanation=".get() safely returns a default if the key doesn't exist",
                key_learning="Use .get() for safe dictionary access"
            ),
        ],
        common_mistakes=[
            "Forgetting that functions can return None",
            "Not checking if a dictionary key exists before accessing it",
            "Assuming API responses will always have data",
            "Not handling empty lists or empty results",
        ],
        tips_for_mastery=[
            "Always think: 'What if this is None?'",
            "Use defensive programming - assume things might be missing",
            "Check error messages - they often point to where None was used",
            "Use .get() for dictionaries and check list length before indexing",
        ],
        learning_resources=[
            {"title": "Python None Type", "url": "https://www.w3schools.com/python/ref_keyword_none.asp"},
            {"title": "Exception Handling", "url": "https://www.w3schools.com/python/python_try_except.asp"},
        ]
    ),
    
    "loop_control": ConceptExplanation(
        concept_name="Loop Control - When to Stop",
        difficulty=ConceptDifficulty.BEGINNER,
        simple_explanation=(
            "Loops repeat code. You need to tell the loop when to stop. "
            "If the stopping condition never happens, the loop runs forever."
        ),
        detailed_explanation=(
            "Every loop needs a stopping condition. Without it, the loop never ends.\n\n"
            "In a for loop:\n"
            "• for i in range(5): stops automatically after 5 times\n"
            "• for item in list: stops after processing every item\n\n"
            "In a while loop:\n"
            "• You must write the stopping condition: while i < 10:\n"
            "• You must change the variable so it eventually matches the condition\n\n"
            "Common infinite loop mistakes:\n"
            "• Variable never changes: while x < 10: (but x never changes inside)\n"
            "• Condition always true: while True: (with no break)\n"
            "• Wrong comparison: while x < 10: when x = 10 initially\n\n"
            "How to debug:\n"
            "• Add print statements to see values each iteration\n"
            "• Manually trace what happens with starting values\n"
            "• Ask: 'Does this condition ever become false?'"
        ),
        prerequisites=["loops", "comparison_operators"],
        related_concepts=["break_continue", "conditionals"],
        examples=[
            CodeExample(
                title="Infinite Loop Problem",
                wrong_code="i = 1\nwhile i < 10:\n    print(i)\n    # i never changes! Infinite loop",
                right_code="i = 1\nwhile i < 10:\n    print(i)\n    i += 1  # i increases each time",
                language="python",
                explanation="The variable must change toward the stopping condition",
                key_learning="Always update the loop variable"
            ),
            CodeExample(
                title="Safe Loop with For",
                wrong_code="while True:\n    print('forever...')",
                right_code="for i in range(5):\n    print('i:', i)  # Stops after 5",
                language="python",
                explanation="for loops are safer - they stop automatically",
                key_learning="Use for when you know how many times to loop"
            ),
        ],
        common_mistakes=[
            "Forgetting to update the loop variable",
            "Using = instead of == in the condition",
            "Having a condition that's never false",
            "Modifying the loop variable in the wrong direction",
        ],
        tips_for_mastery=[
            "Use for loops when you know how many times to repeat",
            "Use while loops only when the number of times is unknown",
            "Add print statements to debug loops",
            "Manually trace: what are the values on iteration 1, 2, 3, and when does it stop?",
        ],
        learning_resources=[
            {"title": "Python While Loops", "url": "https://www.w3schools.com/python/python_while_loops.asp"},
            {"title": "Python For Loops", "url": "https://www.w3schools.com/python/python_for_loops.asp"},
        ]
    ),
}


def get_concept_explanation(concept_name: str, level: str = "beginner") -> Optional[ConceptExplanation]:
    """Get explanation for a concept at a specific level"""
    return CONCEPT_LIBRARY.get(concept_name.lower())


def get_learning_path(starting_concept: str) -> Dict[str, List[str]]:
    """Get a learning path starting from a concept"""
    concept = get_concept_explanation(starting_concept)
    if not concept:
        return {}
    
    return {
        "start": starting_concept,
        "prerequisites": concept.prerequisites,
        "learn_next": concept.related_concepts,
        "difficulty": concept.difficulty.value,
    }


def get_concept_examples(concept_name: str, language: str = "python") -> List[CodeExample]:
    """Get code examples for a concept in a specific language"""
    concept = get_concept_explanation(concept_name)
    if not concept:
        return []
    
    return [ex for ex in concept.examples if ex.language.lower() == language.lower()]


def format_concept_for_learning(concept_name: str) -> Dict:
    """Format concept explanation for API response"""
    concept = get_concept_explanation(concept_name)
    if not concept:
        return {"error": f"Concept '{concept_name}' not found"}
    
    return {
        "concept_name": concept.concept_name,
        "difficulty": concept.difficulty.value,
        "simple_explanation": concept.simple_explanation,
        "detailed_explanation": concept.detailed_explanation,
        "prerequisites": concept.prerequisites,
        "related_concepts": concept.related_concepts,
        "common_mistakes": concept.common_mistakes,
        "tips_for_mastery": concept.tips_for_mastery,
        "learning_resources": concept.learning_resources,
        "examples_count": len(concept.examples),
    }
