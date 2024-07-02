# database.py
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from models.models import Base


DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/booksdb"


async def create_tables(conn):
    # Check for existing tables (optional, for more control)
    # You can use `inspect` or a database-specific method here
    # if desired.
    # Example using `inspect` (uncomment if needed):
    # from sqlalchemy import inspect
    # for table in Base.metadata.tables:
    #     if not inspect(conn).has_table(table):
    #         await table.create(conn)
    print("Before tables Creation")
    await conn.run_sync(Base.metadata.create_all)
    print("After tables Creation")

engine = create_async_engine(DATABASE_URL, echo=True)


# Dependency to get the async database session - This is a generator which is used to inject Async sessions into routes
async def get_session():
    async_session = async_sessionmaker(bind=engine, expire_on_commit=True, autocommit=False, autoflush=False)

    async with async_session() as session:
        if session is None:
            raise Exception("DatabaseSessionManager is not initialized")
        try:
            yield session
        except Exception:

            await session.rollback()
            raise
        finally:
            # Closing the session after use...
            await session.close()
    await engine.dispose()


# @asynccontextmanager
# async def get_session():
#   engine = create_async_engine(DATABASE_URL, future=True)
#   session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)()
#   async with engine.begin() as connection:
#     async with session.begin_nested() as session:
#       yield session
#   await session.close()

