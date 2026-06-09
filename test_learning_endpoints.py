#!/usr/bin/env python3
"""Test the learning guidance endpoints"""

import requests
import json

BASE_URL = "http://localhost:8000"

# Test 1: List concepts
print("=" * 70)
print("TEST 1: GET /learn/concepts - List all available concepts")
print("=" * 70)
response = requests.get(f"{BASE_URL}/learn/concepts")
print(json.dumps(response.json(), indent=2))

# Test 2: Get detailed concept
print("\n" + "=" * 70)
print("TEST 2: GET /learn/concept/comparison_operators - Detailed concept")
print("=" * 70)
response = requests.get(f"{BASE_URL}/learn/concept/comparison_operators")
data = response.json()
print(f"Concept: {data['concept_name']}")
print(f"Difficulty: {data['difficulty']}")
print(f"Simple Explanation: {data['simple_explanation'][:150]}...")
print(f"Number of examples: {len(data['code_examples'])}")

# Test 3: Learn from error
print("\n" + "=" * 70)
print("TEST 3: POST /learn/from-error - Learn from buggy code")
print("=" * 70)
buggy_code = """for i in range(5):
    if i = 5:
        print(i)"""

response = requests.post(
    f"{BASE_URL}/learn/from-error",
    json={
        "code": buggy_code,
        "language": "python",
        "level": "beginner"
    }
)
data = response.json()
print(f"Status: {data['status']}")
print(f"Total errors: {data['total_errors']}")
print(f"Overall advice: {data['overall_advice']}")
if data.get('learning_materials'):
    print(f"\nFirst error learning material:")
    error_material = data['learning_materials'][0]
    print(f"  Error: {error_material['error']['message']}")
    print(f"  Category: {error_material['error']['category']}")
    print(f"  Severity: {error_material['error']['severity']}")
    if error_material.get('concept'):
        print(f"  Related concept: {error_material['concept']['name']}")
        print(f"  Concept explanation: {error_material['concept']['simple_explanation'][:100]}...")

# Test 4: Get learning path
print("\n" + "=" * 70)
print("TEST 4: GET /learn/path/comparison_operators - Learning path")
print("=" * 70)
response = requests.get(f"{BASE_URL}/learn/path/comparison_operators")
data = response.json()
print(f"Starting concept: {data['starting_concept']}")
print(f"Difficulty: {data['difficulty']}")
print(f"Tips:")
for tip in data['tips'][:3]:
    print(f"  - {tip}")

# Test 5: Explain code
print("\n" + "=" * 70)
print("TEST 5: POST /learn/explain-code - Explain what code does")
print("=" * 70)
code = """for i in range(5):
    if i == 3:
        print("Found 3!")"""

response = requests.post(
    f"{BASE_URL}/learn/explain-code",
    json={
        "code": code,
        "language": "python",
        "level": "beginner"
    }
)
data = response.json()
print(f"Status: {data['status']}")
print(f"Quality score: {data['quality_score']}")
print(f"Code length: {data['code_length']}")
print(f"Detected concepts: {', '.join([c['concept'] for c in data['detected_concepts']])}")
print(f"What this code does: {data['what_this_code_does']}")
print(f"Improvements: {', '.join(data['improvements_suggested'][:2])}")

print("\n" + "=" * 70)
print("✅ All tests completed successfully!")
print("=" * 70)
