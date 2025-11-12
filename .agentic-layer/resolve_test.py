"""Module for resolving failed tests using Claude Code."""
# /// script
# dependencies = [
#   "claude-agent-sdk",
#   "python-dotenv",
#   "junitparser",
# ]
# ///

import logging
from dotenv import load_dotenv
from coding_agent import call_coding_agent
from agent_types import AgentType
from junitparser import TestSuite, TestCase

load_dotenv()


async def resolve_test(
    test_case: TestCase,
    spec_file_path: str,
    agent_type: AgentType = AgentType.CLAUDE
) -> bool:
    """
    Resolves a single failed test case by calling Claude Code with
    the /resolve_failed_test command.

    Args:
        test_case: A junitparser TestCase object representing the failed test
        spec_file_path: Path to the specification file

    Returns:
        bool: True if resolution completed successfully, False otherwise
    """
    logger = logging.getLogger(__name__)
    logger.info("Resolving test case: %s", test_case.name)

    # Stringify the test case to XML format (returns bytes with utf-8 encoding)
    stringified_test = test_case.tostring().decode('utf-8')

    # Call the coding agent to resolve tests
    # Note: Arguments are automatically sanitized in call_coding_agent to prevent
    # command parsing issues with special characters
    try:
        await call_coding_agent(
            agent_type, "resolve_failed_test", [stringified_test, spec_file_path]
        )
    except Exception as e:
        logger.error("Test resolution failed for test case %s: %s", test_case.name, e, exc_info=True)
        raise

    logger.info("Resolution command completed for test case: %s", test_case.name)
    return True
