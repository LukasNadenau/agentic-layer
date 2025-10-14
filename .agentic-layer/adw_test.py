"""Agentic Development Workflow Test Script.

This script orchestrates running tests for a workflow run.
"""
# /// script
# dependencies = [
#   "claude-agent-sdk",
#   "python-dotenv",
# ]
# ///

import sys
import asyncio
import argparse

from run_tests import implement_spec


async def main():
    """Main orchestration function for the ADW test flow."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Run tests for Agentic Development Workflow")
    parser.add_argument("--run_id", required=True, help="The run identifier")
    parser.add_argument("--test_results", required=True, help="Path to the test results folder")

    args = parser.parse_args()

    try:
        success = await implement_spec(args.run_id, args.test_results)
        if not success:
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
