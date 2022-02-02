from fastapi import FastAPI

from app.routers.notifications import notifications_router
from app.routers.test_page import test_page_router

app = FastAPI()
app.include_router(notifications_router)
app.include_router(test_page_router)

import uvicorn

uvicorn.run(app, host="0.0.0.0", port=8000)
