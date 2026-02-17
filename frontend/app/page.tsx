"use client";

import { useState } from "react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';

export default function Home() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const [formData, setFormData] = useState({
    grid: 55,
    diesel: 45,
    production_output: 25000,
    energy_intensity_kwh_per_unit: 0.5,
    distance_km: 1500,
    fuel_liters: 150,
    reported_co2_tons: 2.5,
    sustainability_claim: "We will achieve Net Zero by 2028 through efficiency gains.",
  });

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: name === "sustainability_claim" ? value : Number(value),
    }));
  };

  const runAudit = async () => {
    setLoading(true);
    setError(null);
    setResult(null);

    const payload = {
      energy_mix: {
        grid: formData.grid,
        diesel: formData.diesel,
      },
      production_output: formData.production_output,
      energy_intensity_kwh_per_unit: formData.energy_intensity_kwh_per_unit,
      transport: {
        distance_km: formData.distance_km,
        fuel_liters: formData.fuel_liters,
      },
      reported_co2_tons: formData.reported_co2_tons,
      sustainability_claim: formData.sustainability_claim,
    };

    try {
      const response = await fetch("http://127.0.0.1:8000/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error(`Server error: ${response.statusText}`);
      }

      const data = await response.json();
      setResult(data);
    } catch (err: any) {
      setError(err.message || "Failed to connect to the audit engine.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 p-8 text-slate-900">
      <div className="max-w-7xl mx-auto space-y-8">
        
        <header className="border-b border-slate-200 pb-4">
          <h1 className="text-3xl font-bold text-slate-900 tracking-tight">nz sim</h1>
          <p className="text-slate-500 mt-2">net-zero scenario auditor</p>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          
          <div className="lg:col-span-4 space-y-6">
            <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200 sticky top-8">
              <h2 className="text-lg font-semibold mb-4 text-slate-800">Operational Data</h2>
              
              <div className="space-y-4 text-sm">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-slate-600 mb-1">Grid Energy (%)</label>
                    <input type="number" name="grid" value={formData.grid} onChange={handleInputChange} className="w-full p-2 border border-slate-300 rounded-md bg-slate-50" />
                  </div>
                  <div>
                    <label className="block text-slate-600 mb-1">Diesel Energy (%)</label>
                    <input type="number" name="diesel" value={formData.diesel} onChange={handleInputChange} className="w-full p-2 border border-slate-300 rounded-md bg-slate-50" />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-slate-600 mb-1">Production (Units)</label>
                    <input type="number" name="production_output" value={formData.production_output} onChange={handleInputChange} className="w-full p-2 border border-slate-300 rounded-md bg-slate-50" />
                  </div>
                  <div>
                    <label className="block text-slate-600 mb-1">Intensity (kWh/Unit)</label>
                    <input type="number" step="0.1" name="energy_intensity_kwh_per_unit" value={formData.energy_intensity_kwh_per_unit} onChange={handleInputChange} className="w-full p-2 border border-slate-300 rounded-md bg-slate-50" />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-slate-600 mb-1">Transport (km)</label>
                    <input type="number" name="distance_km" value={formData.distance_km} onChange={handleInputChange} className="w-full p-2 border border-slate-300 rounded-md bg-slate-50" />
                  </div>
                  <div>
                    <label className="block text-slate-600 mb-1">Fuel Used (Liters)</label>
                    <input type="number" name="fuel_liters" value={formData.fuel_liters} onChange={handleInputChange} className="w-full p-2 border border-slate-300 rounded-md bg-slate-50" />
                  </div>
                </div>

                <div>
                  <label className="block text-slate-600 mb-1">Reported CO2 (Tons)</label>
                  <input type="number" step="0.1" name="reported_co2_tons" value={formData.reported_co2_tons} onChange={handleInputChange} className="w-full p-2 border border-slate-300 rounded-md bg-slate-50 font-semibold text-blue-700" />
                </div>

                <div>
                  <label className="block text-slate-600 mb-1">Public Sustainability Claim</label>
                  <textarea name="sustainability_claim" value={formData.sustainability_claim} onChange={handleInputChange} rows={3} className="w-full p-2 border border-slate-300 rounded-md bg-slate-50 resize-none" />
                </div>

                <button 
                  onClick={runAudit}
                  disabled={loading}
                  className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 rounded-lg transition-colors disabled:bg-blue-300"
                >
                  {loading ? "Running K2 Agent Chain..." : "Run AI Audit"}
                </button>
              </div>
            </div>
          </div>

          <div className="lg:col-span-8">
            {error && (
              <div className="bg-red-50 border border-red-200 text-red-700 p-4 rounded-xl mb-6">
                <strong>Error:</strong> {error}
              </div>
            )}

            {loading && (
              <div className="flex flex-col items-center justify-center h-64 border-2 border-dashed border-slate-200 rounded-xl bg-slate-50">
                <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-blue-600 mb-4"></div>
                <p className="text-slate-500 font-medium animate-pulse">K2 Multi-Agent Engine computing...</p>
              </div>
            )}

            {result && !loading && (
              <div className="space-y-6">
                
                <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
                  <h2 className="text-xl font-bold mb-4 text-slate-900 border-b pb-2">Executive Summary</h2>
                  <div className="space-y-4 text-slate-700 leading-relaxed text-sm">
                    {result.executive_summary ? (
                      result.executive_summary.split('\n').map((paragraph: string, idx: number) => (
                        paragraph.trim() && <p key={idx}>{paragraph}</p>
                      ))
                    ) : (
                      <p className="text-red-500 font-medium">Executive summary not generated. Check backend Layer 5.</p>
                    )}
                  </div>
                </div>

                <div className="grid grid-cols-3 gap-4">
                  <div className="bg-white p-4 rounded-xl shadow-sm border border-slate-200 text-center">
                    <p className="text-xs text-slate-500 uppercase tracking-wider font-semibold">True Baseline</p>
                    <p className="text-2xl font-bold text-slate-900 mt-1">{result.baseline.baseline_co2_tons.toFixed(2)} t</p>
                  </div>
                  <div className="bg-white p-4 rounded-xl shadow-sm border border-slate-200 text-center">
                    <p className="text-xs text-slate-500 uppercase tracking-wider font-semibold">Reported Claim</p>
                    <p className="text-2xl font-bold text-blue-600 mt-1">{result.baseline.reported_co2_tons.toFixed(2)} t</p>
                  </div>
                  <div className="bg-red-50 p-4 rounded-xl shadow-sm border border-red-200 text-center">
                    <p className="text-xs text-red-600 uppercase tracking-wider font-semibold">Unexplained Gap</p>
                    <p className="text-2xl font-bold text-red-700 mt-1">{result.baseline.delta_tons.toFixed(2)} t</p>
                  </div>
                </div>

                <div className={`p-6 rounded-xl shadow-sm border ${result.strategic_feasibility.claim_assessment.is_claim_realistic ? 'bg-green-50 border-green-200' : 'bg-orange-50 border-orange-200'}`}>
                  <div className="flex items-center gap-3 mb-2">
                    <div className={`w-3 h-3 rounded-full ${result.strategic_feasibility.claim_assessment.is_claim_realistic ? 'bg-green-500' : 'bg-orange-500'}`}></div>
                    <h2 className="text-lg font-bold text-slate-900">Claim Reality Check</h2>
                  </div>
                  <p className="text-sm text-slate-800 font-medium mb-2">
                    Verdict: {result.strategic_feasibility.claim_assessment.is_claim_realistic ? "Plausible" : "Unrealistic"}
                  </p>
                  <p className="text-sm text-slate-700">
                    {result.strategic_feasibility.claim_assessment.critique}
                  </p>
                </div>

                <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
                  <h2 className="text-sm font-bold text-slate-900 uppercase tracking-wider mb-6 border-b pb-2">Simulation Impact Analysis</h2>
                  <div className="h-72 w-full">
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart
                        data={[
                          {
                            name: 'True Baseline',
                            emissions: result.baseline.baseline_co2_tons,
                          },
                          ...result.counterfactual_simulation.scenarios.map((s: any) => ({
                            name: s.name,
                            emissions: s.estimated_new_co2_tons,
                          }))
                        ]}
                        margin={{ top: 20, right: 30, left: 0, bottom: 5 }}
                      >
                        <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
                        <XAxis 
                          dataKey="name" 
                          axisLine={false} 
                          tickLine={false} 
                          tick={{ fill: '#64748b', fontSize: 11 }} 
                          width={150}
                        />
                        <YAxis 
                          axisLine={false} 
                          tickLine={false} 
                          tick={{ fill: '#64748b', fontSize: 12 }}
                        />
                        <Tooltip 
                          cursor={{ fill: '#f8fafc' }}
                          contentStyle={{ borderRadius: '8px', border: '1px solid #e2e8f0', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                        />
                        <Bar dataKey="emissions" radius={[4, 4, 0, 0]} maxBarSize={60}>
                          {
                            [
                              { name: 'Original Baseline', color: '#ef4444' },
                              ...result.counterfactual_simulation.scenarios
                            ].map((entry: any, index: number) => (
                              <Cell key={`cell-${index}`} fill={index === 0 ? '#ef4444' : '#10b981'} />
                            ))
                          }
                        </Bar>
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                </div>

                <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
                  <h3 className="text-sm font-bold text-slate-900 uppercase tracking-wider mb-4 flex justify-between items-center">
                    <span>Identified Carbon Leakage & Inconsistencies</span>
                    <span className="text-red-500 bg-red-50 px-3 py-1 rounded-full border border-red-200">
                      Risk Score: {result.leak_detection.leakage_risk_score}/100
                    </span>
                  </h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <h4 className="text-xs font-bold text-slate-500 uppercase mb-2">Scope Gaps</h4>
                      <ul className="space-y-2">
                        {result.leak_detection.scope_gaps.slice(0, 4).map((gap: string, i: number) => (
                          <li key={i} className="text-sm text-slate-600 flex gap-2 items-start">
                            <span className="text-orange-500 shrink-0 mt-0.5">⚠️</span>
                            {gap}
                          </li>
                        ))}
                      </ul>
                    </div>
                    <div>
                      <h4 className="text-xs font-bold text-slate-500 uppercase mb-2">Potential Leaks</h4>
                      <ul className="space-y-2">
                        {result.leak_detection.potential_leaks.slice(0, 4).map((leak: string, i: number) => (
                          <li key={i} className="text-sm text-slate-600 flex gap-2 items-start">
                            <span className="text-red-500 shrink-0 mt-0.5">🚨</span>
                            {leak}
                          </li>
                        ))}
                      </ul>
                    </div>
                  </div>
                </div>

                <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200 overflow-hidden">
                  <h3 className="text-sm font-bold text-slate-900 uppercase tracking-wider mb-4">
                    Mitigation Implementation Roadmap
                  </h3>
                  <div className="overflow-x-auto">
                    <table className="w-full text-sm text-left">
                      <thead className="bg-slate-50 text-slate-600 font-medium border-b border-slate-200">
                        <tr>
                          <th className="py-3 px-4 font-semibold">Scenario Path</th>
                          <th className="py-3 px-4 font-semibold">Timeline</th>
                          <th className="py-3 px-4 font-semibold">Risk Level</th>
                          <th className="py-3 px-4 font-semibold">Primary Business Barrier</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-slate-100">
                        {result.strategic_feasibility.business_feasibility_ranking.map((rank: any, i: number) => (
                          <tr key={i} className="hover:bg-slate-50 transition-colors">
                            <td className="py-3 px-4 font-medium text-slate-800">{rank.scenario_name}</td>
                            <td className="py-3 px-4 text-slate-600 whitespace-nowrap">{rank.estimated_timeline_months} months</td>
                            <td className="py-3 px-4">
                              <span className={`px-2 py-1 rounded text-xs font-bold ${
                                rank.risk_level.toLowerCase() === 'high' ? 'bg-red-100 text-red-700 border border-red-200' :
                                rank.risk_level.toLowerCase() === 'medium' ? 'bg-orange-100 text-orange-700 border border-orange-200' :
                                'bg-green-100 text-green-700 border border-green-200'
                              }`}>
                                {rank.risk_level.toUpperCase()}
                              </span>
                            </td>
                            <td className="py-3 px-4 text-slate-600">{rank.primary_business_barrier}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>

              </div>
            )}

            {!result && !loading && !error && (
              <div className="flex flex-col items-center justify-center h-full min-h-100 border-2 border-dashed border-slate-200 rounded-xl bg-white text-slate-400">
                <svg className="w-16 h-16 mb-4 text-slate-300" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
                <p className="font-medium text-slate-500">Awaiting operational inputs</p>
                <p className="text-sm mt-1">Adjust parameters on the left and click "Run AI Audit" to begin</p>
              </div>
            )}

          </div>
        </div>
      </div>
    </div>
  );
}