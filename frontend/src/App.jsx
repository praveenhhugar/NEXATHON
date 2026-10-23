import { useState, useEffect } from 'react';

export default function App() {
  const [risk, setRisk] = useState(0);
  const [intent, setIntent] = useState("normal");
  const [activeDecoy, setActiveDecoy] = useState(null);
  const [honeytokenFired, setHoneytokenFired] = useState(false);
  
  // New Firewall States
  const [firewallStatus, setFirewallStatus] = useState("MONITORING");
  const [blockedIps, setBlockedIps] = useState([]);
  
  // The timeline feed
  const [feed, setFeed] = useState([
    { type: "system", text: "System initialized. Sandbox environment ready." }
  ]);

  // --- LIVE BACKEND POLLING ---
  useEffect(() => {
    const interval = setInterval(async () => {
      try {
        // Make sure we are fetching from /api/state
        const res = await fetch('http://127.0.0.1:8000/api/state');
        const data = await res.json();
        
        setRisk(data.risk);
        setIntent(data.intent);
        if (data.active_decoy) setActiveDecoy(data.active_decoy);
        if (data.honeytoken_hit && !honeytokenFired) setHoneytokenFired(true);

        // Update Firewall Data
        if (data.firewall_status) setFirewallStatus(data.firewall_status);
        if (data.blocked_ips) setBlockedIps(data.blocked_ips);
        
      } catch (err) {
        // Ignore errors if backend is restarting
      }
    }, 1000);
    return () => clearInterval(interval);
  }, [honeytokenFired]);

  const resetDemo = async () => {
    try {
      await fetch('http://127.0.0.1:8000/api/reset', { method: 'POST' });
    } catch (e) {}
    
    setRisk(0);
    setIntent("normal");
    setActiveDecoy(null);
    setHoneytokenFired(false);
    setFirewallStatus("MONITORING");
    setFeed([{ type: "system", text: "System reset. Ready." }]);
  };

  // --- ANIMATED SEMI-CIRCLE GAUGE ---
  const Radius = 80;
  const Circumference = Math.PI * Radius; 
  const StrokeDashoffset = Circumference - (risk / 100) * Circumference;

  return (
    <div className="min-h-screen p-8 font-sans bg-[#0B0F19] text-slate-200 overflow-hidden relative selection:bg-purple-500/30">
      
      <div className="absolute top-0 left-1/4 w-96 h-96 bg-purple-600/20 rounded-full blur-[120px] pointer-events-none"></div>
      <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-blue-600/20 rounded-full blur-[120px] pointer-events-none"></div>

      {/* HONEYTOKEN ALERT MODAL */}
      {honeytokenFired && (
        <div className="fixed inset-0 bg-[#0B0F19]/90 flex items-center justify-center z-50 backdrop-blur-lg">
          <div className="bg-gradient-to-b from-red-900/40 to-[#0B0F19] border border-red-500/50 p-12 rounded-3xl shadow-[0_0_80px_rgba(239,68,68,0.3)] text-center animate-[pulse_2s_ease-in-out_infinite]">
            <h1 className="text-5xl font-black text-transparent bg-clip-text bg-gradient-to-r from-red-400 to-orange-400 mb-4 tracking-widest drop-shadow-[0_0_15px_rgba(239,68,68,0.8)]">
              HONEYTOKEN TRIGGERED
            </h1>
            <p className="text-xl text-red-200 mb-8 font-mono tracking-widest">ENGAGEMENT CONFIRMED</p>
            <button onClick={resetDemo} className="bg-red-500 hover:bg-red-400 text-white font-bold py-3 px-8 rounded-full uppercase tracking-widest transition-all shadow-[0_0_20px_rgba(239,68,68,0.6)]">
              Reset System
            </button>
          </div>
        </div>
      )}

      {/* HEADER */}
      <header className="relative flex justify-between items-center mb-8 z-10">
        <div>
          <h1 className="text-4xl font-bold tracking-tight text-white mb-2">
            DECEPTOR <span className="text-transparent bg-clip-text bg-gradient-to-r from-orange-400 to-red-500">AI</span>
          </h1>
          <p className="text-slate-400 text-sm">Every attack teaches the defense how to deceive better.</p>
        </div>
        <div className="flex gap-4">
          <button onClick={resetDemo} className="border border-slate-700 hover:bg-slate-800 text-slate-300 font-bold py-3 px-8 rounded-full transition-all">
            Reset
          </button>
        </div>
      </header>

      {/* MAIN GRID */}
      <div className="relative grid grid-cols-1 lg:grid-cols-12 gap-6 z-10">
        
        {/* LEFT: TIMELINE FEED */}
        <div className="lg:col-span-7 bg-[#111827]/80 border border-slate-800 rounded-3xl p-6 shadow-2xl backdrop-blur-md h-[75vh] flex flex-col">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-lg font-semibold text-slate-200">Simulation Timeline</h2>
            <span className="text-xs font-mono text-emerald-400 bg-emerald-400/10 px-3 py-1 rounded-full border border-emerald-400/20">LIVE SANDBOX</span>
          </div>
          
          <div className="flex-1 overflow-y-auto space-y-4 font-mono text-sm pr-4 custom-scrollbar">
            {feed.map((item, index) => {
              let textColor = "text-slate-400";
              if (item.type === "attacker") textColor = "text-pink-400";
              if (item.type === "observer") textColor = "text-cyan-400";
              
              return (
                <div key={index} className="flex gap-4">
                  <span className="text-slate-600 text-xs w-12 pt-1">14:0{index}</span>
                  <div className={`${textColor} flex-1 border-b border-slate-800/50 pb-2`}>
                    {item.type !== 'system' && <span className="opacity-50 mr-2">[{item.type.toUpperCase()}]</span>}
                    {item.text}
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* RIGHT SIDE */}
        <div className="lg:col-span-5 flex flex-col gap-6">
          
          {/* DEFENDER GAUGE */}
          <div className="bg-[#111827]/80 border border-slate-800 rounded-3xl p-6 shadow-2xl backdrop-blur-md flex flex-col items-center justify-center relative overflow-hidden">
             <div className="absolute top-0 w-full h-1 bg-gradient-to-r from-purple-500 to-pink-500"></div>
             <h2 className="text-sm font-semibold text-slate-400 mb-4 w-full text-left">Defender View</h2>
             
             <div className="relative w-64 h-32 flex justify-center overflow-hidden mt-4">
                <svg viewBox="0 0 200 100" className="w-full h-full overflow-visible">
                  <path d="M 20 100 A 80 80 0 0 1 180 100" fill="none" stroke="#1e293b" strokeWidth="12" strokeLinecap="round" />
                  <path 
                    d="M 20 100 A 80 80 0 0 1 180 100" 
                    fill="none" 
                    stroke={risk > 70 ? "#ef4444" : (risk > 30 ? "#f59e0b" : "#10b981")} 
                    strokeWidth="12" 
                    strokeLinecap="round"
                    strokeDasharray={Circumference}
                    strokeDashoffset={StrokeDashoffset}
                    className="transition-all duration-1000 ease-out"
                  />
                </svg>
                <div className="absolute bottom-0 flex flex-col items-center">
                  <span className="text-5xl font-bold text-white tracking-tighter">{risk}</span>
                  <span className="text-xs text-slate-500 uppercase tracking-widest mt-1">Risk Score</span>
                </div>
             </div>

             <div className="w-full grid grid-cols-2 gap-4 mt-6">
                <div className="bg-slate-900/50 p-3 rounded-xl border border-slate-800">
                  <p className="text-[10px] text-slate-500 uppercase tracking-wider mb-1">Inferred Intent</p>
                  <p className={`text-sm font-mono font-bold ${intent !== 'normal' ? 'text-cyan-400' : 'text-slate-400'}`}>{intent}</p>
                </div>
                <div className="bg-slate-900/50 p-3 rounded-xl border border-slate-800">
                  <p className="text-[10px] text-slate-500 uppercase tracking-wider mb-1">Active Decoy</p>
                  <p className={`text-sm font-mono font-bold ${activeDecoy ? 'text-purple-400' : 'text-slate-400'}`}>{activeDecoy || "None"}</p>
                </div>
             </div>
          </div>

          {/* FIREWALL MONITOR */}
          <div className="bg-[#111827]/80 border border-slate-800 rounded-3xl p-6 shadow-2xl backdrop-blur-md">
            <h2 className="text-sm font-semibold text-slate-400 mb-4">Firewall Monitor</h2>
            <div className="mb-4">
              <p className="text-xs text-slate-500 mb-2">Current Status:</p>
              <span className={`px-3 py-1 rounded-full text-xs font-bold ${
                firewallStatus.includes("BLOCKED") ? "bg-red-500/20 text-red-400" : 
                firewallStatus.includes("DECEIVED") ? "bg-purple-500/20 text-purple-400" : 
                "bg-emerald-500/20 text-emerald-400"
              }`}>
                {firewallStatus}
              </span>
            </div>
            <div>
              <p className="text-xs text-slate-500 mb-2">Blocked IPs:</p>
              <ul className="text-sm font-mono text-red-400">
                {blockedIps?.map((ip, i) => <li key={i}>⛔ {ip}</li>)}
              </ul>
            </div>
          </div>

        </div>
      </div>
    </div>
  );
}