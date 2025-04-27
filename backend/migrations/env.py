from logging.config import fileConfig

from sqlalchemy import create_engine
from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
# target_metadata = None

# from backend.common.database import Base  # Corrected import
from backend.common.database import Base, SYNC_ENGINE as engine  # Corrected import
from backend.social.app.models import Base as SocialBase
from backend.marketplace.app.models import Base as MPBase
from backend.facility.app.models import Base as FacilityBase

# ...

config.set_main_option("sqlalchemy.url", str(engine.url))

target_metadata = [
    SocialBase.metadata,
    MPBase.metadata,
    FacilityBase.metadata,
]
