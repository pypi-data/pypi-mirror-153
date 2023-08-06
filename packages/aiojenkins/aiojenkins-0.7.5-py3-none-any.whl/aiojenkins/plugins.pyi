from _typeshed import Incomplete
from typing import Dict, Optional

class Plugins:
    jenkins: Incomplete
    def __init__(self, jenkins) -> None: ...
    async def get_all(self, depth: Optional[int] = ...) -> Dict[str, dict]: ...
