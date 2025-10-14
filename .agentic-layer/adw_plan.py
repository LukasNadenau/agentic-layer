"""Agentic Development Workflow Planning Script.

This script orchestrates the creation of specification files for a workflow run.
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

from create_spec import create_spec
from models import DraftClass


async def main():
    """Main orchestration function for the ADW planning flow."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Create specification file for Agentic Development Workflow")
    parser.add_argument("--run_id", required=True, help="The run identifier")
    parser.add_argument("--draft", required=True, help="Path to the draft file")
    parser.add_argument("--draft_class", required=True, choices=["feature", "bug"], help="Classification of the draft (feature or bug)")

    args = parser.parse_args()

    # Convert draft_class string to DraftClass enum
    draft_class = DraftClass.FEATURE if args.draft_class.lower() == "feature" else DraftClass.BUG

    try:
        success = await create_spec(args.run_id, args.draft, draft_class)
        if not success:
            sys.exit(1)
    except (FileNotFoundError, ValueError, RuntimeError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
