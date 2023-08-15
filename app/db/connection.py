from app.core.config import settings
from sqlalchemy.engine import Engine
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase

if not settings.MYSQL_DATABASE_URI:
    raise ValueError('Missing database URI')

mysqlEngine: Engine = create_engine(
    settings.MYSQL_DATABASE_URI,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    connect_args={
        'ssl_ca': settings.MYSQL_SSL,
    },
)


class MySQLTableBase(DeclarativeBase):
    pass


def MySqlSession(expireOnCommit: bool = False) -> Session:
    return sessionmaker(bind=mysqlEngine, expire_on_commit=expireOnCommit)()


def createMySQLTables():
    MySQLTableBase.metadata.create_all(mysqlEngine)


def dropMySQLTables():
    MySQLTableBase.metadata.drop_all(mysqlEngine)
