"""Agentic Development Workflow Initialization Script.

This script orchestrates the initialization of a new development workflow run.
"""
# /// script
# dependencies = [
#   "pydantic-ai",
#   "python-dotenv",
# ]
# ///

import sys
import asyncio
import argparse

from init_workflow import adw_init


async def main():
    """Main orchestration function for the ADW initialization flow."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Initialize the Agentic Development Workflow")
    parser.add_argument("--draft", required=True, help="Path to the draft file to process")
    parser.add_argument("--run_id", help="Optional run ID (generated if not provided)")
    parser.add_argument("--issue_id", help="Optional issue ID for branch naming")

    args = parser.parse_args()

    try:
        await adw_init(args.draft, args.run_id, args.issue_id)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
