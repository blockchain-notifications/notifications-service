from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.routers.notifications import notifications_router
from app.routers.test_page import test_page_router

app = FastAPI()
app.include_router(notifications_router)
app.include_router(test_page_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
