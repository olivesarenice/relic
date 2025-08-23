import time
from datetime import datetime, timezone
from uuid import uuid4

from pydantic import BaseModel, Field  # Import Field


class Datum(BaseModel):
    uuid: str = Field(default_factory=lambda: str(uuid4()))
    unix_ts: int = Field(default_factory=lambda: int(time.time()))
    iso_ts: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    collector: str = ""
    source_type: str = ""
    data_json: dict = {}


class Engram(BaseModel):
    placeholder: str = "engram"
