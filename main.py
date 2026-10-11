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
                body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #121212; color: #ffffff; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
                .container { background-color: #1e1e1e; padding: 40px; border-radius: 12px; box-shadow: 0 8px 32px rgba(0,0,0,0.5); text-align: center; width: 600px; border: 1px solid #333; }
                h1 { color: #00d2ff; margin-bottom: 5px; }
                p { color: #888; font-size: 14px; margin-top: 0; }
                .status { padding: 12px; background-color: rgba(0, 210, 255, 0.1); color: #00d2ff; border-radius: 8px; font-weight: bold; margin-top: 20px; border: 1px solid #00d2ff; }
                .metrics-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 30px; }
                .metric-card { background-color: #2a2a2a; padding: 20px; border-radius: 8px; border: 1px solid #444; position: relative; overflow: hidden; }
                .metric-value { font-size: 32px; font-weight: bold; color: #ff5722; margin-top: 10px; transition: color 0.3s; }
                .metric-label { font-size: 12px; color: #aaa; text-transform: uppercase; letter-spacing: 1px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Automated Command Center</h1>
                <p>Live AWS Infrastructure Monitor</p>
                <div class="status" id="connection-status">System Status: CONNECTING... 🟡</div>
                
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
                </div>
            </div>

            <script>
                // Asynchronous loop to fetch data every 2 seconds
                async function fetchMetrics() {
                    try {
                        const response = await fetch('/metrics');
                        const data = await response.json();
                        
                        document.getElementById('val-uptime').innerText = data.uptime;
                        document.getElementById('val-visits').innerText = data.visits;
                        document.getElementById('val-cpu').innerText = data.cpu + '%';
                        document.getElementById('val-ram').innerText = data.ram + '%';
                        document.getElementById('val-disk').innerText = data.disk + '%';
                        
                        document.getElementById('connection-status').innerText = 'System Status: LIVE 🟢';
                        document.getElementById('connection-status').style.color = '#00d2ff';
                    } catch (error) {
                        document.getElementById('connection-status').innerText = 'System Status: CONNECTION LOST 🔴';
                        document.getElementById('connection-status').style.color = '#ff5722';
                    }
                }
                
                // Run instantly, then repeat every 2000 milliseconds
                fetchMetrics();
                setInterval(fetchMetrics, 2000);
            </script>
        </body>
    </html>
    """
    return html_content