"""Utility module for parsing JUnit XML test results and extracting failing test suites."""

from pathlib import Path
from junitparser import JUnitXml, TestSuite, TestCase


def _extract_failing_tests_from_suite(suite: TestSuite) -> TestSuite | None:
    """
    Extract failing tests from a test suite.

    Args:
        suite: TestSuite to process

    Returns:
        New TestSuite containing only failing tests, or None if no failures
    """
    failing_tests = []

    for test in suite:
        if not isinstance(test, TestCase):
            continue
        # Only include tests with errors or failures (not skipped)
        if test.is_error or test.is_failure:
            failing_tests.append(test)

    if not failing_tests:
        return None

    new_suite = TestSuite(suite.name)
    for test in failing_tests:
        new_suite.add_testcase(test)
    return new_suite


def get_failing_test_suites(path) -> list[TestSuite]:
    """
    Parse all XML files in the given directory and return test suites containing only failing tests.

    Args:
        path: Directory path containing JUnit XML files

    Returns:
        List of TestSuite objects containing only failing tests
    """
    failing_suites = []
    xml_files = Path(path).glob("*.xml")

    for xml_file in xml_files:
        try:
            xml = JUnitXml.fromfile(str(xml_file))

            # Handle both single TestSuite and collection of TestSuites
            suites = [xml] if isinstance(xml, TestSuite) else xml

            for suite in suites:
                failing_suite = _extract_failing_tests_from_suite(suite)
                if failing_suite:
                    failing_suites.append(failing_suite)

        except (OSError, AttributeError, ImportError, ValueError) as e:
            # Skip files that can't be parsed
            print(f"Warning: Could not parse {xml_file}: {e}")
            return []

    return failing_suites
