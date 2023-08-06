from ssb_altinn3_util.database import schema
from ssb_altinn3_util.database.altinn_mottak_db_adapter import AltinnMottakDbAdapter


def init_db_adapter(database_url: str) -> AltinnMottakDbAdapter:
    adapter = AltinnMottakDbAdapter(database_url=database_url)
    schema.AltinnMottakDbAdapter.Base.metadata.create_all(bind=adapter.engine)
    return adapter
