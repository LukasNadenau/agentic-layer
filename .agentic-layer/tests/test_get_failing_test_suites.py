"""Unit tests for get_failing_test_suites module."""
from pathlib import Path
import pytest
from junitparser import JUnitXml, TestSuite, TestCase, Failure, Error, Skipped
from get_failing_test_suites import get_failing_test_suites, _extract_failing_tests_from_suite


# Fixtures for creating test XML files

@pytest.fixture
def xml_with_passing_tests(tmp_path):
    """Create XML file with only passing tests."""
    suite = TestSuite("PassingSuite")
    test1 = TestCase("test_pass_1")
    test2 = TestCase("test_pass_2")
    suite.add_testcase(test1)
    suite.add_testcase(test2)
    
    xml_file = tmp_path / "passing.xml"
    xml = JUnitXml()
    xml.add_testsuite(suite)
    xml.write(str(xml_file))

    return tmp_path


@pytest.fixture
def xml_with_failing_tests(tmp_path):
    """Create XML file with failing tests."""
    suite = TestSuite("FailingSuite")
    
    test1 = TestCase("test_fail_1")
    test1.result = [Failure("AssertionError: expected != actual")]
    
    test2 = TestCase("test_pass")
    # No failure - this is passing
    
    suite.add_testcase(test1)
    suite.add_testcase(test2)
    
    xml_file = tmp_path / "failing.xml"
    xml = JUnitXml()
    xml.add_testsuite(suite)
    xml.write(str(xml_file))
    
    return tmp_path


@pytest.fixture
def xml_with_error_tests(tmp_path):
    """Create XML file with error tests."""
    suite = TestSuite("ErrorSuite")
    
    test1 = TestCase("test_error_1")
    test1.result = [Error("Exception: Something went wrong")]
    
    test2 = TestCase("test_pass")
    # No error - this is passing
    
    suite.add_testcase(test1)
    suite.add_testcase(test2)
    
    xml_file = tmp_path / "error.xml"
    xml = JUnitXml()
    xml.add_testsuite(suite)
    xml.write(str(xml_file))
    
    return tmp_path


@pytest.fixture
def xml_with_mixed_tests(tmp_path):
    """Create XML file with mixed test results."""
    suite = TestSuite("MixedSuite")
    
    passing = TestCase("test_pass")
    suite.add_testcase(passing)
    
    failing = TestCase("test_fail")
    failing.result = [Failure("Failed")]
    suite.add_testcase(failing)
    
    error = TestCase("test_error")
    error.result = [Error("Error occurred")]
    suite.add_testcase(error)
    
    skipped = TestCase("test_skip")
    skipped.result = [Skipped("Skipped test")]
    suite.add_testcase(skipped)
    
    xml_file = tmp_path / "mixed.xml"
    xml = JUnitXml()
    xml.add_testsuite(suite)
    xml.write(str(xml_file))
    
    return tmp_path


@pytest.fixture
def xml_with_empty_suite(tmp_path):
    """Create XML file with empty test suite."""
    suite = TestSuite("EmptySuite")
    # No tests added
    
    xml_file = tmp_path / "empty.xml"
    xml = JUnitXml()
    xml.add_testsuite(suite)
    xml.write(str(xml_file))
    
    return tmp_path


@pytest.fixture
def xml_malformed(tmp_path):
    """Create malformed XML file."""
    bad_xml = tmp_path / "malformed.xml"
    bad_xml.write_text("<invalid><xml>not closed properly")
    
    return tmp_path


# Tests for _extract_failing_tests_from_suite

def test_extract_failing_tests_returns_none_for_passing_suite():
    """Test that extract returns None when all tests pass."""
    suite = TestSuite("AllPass")
    suite.add_testcase(TestCase("test1"))
    suite.add_testcase(TestCase("test2"))
    
    result = _extract_failing_tests_from_suite(suite)
    
    assert result is None


def test_extract_failing_tests_includes_failures():
    """Test that extract includes tests with failures."""
    suite = TestSuite("MixedSuite")
    
    passing = TestCase("test_pass")
    suite.add_testcase(passing)
    
    failing = TestCase("test_fail")
    failing.result = [Failure("Failed")]
    suite.add_testcase(failing)
    
    result = _extract_failing_tests_from_suite(suite)
    
    assert result is not None
    assert result.name == "MixedSuite"
    assert len(list(result)) == 1
    failing_test = list(result)[0]
    assert failing_test.name == "test_fail"


def test_extract_failing_tests_includes_errors():
    """Test that extract includes tests with errors."""
    suite = TestSuite("ErrorSuite")
    
    error_test = TestCase("test_error")
    error_test.result = [Error("Exception occurred")]
    suite.add_testcase(error_test)
    
    result = _extract_failing_tests_from_suite(suite)
    
    assert result is not None
    assert len(list(result)) == 1
    error_test_result = list(result)[0]
    assert error_test_result.name == "test_error"


def test_extract_failing_tests_excludes_skipped():
    """Test that skipped tests are not included in failures."""
    suite = TestSuite("SkippedSuite")
    
    skipped = TestCase("test_skip")
    skipped.result = [Skipped("Skipped test")]
    suite.add_testcase(skipped)
    
    result = _extract_failing_tests_from_suite(suite)
    
    assert result is None


def test_extract_failing_tests_mixed_results():
    """Test correct filtering with mixed test results."""
    suite = TestSuite("MixedResults")
    
    passing = TestCase("test_pass")
    suite.add_testcase(passing)
    
    failing = TestCase("test_fail")
    failing.result = [Failure("Failed")]
    suite.add_testcase(failing)
    
    error = TestCase("test_error")
    error.result = [Error("Error")]
    suite.add_testcase(error)
    
    skipped = TestCase("test_skip")
    skipped.result = [Skipped("Skipped")]
    suite.add_testcase(skipped)
    
    result = _extract_failing_tests_from_suite(suite)
    
    assert result is not None
    assert len(list(result)) == 2
    test_names = [test.name for test in result]
    assert "test_fail" in test_names
    assert "test_error" in test_names
    assert "test_pass" not in test_names
    assert "test_skip" not in test_names


def test_extract_failing_tests_empty_suite():
    """Test that extract returns None for empty suite."""
    suite = TestSuite("EmptySuite")
    
    result = _extract_failing_tests_from_suite(suite)
    
    assert result is None


def test_extract_failing_tests_preserves_suite_name():
    """Test that suite name is preserved in result."""
    suite = TestSuite("CustomSuiteName")
    
    failing = TestCase("test_fail")
    failing.result = [Failure("Failed")]
    suite.add_testcase(failing)
    
    result = _extract_failing_tests_from_suite(suite)
    
    assert result is not None
    assert result.name == "CustomSuiteName"


# Tests for get_failing_test_suites

def test_get_failing_test_suites_single_file(xml_with_failing_tests):
    """Test parsing single XML file with failures."""
    result = get_failing_test_suites(xml_with_failing_tests)
    
    assert len(result) == 1
    suite = result[0]
    assert suite.name == "FailingSuite"
    
    tests = list(suite)
    assert len(tests) == 1
    assert tests[0].name == "test_fail_1"


def test_get_failing_test_suites_multiple_files(tmp_path):
    """Test parsing multiple XML files."""
    # Create file 1 with failures
    suite1 = TestSuite("Suite1")
    fail1 = TestCase("fail1")
    fail1.result = [Failure("Failed")]
    suite1.add_testcase(fail1)
    xml1 = JUnitXml()
    xml1.add_testsuite(suite1)
    xml1.write(str(tmp_path / "file1.xml"))
    
    # Create file 2 with failures
    suite2 = TestSuite("Suite2")
    fail2 = TestCase("fail2")
    fail2.result = [Failure("Failed")]
    suite2.add_testcase(fail2)
    xml2 = JUnitXml()
    xml2.add_testsuite(suite2)
    xml2.write(str(tmp_path / "file2.xml"))
    
    result = get_failing_test_suites(tmp_path)
    
    assert len(result) == 2
    suite_names = [s.name for s in result]
    assert "Suite1" in suite_names
    assert "Suite2" in suite_names


def test_get_failing_test_suites_no_failures(xml_with_passing_tests):
    """Test with XML files containing only passing tests."""
    result = get_failing_test_suites(xml_with_passing_tests)
    
    assert result == []


def test_get_failing_test_suites_empty_directory(tmp_path):
    """Test with directory containing no XML files."""
    result = get_failing_test_suites(tmp_path)
    
    assert result == []


def test_get_failing_test_suites_handles_malformed_xml(xml_malformed):
    """Test that malformed XML is handled gracefully."""
    # Note: Current implementation doesn't catch xml.etree.ElementTree.ParseError
    # This test verifies the actual behavior
    from xml.etree.ElementTree import ParseError
    
    with pytest.raises(ParseError):
        get_failing_test_suites(xml_malformed)


def test_get_failing_test_suites_nested_suites(tmp_path):
    """Test parsing XML with multiple TestSuites in one file."""
    xml = JUnitXml()
    
    suite1 = TestSuite("Nested1")
    fail1 = TestCase("fail1")
    fail1.result = [Failure("Failed")]
    suite1.add_testcase(fail1)
    xml.add_testsuite(suite1)
    
    suite2 = TestSuite("Nested2")
    fail2 = TestCase("fail2")
    fail2.result = [Failure("Failed")]
    suite2.add_testcase(fail2)
    xml.add_testsuite(suite2)
    
    xml.write(str(tmp_path / "nested.xml"))
    
    result = get_failing_test_suites(tmp_path)
    
    assert len(result) == 2
    suite_names = [s.name for s in result]
    assert "Nested1" in suite_names
    assert "Nested2" in suite_names


def test_get_failing_test_suites_non_existent_path():
    """Test with path that doesn't exist."""
    non_existent = Path("/non/existent/path")
    
    result = get_failing_test_suites(non_existent)
    
    assert result == []


def test_get_failing_test_suites_non_xml_files(tmp_path):
    """Test that non-XML files in directory are ignored."""
    # Create a non-XML file
    (tmp_path / "notxml.txt").write_text("This is not XML")
    
    # Create a valid XML with failures
    suite = TestSuite("ValidSuite")
    fail = TestCase("fail1")
    fail.result = [Failure("Failed")]
    suite.add_testcase(fail)
    xml = JUnitXml()
    xml.add_testsuite(suite)
    xml.write(str(tmp_path / "valid.xml"))
    
    result = get_failing_test_suites(tmp_path)
    
    assert len(result) == 1
    assert result[0].name == "ValidSuite"


def test_get_failing_test_suites_with_errors(xml_with_error_tests):
    """Test parsing XML file with error tests."""
    result = get_failing_test_suites(xml_with_error_tests)
    
    assert len(result) == 1
    suite = result[0]
    assert suite.name == "ErrorSuite"
    
    tests = list(suite)
    assert len(tests) == 1
    assert tests[0].name == "test_error_1"


def test_get_failing_test_suites_mixed_results(xml_with_mixed_tests):
    """Test parsing XML file with mixed test results."""
    result = get_failing_test_suites(xml_with_mixed_tests)
    
    assert len(result) == 1
    suite = result[0]
    assert suite.name == "MixedSuite"
    
    tests = list(suite)
    assert len(tests) == 2
    test_names = [test.name for test in tests]
    assert "test_fail" in test_names
    assert "test_error" in test_names
    assert "test_pass" not in test_names
    assert "test_skip" not in test_names
