import requests
from clients.base_client import BaseClient

class BookingClient(BaseClient):
    def authenticate(self, username: str, password: str) -> str:
        payload = {"username": username, "password": password}
        resp = self.request("POST", "/auth", json=payload)
        resp.raise_for_status()
        token = resp.json().get("token")
        if not token:
            raise ValueError("Token not found in auth response")
        return token

    def set_auth_token(self, token: str):
        # Restful-Booker supports Cookie: token=... or basic/custom headers
        self.session.headers.update({"Cookie": f"token={token}"})

    def get_booking_ids(self, params: dict = None) -> requests.Response:
        return self.request("GET", "/booking", params=params)

    def get_booking(self, booking_id: int) -> requests.Response:
        return self.request("GET", f"/booking/{booking_id}")

    def create_booking(self, payload: dict) -> requests.Response:
        return self.request("POST", "/booking", json=payload)

    def update_booking(self, booking_id: int, payload: dict) -> requests.Response:
        return self.request("PUT", f"/booking/{booking_id}", json=payload)

    def partial_update_booking(self, booking_id: int, payload: dict) -> requests.Response:
        return self.request("PATCH", f"/booking/{booking_id}", json=payload)

    def delete_booking(self, booking_id: int) -> requests.Response:
        return self.request("DELETE", f"/booking/{booking_id}")