from ssb_altinn3_util.database import schema
from ssb_altinn3_util.database.altinn_mottak_db_adapter import AltinnMottakDbAdapter


def init_db_adapter(
    user_name: str,
    database_name: str,
    user_password: str = None,
    cloud_sql_instance_connection: str = None,
    local_db: bool = False,
) -> AltinnMottakDbAdapter:
    """
    Initiates the database adapter enabling database storage through the database.crud module

    :param user_name: Name of the database user used for the connection.  Regular database user when running locally,
    IAM enabled user when running against a cloud sql instance.
    :param database_name: The name of the database to connect to
    :param user_password: Password for the database user.  Only required when using local database or ordinary database
    authentication.
    :param cloud_sql_instance_connection: Connectionstring used to connect to the cload sql instance.  Uses the
    format "project:region:instance"
    :param local_db: Set to true if connecting to a local database. Will use localhost:5432 as database server
    :return: A configured data adapter ready for use.
    """
    adapter = AltinnMottakDbAdapter()
    adapter.init_engine(
        cloud_sql_instance_connection=cloud_sql_instance_connection,
        user_name=user_name,
        user_password=user_password,
        database_name=database_name,
        local_db=local_db,
    )
    schema.AltinnMottakDbAdapter.Base.metadata.create_all(bind=adapter.engine)
    return adapter
