"""
database.py
-----------
This file sets up the connection to our SQLite database.

Beginner notes:
- SQLite is a database that lives inside a SINGLE FILE (evolio.db).
- There is NOTHING to install or run separately. Python already knows SQLite.
- SQLAlchemy is the library that lets us talk to the database using Python
  classes instead of writing raw SQL by hand.

The 4 important objects every SQLAlchemy app has:
- engine        -> the actual connection to the database file
- SessionLocal  -> a "session" is one conversation with the database
- Base          -> the parent class that all our table models inherit from
- get_db()      -> a helper FastAPI uses to give each request its own session
"""

from pathlib import Path

from sqlalchemy import create_engine, event
from sqlalchemy.orm import declarative_base, sessionmaker

# ---------------------------------------------------------------------------
# Where does the database file live?
# We build an ABSOLUTE path based on THIS file's location, not the folder you
# happen to be standing in when you run the app. That way it always points to
# backend/db/evolio.db whether you run from "backend/" or from the project root.
# ---------------------------------------------------------------------------
DB_DIR = Path(__file__).resolve().parent          # .../backend/db
DB_PATH = DB_DIR / "evolio.db"                     # .../backend/db/evolio.db

# The connection string for SQLite. Three slashes + an absolute path.
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

# create_engine = open the connection to the database file.
# check_same_thread=False is required for SQLite when used with FastAPI,
# because FastAPI may touch the connection from different threads.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)


# Make SQLite actually enforce foreign keys (it does NOT by default).
# This is what makes "cascade delete" work at the database level too.
@event.listens_for(engine, "connect")
def _enable_sqlite_foreign_keys(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


# A session factory. Calling SessionLocal() gives us one new session.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = the class every model (table) will inherit from.
Base = declarative_base()


def get_db():
    """
    FastAPI dependency.

    Each incoming request gets its own database session, and we always close
    it when the request is done (even if an error happens). You use it like:

        @router.get("/something")
        def handler(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Create all tables that don't exist yet, based on the models in model.py.

    We import model.py here (not at the top) so that Python has already loaded
    every model class before we ask SQLAlchemy to create the tables.
    """
    from db import model  # noqa: F401  (imported for its side effect)

    Base.metadata.create_all(bind=engine)
