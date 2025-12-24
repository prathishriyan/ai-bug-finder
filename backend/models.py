# -------------------- Request Model --------------------

from pydantic import BaseModel

class CodeInput(BaseModel):
    language: str
    code: str
