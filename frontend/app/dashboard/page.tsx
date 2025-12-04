"use client";

import { useEffect, useState } from "react";
import axios from "axios";
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer
} from "recharts";

export default function Dashboard() {
  const [nsCost, setNsCost] = useState<any>(null);
  const [podCosts, setPodCosts] = useState<any[]>([]);

  useEffect(() => {
    const fetchData = () => {
      axios.get("http://127.0.0.1:8080/namespaces/cost")
        .then(res => setNsCost(res.data))
        .catch(err => console.error(err));

      axios.get("http://127.0.0.1:8080/pods/cost")
        .then(res => setPodCosts(res.data.costs))
        .catch(err => console.error(err));
    };

    fetchData();
    const interval = setInterval(fetchData, 10000);
    return () => clearInterval(interval);
  }, []);

  if (!nsCost) return <div className="p-10 text-white">Yükleniyor...</div>;

  const chartData = Object.entries(nsCost).map(([ns, values]: any) => ({
    namespace: ns,
    cost: values.total_cost_per_hour
  }));

  const totalClusterCost = chartData
    .reduce((acc, item) => acc + item.cost, 0)
    .toFixed(6);

  return (
    <div className="p-10 space-y-10 bg-[#0f0f0f] min-h-screen text-[#e5e5e5]">

      {/* HEADER */}
      <h1 className="text-4xl font-bold tracking-wide">Cluster Maliyet Dashboard</h1>

      {/* TOTAL COST CARD */}
      <div className="text-2xl bg-[#1e1e1e] p-5 rounded-lg shadow-md inline-block border border-[#333]">
        Toplam Cluster Saatlik Maliyet:
        <span className="font-bold text-green-400"> ${totalClusterCost}</span>
      </div>

      {/* NAMESPACE COST GRAPH */}
      <div className="bg-[#1a1a1a] p-6 shadow-xl rounded-lg border border-[#333]">
        <h2 className="text-2xl mb-4 font-semibold text-[#f0f0f0]">Namespace Bazlı Maliyetler</h2>

        <div className="w-full h-80">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={chartData}>
              <XAxis
                dataKey="namespace"
                stroke="#cfcfcf"
                tick={{ fill: "#cfcfcf", fontSize: 13 }}
              />
              <YAxis
                stroke="#cfcfcf"
                tick={{ fill: "#cfcfcf", fontSize: 13 }}
              />
              <Tooltip
                contentStyle={{
                  backgroundColor: "#1e1e1e",
                  border: "1px solid #444",
                  borderRadius: "6px",
                  color: "#fff"
                }}
                labelStyle={{ color: "#fff" }}
                itemStyle={{ color: "#fff" }}
              />
              <Bar dataKey="cost" fill="#818cf8" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* POD TABLE */}
      <div className="bg-[#1a1a1a] p-6 shadow-xl rounded-lg border border-[#333]">
        <h2 className="text-2xl mb-4 font-semibold text-[#f0f0f0]">Pod Bazlı Maliyetler</h2>

        <table className="w-full border-collapse text-[#e5e5e5]">
          <thead>
            <tr className="bg-[#2a2a2a] text-left font-semibold">
              <th className="p-3 border border-[#333]">Namespace</th>
              <th className="p-3 border border-[#333]">Pod</th>
              <th className="p-3 border border-[#333]">CPU (cores)</th>
              <th className="p-3 border border-[#333]">Memory (GB)</th>
              <th className="p-3 border border-[#333]">Saatlik Maliyet ($)</th>
            </tr>
          </thead>

          <tbody>
            {podCosts.map((pod, i) => (
              <tr key={i} className="hover:bg-[#2a2a2a] transition">
                <td className="p-3 border border-[#333]">{pod.namespace}</td>
                <td className="p-3 border border-[#333]">{pod.pod}</td>
                <td className="p-3 border border-[#333]">{pod.cpu_cores.toFixed(4)}</td>
                <td className="p-3 border border-[#333]">{pod.memory_gb.toFixed(4)}</td>
                <td className="p-3 border border-[#333] font-bold text-indigo-400">
                  ${pod.total_cost_per_hour.toFixed(6)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

    </div>
  );
}
