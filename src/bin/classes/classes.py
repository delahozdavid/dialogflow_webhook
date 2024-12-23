from pydantic import BaseModel
from typing import Dict, Any

class claseSociosSteren(BaseModel):
    queryResult: Dict[str, Any]
    session: str