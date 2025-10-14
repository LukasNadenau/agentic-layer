"""Agentic Development Workflow Test Resolution Script.

This script orchestrates the resolution of failed tests from JUnit XML test results.
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

from get_failing_test_suites import get_failing_test_suites
from resolve_test import resolve_test


async def main():
    """Main orchestration function for the ADW test resolution flow."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Resolve failed tests from JUnit XML results")
    parser.add_argument("--path", required=True, help="Path to directory containing JUnit XML test result files")

    args = parser.parse_args()

    try:
        # Get all failing test suites from the XML files
        failing_suites = get_failing_test_suites(args.path)

        if not failing_suites:
            print("No failing tests found.")
            return

        print(f"Found {len(failing_suites)} test suite(s) with failures.")

        # Resolve each failing test suite
        for suite in failing_suites:
            print(f"\nResolving test suite: {suite.name}")
            success = await resolve_test(suite)
            if not success:
                print(f"Warning: Resolution may not have completed successfully for suite: {suite.name}", file=sys.stderr)

        print("\nAll test suites processed.")

    except (FileNotFoundError, ValueError, RuntimeError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
