"use client";
import { useState, useEffect } from "react";
import ReactFlow, {
  Node,
  Edge,
  Controls,
  Background,
  MiniMap,
  useNodesState,
  useEdgesState,
} from "reactflow";
import "reactflow/dist/style.css";
import {
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import Dagre from "@dagrejs/dagre";

const g = new Dagre.graphlib.Graph().setDefaultEdgeLabel(() => ({}));
g.setGraph({ rankdir: "LR", ranksep: 100, nodesep: 70 });

function getLayoutedElements(nodes: Node[], edges: Edge[]) {
  g.nodes().forEach((n) => g.removeNode(n));
  g.edges().forEach((e) => g.removeEdge(e.v, e.w));
  nodes.forEach((node) => {
    g.setNode(node.id, { width: 150, height: 50 });
  });
  edges.forEach((edge) => {
    g.setEdge(edge.source, edge.target);
  });
  Dagre.layout(g);

  return {
    nodes: nodes.map((node) => {
      const position = g.node(node.id);
      const x = position.x - 150 / 2;
      const y = position.y - 50 / 2;
      return { ...node, position: { x, y } };
    }),
    edges,
  };
}

type User = {
  user_id: string;
  name: string;
  email: string;
  department: string;
  title: string;
  status: string;
  platforms: Record<string, any>;
};

type Risk = {
  user_id: string;
  name: string;
  risk_score: number;
  severity: "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";
  reasons: string[];
};

type Incident = {
  incident_id: string;
  user_id: string;
  user_name: string;
  severity: string;
  alerts: string[];
  timestamp: string;
};

type Metrics = {
  total_users: number;
  avg_risk_score: number;
  risk_distribution: Record<string, number>;
  ml_anomalies: number;
  offboarding_gaps: number;
};

type GraphData = {
  nodes: { id: string; type: string; label: string; platform?: string }[];
  edges: { source: string; target: string; type: string }[];
};

type OffboardingGap = {
  user_id: string;
  name: string;
  email: string;
  termination_date: string;
  orphaned_platforms: string[];
  hr_status: string;
  last_activity: string;
};

const COLORS = {
  CRITICAL: "#ffb4ab",
  HIGH: "#f97316",
  MEDIUM: "#eab308",
  LOW: "#22c55e",
};

export default function Home() {
  const [currentTab, setCurrentTab] = useState("overview");
  const [users, setUsers] = useState<User[]>([]);
  const [risks, setRisks] = useState<Risk[]>([]);
  const [incidents, setIncidents] = useState<Incident[]>([]);
  const [anomalies, setAnomalies] = useState<any[]>([]);
  const [metrics, setMetrics] = useState<Metrics | null>(null);
  const [graphData, setGraphData] = useState<GraphData | null>(null);
  const [offboardingGaps, setOffboardingGaps] = useState<OffboardingGap[]>([]);
  const [loading, setLoading] = useState(true);
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);

  useEffect(() => {
    const API_URL = process.env.NEXT_PUBLIC_API_URL || "";
    Promise.all([
      fetch(`${API_URL}/api/users`).then((res) => res.json()),
      fetch(`${API_URL}/api/risks`).then((res) => res.json()),
      fetch(`${API_URL}/api/incidents`).then((res) => res.json()),
      fetch(`${API_URL}/api/anomalies`).then((res) => res.json()),
      fetch(`${API_URL}/api/metrics`).then((res) => res.json()),
      fetch(`${API_URL}/api/graph`).then((res) => res.json()),
      fetch(`${API_URL}/api/offboarding`).then((res) => res.json()),
    ])
      .then(([usersRes, risksRes, incidentsRes, anomaliesRes, metricsRes, graphRes, offboardingRes]) => {
        setUsers(usersRes);
        setRisks(risksRes);
        setIncidents(incidentsRes);
        setAnomalies(anomaliesRes);
        setMetrics(metricsRes);
        setGraphData(graphRes);
        setOffboardingGaps(offboardingRes);

        const initialNodes: Node[] = (graphRes?.nodes || []).map((node: any) => {
          let color = "#98cbff";
          let borderColor = "#98cbff";
          let bg = "#161d23";
          
          if (node.type === "user") {
            color = "#22c55e";
            borderColor = "#22c55e";
            bg = "#14532d";
          }
          else if (node.platform === "AD") {
            color = "#16a34a";
            borderColor = "#16a34a";
            bg = "#052e16";
          }
          else if (node.platform === "AWS") {
            color = "#f97316";
            borderColor = "#f97316";
            bg = "#431407";
          }
          else if (node.platform === "Okta") {
            color = "#8b5cf6";
            borderColor = "#8b5cf6";
            bg = "#2e1065";
          }
          
          return {
            id: node.id,
            type: "default",
            position: { x: 0, y: 0 },
            data: { label: node.label },
            style: {
              background: bg,
              color: color,
              border: `2px solid ${borderColor}`,
              borderRadius: "8px",
              padding: "8px",
              fontWeight: "bold",
            },
          };
        });
        
        const initialEdges: Edge[] = (graphRes?.edges || []).map((edge: any, index: number) => ({
          id: `edge-${index}`,
          source: edge.source,
          target: edge.target,
          animated: true,
          style: { stroke: "#3f4852", strokeWidth: 2 },
        }));

        const { nodes: layoutedNodes, edges: layoutedEdges } = getLayoutedElements(initialNodes, initialEdges);
        
        setNodes(layoutedNodes);
        setEdges(layoutedEdges);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  const highRiskCount = risks.filter((r) => ["CRITICAL", "HIGH"].includes(r.severity)).length;
  const mlAnomalyCount = anomalies.filter((a) => a.is_anomaly).length;

  const riskChartData = metrics ? Object.entries(metrics.risk_distribution).map(([severity, count]) => ({
    name: severity,
    value: count,
  })) : [];

  const deptRiskData = users.reduce((acc, user) => {
    const dept = user.department || "Unknown";
    const risk = risks.find(r => r.user_id === user.user_id);
    const avgRisk = acc[dept] ? (acc[dept].avg * acc[dept].count + (risk?.risk_score || 0)) / (acc[dept].count + 1) : (risk?.risk_score || 0);
    return {
      ...acc,
      [dept]: {
        count: (acc[dept]?.count || 0) + 1,
        avg: avgRisk,
      }
    };
  }, {} as Record<string, { count: number, avg: number }>);

  const deptChartData = Object.entries(deptRiskData).map(([name, data]) => ({
    name,
    avgRisk: Math.round(data.avg),
  }));

  const renderOverviewTab = () => (
    <div className="space-y-gutter">
      <div className="grid grid-cols-1 md:grid-cols-4 gap-gutter">
        <div className="bg-surface-container border border-outline-variant p-stack-md rounded-lg flex flex-col justify-between" style={{ boxShadow: "0 0 12px rgba(152, 203, 255, 0.2)" }}>
          <div className="flex justify-between items-start">
            <span className="font-label-mono text-label-mono text-on-surface-variant uppercase">Total Identities</span>
            <span className="material-symbols-outlined text-primary text-sm">groups</span>
          </div>
          <div className="mt-4">
            <h2 className="font-display-lg text-display-lg">{loading ? "..." : users.length}</h2>
          </div>
        </div>
        <div className="bg-surface-container border border-error/30 p-stack-md rounded-lg flex flex-col justify-between" style={{ boxShadow: "0 0 12px rgba(255, 180, 171, 0.15)" }}>
          <div className="flex justify-between items-start">
            <span className="font-label-mono text-label-mono text-error uppercase">High Risk</span>
            <span className="material-symbols-outlined text-error text-sm">warning</span>
          </div>
          <div className="mt-4">
            <h2 className="font-display-lg text-display-lg text-error">{loading ? "..." : highRiskCount}</h2>
          </div>
        </div>
        <div className="bg-surface-container border border-outline-variant p-stack-md rounded-lg flex flex-col justify-between">
          <div className="flex justify-between items-start">
            <span className="font-label-mono text-label-mono text-on-surface-variant uppercase">Offboarding Gaps</span>
            <span className="material-symbols-outlined text-tertiary text-sm">person_off</span>
          </div>
          <div className="mt-4">
            <h2 className="font-display-lg text-display-lg">{loading ? "..." : offboardingGaps.length}</h2>
          </div>
        </div>
        <div className="bg-surface-container border border-outline-variant p-stack-md rounded-lg flex flex-col justify-between">
          <div className="flex justify-between items-start">
            <span className="font-label-mono text-label-mono text-on-surface-variant uppercase">ML Anomalies</span>
            <span className="material-symbols-outlined text-on-surface-variant text-sm">history_toggle_off</span>
          </div>
          <div className="mt-4">
            <h2 className="font-display-lg text-display-lg">{loading ? "..." : mlAnomalyCount}</h2>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-gutter">
        <div className="lg:col-span-8 bg-surface-container border border-outline-variant rounded-lg p-stack-md relative overflow-hidden h-[400px]">
          <div className="flex justify-between items-center mb-8 relative z-10">
            <div>
              <h3 className="font-headline-md text-headline-md font-semibold">Risk Distribution</h3>
              <p className="font-body-md text-body-md text-on-surface-variant">Identity concentration vs permission scope</p>
            </div>
          </div>
          {loading ? (
            <div className="h-64 flex items-center justify-center text-on-surface-variant">Loading...</div>
          ) : (
            <ResponsiveContainer width="100%" height={280}>
              <PieChart>
                <Pie
                  data={riskChartData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                  outerRadius={100}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {riskChartData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[entry.name as keyof typeof COLORS] || "#98cbff"} />
                  ))}
                </Pie>
                <Tooltip
                  contentStyle={{ backgroundColor: "#1b2026", borderColor: "#3f4852" }}
                  labelStyle={{ color: "#dfe3ea" }}
                />
              </PieChart>
            </ResponsiveContainer>
          )}
        </div>
        <div className="lg:col-span-4 bg-surface-container border border-outline-variant rounded-lg p-stack-md h-[400px] flex flex-col">
          <div className="mb-4">
            <h3 className="font-headline-md text-headline-md font-semibold text-error flex items-center gap-2">
              <span className="material-symbols-outlined">cancel</span>
              Active Offboarding Gaps
            </h3>
            <p className="font-body-md text-body-md text-on-surface-variant">Disabled in AD, Active in Cloud</p>
          </div>
          <div className="flex-1 overflow-y-auto space-y-3 pr-2">
            {loading ? (
              <div className="text-on-surface-variant py-8 text-center">Loading...</div>
            ) : offboardingGaps.length === 0 ? (
              <div className="text-on-surface-variant py-8 text-center">No gaps detected</div>
            ) : (
              offboardingGaps.slice(0, 6).map((gap) => (
                <div key={gap.user_id} className="bg-surface-variant p-3 rounded border-l-4 border-error flex justify-between items-center group hover:bg-surface-container-highest transition-colors">
                  <div>
                    <p className="font-body-md font-bold">{gap.name}</p>
                    <p className="text-[10px] text-on-surface-variant font-label-mono">Active in: {gap.orphaned_platforms.join(", ")}</p>
                  </div>
                  <button className="opacity-0 group-hover:opacity-100 bg-error text-on-error text-[10px] px-2 py-1 rounded transition-opacity">REVOKE</button>
                </div>
              ))
            )}
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-gutter">
        <div className="lg:col-span-2 bg-surface-container border border-outline-variant rounded-lg overflow-hidden">
          <div className="p-stack-md border-b border-outline-variant flex justify-between items-center">
            <div><h3 className="font-headline-md text-headline-md font-semibold">High Risk Identity Watchlist</h3></div>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-left">
              <thead className="bg-surface-container-low text-[10px] font-label-mono text-on-surface-variant uppercase">
                <tr>
                  <th className="px-6 py-4">Identity</th>
                  <th className="px-6 py-4">Presence</th>
                  <th className="px-6 py-4">Risk Score</th>
                  <th className="px-6 py-4">Risk Factors</th>
                  <th className="px-6 py-4">Last Activity</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-outline-variant">
                {loading ? (
                  <tr><td colSpan={5} className="px-6 py-12 text-center text-on-surface-variant">Loading...</td></tr>
                ) : (
                  risks.filter(r => ["CRITICAL", "HIGH"].includes(r.severity)).slice(0, 10).map((risk) => {
                    const user = users.find(u => u.user_id === risk.user_id);
                    const userPlatforms = user?.platforms ? Object.keys(user.platforms) : [];
                    return (
                      <tr key={risk.user_id} className="hover:bg-surface-variant/40 transition-colors">
                        <td className="px-6 py-4">
                          <div className="flex items-center gap-3">
                            <div className="w-8 h-8 rounded bg-primary-container/20 flex items-center justify-center text-primary-fixed-dim border border-primary/20 font-bold text-sm">{user?.name?.charAt(0) || risk.user_id.charAt(0)}</div>
                            <div>
                              <p className="text-table-data font-semibold">{user?.name || risk.name}</p>
                              <p className="text-[10px] text-on-surface-variant">{user?.title || "-"}</p>
                            </div>
                          </div>
                        </td>
                        <td className="px-6 py-4">
                          <div className="flex gap-1.5">
                            {userPlatforms.slice(0,3).map(p => (
                              <span key={p} className="text-[9px] bg-secondary-container/50 px-1.5 py-0.5 rounded font-label-mono text-on-secondary-container">{p}</span>
                            ))}
                          </div>
                        </td>
                        <td className="px-6 py-4">
                          <div className="flex items-center gap-2">
                            <div className="w-24 h-1.5 bg-surface-container-highest rounded-full overflow-hidden">
                              <div className={`h-full ${
                                risk.severity === "CRITICAL" ? "bg-error" : risk.severity === "HIGH" ? "bg-orange-500" : risk.severity === "MEDIUM" ? "bg-yellow-500" : "bg-green-500"
                              }`} style={{ width: `${Math.min(risk.risk_score, 100)}%` }} />
                            </div>
                            <span className="text-table-data font-bold">{risk.risk_score}</span>
                          </div>
                        </td>
                        <td className="px-6 py-4">
                          <span className={`px-2 py-1 rounded-full text-[11px] font-bold flex items-center gap-1 w-fit ${
                            risk.severity === "CRITICAL" ? "bg-error-container/30 text-error border border-error/20" :
                            risk.severity === "HIGH" ? "bg-orange-500/20 text-orange-300 border border-orange-400" :
                            risk.severity === "MEDIUM" ? "bg-yellow-500/20 text-yellow-300 border border-yellow-400" :
                            "bg-green-500/20 text-green-300"
                          }`}>
                            <span className="w-1.5 h-1.5 rounded-full bg-current animate-pulse" />
                            {risk.reasons[0]}
                          </span>
                        </td>
                        <td className="px-6 py-4 font-label-mono text-[11px] text-on-surface-variant">2023-11-24 14:02</td>
                      </tr>
                    );
                  })
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );

  const renderRisksTab = () => (
    <div className="bg-surface-container border border-outline-variant rounded-lg p-stack-md">
      <h2 className="font-headline-md text-headline-md font-semibold mb-4">All Risk Assessments</h2>
      <div className="overflow-x-auto">
        <table className="w-full text-left">
          <thead className="bg-surface-container-low text-[10px] font-label-mono text-on-surface-variant uppercase">
            <tr>
              <th className="px-6 py-4">User ID</th>
              <th className="px-6 py-4">Name</th>
              <th className="px-6 py-4">Risk Score</th>
              <th className="px-6 py-4">Severity</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-outline-variant">
            {loading ? (
              <tr><td colSpan={4} className="px-6 py-12 text-center text-on-surface-variant">Loading...</td></tr>
            ) : (
              risks.map((risk) => (
                <tr key={risk.user_id} className="hover:bg-surface-variant/40 transition-colors">
                  <td className="px-6 py-4 text-table-data">{risk.user_id}</td>
                  <td className="px-6 py-4 text-table-data font-semibold">{risk.name}</td>
                  <td className="px-6 py-4 text-table-data font-bold">{risk.risk_score}</td>
                  <td className="px-6 py-4 text-table-data">{risk.severity}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );

  const renderIncidentsTab = () => (
    <div className="bg-surface-container border border-outline-variant rounded-lg p-stack-md">
      <h2 className="font-headline-md text-headline-md font-semibold mb-4">Correlated Incidents</h2>
      <div className="space-y-3">
        {loading ? (
          <div className="text-on-surface-variant py-12 text-center">Loading...</div>
        ) : (
          incidents.slice(0, 10).map((incident) => (
            <div key={incident.incident_id} className="p-3 bg-surface-variant rounded border border-outline-variant">
              <div className="flex justify-between items-start mb-2">
                <div>
                  <p className="font-bold text-table-data">{incident.incident_id}</p>
                  <p className="text-[10px] text-on-surface-variant">{incident.user_name}</p>
                </div>
                <span className={`px-2 py-1 rounded-full text-xs font-bold ${incident.severity === "CRITICAL" ? "bg-error-container/30 text-error" : "bg-orange-500/20 text-orange-300"}`}>
                  {incident.severity}
                </span>
              </div>
              <p className="text-body-md">{incident.alerts.join(" • ")}</p>
            </div>
          ))
        )}
      </div>
    </div>
  );

  const renderGraphTab = () => (
    <div className="bg-surface-container border border-outline-variant rounded-lg p-0 overflow-hidden">
      <div className="p-stack-md border-b border-outline-variant flex justify-between items-center">
        <h2 className="font-headline-md text-headline-md font-semibold">Effective Privilege Graph</h2>
        <div className="flex gap-2">
          <button className="bg-secondary-container text-on-secondary-container px-3 py-1 rounded font-label-mono text-[10px] hover:bg-surface-container-highest transition-colors">Export Map</button>
          <button className="bg-surface-container-highest text-on-surface px-3 py-1 rounded font-label-mono text-[10px] border border-outline-variant">Refresh Sync</button>
        </div>
      </div>
      <div style={{ height: 600 }}>
        {loading ? (
          <div className="h-full flex items-center justify-center text-on-surface-variant">Loading...</div>
        ) : (
          <ReactFlow
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            fitView
          >
            <Background />
            <Controls />
            <MiniMap />
          </ReactFlow>
        )}
      </div>
    </div>
  );

  const renderOffboardingTab = () => (
    <div className="grid grid-cols-1 xl:grid-cols-12 gap-gutter">
      <div className="xl:col-span-9 bg-surface-container border border-outline-variant rounded-lg flex flex-col min-h-[500px]">
        <div className="p-4 border-b border-outline-variant flex justify-between items-center">
          <div className="flex items-center gap-2">
            <span className="material-symbols-outlined text-warning animate-pulse">warning</span>
            <h3 className="font-headline-md text-headline-md font-bold text-on-surface">Detected Orphaned Accounts</h3>
          </div>
          <div className="flex items-center gap-2">
            <div className="relative">
              <input className="bg-surface-dim border border-outline-variant rounded-lg px-8 py-1.5 text-body-md focus:border-primary outline-none transition-all" placeholder="Search users..." type="text"/>
              <span className="material-symbols-outlined absolute left-2 top-2 text-[18px] text-on-surface-variant">search</span>
            </div>
          </div>
        </div>
        <div className="overflow-x-auto flex-1">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-surface-dim/50 border-b border-outline-variant">
                <th className="px-6 py-4"></th>
                <th className="px-6 py-4 font-label-mono text-label-mono text-on-surface-variant uppercase tracking-wider">User Identity</th>
                <th className="px-6 py-4 font-label-mono text-label-mono text-on-surface-variant uppercase tracking-wider">HR Status</th>
                <th className="px-6 py-4 font-label-mono text-label-mono text-on-surface-variant uppercase tracking-wider">Orphaned Platforms</th>
                <th className="px-6 py-4 font-label-mono text-label-mono text-on-surface-variant uppercase tracking-wider">Last Activity</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-outline-variant">
              {loading ? (
                <tr><td colSpan={5} className="px-6 py-12 text-center text-on-surface-variant">Loading...</td></tr>
              ) : offboardingGaps.length === 0 ? (
                <tr><td colSpan={5} className="px-6 py-12 text-center text-on-surface-variant">No offboarding gaps detected</td></tr>
              ) : (
                offboardingGaps.map((gap) => (
                  <tr key={gap.user_id} className="hover:bg-surface-variant/50 transition-colors">
                    <td className="px-6 py-4"><input className="rounded bg-background border-outline-variant text-primary focus:ring-primary" type="checkbox"/></td>
                    <td className="px-6 py-4">
                      <div className="flex items-center gap-3">
                        <div className="w-8 h-8 rounded bg-secondary-container flex items-center justify-center text-on-secondary-container font-bold text-[12px]">{gap.name.charAt(0)}</div>
                        <div>
                          <div className="font-bold text-on-surface text-body-md">{gap.name}</div>
                          <div className="text-on-surface-variant text-[12px] font-label-mono">{gap.email}</div>
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <span className="inline-flex items-center px-2 py-0.5 rounded text-[11px] font-bold bg-error-container text-on-error-container border border-error/20">
                        <span className="w-1.5 h-1.5 rounded-full bg-error mr-1.5"></span>
                        {gap.hr_status}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex gap-2">
                        {gap.orphaned_platforms.map(p => (
                          <span key={p} className="px-2 py-1 bg-surface-variant rounded text-[10px] font-bold border border-outline-variant">{p}</span>
                        ))}
                      </div>
                    </td>
                    <td className="px-6 py-4 text-on-surface-variant font-label-mono text-table-data">{gap.last_activity}</td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
      <div className="xl:col-span-3 space-y-gutter">
        <div className="bg-surface-container border border-outline-variant rounded-lg p-stack-md relative overflow-hidden">
          <div className="absolute top-0 left-0 w-1 h-full bg-warning"></div>
          <h3 className="font-headline-md text-headline-md font-bold text-on-surface mb-stack-sm flex items-center gap-2">
            <span className="material-symbols-outlined text-warning">bolt</span>
            Remediation
          </h3>
          <p className="text-body-md text-on-surface-variant mb-stack-lg">Execute bulk actions on selected identities to close offboarding gaps immediately.</p>
          <div className="space-y-stack-sm">
            <button className="w-full bg-error text-on-error py-3 rounded font-bold text-body-md flex items-center justify-center gap-2 hover:bg-red-500 transition-colors shadow-lg active:scale-95 duration-200">
              <span className="material-symbols-outlined">person_off</span>
              Disable All Selected
            </button>
            <button className="w-full bg-surface-variant text-on-surface py-3 rounded font-bold text-body-md border border-outline-variant flex items-center justify-center gap-2 hover:bg-outline-variant transition-colors active:scale-95 duration-200">
              <span className="material-symbols-outlined">mail</span>
              Notify Owners
            </button>
          </div>
        </div>
        <div className="bg-surface-container border border-outline-variant rounded-lg p-stack-md border-l-4 border-l-error">
          <h4 className="text-on-surface font-bold text-body-md mb-2 flex items-center gap-2">
            <span className="material-symbols-outlined text-error text-[20px]">priority_high</span>
            Risk Intelligence
          </h4>
          <p className="text-table-data text-on-surface-variant leading-relaxed">
            Orphaned accounts represent <span className="text-error font-bold">78%</span> of successful identity-based lateral movement attacks.
          </p>
        </div>
      </div>
    </div>
  );

  const renderMetricsTab = () => (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-gutter">
      <div className="bg-surface-container border border-outline-variant rounded-lg p-stack-md">
        <h2 className="font-headline-md text-headline-md font-semibold mb-4">Risk Distribution</h2>
        {loading || !metrics ? (
          <div className="text-on-surface-variant py-12 text-center">Loading...</div>
        ) : (
          <ResponsiveContainer width="100%" height={256}>
            <PieChart>
              <Pie
                data={riskChartData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {riskChartData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[entry.name as keyof typeof COLORS] || "#98cbff"} />
                ))}
              </Pie>
              <Tooltip
                contentStyle={{ backgroundColor: "#1b2026", borderColor: "#3f4852" }}
                labelStyle={{ color: "#dfe3ea" }}
              />
            </PieChart>
          </ResponsiveContainer>
        )}
      </div>
      <div className="bg-surface-container border border-outline-variant rounded-lg p-stack-md">
        <h2 className="font-headline-md text-headline-md font-semibold mb-4">System Metrics</h2>
        {loading || !metrics ? (
          <div className="text-on-surface-variant py-12 text-center">Loading...</div>
        ) : (
          <div className="space-y-2">
            <div className="flex justify-between items-center py-2 border-b border-outline-variant">
              <span>Total Users</span><span className="font-bold">{metrics.total_users}</span>
            </div>
            <div className="flex justify-between items-center py-2 border-b border-outline-variant">
              <span>Average Risk Score</span><span className="font-bold">{Number(metrics.avg_risk_score).toFixed(1)}</span>
            </div>
            <div className="flex justify-between items-center py-2 border-b border-outline-variant">
              <span>ML Anomalies</span><span className="font-bold">{metrics.ml_anomalies}</span>
            </div>
            <div className="flex justify-between items-center py-2">
              <span>Offboarding Gaps</span><span className="font-bold">{offboardingGaps.length}</span>
            </div>
          </div>
        )}
      </div>
    </div>
  );

  return (
    <div className="flex min-h-screen">
      <aside className="fixed left-0 top-0 h-full w-[240px] flex flex-col p-stack-md gap-stack-sm border-r border-outline-variant bg-surface-container z-50">
        <div className="flex items-center gap-3 mb-stack-lg px-3">
          <span className="material-symbols-outlined text-primary text-headline-md">shield_person</span>
          <span className="font-headline-md text-headline-md text-primary font-bold">IdentityLens AI</span>
        </div>
        <nav className="flex-1 space-y-1">
          {[
            { id: "overview", label: "Overview", icon: "dashboard" },
            { id: "risks", label: "Risk Center", icon: "speed" },
            { id: "incidents", label: "Incidents", icon: "report" },
            { id: "graph", label: "Identity Graph", icon: "account_tree" },
            { id: "offboarding", label: "Offboarding Gaps", icon: "door_front" },
            { id: "metrics", label: "Metrics", icon: "analytics" },
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setCurrentTab(tab.id)}
              className={`flex items-center gap-3 px-3 py-2 rounded transition-all ${
                currentTab === tab.id
                  ? "bg-secondary-container text-on-secondary-container shadow-[0_0_8px_rgba(152,203,255,0.3)]"
                  : "text-on-surface-variant hover:bg-surface-container-highest hover:text-on-surface"
              }`}
            >
              <span className="material-symbols-outlined">{tab.icon}</span>
              <span className="font-label-mono text-label-mono">{tab.label}</span>
            </button>
          ))}
        </nav>
      </aside>

      <main className="ml-[240px] flex-1 min-w-0 bg-background pb-12">
        <header className="flex justify-between items-center w-full px-container-padding h-16 sticky top-0 z-40 bg-background/80 backdrop-blur-md border-b border-outline-variant">
          <h1 className="font-headline-md font-bold text-primary">
            {currentTab === "overview" ? "Identity Risk Overview" :
             currentTab === "risks" ? "Risk Center" :
             currentTab === "incidents" ? "Incidents" :
             currentTab === "graph" ? "Effective Privilege Graph" :
             currentTab === "offboarding" ? "Offboarding Gaps" : "Metrics"}
          </h1>
          <div className="flex items-center gap-4">
            <button className="p-2 text-on-surface-variant hover:bg-surface-variant rounded-full transition-colors relative">
              <span className="material-symbols-outlined">notifications</span>
              <span className="absolute top-2 right-2 w-2 h-2 bg-error rounded-full border border-background animate-pulse" />
            </button>
            <button className="p-2 text-on-surface-variant hover:bg-surface-variant rounded-full transition-colors">
              <span className="material-symbols-outlined">settings</span>
            </button>
          </div>
        </header>

        <div className="p-container-padding">
          {currentTab === "overview" && renderOverviewTab()}
          {currentTab === "risks" && renderRisksTab()}
          {currentTab === "incidents" && renderIncidentsTab()}
          {currentTab === "graph" && renderGraphTab()}
          {currentTab === "offboarding" && renderOffboardingTab()}
          {currentTab === "metrics" && renderMetricsTab()}
        </div>
      </main>
    </div>
  );
}
