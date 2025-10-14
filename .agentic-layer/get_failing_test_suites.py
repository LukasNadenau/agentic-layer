"""Utility module for parsing JUnit XML test results and extracting failing test suites."""

from pathlib import Path
from junitparser import JUnitXml, TestSuite, TestCase


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
                # Create a new suite to hold only failing tests
                failing_tests = []

                for test in suite:
                    if isinstance(test, TestCase):
                        # Only include tests with errors (not failures or skipped)
                        if test.is_error or test.is_failure:
                            failing_tests.append(test)

                # Only add suite if it has failing tests
                if failing_tests:
                    new_suite = TestSuite(suite.name)
                    for test in failing_tests:
                        new_suite.add_testcase(test)
                    failing_suites.append(new_suite)

        except (OSError, AttributeError, ImportError, ValueError) as e:
            # Skip files that can't be parsed
            print(f"Warning: Could not parse {xml_file}: {e}")
            return []

    return failing_suites
