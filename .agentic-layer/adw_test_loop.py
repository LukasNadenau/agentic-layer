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


async def main():
    """Main orchestration function for the ADW test loop flow."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Run tests and resolve failures in a loop until all tests pass")
    parser.add_argument("--path", required=True, help="Path to directory for test result XML files")
    parser.add_argument("--run_id", required=True, help="The run identifier")

    args = parser.parse_args()

    try:
        test_path = Path(args.path)
        if not test_path.exists():
            raise FileNotFoundError(f"Test results path does not exist: {args.path}")

        iteration = 0
        max_iterations = 10  # Prevent infinite loops

        while iteration < max_iterations:
            iteration += 1
            print(f"\n{'='*60}")
            print(f"Test Loop Iteration {iteration}")
            print(f"{'='*60}")

            # Run tests
            print("\n[1/4] Running tests...")
            success = await run_tests(args.run_id, args.path)
            if not success:
                print("Warning: Test run may not have completed successfully", file=sys.stderr)

            # Check for failing tests
            print("\n[2/4] Checking for failures...")
            failing_suites = get_failing_test_suites(args.path)

            if not failing_suites:
                print("\n All tests passed! Exiting loop.")
                break

            print(f"\n[3/4] Found {len(failing_suites)} test suite(s) with failures.")

            # Resolve each failing test suite
            for suite in failing_suites:
                print(f"  ’ Resolving test suite: {suite.name}")
                success = await resolve_test(suite)
                if not success:
                    print(f"  Warning: Resolution may not have completed successfully for suite: {suite.name}", file=sys.stderr)

            # Clean up XML files for next iteration
            print("\n[4/4] Cleaning up test results...")
            xml_files = list(test_path.glob("*.xml"))
            for xml_file in xml_files:
                xml_file.unlink()
            print(f"  Deleted {len(xml_files)} XML file(s)")

        if iteration >= max_iterations:
            print(f"\nWarning: Reached maximum iteration limit ({max_iterations}). Some tests may still be failing.", file=sys.stderr)
            sys.exit(1)

    except (FileNotFoundError, ValueError, RuntimeError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
