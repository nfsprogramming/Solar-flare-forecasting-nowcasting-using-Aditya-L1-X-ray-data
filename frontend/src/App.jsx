import { useState, useEffect, useRef } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts';
import { Activity, AlertTriangle, ShieldCheck } from 'lucide-react';
import './index.css';

function App() {
  const [data, setData] = useState([]);
  const [prediction, setPrediction] = useState({ probability: 0, severity: "System Standby", color: "#66fcf1" });
  const [isSimulating, setIsSimulating] = useState(false);
  const [backendStatus, setBackendStatus] = useState("Checking...");
  const [sensor, setSensor] = useState('hel1os');
  const dataQueue = useRef([]);
  const intervalRef = useRef(null);

  // Check backend health
  useEffect(() => {
    fetch('http://127.0.0.1:8000/')
      .then(res => res.json())
      .then(data => setBackendStatus(data.status))
      .catch(() => setBackendStatus("Offline"));
  }, []);

  const runSimulation = () => {
    if (isSimulating) {
      clearInterval(intervalRef.current);
      setIsSimulating(false);
      return;
    }

    setIsSimulating(true);
    
    // Stream real data from the backend
    intervalRef.current = setInterval(async () => {
      try {
        // 1. Fetch the real physics data from the CSV stream
        const streamResponse = await fetch(`http://127.0.0.1:8000/api/stream_real_data?sensor=${sensor}`);
        if (!streamResponse.ok) return;
        
        const streamResult = await streamResponse.json();
        const currentSequence = streamResult.sequence;
        
        setData(currentSequence);

        // 2. Format payload for FastAPI prediction
        const payload = currentSequence.map(d => [d.flux, d.error]);
        
        // Read the current sensor state for the API request
        // Using a functional state update trick or relying on the outer scope 
        // Wait, setInterval might trap the stale state of `sensor`. 
        // We should use a ref for the active sensor or pass it dynamically.
        // I will fix this immediately by just letting it use the `sensor` state (since we might need to recreate the interval, but it's simpler to just re-create the simulation when sensor changes).
        // For now, to avoid stale state in interval, we'll fetch using a ref.

        
        if (predictResponse.ok) {
          const result = await predictResponse.json();
          setPrediction(result);
        }
      } catch (err) {
        console.error("API Error:", err);
      }
      
    }, 1000); // Update every 1 second for true real-time streaming
  };

  // Re-run simulation when sensor changes to avoid stale state in interval
  useEffect(() => {
    if (isSimulating) {
      clearInterval(intervalRef.current);
      // We will create a fresh interval that captures the new sensor state
      intervalRef.current = setInterval(async () => {
        try {
          const streamResponse = await fetch(`http://127.0.0.1:8000/api/stream_real_data?sensor=${sensor}`);
          if (!streamResponse.ok) return;
          
          const streamResult = await streamResponse.json();
          setData(streamResult.sequence);
  
          const payload = streamResult.sequence.map(d => [d.flux, d.error]);
          
          const predictResponse = await fetch(`http://127.0.0.1:8000/api/predict?sensor=${sensor}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ sequence: payload })
          });
          
          if (predictResponse.ok) {
            const result = await predictResponse.json();
            setPrediction(result);
          }
        } catch (err) {
          console.error("API Error:", err);
        }
      }, 1000);
    }
    
    return () => clearInterval(intervalRef.current);
  }, [sensor, isSimulating]);

  useEffect(() => {
    return () => clearInterval(intervalRef.current);
  }, []);

  const jumpToFlare = async () => {
    try {
      await fetch('http://127.0.0.1:8000/api/jump_to_flare', { method: 'POST' });
      if (!isSimulating) {
        runSimulation();
      }
    } catch (err) {
      console.error("Failed to jump to flare:", err);
    }
  };

  const isAlert = prediction.probability > 50;
  const latestTime = data.length > 0 ? data[data.length - 1].time : "Awaiting Stream...";

  return (
    <div className="dashboard-container">
      <header className="header">
        <h1>Aditya-L1 Space Weather Intelligence</h1>
        <p>Real-Time X-Ray Flux Telemetry & LSTM Flare Prediction</p>
      </header>

      <div className="glass-panel">
        <div style={{ display: 'flex', justifyContent: 'center', marginBottom: '20px', gap: '15px' }}>
          <button 
            onClick={() => setSensor('hel1os')}
            style={{ 
              padding: '10px 20px', 
              backgroundColor: sensor === 'hel1os' ? 'rgba(102, 252, 241, 0.2)' : 'transparent',
              border: `2px solid ${sensor === 'hel1os' ? '#66fcf1' : '#444'}`,
              color: sensor === 'hel1os' ? '#66fcf1' : '#888',
              borderRadius: '8px',
              cursor: 'pointer',
              fontWeight: 'bold',
              transition: 'all 0.3s ease'
            }}>
            HEL1OS CAMERA
          </button>
          <button 
            onClick={() => setSensor('solexs')}
            style={{ 
              padding: '10px 20px', 
              backgroundColor: sensor === 'solexs' ? 'rgba(255, 136, 0, 0.2)' : 'transparent',
              border: `2px solid ${sensor === 'solexs' ? '#ff8800' : '#444'}`,
              color: sensor === 'solexs' ? '#ff8800' : '#888',
              borderRadius: '8px',
              cursor: 'pointer',
              fontWeight: 'bold',
              transition: 'all 0.3s ease'
            }}>
            SoLEXS CAMERA
          </button>
        </div>
        
        <div className="grid-container">
          
          {/* Main Chart Area */}
          <div className="chart-section">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <h2><Activity size={20} style={{display: 'inline', marginRight: '10px'}}/> Live X-Ray Flux Stream ({sensor === 'hel1os' ? 'HEL1OS' : 'SoLEXS'})</h2>
              <div style={{ color: '#00ffcc', fontFamily: 'monospace', fontSize: '1.2rem', fontWeight: 'bold' }}>
                {latestTime}
              </div>
            </div>
            <div style={{ height: '400px', width: '100%' }}>
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={data}>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                  <XAxis 
                    dataKey="time" 
                    stroke="#888" 
                    tick={{fill: '#888'}} 
                    tickFormatter={(tick) => {
                      if (typeof tick === 'string' && tick.includes(', ')) {
                        return tick.split(', ')[1];
                      }
                      return tick;
                    }}
                  />
                  <YAxis stroke="#888" tick={{fill: '#888'}} domain={[0, 1]} />
                  <Tooltip 
                    contentStyle={{ backgroundColor: 'rgba(0,0,0,0.8)', border: '1px solid #333' }}
                    itemStyle={{ color: '#fff' }}
                  />
                  <ReferenceLine y={0.8} label="X-Class Threshold" stroke="#ff003c" strokeDasharray="3 3" />
                  <ReferenceLine y={0.5} label="M-Class Threshold" stroke="#ff8800" strokeDasharray="3 3" />
                  <Line 
                    type="monotone" 
                    dataKey="flux" 
                    stroke={prediction.color} 
                    strokeWidth={3} 
                    dot={false}
                    activeDot={{ r: 8 }}
                    isAnimationActive={false}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Status Panel Area */}
          <div className="status-section">
            
            <div className={`status-card ${isAlert ? 'alert-pulse' : ''}`} style={{ '--card-color': prediction.color }}>
              <h3>AI Threat Assessment</h3>
              <div className="status-value">{prediction.probability}%</div>
              <div className="severity-label">
                {isAlert ? <AlertTriangle size={24} style={{verticalAlign: 'bottom'}}/> : <ShieldCheck size={24} style={{verticalAlign: 'bottom'}}/>} 
                &nbsp;{prediction.severity}
              </div>
            </div>

            {/* Predictive Forecasting Card */}
            {prediction.forecast && (
              <div className="status-card" style={{ '--card-color': '#b35900', marginTop: '20px' }}>
                <h3 style={{ fontSize: '1rem', color: '#fff' }}>Predictive Forecasting</h3>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', marginTop: '12px' }}>
                  
                  {/* T+15m */}
                  <div>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '4px' }}>
                      <span style={{ color: '#aaa', fontSize: '0.85rem' }}>+15 Minutes</span>
                      <span style={{ color: prediction.forecast.t_15m > 50 ? '#ff003c' : '#00ffcc', fontWeight: 'bold', fontSize: '0.85rem' }}>
                        {prediction.forecast.t_15m}%
                      </span>
                    </div>
                    <div style={{ width: '100%', height: '4px', backgroundColor: '#333', borderRadius: '2px' }}>
                      <div style={{ width: `${prediction.forecast.t_15m}%`, height: '100%', backgroundColor: prediction.forecast.t_15m > 50 ? '#ff003c' : '#00ffcc', borderRadius: '2px', transition: 'width 0.5s' }}></div>
                    </div>
                  </div>

                  {/* T+30m */}
                  <div>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '4px' }}>
                      <span style={{ color: '#aaa', fontSize: '0.85rem' }}>+30 Minutes</span>
                      <span style={{ color: prediction.forecast.t_30m > 50 ? '#ff003c' : (prediction.forecast.t_30m > 20 ? '#ffdd00' : '#00ffcc'), fontWeight: 'bold', fontSize: '0.85rem' }}>
                        {prediction.forecast.t_30m}%
                      </span>
                    </div>
                    <div style={{ width: '100%', height: '4px', backgroundColor: '#333', borderRadius: '2px' }}>
                      <div style={{ width: `${prediction.forecast.t_30m}%`, height: '100%', backgroundColor: prediction.forecast.t_30m > 50 ? '#ff003c' : (prediction.forecast.t_30m > 20 ? '#ffdd00' : '#00ffcc'), borderRadius: '2px', transition: 'width 0.5s' }}></div>
                    </div>
                  </div>

                  {/* T+60m */}
                  <div>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '4px' }}>
                      <span style={{ color: '#aaa', fontSize: '0.85rem' }}>+1 Hour</span>
                      <span style={{ color: prediction.forecast.t_60m > 50 ? '#ff003c' : (prediction.forecast.t_60m > 20 ? '#ffdd00' : '#00ffcc'), fontWeight: 'bold', fontSize: '0.85rem' }}>
                        {prediction.forecast.t_60m}%
                      </span>
                    </div>
                    <div style={{ width: '100%', height: '4px', backgroundColor: '#333', borderRadius: '2px' }}>
                      <div style={{ width: `${prediction.forecast.t_60m}%`, height: '100%', backgroundColor: prediction.forecast.t_60m > 50 ? '#ff003c' : (prediction.forecast.t_60m > 20 ? '#ffdd00' : '#00ffcc'), borderRadius: '2px', transition: 'width 0.5s' }}></div>
                    </div>
                  </div>

                </div>
              </div>
            )}

            <div className="status-card" style={{ '--card-color': backendStatus.includes("Online") ? '#00ffcc' : '#ff003c' }}>
              <h3>API Connection</h3>
              <div style={{ color: backendStatus.includes("Online") ? '#00ffcc' : '#ff003c', fontSize: '1.2rem', fontWeight: 600 }}>
                {backendStatus}
              </div>
            </div>

            <div className="controls">
              <button 
                onClick={runSimulation} 
                style={{
                  borderColor: isSimulating ? '#ff003c' : '#66fcf1',
                  color: isSimulating ? '#ff003c' : '#66fcf1'
                }}
              >
                {isSimulating ? 'HALT TELEMETRY' : 'ENGAGE LIVE STREAM'}
              </button>
              <button 
                onClick={jumpToFlare} 
                style={{
                  borderColor: '#ff8800',
                  color: '#ff8800',
                  marginLeft: '15px'
                }}
              >
                TRIGGER SOLAR FLARE
              </button>
            </div>
            
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
