from fastapi import APIRouter
from pydantic import BaseModel

from ..db.db import async_db


class FeatureFlag(BaseModel):
    name: str
    enabled: bool


router = APIRouter(prefix="/feature-flags")


@router.get("/", response_model=list[FeatureFlag])
async def get():
    rows = await async_db.fetch_all("SELECT name, enabled FROM feature_flags;")
    features = [
        FeatureFlag(**dict(zip(["name", "enabled"], [row.name, row.enabled])))
        for row in rows
    ]
    return features
