import os

HOSTNAME = os.environ.get("HOST", "51.158.148.158:3000")
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@postgres:5432/notifications")
