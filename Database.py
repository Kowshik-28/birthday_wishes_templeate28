import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Check for DATABASE_URL environment variable (useful for Render deployments),
# otherwise fallback to local SQLite database.
SQLALCHEMY_DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///./birthday_app.db')

# Connect arguments are only needed for SQLite
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})
else:
    # If using PostgreSQL, Render URLs sometimes start with postgres:// which needs to be replaced with postgresql:// for SQLAlchemy
    if SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

