"use client";
import { useState, useEffect } from "react";
import Link from "next/link";

type Incident = {
  incident_id: string;
  title: string;
  severity: string;
  user_id: string;
  user_name: string;
  reasons: string[];
  status: string;
};

export default function Incidents() {
  const [incidents, setIncidents] = useState<Incident[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || "";
    fetch(`${apiUrl}/api/incidents`)
      .then((res) => res.json())
      .then((data) => {
        setIncidents(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  function getSeverityColor(severity: string) {
    switch (severity) {
      case "CRITICAL":
        return "bg-red-600";
      case "HIGH":
        return "bg-orange-600";
      case "MEDIUM":
        return "bg-yellow-600";
      default:
        return "bg-green-600";
    }
  }

  return (
    <div className="min-h-screen p-8">
      <div className="max-w-7xl mx-auto">
        <div className="flex items-center justify-between mb-8">
          <h1 className="text-4xl font-bold">Incidents</h1>
          <Link href="/" className="text-purple-300 hover:text-purple-100">← Back to Home</Link>
        </div>

        <div className="grid grid-cols-1 gap-6">
          {loading ? (
            <div className="p-12 text-center bg-white/10 rounded-2xl border border-white/20">Loading...</div>
          ) : (
            incidents.map((incident) => (
              <div
                key={incident.incident_id}
                className="bg-white/10 backdrop-blur rounded-2xl border border-white/20 p-6 hover:bg-white/15 transition-all"
              >
                <div className="flex items-start justify-between mb-4">
                  <div>
                    <div className="flex items-center gap-3 mb-2">
                      <span className={`px-3 py-1 rounded-full text-xs font-bold ${getSeverityColor(incident.severity)}`}>
                        {incident.severity}
                      </span>
                      <span className="text-gray-400 text-sm">{incident.incident_id}</span>
                    </div>
                    <h3 className="text-xl font-semibold">{incident.title}</h3>
                  </div>
                  <span className="px-4 py-2 bg-yellow-500/20 text-yellow-300 rounded-full text-sm font-bold">
                    {incident.status}
                  </span>
                </div>
                <div className="mb-4">
                  <p className="text-gray-300">User: {incident.user_name} ({incident.user_id})</p>
                </div>
                <div>
                  <h4 className="font-semibold mb-2">Risk Reasons:</h4>
                  <ul className="list-disc pl-6 text-sm">
                    {incident.reasons.map((reason, i) => (
                      <li key={i} className="text-gray-300">{reason}</li>
                    ))}
                  </ul>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
