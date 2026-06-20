from fastapi import APIRouter
from app.graph.builder import build_identity_graph

router = APIRouter()

@router.get("/")
def get_graph():
    graph_data = build_identity_graph()
    return graph_data
