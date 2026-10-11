from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def read_root():
    html_content = """
    <html>
        <head>
            <title>DevOps Dashboard</title>
            <style>
                body { font-family: Arial, sans-serif; background-color: #f4f4f9; color: #333; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
                .container { background-color: white; padding: 40px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); text-align: center; }
                h1 { color: #0073e6; }
                .status { padding: 10px; background-color: #d4edda; color: #155724; border-radius: 5px; font-weight: bold; margin-top: 20px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>My CI/CD DevOps Dashboard</h1>
                <p>Welcome to my automated cloud infrastructure.</p>
                <div class="status">System Status: ALL SYSTEMS OPERATIONAL</div>
                <p style="margin-top: 30px; font-size: 12px; color: #777;">Version 3.0 - Deployed via GitHub Actions</p>
            </div>
        </body>
    </html>
    """
    return html_content