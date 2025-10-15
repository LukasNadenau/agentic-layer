---
argument-hint: [path to test results]
description: Run unit tests
---

# Feature Planning

Create a file following the `Create File` using the `Variables`.

## Variables

`path to test results`: $1

## Create File

Create a xml file at "`path to test results`/test.xml" with content:

---file content

<?xml version="1.0" encoding="UTF-8"?>
<testsuites name="Full Test Suite" tests="5" failures="2" errors="1" time="3.142">
    
    <!-- First Test Suite: User Authentication Tests -->
    <testsuite name="UserAuthenticationTests" tests="3" failures="1" errors="0" skipped="0" time="1.523" timestamp="2025-10-14T10:30:00">
        
        <!-- Passing test -->
        <testcase classname="auth.LoginTests" name="test_successful_login" time="0.421">
            <system-out>User logged in successfully with valid credentials</system-out>
        </testcase>
        
        <!-- Failing test -->
        <testcase classname="auth.LoginTests" name="test_invalid_password" time="0.652">
            <failure message="AssertionError: Expected status code 401, got 200" type="AssertionError">
AssertionError: Expected status code 401, got 200
    at LoginTests.test_invalid_password (auth.test.js:45)
    at Object.&lt;anonymous&gt; (auth.test.js:12)
Expected: 401
Actual: 200
            </failure>
            <system-err>Warning: Authentication bypass detected</system-err>
        </testcase>
        
        <!-- Passing test -->
        <testcase classname="auth.LoginTests" name="test_logout" time="0.450">
            <system-out>Session terminated successfully</system-out>
        </testcase>
        
    </testsuite>
    
    <!-- Second Test Suite: Database Operations -->
    <testsuite name="DatabaseTests" tests="2" failures="1" errors="1" skipped="0" time="1.619" timestamp="2025-10-14T10:30:02">
        
        <!-- Test with error (not a failure, but an error like exception) -->
        <testcase classname="db.ConnectionTests" name="test_database_connection" time="0.089">
            <error message="ConnectionError: Unable to connect to database" type="ConnectionError">
ConnectionError: Unable to connect to database at localhost:5432
    at DatabaseConnection.connect (db.js:23)
    at ConnectionTests.setUp (db.test.js:15)
Caused by: ECONNREFUSED
            </error>
        </testcase>
        
        <!-- Failing test -->
        <testcase classname="db.QueryTests" name="test_user_query" time="1.530">
            <failure message="Expected 10 results, but got 8" type="AssertionError">
AssertionError: Expected 10 results, but got 8
    at QueryTests.test_user_query (db.test.js:67)
Expected length: 10
Actual length: 8
Missing records: [ID-009, ID-010]
            </failure>
        </testcase>
        
    </testsuite>
    
</testsuites>

---
