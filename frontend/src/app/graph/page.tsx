"use client";
import { useState, useEffect, useCallback } from "react";
import ReactFlow, {
  Background,
  Controls,
  MiniMap,
  useNodesState,
  useEdgesState,
  addEdge,
  Connection,
  Edge,
  Node,
} from "reactflow";
import "reactflow/dist/style.css";
import Link from "next/link";

type GraphData = {
  nodes: { id: string; label: string; type: string; platform?: string }[];
  edges: { source: string; target: string; type: string }[];
};

export default function GraphPage() {
  const [graphData, setGraphData] = useState<GraphData | null>(null);
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || "";
    fetch(`${apiUrl}/api/graph`)
      .then((res) => res.json())
      .then((data) => {
        setGraphData(data);
        const parsedNodes: Node[] = data.nodes.map((n, index) => ({
          id: n.id,
          type: "default",
          position: { x: Math.random() * 800, y: Math.random() * 600 },
          data: { label: n.label },
          style: getNodeStyle(n.type, n.platform),
        }));
        const parsedEdges: Edge[] = data.edges.map((e, index) => ({
          id: `e-${index}`,
          source: e.source,
          target: e.target,
          animated: true,
        }));
        setNodes(parsedNodes);
        setEdges(parsedEdges);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setLoading(false);
      });
  }, [setNodes, setEdges]);

  const onConnect = useCallback(
    (params: Connection) => setEdges((eds) => addEdge(params, eds)),
    [setEdges]
  );

  function getNodeStyle(type: string, platform?: string) {
    let color = "#8b5cf6";
    if (type === "user") color = "#10b981";
    else if (platform === "AWS") color = "#f59e0b";
    else if (platform === "AD") color = "#3b82f6";
    else if (platform === "Okta") color = "#ec4899";
    else if (type === "role" || type === "group") color = "#6366f1";

    return {
      background: color,
      color: "#fff",
      border: "2px solid #fff",
      borderRadius: 8,
      padding: "10px 20px",
    };
  }

  return (
    <div className="min-h-screen flex flex-col">
      <div className="p-8 max-w-7xl mx-auto w-full">
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-4xl font-bold">Graph View</h1>
          <Link href="/" className="text-purple-300 hover:text-purple-100">← Back to Home</Link>
        </div>
        {loading ? (
          <div className="p-12 text-center">Loading graph...</div>
        ) : (
          <div className="h-[700px] bg-white/10 backdrop-blur rounded-2xl border border-white/20 overflow-hidden">
            <ReactFlow
              nodes={nodes}
              edges={edges}
              onNodesChange={onNodesChange}
              onEdgesChange={onEdgesChange}
              onConnect={onConnect}
              fitView
            >
              <Background />
              <Controls />
              <MiniMap />
            </ReactFlow>
          </div>
        )}
      </div>
    </div>
  );
}
