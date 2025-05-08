from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite-tietokanta kehitystä varten
SQLALCHEMY_DATABASE_URL = "sqlite:///./varasto.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Apufunktio tietokantaistunnon noutamiseen
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()