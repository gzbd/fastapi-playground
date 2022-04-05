from fastapi import FastAPI

from .db.db import engine, async_db
from sqlalchemy.sql import text
import time

app = FastAPI()

from .routes.feature_flags import router

app.include_router(router)


@app.on_event("startup")
async def startup():
    await async_db.connect()


@app.on_event("shutdown")
async def shutdown():
    await async_db.disconnect()


@app.get("/db-message-async")
async def async_db_message():
    """async function with async calls to the DB"""
    rows = await async_db.fetch_all("SELECT pg_sleep(1), 'Hello', 'World!';")
    return {"message": " ".join(rows[0][1:])}


@app.get("/db-message-blocking")
async def db_message_blocking():
    """async function with blocking calls"""
    with engine.connect() as conn:
        rows = conn.execute(text("SELECT pg_sleep(1), 'Hello', 'World!';"))
        return {"message": " ".join(rows.all()[0][1:])}


@app.get("/db-message-nonblocking")
def db_message_nonblocking():
    """regular function run in separate thread, nonblocking"""
    with engine.connect() as conn:
        rows = conn.execute(text("SELECT pg_sleep(1), 'Hello', 'World!';"))
        return {"message": " ".join(rows.all()[0][1:])}


@app.get("/message-blocking")
async def blocking_message():
    "async function witl blocking call to time.sleep() will block main thread"
    time.sleep(1)
    return {"message": "Hello World!"}


@app.get("/message-nonblocking")
def nonblocking_message():
    """regular function fallback to be run in separate thread. time.sleep() won't
    block here"""
    time.sleep(1)
    return {"message": "Hello World!"}
