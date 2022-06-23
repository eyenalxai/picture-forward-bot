import ormar

from config.database import BaseMeta


class Saved(ormar.Model):
    class Meta(BaseMeta):
        tablename = "saved"

    id: int = ormar.Integer(primary_key=True)
    file_id: str = ormar.String(max_length=512, nullable=False, unique=True)
