import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, "lifelink.db")
SECRET_KEY = os.getenv("LIFELINK_SECRET_KEY", "change-this-development-secret")
JWT_EXPIRY_HOURS = int(os.getenv("JWT_EXPIRY_HOURS", "12"))
