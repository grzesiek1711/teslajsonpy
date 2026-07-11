"""Test exception retry logic."""

from httpx import RequestError
from tenacity import RetryCallState, Retrying

from teslajsonpy.const import MAX_API_RETRY_TIME
from teslajsonpy.exceptions import (
    custom_retry,
    custom_retry_except_unavailable,
    custom_wait,
    HomelinkError,
    IncompleteCredentials,
    RetryLimitError,
    TeslaException,
    UnknownPresetMode,
)


def test_tesla_exception_retryable():
    # code, retryable
    test_set = [
        (408, True),
        (540, True),
        (401, False),
        (404, False),
        (405, False),
        (423, False),
        (429, False),
    ]

    for code, expected in test_set:
        exc = TeslaException(code)
        assert exc.retryable == expected


def test_custom_retry():
    # No exceptions means we don't retry
    rs = RetryCallState(Retrying(), None, None, None)
    rs.set_result(None)
    assert custom_retry(rs) is False

    # Add a retryable exception
    ex = TeslaException(408)
    rs.set_exception((type(ex), ex, None))
    assert custom_retry(rs) is True

    # Add a non-retryable exception
    ex = TeslaException(401)
    rs.set_exception((type(ex), ex, None))
    assert custom_retry(rs) is False

    # Any RequestError should also retry
    ex = RequestError("")
    rs.set_exception((type(ex), ex, None))
    assert custom_retry(rs) is True


def test_custom_wait():
    rs = RetryCallState(Retrying(), None, None, None)
    # sec_since_start, attempt, wait_min, wait_max
    test_set = [
        (0, 1, 1, 2),
        (0, 2, 2, 3),
        (0, 3, 4, 5),
        (0, 4, 8, 9),
        (0, 5, 15, 15),
        (14, 2, 1, 1),
        (16, 1, 0, 0),
    ]
    assert MAX_API_RETRY_TIME == 15
    for sec, attempt, expected_min, expected_max in test_set:
        rs.outcome_timestamp = rs.start_time + sec
        rs.attempt_number = attempt
        wait = custom_wait(rs)
        assert wait >= expected_min
        assert wait <= expected_max


def test_custom_retry_except_unavailable():
    """Test custom_retry_except_unavailable doesn't retry on 408."""
    # Vehicle unavailable (408) should not retry
    rs = RetryCallState(Retrying(), None, None, None)
    ex = TeslaException(408)
    rs.set_exception((type(ex), ex, None))
    assert custom_retry_except_unavailable(rs) is False

    # Other retryable exceptions should retry
    ex = TeslaException(500)
    rs.set_exception((type(ex), ex, None))
    assert custom_retry_except_unavailable(rs) is True

    # Non-retryable exceptions should not retry
    ex = TeslaException(401)
    rs.set_exception((type(ex), ex, None))
    assert custom_retry_except_unavailable(rs) is False

    # Non-TeslaException errors should not retry (because custom_retry returns False)
    rs.set_result(None)
    assert custom_retry_except_unavailable(rs) is False


def test_incomplete_credentials_exception():
    """Test IncompleteCredentials exception with devices."""
    devices = {"device1": {"id": 1}, "device2": {"id": 2}}
    exc = IncompleteCredentials(401, devices=devices)
    assert exc.devices == devices
    assert exc.code == 401

    # Test without devices (default)
    exc = IncompleteCredentials(401)
    assert exc.devices == {}


def test_retry_limit_error():
    """Test RetryLimitError exception."""
    exc = RetryLimitError(429)
    assert exc.code == 429
    assert exc.message == "TOO_MANY_REQUESTS"


def test_unknown_preset_mode_exception():
    """Test UnknownPresetMode exception."""
    exc = UnknownPresetMode("invalid_preset")
    assert exc.code == "invalid_preset"


def test_homelink_error_exception():
    """Test HomelinkError exception."""
    exc = HomelinkError(400)
    assert exc.code == 400


def test_custom_wait_overflow():
    """Test custom_wait handles OverflowError for very large attempt numbers."""
    rs = RetryCallState(Retrying(), None, None, None)
    rs.outcome_timestamp = rs.start_time + 0
    # Very large attempt number that would cause overflow in 2^(attempt-1)
    rs.attempt_number = 10000
    wait = custom_wait(rs)
    # Should return max_wait (15 seconds) instead of overflowing
    assert wait <= MAX_API_RETRY_TIME
    assert wait >= 0
