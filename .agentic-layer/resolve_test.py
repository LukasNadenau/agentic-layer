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
from junitparser import TestSuite

load_dotenv()


async def resolve_test(
    test_suite: TestSuite,
    spec_file_path: str,
    agent_type: AgentType = AgentType.CLAUDE
) -> bool:
    """
    Resolves failed tests in a test suite by calling Claude Code with
    the /resolve_failed_test command.

    Args:
        test_suite: A junitparser TestSuite object containing failed tests
        spec_file_path: Path to the specification file

    Returns:
        bool: True if resolution completed successfully, False otherwise
    """
    logger = logging.getLogger(__name__)
    logger.info("Resolving test suite: %s", test_suite.name)
    logger.debug("Test count in suite: %s", len(list(test_suite)))

    # Stringify the test suite to XML format (returns bytes with utf-8 encoding)
    stringified_tests = test_suite.tostring().decode('utf-8')

    # Sanitize the stringified tests to avoid issues with argument parsing
    # Replace problematic characters that can destroy command parsing
    sanitized_tests = (stringified_tests
                      .replace("'", "\\'")    # Escape single quotes
                      .replace('"', '\\"')    # Escape double quotes
                      .replace('\n', '\\n')   # Escape newlines
                      .replace('\r', '\\r'))  # Escape carriage returns

    # Call the coding agent to resolve tests
    try:
        await call_coding_agent(
            agent_type, "resolve_failed_test", [sanitized_tests, spec_file_path]
        )
    except Exception as e:
        logger.error("Test resolution failed for suite %s: %s", test_suite.name, e, exc_info=True)
        raise

    logger.info("Resolution command completed for test suite: %s", test_suite.name)
    return True
