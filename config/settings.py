import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://restful-booker.herokuapp.com")
DEFAULT_USERNAME = os.getenv("BOOKER_USER", "admin")
DEFAULT_PASSWORD = os.getenv("BOOKER_PASS", "password123")
DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", "10"))