import redis
import psutil
import time
import datetime
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()
cache = redis.Redis(host='redis', port=6379)

# 1. The REST API Endpoint (Returns raw data)
@app.get("/metrics")
def get_metrics():
    try:
        cache.incr('hits') # Increment on every data pull
        visits = cache.get('hits').decode('utf-8')
    except redis.exceptions.ConnectionError:
        visits = "Offline"

    return {
        "cpu": psutil.cpu_percent(interval=0.1),
        "ram": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage('/').percent,
        "uptime": str(datetime.timedelta(seconds=int(time.time() - psutil.boot_time()))),
        "visits": visits
    }

# 2. The Frontend (Loads once, updates via Javascript)
@app.get("/", response_class=HTMLResponse)
def read_root():
    html_content = """
    <html>
        <head>
            <title>DevOps Automated Command Center</title>
            <style>
                * { box-sizing: border-box; }
                body {
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #0b1020, #121827 45%, #1d2333);
                    color: #ffffff;
                    margin: 0;
                    min-height: 100vh;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    padding: 32px 16px;
                }
                .container {
                    background-color: rgba(30, 41, 59, 0.9);
                    padding: 32px;
                    border-radius: 18px;
                    box-shadow: 0 18px 50px rgba(0,0,0,0.45);
                    width: min(920px, 100%);
                    border: 1px solid rgba(148, 163, 184, 0.25);
                }
                .topbar {
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    gap: 12px;
                    flex-wrap: wrap;
                    margin-bottom: 18px;
                }
                .badge {
                    background: rgba(59, 130, 246, 0.15);
                    border: 1px solid rgba(96, 165, 250, 0.4);
                    color: #8ec5ff;
                    padding: 8px 12px;
                    border-radius: 999px;
                    font-size: 12px;
                    letter-spacing: 0.08em;
                    text-transform: uppercase;
                }
                h1 {
                    color: #00d2ff;
                    margin: 0 0 8px;
                    font-size: clamp(2rem, 3vw, 2.8rem);
                }
                p {
                    color: #cbd5e1;
                    font-size: 14px;
                    margin: 0;
                }
                .status {
                    padding: 14px 18px;
                    background-color: rgba(0, 210, 255, 0.1);
                    color: #00d2ff;
                    border-radius: 10px;
                    font-weight: bold;
                    margin-top: 22px;
                    border: 1px solid #00d2ff;
                    text-align: center;
                }
                .summary-grid {
                    display: grid;
                    grid-template-columns: repeat(4, minmax(0, 1fr));
                    gap: 18px;
                    margin-top: 26px;
                }
                .summary-card {
                    background: rgba(15, 23, 42, 0.8);
                    border: 1px solid rgba(148, 163, 184, 0.2);
                    border-radius: 12px;
                    padding: 18px 16px;
                }
                .summary-label {
                    font-size: 11px;
                    color: #94a3b8;
                    letter-spacing: 0.12em;
                    text-transform: uppercase;
                }
                .summary-value {
                    margin-top: 10px;
                    font-size: 24px;
                    font-weight: bold;
                    color: #f8fafc;
                }
                .summary-sub {
                    margin-top: 8px;
                    color: #22c55e;
                    font-size: 12px;
                }
                .metrics-grid {
                    display: grid;
                    grid-template-columns: repeat(3, minmax(0, 1fr));
                    gap: 18px;
                    margin-top: 28px;
                }
                .metric-card {
                    background: linear-gradient(180deg, rgba(42, 42, 42, 0.95), rgba(30, 30, 30, 0.95));
                    padding: 20px;
                    border-radius: 12px;
                    border: 1px solid rgba(148, 163, 184, 0.2);
                    position: relative;
                    overflow: hidden;
                }
                .metric-value {
                    font-size: clamp(1.7rem, 2vw, 2.4rem);
                    font-weight: bold;
                    color: #ff8a65;
                    margin-top: 10px;
                    transition: color 0.3s;
                }
                .metric-label {
                    font-size: 12px;
                    color: #aaa;
                    text-transform: uppercase;
                    letter-spacing: 1px;
                }
                .activity {
                    margin-top: 28px;
                    background: rgba(15, 23, 42, 0.8);
                    border: 1px solid rgba(148, 163, 184, 0.2);
                    border-radius: 12px;
                    padding: 20px 18px;
                }
                .activity h2 {
                    margin: 0 0 14px;
                    color: #dbeafe;
                    font-size: 18px;
                }
                .activity-list {
                    list-style: none;
                    padding: 0;
                    margin: 0;
                    display: grid;
                    gap: 10px;
                    color: #cbd5e1;
                }
                .activity-list li {
                    border-left: 3px solid #00d2ff;
                    padding-left: 12px;
                }
                @media (max-width: 720px) {
                    .summary-grid,
                    .metrics-grid {
                        grid-template-columns: 1fr 1fr;
                    }
                }
                @media (max-width: 520px) {
                    .summary-grid,
                    .metrics-grid {
                        grid-template-columns: 1fr;
                    }
                    .container {
                        padding: 22px 18px;
                    }
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="topbar">
                    <div>
                        <h1>Automated Command Center</h1>
                        <p>Live AWS Infrastructure Monitor</p>
                    </div>
                    <div class="badge">Production Cluster</div>
                </div>

                <div class="status" id="connection-status">System Status: CONNECTING... 🟡</div>

                <div class="summary-grid">
                    <div class="summary-card">
                        <div class="summary-label">Environment</div>
                        <div class="summary-value">AWS</div>
                        <div class="summary-sub">Cloud ready</div>
                    </div>
                    <div class="summary-card">
                        <div class="summary-label">Deployment</div>
                        <div class="summary-value">Blue</div>
                        <div class="summary-sub">Stable release</div>
                    </div>
                    <div class="summary-card">
                        <div class="summary-label">Traffic</div>
                        <div class="summary-value">2.4k</div>
                        <div class="summary-sub">Requests/min</div>
                    </div>
                    <div class="summary-card">
                        <div class="summary-label">Alerts</div>
                        <div class="summary-value">0</div>
                        <div class="summary-sub">No incidents</div>
                    </div>
                </div>

                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="metric-label">Server Uptime</div>
                        <div class="metric-value" id="val-uptime">--:--:--</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Redis Operations</div>
                        <div class="metric-value" id="val-visits">--</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">CPU Usage</div>
                        <div class="metric-value" id="val-cpu">--%</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">RAM Usage</div>
                        <div class="metric-value" id="val-ram">--%</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Disk Capacity</div>
                        <div class="metric-value" id="val-disk">--%</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Last Sync</div>
                        <div class="metric-value" id="val-sync">--:--</div>
                    </div>
                </div>

                <div class="activity">
                    <h2>Operational Highlights</h2>
                    <ul class="activity-list">
                        <li>CI pipeline and environment checks are running as expected.</li>
                        <li>Redis cache is active and processing incoming requests.</li>
                        <li>Infrastructure health checks are synchronized every 2 seconds.</li>
                    </ul>
                </div>
            </div>

            <script>
                async function fetchMetrics() {
                    try {
                        const response = await fetch('/metrics');
                        const data = await response.json();

                        document.getElementById('val-uptime').innerText = data.uptime;
                        document.getElementById('val-visits').innerText = data.visits;
                        document.getElementById('val-cpu').innerText = data.cpu + '%';
                        document.getElementById('val-ram').innerText = data.ram + '%';
                        document.getElementById('val-disk').innerText = data.disk + '%';
                        document.getElementById('val-sync').innerText = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

                        document.getElementById('connection-status').innerText = 'System Status: LIVE 🟢';
                        document.getElementById('connection-status').style.color = '#00d2ff';
                    } catch (error) {
                        document.getElementById('connection-status').innerText = 'System Status: CONNECTION LOST 🔴';
                        document.getElementById('connection-status').style.color = '#ff5722';
                    }
                }

                fetchMetrics();
                setInterval(fetchMetrics, 2000);
            </script>
        </body>
    </html>
    """
    return html_content