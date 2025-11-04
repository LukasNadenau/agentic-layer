"""Agentic Development Workflow Review Loop Script.

This script orchestrates running reviews and patching issues in a loop
until no blocker issues remain.
"""
# /// script
# dependencies = [
#   "claude-agent-sdk",
#   "python-dotenv",
#   "rich",
# ]
# ///

import json
import logging
from pathlib import Path

from console import console
from coding_agent import call_coding_agent
from get_or_create_folders import get_or_create_review_folder
from agent_types import AgentType


async def adw_review(
    run_id: str,
    spec_file_path: str,
    agent_type: AgentType,
    review_json_path: str | None = None
) -> bool:
    # pylint: disable=too-many-locals,too-many-statements
    """
    Run review and patch loop until no blocker issues remain.

    Args:
        run_id: The run identifier for this workflow execution
        spec_file_path: Path to the specification file
        agent_type: Type of coding agent to use (CLAUDE or COPILOT)
        review_json_path: Optional path where the review JSON output should be written.
                         If not provided, will be constructed as {review_folder}/review.json

    Returns:
        bool: True if review passed (no blocker issues), False if max iterations reached
    """
    logger = logging.getLogger(__name__)
    logger.info("Starting review loop - run_id: %s, spec: %s", run_id, spec_file_path)

    iteration = 0
    max_iterations = 5

    # Determine review JSON path - construct if not provided
    if review_json_path is None:
        review_folder = get_or_create_review_folder(run_id)
        review_json_path_obj = review_folder / "review.json"
    else:
        review_json_path_obj = Path(review_json_path)

    while iteration < max_iterations:
        iteration += 1
        console.rule(f"[cyan]Review Loop Iteration {iteration}[/cyan]")
        logger.info("Review loop iteration %s starting", iteration)

        # Step 1: Run review command
        console.print("\n[blue][1/3][/blue] Running review...")
        logger.info("Calling review agent")
        try:
            await call_coding_agent(
                agent_type, "review", [run_id, str(spec_file_path), str(review_json_path_obj)]
            )
        except Exception as e:
            logger.error("Review command failed: %s", e, exc_info=True)
            raise RuntimeError(f"Review command failed: {e}") from e

        # Step 2: Parse review results
        console.print("\n[blue][2/3][/blue] Parsing review results...")
        logger.debug("Reading review JSON from: %s", review_json_path_obj)

        if not review_json_path_obj.exists():
            logger.warning("Review JSON not found at %s - treating as successful review", review_json_path_obj)
            console.print("\n[green]✓[/green] No review JSON found - treating as successful review (no issues).")
            return True

        try:
            with open(review_json_path_obj, 'r', encoding='utf-8') as f:
                review_data = json.load(f)
        except json.JSONDecodeError as e:
            logger.error("Failed to parse review JSON: %s", e, exc_info=True)
            raise RuntimeError(f"Invalid review JSON: {e}") from e

        # Step 4: Check for issues
        review_issues = review_data.get('review_issues', [])
        blocker_issues = [
            issue for issue in review_issues
            if issue.get('issue_severity') == 'blocker'
        ]

        review_msg = (
            f"  Found {len(review_issues)} total issues, "
            f"{len(blocker_issues)} blockers"
        )
        console.print(review_msg)
        logger.info(
            "Review found %s total issues, %s blockers",
            len(review_issues), len(blocker_issues)
        )

        # Step 5: If no blockers, we're done
        if not blocker_issues:
            console.print(
                "\n[green]✓[/green] No blocker issues found! Review passed."
            )
            logger.info("Review passed - no blocker issues")
            return True

        # Step 6: Fix blocker issues
        issue_count = len(blocker_issues)
        console.print(
            f"\n[blue][3/3][/blue] Fixing {issue_count} blocker issue(s)..."
        )
        for issue in blocker_issues:
            issue_num = issue.get('review_issue_number')
            issue_desc = issue.get('issue_description')
            issue_resolution = issue.get('issue_resolution')

            console.print(
                f"  Patching issue #{issue_num}: {issue_desc[:60]}..."
            )
            logger.info("Patching issue #%s: %s", issue_num, issue_desc)

            # Create combined description for patch agent
            combined_desc = (
                f"Issue: {issue_desc}\nResolution: {issue_resolution}"
            )

            try:
                await call_coding_agent(
                    agent_type, "patch", [combined_desc, str(spec_file_path)]
                )
            except Exception as e:
                logger.error(
                    "Patch failed for issue #%s: %s", issue_num, e,
                    exc_info=True
                )
                raise RuntimeError(
                    f"Patch failed for issue #{issue_num}: {e}"
                ) from e

        # Step 7: Clean up JSON for next iteration
        logger.debug("Cleaning up review JSON for next iteration")
        review_json_path_obj.unlink(missing_ok=True)

        logger.info("Review loop iteration %s complete", iteration)

    # Max iterations reached
    warning_msg = (
        f"Reached maximum iteration limit ({max_iterations}). "
        "Some blocker issues may remain."
    )
    console.print(f"\n[yellow]⚠[/yellow] {warning_msg}")
    logger.warning(warning_msg)
    return False
