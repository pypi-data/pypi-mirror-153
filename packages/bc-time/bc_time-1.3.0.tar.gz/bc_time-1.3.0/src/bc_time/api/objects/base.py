from abc import ABC
from bc_time.api.api import Api

class Base(ABC):
    api = None
    content_type_id = None

    def __init__(self, api: Api=None) -> None:
        self.api = Api() if not api else api