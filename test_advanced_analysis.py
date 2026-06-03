"""
Test suite for Advanced Code Analysis System
============================================

Tests all new endpoints for multi-language code analysis,
error detection, and real-time suggestions.
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")

def print_success(text):
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")

def print_error(text):
    print(f"{Colors.RED}✗ {text}{Colors.END}")

def print_info(text):
    print(f"{Colors.BLUE}ℹ {text}{Colors.END}")

def print_json(data):
    print(json.dumps(data, indent=2))

# =========================================================================
# TEST CASES
# =========================================================================

def test_get_languages():
    """Test GET /languages endpoint"""
    print_header("TEST 1: GET /languages")
    
    try:
        response = requests.get(f"{BASE_URL}/languages")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        assert "supported_languages" in data
        assert len(data["supported_languages"]) >= 4
        
        print_success("Endpoint works")
        print_info(f"Supported languages: {', '.join(data['supported_languages'])}")
        return True
    except Exception as e:
        print_error(f"Test failed: {e}")
        return False


def test_analyze_detailed_python():
    """Test POST /analyze/detailed for Python"""
    print_header("TEST 2: Analyze Python Code (Detailed)")
    
    code = """
def calculate_sum(numbers):
    total = 0
    for i in range(len(numbers) + 1):  # off-by-one error
        total += numbers[i]
    return total
"""
    
    try:
        response = requests.post(
            f"{BASE_URL}/analyze/detailed",
            json={"code": code, "language": "python"}
        )
        assert response.status_code == 200
        
        data = response.json()
        assert data["supported"] == True
        assert data["total_errors"] > 0
        
        print_success("Endpoint works")
        print_info(f"Detected {data['total_errors']} error(s)")
        print_info(f"Quality score: {data['quality_score']}/100")
        
        if data["errors"]:
            print_info("First error:")
            print_json(data["errors"][0])
        
        return True
    except Exception as e:
        print_error(f"Test failed: {e}")
        return False


def test_analyze_detailed_javascript():
    """Test POST /analyze/detailed for JavaScript"""
    print_header("TEST 3: Analyze JavaScript Code (Detailed)")
    
    code = """
function processArray(arr) {
    var result = [];
    for (var i = 0; i < arr.length; i++) {
        if (arr[i] = null) {  // assignment instead of comparison
            result.push(0);
        }
    }
    return result;
}
"""
    
    try:
        response = requests.post(
            f"{BASE_URL}/analyze/detailed",
            json={"code": code, "language": "javascript"}
        )
        assert response.status_code == 200
        
        data = response.json()
        print_success("Endpoint works")
        print_info(f"Detected {data['total_errors']} error(s)")
        print_info(f"Severity breakdown: {data['severity_breakdown']}")
        
        return True
    except Exception as e:
        print_error(f"Test failed: {e}")
        return False


def test_analyze_detailed_cpp():
    """Test POST /analyze/detailed for C++"""
    print_header("TEST 4: Analyze C++ Code (Detailed)")
    
    code = """
#include <iostream>
using namespace std;

int main() {
    int* ptr = new int(5);
    // forgot to delete
    return 0
}
"""
    
    try:
        response = requests.post(
            f"{BASE_URL}/analyze/detailed",
            json={"code": code, "language": "cpp"}
        )
        assert response.status_code == 200
        
        data = response.json()
        print_success("Endpoint works")
        print_info(f"Detected {data['total_errors']} error(s)")
        
        return True
    except Exception as e:
        print_error(f"Test failed: {e}")
        return False


def test_analyze_detailed_java():
    """Test POST /analyze/detailed for Java"""
    print_header("TEST 5: Analyze Java Code (Detailed)")
    
    code = """
public class StringCompare {
    public static void main(String[] args) {
        String name = "John";
        if (name == "John") {  // should use .equals()
            System.out.println("Hello");
        }
    }
}
"""
    
    try:
        response = requests.post(
            f"{BASE_URL}/analyze/detailed",
            json={"code": code, "language": "java"}
        )
        assert response.status_code == 200
        
        data = response.json()
        print_success("Endpoint works")
        print_info(f"Detected {data['total_errors']} error(s)")
        
        return True
    except Exception as e:
        print_error(f"Test failed: {e}")
        return False


def test_quality_score():
    """Test POST /quality-score endpoint"""
    print_header("TEST 6: Quality Score")
    
    test_cases = [
        ("def add(a, b):\n    return a + b", "python", 85),
        ("const x = 5;", "javascript", 75),
        ("int x = 0;", "cpp", 75),
        ("int x = 5;", "java", 75),
    ]
    
    try:
        for code, language, min_score in test_cases:
            response = requests.post(
                f"{BASE_URL}/quality-score",
                json={"code": code, "language": language}
            )
            assert response.status_code == 200
            
            data = response.json()
            print_info(f"{language}: {data['quality_score']}/100 ({data['interpretation']})")
        
        print_success("All quality scores retrieved")
        return True
    except Exception as e:
        print_error(f"Test failed: {e}")
        return False


def test_suggestions():
    """Test POST /suggestions endpoint"""
    print_header("TEST 7: Real-Time Suggestions")
    
    code_with_issues = """
def process_data(x, y, z, a, b):
    ######################
    x = x + y
    y = y + z
    result = x + y
    # TODO: fix this
    ######################
    return result
"""
    
    try:
        response = requests.post(
            f"{BASE_URL}/suggestions",
            json={"code": code_with_issues, "language": "python"}
        )
        assert response.status_code == 200
        
        data = response.json()
        print_success(f"Generated {data['total_suggestions']} suggestion(s)")
        
        for suggestion in data["suggestions"][:3]:  # show first 3
            print_info(suggestion)
        
        return True
    except Exception as e:
        print_error(f"Test failed: {e}")
        return False


def test_errors_by_category():
    """Test POST /analyze/errors-by-category endpoint"""
    print_header("TEST 8: Errors by Category")
    
    code = """
def process():
    while True:  # infinite loop
        x = y  # undefined variable
        eval(x)  # security issue
"""
    
    try:
        response = requests.post(
            f"{BASE_URL}/analyze/errors-by-category",
            json={"code": code, "language": "python"}
        )
        assert response.status_code == 200
        
        data = response.json()
        print_success(f"Analyzed and categorized {data['total_errors']} error(s)")
        print_info(f"Categories found: {list(data['categories'].keys())}")
        
        for category, errors in data["categories"].items():
            print_info(f"  {category}: {len(errors)} error(s)")
        
        return True
    except Exception as e:
        print_error(f"Test failed: {e}")
        return False


def test_errors_by_severity():
    """Test POST /analyze/by-severity endpoint"""
    print_header("TEST 9: Errors by Severity")
    
    code = """
def buggy_function():
    for i in range(10):
        if i = 5:  # CRITICAL syntax error
            x = 1 / 0  # HIGH: division by zero
        else:
            y = y + 1  # MEDIUM: potential undefined
    
    # LOW: poor style
    MAGIC_NUMBER = 42
"""
    
    try:
        response = requests.post(
            f"{BASE_URL}/analyze/by-severity",
            json={"code": code, "language": "python"}
        )
        assert response.status_code == 200
        
        data = response.json()
        print_success("Severity analysis complete")
        print_info(f"Critical: {data['critical_count']}")
        print_info(f"High: {data['high_count']}")
        print_info(f"Medium: {data['medium_count']}")
        print_info(f"Low: {data['low_count']}")
        
        return True
    except Exception as e:
        print_error(f"Test failed: {e}")
        return False


def test_performance():
    """Test performance/response times"""
    print_header("TEST 10: Performance Benchmark")
    
    test_code = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
"""
    
    try:
        times = []
        
        for i in range(5):
            start = time.time()
            response = requests.post(
                f"{BASE_URL}/analyze/detailed",
                json={"code": test_code, "language": "python"}
            )
            elapsed = (time.time() - start) * 1000
            times.append(elapsed)
        
        avg_time = sum(times) / len(times)
        max_time = max(times)
        min_time = min(times)
        
        print_success("Performance test complete")
        print_info(f"Average response time: {avg_time:.2f}ms")
        print_info(f"Min: {min_time:.2f}ms, Max: {max_time:.2f}ms")
        
        if avg_time < 5:
            print_success("Performance is excellent (< 5ms)")
        elif avg_time < 10:
            print_info("Performance is good (< 10ms)")
        else:
            print_error("Performance could be improved (> 10ms)")
        
        return avg_time < 10  # Pass if < 10ms
    except Exception as e:
        print_error(f"Test failed: {e}")
        return False


def test_empty_code():
    """Test handling of empty code"""
    print_header("TEST 11: Empty Code Handling")
    
    try:
        response = requests.post(
            f"{BASE_URL}/analyze/detailed",
            json={"code": "", "language": "python"}
        )
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "empty"
        assert data["total_errors"] == 0
        
        print_success("Empty code handled correctly")
        return True
    except Exception as e:
        print_error(f"Test failed: {e}")
        return False


def test_unsupported_language():
    """Test handling of unsupported language"""
    print_header("TEST 12: Unsupported Language")
    
    try:
        response = requests.post(
            f"{BASE_URL}/analyze/detailed",
            json={"code": "x = 5", "language": "rust"}
        )
        assert response.status_code == 200
        
        data = response.json()
        assert data["supported"] == False
        
        print_success("Unsupported language handled gracefully")
        return True
    except Exception as e:
        print_error(f"Test failed: {e}")
        return False


def test_clean_code():
    """Test with clean, well-written code"""
    print_header("TEST 13: Clean Code Detection")
    
    code = """
def calculate_average(numbers: list) -> float:
    \"\"\"Calculate the average of a list of numbers.\"\"\"
    if not numbers:
        return 0.0
    return sum(numbers) / len(numbers)
"""
    
    try:
        response = requests.post(
            f"{BASE_URL}/analyze/detailed",
            json={"code": code, "language": "python"}
        )
        assert response.status_code == 200
        
        data = response.json()
        print_success("Clean code analysis complete")
        print_info(f"Quality score: {data['quality_score']}/100")
        
        if data["quality_score"] >= 80:
            print_success("Code quality is high")
        
        return True
    except Exception as e:
        print_error(f"Test failed: {e}")
        return False


# =========================================================================
# MAIN TEST RUNNER
# =========================================================================

def run_all_tests():
    """Run all test cases and report results"""
    print_header("POLYMENTOR ADVANCED ANALYSIS SYSTEM - TEST SUITE")
    print_info("Testing all new API endpoints for code analysis")
    print()
    
    tests = [
        ("Supported Languages", test_get_languages),
        ("Detailed Python Analysis", test_analyze_detailed_python),
        ("Detailed JavaScript Analysis", test_analyze_detailed_javascript),
        ("Detailed C++ Analysis", test_analyze_detailed_cpp),
        ("Detailed Java Analysis", test_analyze_detailed_java),
        ("Quality Score", test_quality_score),
        ("Real-Time Suggestions", test_suggestions),
        ("Errors by Category", test_errors_by_category),
        ("Errors by Severity", test_errors_by_severity),
        ("Performance Benchmark", test_performance),
        ("Empty Code Handling", test_empty_code),
        ("Unsupported Language", test_unsupported_language),
        ("Clean Code Detection", test_clean_code),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print_error(f"Test crashed: {e}")
            results.append((name, False))
    
    # Summary
    print_header("TEST SUMMARY")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = f"{Colors.GREEN}PASS{Colors.END}" if result else f"{Colors.RED}FAIL{Colors.END}"
        print(f"{status} - {name}")
    
    print()
    print_info(f"Tests passed: {passed}/{total} ({100*passed//total}%)")
    
    if passed == total:
        print_success("All tests passed! ✓")
    elif passed >= total * 0.8:
        print_info(f"Most tests passed ({passed}/{total})")
    else:
        print_error(f"Some tests failed ({passed}/{total})")
    
    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
