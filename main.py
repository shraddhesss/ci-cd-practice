import redis
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

# Connect to the Redis database container
cache = redis.Redis(host='redis', port=6379)

@app.get("/", response_class=HTMLResponse)
def read_root():
    try:
        # Tell the database to add 1 to the visitor count
        visits = cache.incr('hits')
    except redis.exceptions.ConnectionError:
        visits = "Database Offline"

    html_content = f"""
    <html>
        <head>
            <title>DevOps Dashboard</title>
            <style>
                body {{ font-family: Arial, sans-serif; background-color: #f4f4f9; color: #333; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }}
                .container {{ background-color: white; padding: 40px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); text-align: center; }}
                h1 {{ color: #0073e6; }}
                .status {{ padding: 10px; background-color: #d4edda; color: #155724; border-radius: 5px; font-weight: bold; margin-top: 20px; }}
                .metric {{ margin-top: 20px; font-size: 24px; font-weight: bold; color: #ff5722; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>My CI/CD DevOps Dashboard</h1>
                <p>Welcome to my automated cloud infrastructure.</p>
                <div class="status">System Status: ALL SYSTEMS OPERATIONAL</div>
                <div class="metric">Page Views: {visits}</div>
            </div>
        </body>
    </html>
    """
    return html_content