from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from core.configs import settings

engine: Session = create_engine(settings.DB_URL)


session_maker = sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=Session,
    bind=engine
)


def get_session():
    session = session_maker()

    try:
        yield session
    finally:
        session.close()
