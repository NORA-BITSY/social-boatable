import os, pytest, time
from testcontainers.postgresql import PostgresContainer
from backend.common.database import SYNC_ENGINE, Base

@pytest.fixture(scope="session", autouse=True)
def _pg_container():
    with PostgresContainer("postgres:16") as pg:
        os.environ["DATABASE_URL"] = pg.get_connection_url()
        # wait for container then prepare schema using sync engine
        Base.metadata.create_all(bind=SYNC_ENGINE)
        yield
