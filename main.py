from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Oasis(BaseModel):
    id: str
    rev: str
    pc: str


class LatLon(BaseModel):
    lat: float
    lon: float


Layout = list[LatLon] | Oasis


class Farm(BaseModel):
    from_date: int
    layout: Layout


@app.post("/")
async def root(layout: Layout) -> Farm:
    return Farm(from_date=5, layout=layout)
