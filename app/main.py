from fastapi import FastAPI

from .routers.notifications import notifications_router
from .routers.test_page import test_page_router

app = FastAPI()
app.include_router(notifications_router)
app.include_router(test_page_router)
