"""Agentic Development Workflow Test Loop Script.

This script orchestrates running tests and resolving failures in a loop until all tests pass.
"""
# /// script
# dependencies = [
#   "claude-agent-sdk",
#   "python-dotenv",
#   "junitparser",
# ]
# ///

import sys
import asyncio
import argparse
from pathlib import Path

from run_tests import run_tests
from get_failing_test_suites import get_failing_test_suites
from resolve_test import resolve_test


async def adw_test_loop(test_result_folder: str) -> bool:
    """
    Run tests and resolve failures in a loop until all tests pass.

    Args:
        run_id: The run identifier
        test_path: Path to directory for test result XML files

    Returns:
        bool: True if all tests passed, False if max iterations reached
    """
    test_path_obj = Path(test_result_folder)
    if not test_path_obj.exists():
        raise FileNotFoundError(f"Test results path does not exist: {test_result_folder}")

    iteration = 0
    max_iterations = 10  # Prevent infinite loops

    while iteration < max_iterations:
        iteration += 1
        print(f"\n{'='*60}")
        print(f"Test Loop Iteration {iteration}")
        print(f"{'='*60}")

        # Run tests
        print("\n[1/4] Running tests...")
        success = await run_tests(test_result_folder)
        if not success:
            print("Warning: Test run may not have completed successfully", file=sys.stderr)

        # Check for failing tests
        print("\n[2/4] Checking for failures...")
        failing_suites = get_failing_test_suites(test_result_folder)

        if not failing_suites:
            print("\nAll tests passed! Exiting loop.")
            return True

        print(f"\n[3/4] Found {len(failing_suites)} test suite(s) with failures.")

        # Resolve each failing test suite
        for suite in failing_suites:
            print(f"  Resolving test suite: {suite.name}")
            success = await resolve_test(suite)
            if not success:
                print(f"  Warning: Resolution may not have completed successfully for suite: {suite.name}", file=sys.stderr)

        # Clean up XML files for next iteration
        print("\n[4/4] Cleaning up test results...")
        xml_files = list(test_path_obj.glob("*.xml"))
        for xml_file in xml_files:
            xml_file.unlink()
        print(f"  Deleted {len(xml_files)} XML file(s)")

    print(f"\nWarning: Reached maximum iteration limit ({max_iterations}). Some tests may still be failing.", file=sys.stderr)
    return False


async def main():
    """Main orchestration function for the ADW test loop flow."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Run tests and resolve failures in a loop until all tests pass")
    parser.add_argument("--path", required=True, help="Path to directory for test result XML files")

    args = parser.parse_args()

    try:
        success = await adw_test_loop(args.path)
        if not success:
            sys.exit(1)
    except (FileNotFoundError, ValueError, RuntimeError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
