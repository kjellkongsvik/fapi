from pydantic import BaseModel


class Hello(BaseModel):
    val: int = 42
