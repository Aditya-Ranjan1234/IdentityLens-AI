
"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { ArrowLeft, ShieldAlert, Users, Lock, Activity, Shield } from "lucide-react";

interface User {
  user_id: string;
  name: string;
  email: string;
  department: string;
  title: string;
  manager: string;
  employment_type: string;
  hire_date: string;
  termination_date?: string;
  status: string;
}

interface Privilege {
  user_id: string;
  effective_permissions: string[];
  roles: string[];
  groups: string[];
  privilege_score: number;
  is_admin: boolean;
}

interface Anomaly {
  user_id: string;
  is_anomaly: boolean;
  anomaly_score: number;
  model?: string;
  features: {
    login_count: number;
    platform_count: number;
    resource_count: number;
    country_count: number;
    hour_variance: number;
  };
}

export default function IdentityExplorer() {
  const params = useParams();
  const router = useRouter();
  const [user, setUser] = useState<User | null>(null);
  const [privileges, setPrivileges] = useState<Privilege | null>(null);
  const [anomaly, setAnomaly] = useState<Anomaly | null>(null);
  const [loading, setLoading] = useState(true);

  const userId = params.user_id as string;

  useEffect(() => {
    async function loadData() {
      try {
        const [usersRes, privilegesRes, anomalyRes] = await Promise.all([
          fetch("http://localhost:8000/api/users"),
          fetch(`http://localhost:8000/api/privileges/${userId}`),
          fetch("http://localhost:8000/api/anomalies?model_type=isolation_forest"),
        ]);
        const users = await usersRes.json();
        const userData = users.find((u: User) => u.user_id === userId);
        setUser(userData);
        setPrivileges(await privilegesRes.json());
        const anomalies = await anomalyRes.json();
        setAnomaly(anomalies.find((a: Anomaly) => a.user_id === userId));
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, [userId]);

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen p-8">
        <p className="text-lg text-gray-400">Loading...</p>
      </div>
    );
  }

  if (!user) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen p-8">
        <h2 className="text-xl text-white">User not found</h2>
        <button
          className="mt-4 px-4 py-2 border border-gray-600 rounded hover:bg-gray-700 text-white"
          onClick={() => router.push("/dashboard")}
        >
          <div className="flex items-center">
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Dashboard
          </div>
        </button>
      </div>
    );
  }

  const getSeverityColor = (score: number) => {
    if (score > 150) return "bg-red-500";
    if (score > 100) return "bg-yellow-500";
    if (score > 50) return "bg-blue-500";
    return "bg-green-500";
  };

  const Badge = ({ children, className = "" }: { children: React.ReactNode; className?: string }) => (
    <span className={`px-2 py-1 text-xs rounded-full ${className}`}>{children}</span>
  );

  return (
    <div className="p-8 max-w-7xl mx-auto">
      <button
        className="mb-6 px-4 py-2 border border-gray-600 rounded hover:bg-gray-700 text-white"
        onClick={() => router.push("/dashboard")}
      >
        <div className="flex items-center">
          <ArrowLeft className="w-4 h-4 mr-2" />
          Back to Dashboard
        </div>
      </button>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column: User Info */}
        <div className="bg-slate-800 border border-slate-700 text-white rounded-lg p-6">
          <div className="flex items-center gap-3 mb-6">
            <div className="w-12 h-12 rounded-full bg-slate-700 flex items-center justify-center text-2xl font-bold">
              {user.name.split(" ").map(n => n[0]).join("").toUpperCase()}
            </div>
            <div>
              <h3 className="text-xl font-semibold">{user.name}</h3>
              <p className="text-sm text-gray-400">{user.title} · {user.department}</p>
            </div>
          </div>
          <div className="space-y-4">
            <div>
              <p className="text-sm text-gray-400">User ID</p>
              <p className="text-white font-mono">{user.user_id}</p>
            </div>
            <div>
              <p className="text-sm text-gray-400">Email</p>
              <p className="text-white">{user.email}</p>
            </div>
            <div>
              <p className="text-sm text-gray-400">Manager</p>
              <p className="text-white">{user.manager}</p>
            </div>
            <div>
              <p className="text-sm text-gray-400">Employment Type</p>
              <Badge className="border border-gray-600">{user.employment_type}</Badge>
            </div>
            <div>
              <p className="text-sm text-gray-400">Status</p>
              <Badge className={user.status === "ACTIVE" ? "bg-green-600" : "bg-red-600"}>
                {user.status}
              </Badge>
            </div>
          </div>
        </div>

        {/* Right Column: Privileges and Anomalies */}
        <div className="lg:col-span-2 space-y-6">
          {privileges && (
            <div className="bg-slate-800 border border-slate-700 text-white rounded-lg p-6">
              <div className="flex items-center justify-between mb-6">
                <h3 className="text-lg font-semibold flex items-center gap-2">
                  <Shield className="w-5 h-5" />
                  Effective Privileges
                </h3>
                <div className="flex items-center gap-3">
                  <p className="text-sm text-gray-400">Score</p>
                  <div className="flex items-center gap-2">
                    <div
                      className={`w-3 h-3 rounded-full ${getSeverityColor(privileges.privilege_score)}`}
                    />
                    <span className="font-bold">{privileges.privilege_score}</span>
                  </div>
                </div>
              </div>
              <div className="space-y-4">
                <div>
                  <h4 className="text-sm font-medium text-gray-400 mb-2">Roles</h4>
                  <div className="flex flex-wrap gap-2">
                    {privileges.roles.map(role => (
                      <Badge key={role} className="border border-gray-600 flex items-center gap-1">
                        <Lock className="w-3 h-3" />
                        {role}
                      </Badge>
                    ))}
                  </div>
                </div>
                <hr className="my-4 border-slate-700" />
                <div>
                  <h4 className="text-sm font-medium text-gray-400 mb-2">Groups</h4>
                  <div className="flex flex-wrap gap-2">
                    {privileges.groups.map(group => (
                      <Badge key={group} className="border border-gray-600 flex items-center gap-1">
                        <Users className="w-3 h-3" />
                        {group}
                      </Badge>
                    ))}
                  </div>
                </div>
                <hr className="my-4 border-slate-700" />
                <div>
                  <h4 className="text-sm font-medium text-gray-400 mb-2">Effective Permissions</h4>
                  <div className="h-48 border border-slate-700 rounded-md p-3 overflow-y-auto">
                    <ul className="space-y-1">
                      {privileges.effective_permissions.map((perm, i) => (
                        <li key={i} className="text-sm text-gray-300">• {perm}</li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          )}
          {anomaly && (
            <div className="bg-slate-800 border border-slate-700 text-white rounded-lg p-6">
              <h3 className="text-lg font-semibold flex items-center gap-2 mb-6">
                <Activity className="w-5 h-5" />
                Activity Anomaly Detection
              </h3>
              <div className="space-y-4">
                <div className="flex items-center gap-3">
                  <p className="text-sm text-gray-400">Anomaly Status:</p>
                  <Badge className={anomaly.is_anomaly ? "bg-red-600" : "bg-green-600"}>
                    {anomaly.is_anomaly ? "Detected" : "Not Detected"}
                  </Badge>
                </div>
                <div>
                  <p className="text-sm text-gray-400 mb-2">Features:</p>
                  <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
                    <div className="bg-slate-900 p-3 rounded-md">
                      <p className="text-xs text-gray-400">Login Count</p>
                      <p className="text-lg font-bold">{anomaly.features.login_count}</p>
                    </div>
                    <div className="bg-slate-900 p-3 rounded-md">
                      <p className="text-xs text-gray-400">Platforms</p>
                      <p className="text-lg font-bold">{anomaly.features.platform_count}</p>
                    </div>
                    <div className="bg-slate-900 p-3 rounded-md">
                      <p className="text-xs text-gray-400">Resources</p>
                      <p className="text-lg font-bold">{anomaly.features.resource_count}</p>
                    </div>
                    <div className="bg-slate-900 p-3 rounded-md">
                      <p className="text-xs text-gray-400">Countries</p>
                      <p className="text-lg font-bold">{anomaly.features.country_count}</p>
                    </div>
                    <div className="bg-slate-900 p-3 rounded-md">
                      <p className="text-xs text-gray-400">Hour Variance</p>
                      <p className="text-lg font-bold">{anomaly.features.hour_variance.toFixed(2)}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
