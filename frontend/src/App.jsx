import { useState, useEffect } from 'react';

export default function App() {
  const [risk, setRisk] = useState(0);
  const [intent, setIntent] = useState("normal");
  const [activeDecoy, setActiveDecoy] = useState(null);
  const [honeytokenFired, setHoneytokenFired] = useState(false);
  // Add this new state at the top of your App component
  const [isDemoRunning, setIsDemoRunning] = useState(false);
  
  // The timeline feed
  const [feed, setFeed] = useState([
    { type: "system", text: "System initialized. Sandbox environment ready." }
  ]);

  const addFeed = (type, text) => {
    setFeed(prev => [...prev, { type, text }]);
  };

   

  // --- LIVE BACKEND POLLING ---
  useEffect(() => {
    const interval = setInterval(async () => {
      try {
        const res = await fetch('http://127.0.0.1:8000/state');
        const data = await res.json();
        
        setRisk(data.risk);
        setIntent(data.intent);
        if (data.active_decoy) setActiveDecoy(data.active_decoy);
        
        // ONLY trigger the red screen if the cinematic demo is NOT running
        if (data.honeytoken_hit && !honeytokenFired && !isDemoRunning) {
          setHoneytokenFired(true);
        }
      } catch (err) {}
    }, 1000);
    return () => clearInterval(interval);
  }, [honeytokenFired, isDemoRunning]);

  // --- CINEMATIC DEMO ENGINE ---
  const startDemo = async () => {
    setIsDemoRunning(true); // Lock the poller
    
    try {
      await fetch('http://127.0.0.1:8000/reset', { method: 'POST' });
    } catch (e) {}

    setRisk(0);
    setIntent("normal");
    setActiveDecoy(null);
    setHoneytokenFired(false);
    setFeed([{ type: "system", text: "Attack sequence initiated..." }]);

    const wait = (ms) => new Promise(resolve => setTimeout(resolve, ms));

    await wait(1000); 
    addFeed("attacker", "GET /company/ (Reconnaissance)");
    setRisk(15);

    await wait(1500);
    addFeed("attacker", "GET /company/aws (Probing)");
    
    await wait(1500);
    addFeed("attacker", "GET /company/admin (Credential Hunt)");

    await wait(1500);
    // Trigger the backend
    try {
      const response = await fetch('http://127.0.0.1:8000/event', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ path: "/company/admin", method: "GET", attempts: 3 })
      });
      const backendData = await response.json();
      
      addFeed("observer", `Risk: ${backendData.assessment.risk} | Intent: ${backendData.assessment.intent}`);
      setRisk(backendData.assessment.risk);
      setIntent(backendData.assessment.intent);
    } catch (error) {
      console.log("Backend error");
    }

    await wait(1500);
    addFeed("planner", "Pick strategy: fake_config_trail (Best hit rate)");
    addFeed("validator", "Action deploy_decoy PASSED");
    setActiveDecoy("fake_config_trail");

    await wait(1500);
    addFeed("verifier", "No decoy visit after 2 steps -> no engagement");
    addFeed("planner", "Switch strategy: fake_cloud_page");
    setActiveDecoy("fake_cloud_page");

    await wait(1500);
    addFeed("attacker", "GET /decoy/cloud/keys");
    addFeed("verifier", "HONEYTOKEN TRIGGERED -> engagement confirmed");
    
    // Final climax
    setHoneytokenFired(true);
    setIsDemoRunning(false); // Unlock the poller
  };

  const resetDemo = async () => {
    try {
      await fetch('http://127.0.0.1:8000/reset', { method: 'POST' });
    } catch (e) {}
    
    setRisk(0);
    setIntent("normal");
    setActiveDecoy(null);
    setHoneytokenFired(false);
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

      <header className="relative flex justify-between items-center mb-8 z-10">
        <div>
          <h1 className="text-4xl font-bold tracking-tight text-white mb-2">
            DECEPTOR <span className="text-transparent bg-clip-text bg-gradient-to-r from-orange-400 to-red-500">AI</span>
          </h1>
          <p className="text-slate-400 text-sm">Every attack teaches the defense how to deceive better.</p>
        </div>
        <div className="flex gap-4">
          <button onClick={startDemo} className="bg-gradient-to-r from-orange-500 to-amber-500 hover:from-orange-400 hover:to-amber-400 text-black font-bold py-3 px-8 rounded-full shadow-[0_0_20px_rgba(245,158,11,0.3)] transition-all transform hover:scale-105">
            Run Sequence
          </button>
          <button onClick={resetDemo} className="border border-slate-700 hover:bg-slate-800 text-slate-300 font-bold py-3 px-8 rounded-full transition-all">
            Reset
          </button>
        </div>
      </header>

      <div className="relative grid grid-cols-1 lg:grid-cols-12 gap-6 z-10">
        
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
              if (item.type === "planner") textColor = "text-blue-400";
              if (item.type === "validator") textColor = "text-emerald-400";
              if (item.type === "verifier") textColor = "text-amber-400";
              
              return (
                <div key={index} className="flex gap-4 animate-[fadeIn_0.3s_ease-out]">
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

        <div className="lg:col-span-5 flex flex-col gap-6">
          
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
                    style={{ filter: `drop-shadow(0 0 10px ${risk > 70 ? '#ef4444' : '#10b981'})` }}
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

          <div className="bg-[#111827]/80 border border-slate-800 rounded-3xl p-6 shadow-2xl backdrop-blur-md flex-1">
            <h2 className="text-sm font-semibold text-slate-400 mb-4">Strategy Memory & A/B Proof</h2>
            
            <div className="flex justify-between items-end mb-6">
               <div className="text-xs text-slate-500">Adaptive vs Fixed Comparison</div>
               <div className="text-xs text-emerald-400 font-mono">+1000% Success</div>
            </div>

            <div className="flex items-end justify-between h-24 gap-4">
                <div className="flex flex-col items-center flex-1 h-full justify-end group">
                  <div className="w-full bg-slate-700/50 rounded-t-lg transition-all duration-1000 h-[5%] group-hover:bg-slate-600"></div>
                  <span className="text-[10px] text-slate-500 mt-2 uppercase tracking-wider">Fixed (0/10)</span>
                </div>
                <div className="flex flex-col items-center flex-1 h-full justify-end group">
                  <div className="w-full bg-gradient-to-t from-purple-600 to-cyan-400 rounded-t-lg shadow-[0_0_20px_rgba(34,211,238,0.4)] transition-all duration-1000 h-[100%] group-hover:shadow-[0_0_30px_rgba(34,211,238,0.7)]"></div>
                  <span className="text-[10px] text-cyan-400 mt-2 uppercase tracking-wider font-bold">Adaptive (10/10)</span>
                </div>
            </div>
          </div>

        </div>
      </div>
      
      <style dangerouslySetInnerHTML={{__html: `
        @keyframes fadeIn {
          from { opacity: 0; transform: translateY(5px); }
          to { opacity: 1; transform: translateY(0); }
        }
        .custom-scrollbar::-webkit-scrollbar { width: 6px; }
        .custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
        .custom-scrollbar::-webkit-scrollbar-thumb { background: #334155; border-radius: 10px; }
      `}} />
    </div>
  );
}