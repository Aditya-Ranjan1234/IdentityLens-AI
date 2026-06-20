from fastapi import APIRouter
from app.services.identity_resolver import resolve_identities

router = APIRouter()

@router.get("/")
def get_master_identities():
    return resolve_identities()
