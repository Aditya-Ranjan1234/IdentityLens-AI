import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app.graph.builder import build_identity_graph
import json

graph = build_identity_graph()
print(f"Nodes count: {len(graph['nodes'])}")
print(f"User nodes: {len([n for n in graph['nodes'] if n['type'] == 'user'])}")
print(f"Platform account nodes: {len([n for n in graph['nodes'] if n['type'] == 'platform_account'])}")
print("Sample nodes:")
print(json.dumps(graph['nodes'][:10], indent=2))
