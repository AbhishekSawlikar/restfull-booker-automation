import pytest
import allure
from schemas.booking_schema import BOOKING_CREATE_SCHEMA, BOOKING_DETAIL_SCHEMA, validate_schema

@allure.feature("Booking Management")
@allure.story("CRUD Lifecycle")
@pytest.mark.crud
class TestBookingCRUD:

    def test_full_booking_lifecycle(self, booking_client, sample_booking_payload):
        # 1. CREATE
        with allure.step("Create a new booking (POST)"):
            create_resp = booking_client.create_booking(sample_booking_payload)
            assert create_resp.status_code == 200
            create_data = create_resp.json()
            validate_schema(create_data, BOOKING_CREATE_SCHEMA)
            booking_id = create_data["bookingid"]
            assert booking_id > 0

        # 2. READ
        with allure.step("Retrieve the created booking (GET)"):
            get_resp = booking_client.get_booking(booking_id)
            assert get_resp.status_code == 200
            validate_schema(get_resp.json(), BOOKING_DETAIL_SCHEMA)
            assert get_resp.json()["firstname"] == sample_booking_payload["firstname"]

        # 3. UPDATE (PUT)
        with allure.step("Fully update the booking (PUT)"):
            updated_payload = sample_booking_payload.copy()
            updated_payload["firstname"] = "Ford"
            updated_payload["totalprice"] = 250

            put_resp = booking_client.update_booking(booking_id, updated_payload)
            assert put_resp.status_code == 200
            assert put_resp.json()["firstname"] == "Ford"
            assert put_resp.json()["totalprice"] == 250

        # 4. PARTIAL UPDATE (PATCH)
        with allure.step("Partially update the booking (PATCH)"):
            patch_payload = {"additionalneeds": "Tea and Biscuits"}
            patch_resp = booking_client.partial_update_booking(booking_id, patch_payload)
            assert patch_resp.status_code == 200
            assert patch_resp.json()["additionalneeds"] == "Tea and Biscuits"

        # 5. DELETE
        with allure.step("Delete the booking (DELETE)"):
            del_resp = booking_client.delete_booking(booking_id)
            assert del_resp.status_code == 201

        # 6. VERIFY DELETION
        with allure.step("Verify booking no longer exists (GET)"):
            verify_resp = booking_client.get_booking(booking_id)
            assert verify_resp.status_code == 404