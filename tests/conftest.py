import pytest
from config.settings import BASE_URL, DEFAULT_USERNAME, DEFAULT_PASSWORD, DEFAULT_TIMEOUT
from clients.booking_client import BookingClient

@pytest.fixture(scope="session")
def auth_token() -> str:
    """Fetch authentication token once across the entire test session."""
    client = BookingClient(base_url=BASE_URL, timeout=DEFAULT_TIMEOUT)
    token = client.authenticate(DEFAULT_USERNAME, DEFAULT_PASSWORD)
    return token

@pytest.fixture(scope="function")
def booking_client(auth_token: str) -> BookingClient:
    """Provides a BookingClient initialized with the session auth token."""
    client = BookingClient(base_url=BASE_URL, timeout=DEFAULT_TIMEOUT)
    client.set_auth_token(auth_token)
    return client

@pytest.fixture
def sample_booking_payload():
    return {
        "firstname": "Arthur",
        "lastname": "Dent",
        "totalprice": 142,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2026-11-01",
            "checkout": "2026-11-10"
        },
        "additionalneeds": "Towel"
    }