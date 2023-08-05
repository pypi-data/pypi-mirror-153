import datetime
import json
from pathlib import Path
from typing import Any
from uuid import UUID


class ExtendedJSONEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, (Path, UUID)):
            return str(o)

        if isinstance(o, (datetime.date, datetime.datetime)):
            return o.isoformat()

        return json.JSONEncoder.default(self, o)
