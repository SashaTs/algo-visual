#!/usr/bin/env python3
"""
Test runner for the Algorithm Visualization Framework

This script runs all tests in the tests/ directory and provides a summary.
Usage:
    python run_tests.py                    # Run all tests
    python run_tests.py test_algorithms    # Run specific test pattern
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

def get_python_executable():
    """Get the correct Python executable path."""
    venv_python = Path(".venv/bin/python")
    if venv_python.exists():
        return str(venv_python.absolute())
    return sys.executable

def find_test_files(pattern=None):
    """Find all test files in the tests directory."""
    tests_dir = Path("tests")
    if not tests_dir.exists():
        print("❌ Tests directory not found!")
        return []
    
    if pattern:
        test_files = list(tests_dir.glob(f"*{pattern}*.py"))
    else:
        test_files = list(tests_dir.glob("test_*.py"))
    
    return [f for f in test_files if f.name != "__init__.py"]

def run_test_file(python_exe, test_file):
    """Run a single test file and return the result."""
    print(f"\n🧪 Running {test_file.name}")
    print("=" * 50)
    
    try:
        result = subprocess.run(
            [python_exe, str(test_file)],
            capture_output=True,
            text=True,
            timeout=60  # 60 second timeout
        )
        
        # Print output
        if result.stdout:
            print(result.stdout)
        if result.stderr and result.returncode != 0:
            print("❌ STDERR:", result.stderr)
        
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        print(f"❌ {test_file.name} timed out after 60 seconds")
        return False
    except Exception as e:
        print(f"❌ Error running {test_file.name}: {e}")
        return False

def main():
    """Main test runner function."""
    parser = argparse.ArgumentParser(description="Run algorithm visualization tests")
    parser.add_argument("pattern", nargs="?", help="Test file pattern to match")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    args = parser.parse_args()
    
    print("🚀 Algorithm Visualization Framework - Test Runner")
    print("=" * 60)
    
    # Find Python executable
    python_exe = get_python_executable()
    print(f"Using Python: {python_exe}")
    
    # Find test files
    test_files = find_test_files(args.pattern)
    if not test_files:
        if args.pattern:
            print(f"❌ No test files found matching pattern: {args.pattern}")
        else:
            print("❌ No test files found in tests/ directory")
        return 1
    
    print(f"Found {len(test_files)} test file(s):")
    for test_file in test_files:
        print(f"  📋 {test_file.name}")
    
    # Run tests
    results = {}
    total_tests = len(test_files)
    passed_tests = 0
    
    for test_file in test_files:
        success = run_test_file(python_exe, test_file)
        results[test_file.name] = success
        if success:
            passed_tests += 1
    
    # Summary
    print("\n📊 Test Results Summary")
    print("=" * 30)
    
    for test_name, success in results.items():
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{status}: {test_name}")
    
    print(f"\nOverall: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 All tests passed!")
        return 0
    else:
        print(f"❌ {total_tests - passed_tests} test(s) failed")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)