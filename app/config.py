import os

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@postgres/notifications")
