import redis
import psutil
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()
cache = redis.Redis(host='redis', port=6379)

@app.get("/", response_class=HTMLResponse)
def read_root():
    # 1. Fetch Database Traffic
    try:
        visits = cache.incr('hits')
    except redis.exceptions.ConnectionError:
        visits = "Offline"

    # 2. Fetch Server Hardware Stats
    cpu_usage = psutil.cpu_percent(interval=0.1)
    ram_usage = psutil.virtual_memory().percent

    # 3. Render the Dark Mode Dashboard
    html_content = f"""
    <html>
        <head>
            <title>DevOps Command Center</title>
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #121212; color: #ffffff; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }}
                .container {{ background-color: #1e1e1e; padding: 40px; border-radius: 12px; box-shadow: 0 8px 32px rgba(0,0,0,0.5); text-align: center; width: 450px; border: 1px solid #333; }}
                h1 {{ color: #00d2ff; margin-bottom: 5px; }}
                p {{ color: #888; font-size: 14px; margin-top: 0; }}
                .status {{ padding: 12px; background-color: rgba(0, 210, 255, 0.1); color: #00d2ff; border-radius: 8px; font-weight: bold; margin-top: 20px; border: 1px solid #00d2ff; }}
                .metrics-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 30px; }}
                .metric-card {{ background-color: #2a2a2a; padding: 20px; border-radius: 8px; border: 1px solid #444; }}
                .metric-value {{ font-size: 32px; font-weight: bold; color: #ff5722; margin-top: 10px; }}
                .metric-label {{ font-size: 12px; color: #aaa; text-transform: uppercase; letter-spacing: 1px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Command Center</h1>
                <p>AWS EC2 Infrastructure Monitor</p>
                <div class="status">System Status: ALL SYSTEMS OPERATIONAL 🟢</div>
                
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="metric-label">Total Page Views</div>
                        <div class="metric-value">{visits}</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Active Containers</div>
                        <div class="metric-value">2</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">CPU Usage</div>
                        <div class="metric-value">{cpu_usage}%</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">RAM Usage</div>
                        <div class="metric-value">{ram_usage}%</div>
                    </div>
                </div>
            </div>
        </body>
    </html>
    """
    return html_content