"use client";
import { useState, useEffect } from "react";
import Link from "next/link";

type RiskItem = {
  user_id: string;
  name: string;
  department: string;
  risk_score: number;
  severity: string;
  reasons: string[];
};

export default function Risks() {
  const [risks, setRisks] = useState<RiskItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://localhost:8000/api/risks")
      .then((res) => res.json())
      .then((data) => {
        setRisks(data);
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
        return "bg-red-500/20 text-red-300 border-red-400";
      case "HIGH":
        return "bg-orange-500/20 text-orange-300 border-orange-400";
      case "MEDIUM":
        return "bg-yellow-500/20 text-yellow-300 border-yellow-400";
      default:
        return "bg-green-500/20 text-green-300 border-green-400";
    }
  }

  return (
    <div className="min-h-screen p-8">
      <div className="max-w-7xl mx-auto">
        <div className="flex items-center justify-between mb-8">
          <h1 className="text-4xl font-bold">Risk Center</h1>
          <Link href="/" className="text-purple-300 hover:text-purple-100">← Back to Home</Link>
        </div>
        
        <div className="bg-white/10 backdrop-blur rounded-2xl border border-white/20 overflow-hidden">
          <div className="p-6 border-b border-white/20">
            <h2 className="text-2xl font-semibold">Risk Ranked Identities</h2>
          </div>
          <div className="overflow-x-auto">
            {loading ? (
              <div className="p-12 text-center">Loading...</div>
            ) : (
              <table className="w-full text-left">
                <thead className="bg-white/5">
                  <tr>
                    <th className="p-4 font-semibold">User ID</th>
                    <th className="p-4 font-semibold">Name</th>
                    <th className="p-4 font-semibold">Department</th>
                    <th className="p-4 font-semibold">Risk Score</th>
                    <th className="p-4 font-semibold">Severity</th>
                    <th className="p-4 font-semibold">Reasons</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-white/10">
                  {risks.map((risk) => (
                    <tr key={risk.user_id} className="hover:bg-white/5">
                      <td className="p-4">{risk.user_id}</td>
                      <td className="p-4 font-medium">{risk.name}</td>
                      <td className="p-4">{risk.department}</td>
                      <td className="p-4 font-extrabold text-2xl">{risk.risk_score}</td>
                      <td className="p-4">
                        <span className={`px-3 py-1 rounded-full text-xs font-bold border ${getSeverityColor(risk.severity)}`}>
                          {risk.severity}
                        </span>
                      </td>
                      <td className="p-4">
                        <ul className="list-disc pl-4 text-sm">
                          {risk.reasons.map((reason, i) => (
                            <li key={i}>{reason}</li>
                          ))}
                        </ul>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
