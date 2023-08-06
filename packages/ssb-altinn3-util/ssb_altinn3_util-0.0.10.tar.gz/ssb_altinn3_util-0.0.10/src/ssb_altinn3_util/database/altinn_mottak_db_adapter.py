from pg8000.dbapi import Connection
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from google.cloud.sql.connector import connector


class AltinnMottakDbAdapter:
    Base = declarative_base()

    def __init__(self):
        self.engine = None
        self.session_provider = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )

    def get_session(self) -> Session:
        db = self.session_provider()
        try:
            yield db
        finally:
            db.close()

    def init_engine(
        self,
        cloud_sql_instance_connection: str,
        user_name: str,
        database_name: str,
        user_password: str,
        local_db: bool,
    ):
        if local_db:
            self._init_connection_db_user(
                db_name=database_name, user_name=user_name, user_password=user_password
            )
        else:
            self._init_connection_iam(
                connection_name=cloud_sql_instance_connection,
                user_name=user_name,
                db_name=database_name,
            )

    # used for connecting with IAM authentication
    def _init_connection_iam(
        self,
        connection_name: str,
        user_name: str,
        db_name: str,
    ):
        def get_connection() -> Connection:
            connection: Connection = connector.connect(
                connection_name,
                "pg8000",
                user=user_name,
                db=db_name,
                enable_iam_auth=True,
            )
            return connection

        engine = create_engine("postgresql+pg8000://", creator=get_connection)
        engine.dialect.description_encoding = None

        self.engine = engine

    # used for connections with a regular database user
    def _init_connection_db_user(
        self,
        db_name: str,
        user_name: str,
        user_password: str,
    ):
        self.engine = create_engine(
            f"postgresql+pg8000://{user_name}:{user_password}@localhost:5432/{db_name}"
        )
