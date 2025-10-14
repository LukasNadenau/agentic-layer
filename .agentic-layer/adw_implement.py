"""Agentic Development Workflow Implementation Script.

This script orchestrates the implementation of specification files for a workflow run.
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

from implement_spec import implement_spec


async def main():
    """Main orchestration function for the ADW implementation flow."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Implement specification file for Agentic Development Workflow")
    parser.add_argument("--run_id", required=True, help="The run identifier")
    parser.add_argument("--spec", required=True, help="Path to the spec file")

    args = parser.parse_args()

    try:
        success = await implement_spec(args.run_id, args.spec)
        if not success:
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
