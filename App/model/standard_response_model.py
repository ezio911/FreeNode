import json
from dataclasses import dataclass, asdict


@dataclass
class RespModel:
    code: int = 200
    msg: str = "success"
    data: dict = None

    def __str__(self):
        return json.dumps(asdict(self), ensure_ascii=False)

    @property
    def dict(self):
        return asdict(self)

    @property
    def json_str(self):
        return json.dumps(asdict(self), ensure_ascii=False)

    def params_to_dict(self, **kwargs):
        self.data = kwargs
