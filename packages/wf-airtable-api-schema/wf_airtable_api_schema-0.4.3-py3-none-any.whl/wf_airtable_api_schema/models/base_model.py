from datetime import datetime

from pydantic import BaseModel


class BaseModel(BaseModel):
    def dict(self, **kwargs):
        output = super().dict(**kwargs)
        for k, v in output.items():
            if isinstance(v, datetime):
                # datetime: "2022-04-16T06:43:56+00:00"
                output[k] = v.isoformat()
        return output
