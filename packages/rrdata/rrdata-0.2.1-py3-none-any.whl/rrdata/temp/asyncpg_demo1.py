#!/usr/bin/env python
import time
import os
import datetime
from venv import create
import asyncpg
import logging
import sqlite3
from typing import Dict


log = logging.getLogger("RRSDK")
logging.basicConfig(level=logging.INFO)


async def check_database(pool: asyncpg.pool.Pool):
    """ check db"""
    try:
        async with pool.acquire() as con:
            await create_database(con)
    except asyncpg.InsufficientPrivilegeError as e:
        log.error(f"error: {e}")
        return False
    return True


tables = [
    """
    CREATE TABLE "stock_lists" (
        id serial NOT NULL,
        stock_name text NOT NULL,

        created timestamptz DEFAULT now(),
        PRIMARY KEY (id),
        UNIQUE(STOCK_NAME)
    )
    """,
    """
    """
]

async def import_legacy_db(pool: asyncpg.pool.Pool, path):
    if not os.path.isfile(path):
        log.error("base file is not exist")
        return
    legacy_conn = sqlite3.connect(path)
    c = legacy_conn.cursor()
    log.info("")

async def create_database(con:asyncpg.connection.Connection):
    """ cteate rrdata's tables and functions"""
    log.info("create tables test")
    for create_query in tables:
        await con.execute(create_query)
    


