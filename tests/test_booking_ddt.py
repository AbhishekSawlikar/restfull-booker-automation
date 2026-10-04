import csv
import json
from pathlib import Path
import pytest
import allure
from schemas.booking_schema import BOOKING_CREATE_SCHEMA, validate_schema

DATA_DIR = Path(__file__).parent.parent / "test_data"


def load_json_data():
    with open(DATA_DIR / "booking_positive.json", encoding="utf-8") as f:
        return json.load(f)


def load_csv_data():
    cases = []
    with open(DATA_DIR / "booking_negative.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cases.append(row)
    return cases


@allure.feature("Booking Management")
@allure.story("Data-Driven Validation")
@pytest.mark.ddt
class TestBookingDDT:

    @pytest.mark.parametrize("payload", load_json_data())
    def test_create_booking_positive_ddt(self, booking_client, payload):
        allure.dynamic.title(f"Positive Test: {payload['firstname']} {payload['lastname']}")
        resp = booking_client.create_booking(payload)

        assert resp.status_code == 200
        data = resp.json()
        validate_schema(data, BOOKING_CREATE_SCHEMA)
        assert data["booking"]["firstname"] == payload["firstname"]
        assert data["booking"]["totalprice"] == payload["totalprice"]

        # Teardown: Clean up generated booking
        booking_client.delete_booking(data["bookingid"])

    @pytest.mark.parametrize("row", load_csv_data())
    def test_create_booking_negative_ddt(self, booking_client, row):
        allure.dynamic.title(f"Negative Test: Expected {row['expected_status']}")

        payload = {
            "firstname": row["firstname"] if row["firstname"] != "" else None,
            "lastname": row["lastname"] if row["lastname"] != "" else None,
            "totalprice": int(row["totalprice"]) if row["totalprice"].isdigit() else row["totalprice"],
            "depositpaid": row["depositpaid"].lower() == "true",
            "bookingdates": {"checkin": "2026-07-01", "checkout": "2026-07-05"}
        }

        resp = booking_client.create_booking(payload)
        assert resp.status_code == int(row["expected_status"])