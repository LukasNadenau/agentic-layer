"""Agentic Development Workflow Test Loop Script.

This script orchestrates running tests and resolving failures in a loop until all tests pass.
"""
# /// script
# dependencies = [
#   "claude-agent-sdk",
#   "python-dotenv",
#   "junitparser",
#   "rich",
# ]
# ///

import sys
import asyncio
import argparse
import logging
from pathlib import Path

from console import console
from run_tests import run_tests
from get_failing_test_suites import get_failing_test_suites
from resolve_test import resolve_test
from agent_types import AgentType
from arg_utils import add_agent_argument, parse_agent_type


async def _resolve_failing_test_cases(
    failing_suites: list, spec_file_path: str, agent_type: AgentType
):
    """Resolve all failing test cases from the failing test suites."""
    logger = logging.getLogger(__name__)

    for suite in failing_suites:
        console.print(f"  Processing test suite: [cyan]{suite.name}[/cyan]")
        logger.info("Processing test suite: %s", suite.name)

        # Iterate through each test case in the suite
        for test_case in suite:
            console.print(f"    Resolving test case: [yellow]{test_case.name}[/yellow]")
            logger.info("Resolving test case: %s", test_case.name)
            try:
                test_success = await resolve_test(test_case, spec_file_path, agent_type)
                if not test_success:
                    console.print(
                        f"    [yellow]⚠[/yellow] Warning: Resolution may not have "
                        f"completed successfully for test: {test_case.name}"
                    )
                    logger.warning(
                        "Resolution may not have completed successfully for test: %s",
                        test_case.name
                    )
            except Exception as e:
                logger.error(
                    "Test resolution failed for test case %s: %s",
                    test_case.name, e, exc_info=True
                )
                raise


async def adw_test_loop(
    test_result_folder: str,
    spec_file_path: str,
    agent_type: AgentType = AgentType.CLAUDE
) -> bool:
    """
    Run tests and resolve failures in a loop until all tests pass.

    Args:
        test_result_folder: Path to directory for test result XML files
        spec_file_path: Path to the specification file

    Returns:
        bool: True if all tests passed, False if max iterations reached
    """
    logger = logging.getLogger(__name__)
    logger.info("Starting test loop - test results: %s, spec: %s",
                test_result_folder, spec_file_path)

    test_path_obj = Path(test_result_folder)
    if not test_path_obj.exists():
        error_msg = f"Test results path does not exist: {test_result_folder}"
        logger.error(error_msg)
        raise FileNotFoundError(error_msg)

    iteration = 0
    max_iterations = 10  # Prevent infinite loops

    while iteration < max_iterations:
        iteration += 1
        console.rule(f"[cyan]Test Loop Iteration {iteration}[/cyan]")
        logger.info("Test loop iteration %s starting", iteration)

        # Run tests
        console.print("\n[blue][1/4][/blue] Running tests...")
        logger.info("Running tests...")
        try:
            success = await run_tests(test_result_folder, agent_type)
            if not success:
                console.print(
                    "[yellow]⚠[/yellow] Warning: Test run may not have completed successfully"
                )
                logger.warning("Test run may not have completed successfully")
        except Exception as e:
            logger.error("Test run failed: %s", e, exc_info=True)
            raise

        # Check for failing tests
        console.print("\n[blue][2/4][/blue] Checking for failures...")
        logger.debug("Checking for failing test suites")
        failing_suites = get_failing_test_suites(test_result_folder)

        if not failing_suites:
            console.print("\n[green]✓[/green] All tests passed! Exiting loop.")
            logger.info("All tests passed - test loop complete")
            return True

        # Count total failing test cases
        total_failing_tests = sum(len(list(suite)) for suite in failing_suites)
        console.print(
            f"\n[blue][3/4][/blue] Found {total_failing_tests} failing test case(s) "
            f"across {len(failing_suites)} test suite(s)."
        )
        logger.info("Found %s failing test cases across %s test suites",
                    total_failing_tests, len(failing_suites))
        for suite in failing_suites:
            logger.debug("Failing suite: %s with %s test(s)", suite.name, len(list(suite)))

        # Resolve each failing test case individually
        await _resolve_failing_test_cases(failing_suites, spec_file_path, agent_type)

        # Clean up XML files for next iteration
        console.print("\n[blue][4/4][/blue] Cleaning up test results...")
        logger.debug("Cleaning up XML test result files")
        xml_files = list(test_path_obj.glob("*.xml"))
        for xml_file in xml_files:
            xml_file.unlink()
        console.print(f"  Deleted {len(xml_files)} XML file(s)")
        logger.debug("Deleted %s XML files", len(xml_files))

        logger.info("Test loop iteration %s complete", iteration)

    # Reached max iterations
    warning_msg = (
        f"Reached maximum iteration limit ({max_iterations}). "
        "Some tests may still be failing."
    )
    console.print(f"\n[yellow]⚠[/yellow] {warning_msg}")
    logger.warning(warning_msg)
    return False


async def main():
    """Main orchestration function for the ADW test loop flow."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Run tests and resolve failures in a loop until all tests pass"
    )
    parser.add_argument(
        "--path",
        required=True,
        help="Path to directory for test result XML files"
    )
    parser.add_argument("--spec", required=True, help="Path to the specification file")
    add_agent_argument(parser)

    args = parser.parse_args()

    try:
        agent_type = parse_agent_type(args)
        success = await adw_test_loop(args.path, args.spec, agent_type)
        if not success:
            sys.exit(1)
    except (FileNotFoundError, ValueError, RuntimeError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
