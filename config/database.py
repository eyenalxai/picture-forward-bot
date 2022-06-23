import databases

import ormar
import sqlalchemy

DATABASE_URL = "sqlite:///db.sqlite"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()


class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = database
