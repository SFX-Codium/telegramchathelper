import aiosqlite
from contextlib import asynccontextmanager

_db = None 

@asynccontextmanager
async def get_db():
    global _db
    if _db is None:
        _db = await aiosqlite.connect("database.db")
        await _db.execute("PRAGMA foreign_keys = ON")
    try:
        yield _db
    finally:
        pass