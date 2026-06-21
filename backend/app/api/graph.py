from fastapi import APIRouter, Query
from app.graph.builder import build_identity_graph
from app.risk.engine import calculate_risk_scores

router = APIRouter()

_cached_graph = None

@router.get("/")
def get_graph(limit: int = Query(60, description="Max users to show in graph (default 60)")):
    global _cached_graph
    if _cached_graph is not None:
        return _cached_graph

    full_graph = build_identity_graph()

    # Get top-N users by risk score so the graph stays renderable in the browser
    try:
        risks = calculate_risk_scores()
        top_user_ids = {
            r["user_id"]
            for r in sorted(risks, key=lambda x: x["risk_score"], reverse=True)[:limit]
        }
    except Exception:
        # Fallback: take first `limit` user nodes
        top_user_ids = list({
            n["id"] for n in full_graph["nodes"] if n["type"] == "user"
        })[:limit]

    # Keep only nodes connected to those users
    allowed_ids: set = set(top_user_ids)
    for edge in full_graph["edges"]:
        if edge["source"] in top_user_ids:
            allowed_ids.add(edge["target"])
        if edge["target"] in top_user_ids:
            allowed_ids.add(edge["source"])

    filtered_nodes = [n for n in full_graph["nodes"] if n["id"] in allowed_ids]
    filtered_edges = [
        e for e in full_graph["edges"]
        if e["source"] in allowed_ids and e["target"] in allowed_ids
    ]

    _cached_graph = {"nodes": filtered_nodes, "edges": filtered_edges}
    return _cached_graph
