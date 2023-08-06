import asyncio
import os

import uvloop
from dotenv import load_dotenv
from sqlalchemy import (BigInteger, Column, Integer, MetaData, Table, select)
from sqlalchemy.ext.asyncio import create_async_engine

load_dotenv()

PASSWORD = os.getenv("Postgres_Password")
IP = os.getenv("Postgres_IP")
USER = os.getenv("Postgres_User")
DATABASE = os.getenv("Postgres_Database")
PORT = os.getenv("Postgres_Port")


class DisQuestUsers:
    def __init__(self):
        self.self = self

    async def initTables(self):
        meta = MetaData()
        engineInit = create_async_engine(
            f"postgresql+asyncpg://{USER}:{PASSWORD}@{IP}:{PORT}/{DATABASE}"
        )
        Table(
            "users",
            meta,
            Column("id", BigInteger),
            Column("gid", BigInteger),
            Column("xp", Integer),
        )
        async with engineInit.begin() as connInit:
            await connInit.run_sync(meta.create_all)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    
    async def getxp(self, uid: int, gid: int):
        meta = MetaData()
        engine = create_async_engine(
            f"postgresql+asyncpg://{USER}:{PASSWORD}@{IP}:{PORT}/{DATABASE}"
        )
        users = Table(
            "users",
            meta,
            Column("id", BigInteger),
            Column("gid", BigInteger),
            Column("xp", Integer),
        )
        async with engine.connect() as conn:
            s = select(users.c.xp).where(
                users.c.id == uid, users.c.gid == gid)
            results = await conn.execute(s)
            results_fetched = results.fetchone()
            for row in results_fetched:
                return row
                
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
                
    async def onInit(self, user_id: int, guild_id: int):
        meta = MetaData()
        engine = create_async_engine(
            f"postgresql+asyncpg://{USER}:{PASSWORD}@{IP}:{PORT}/{DATABASE}"
        )
        users = Table(
            "users",
            meta,
            Column("id", BigInteger),
            Column("gid", BigInteger),
            Column("xp", Integer),
        )
        async with engine.begin() as conn:
            s = select(users.c.xp).filter(users.c.id == user_id).filter(users.c.gid == guild_id)
            results = await conn.execute(s)
            results_fetched = results.fetchone()
            if results_fetched is None:
                insert_new = users.insert().values(xp=0, id=user_id, gid=guild_id)
                await conn.execute(insert_new)
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def setxp(self, xp: int, uid: int, gid: int):
        meta = MetaData()
        engine = create_async_engine(
            f"postgresql+asyncpg://{USER}:{PASSWORD}@{IP}:{PORT}/{DATABASE}"
        )
        users = Table(
            "users",
            meta,
            Column("id", BigInteger),
            Column("gid", BigInteger),
            Column("xp", Integer),
        )
        async with engine.begin() as conn:
            update_values = (
                users.update()
                .values(xp=xp)
                .filter(users.c.id == uid)
                .filter(users.c.gid == gid)
            )
            await conn.execute(update_values)
            
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def addxp(self, offset, uid: int, gid: int):
        pxp = await self.getxp(uid, gid)
        pxp += offset
        await self.setxp(pxp, uid=uid, gid=gid)
        
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
