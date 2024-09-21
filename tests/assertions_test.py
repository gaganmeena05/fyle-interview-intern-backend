from core.libs import assertions
from core.libs.exceptions import FyleError

def test_assert_auth():
    """Test assertion for authorization."""
    try:
        assertions.assert_auth(False)
    except FyleError as e:
        assert e.status_code == 401
        assert e.message == 'UNAUTHORIZED'


def test_assert_true():
    """Test assertion for truth value."""
    try:
        assertions.assert_true(False)
    except FyleError as e:
        assert e.status_code == 403
        assert e.message == 'FORBIDDEN'


def test_assert_valid():
    """Test assertion for validity."""
    try:
        assertions.assert_valid(False)
    except FyleError as e:
        assert e.status_code == 400
        assert e.message is None


def test_assert_found():
    """Test assertion for resource existence."""
    try:
        assertions.assert_found(None)
    except FyleError as e:
        assert e.status_code == 404
        assert e.message == 'NOT_FOUND'
