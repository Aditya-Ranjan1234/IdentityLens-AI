"use client";
import { useState, useEffect } from "react";
import Link from "next/link";

type User = {
  user_id: string;
  name: string;
  email: string;
  department: string;
  title: string;
  status: string;
  platforms: Record<string, any>;
};

export default function Dashboard() {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://localhost:8000/api/users")
      .then((res) => res.json())
      .then((data) => {
        setUsers(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  const counts = {
    total: users.length,
    active: users.filter(u => u.status === "ACTIVE").length,
    inactive: users.filter(u => u.status === "INACTIVE").length,
  };

  return (
    <div className="min-h-screen p-8">
      <div className="max-w-7xl mx-auto">
        <div className="flex items-center justify-between mb-8">
          <h1 className="text-4xl font-bold">Executive Dashboard</h1>
          <Link href="/" className="text-purple-300 hover:text-purple-100">← Back to Home</Link>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white/10 backdrop-blur rounded-2xl p-6 border border-white/20">
            <div className="text-4xl font-extrabold text-purple-400">{counts.total}</div>
            <div className="text-gray-300">Total Identities</div>
          </div>
          <div className="bg-white/10 backdrop-blur rounded-2xl p-6 border border-white/20">
            <div className="text-4xl font-extrabold text-green-400">{counts.active}</div>
            <div className="text-gray-300">Active Users</div>
          </div>
          <div className="bg-white/10 backdrop-blur rounded-2xl p-6 border border-white/20">
            <div className="text-4xl font-extrabold text-red-400">{counts.inactive}</div>
            <div className="text-gray-300">Inactive Users</div>
          </div>
        </div>
        
        <div className="bg-white/10 backdrop-blur rounded-2xl border border-white/20 overflow-hidden">
          <div className="p-6 border-b border-white/20">
            <h2 className="text-2xl font-semibold">All Identities</h2>
            <p className="text-sm text-gray-300 mt-1">Click a user to view their identity details</p>
          </div>
          <div className="overflow-x-auto">
            {loading ? (
              <div className="p-12 text-center">Loading...</div>
            ) : (
              <table className="w-full text-left">
                <thead className="bg-white/5">
                  <tr>
                    <th className="p-4 font-semibold">ID</th>
                    <th className="p-4 font-semibold">Name</th>
                    <th className="p-4 font-semibold">Department</th>
                    <th className="p-4 font-semibold">Status</th>
                    <th className="p-4 font-semibold">Platforms</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-white/10">
                  {users.slice(0, 50).map((user) => (
                    <Link href={`/identity/${user.user_id}`} key={user.user_id}>
                    <tr key={user.user_id} className="hover:bg-white/5 cursor-pointer">
                      <td className="p-4">{user.user_id}</td>
                      <td className="p-4 font-medium">{user.name}</td>
                      <td className="p-4">{user.department}</td>
                      <td className="p-4">
                        <span className={`px-3 py-1 rounded-full text-xs font-bold ${user.status === "ACTIVE" ? "bg-green-500/20 text-green-300" : "bg-red-500/20 text-red-300"}`}>
                          {user.status}
                        </span>
                      </td>
                      <td className="p-4">{Object.keys(user.platforms).join(", ")}</td>
                    </tr>
                    </Link>
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
