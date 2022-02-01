from fastapi import FastAPI

from routes.notifications import notifications_router
from routes.test_page import test_page_router

app = FastAPI()
app.include_router(notifications_router)
app.include_router(test_page_router)
