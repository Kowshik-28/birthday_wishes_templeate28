import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Check for DATABASE_URL environment variable (useful for Render deployments),
# otherwise fallback to local SQLite database.
# Find absolute path of the current directory to avoid path resolution errors on Render
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
default_db_path = os.path.join(BASE_DIR, 'birthday_app.db')

SQLALCHEMY_DATABASE_URL = os.environ.get('DATABASE_URL', f'sqlite:///{default_db_path}')

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

