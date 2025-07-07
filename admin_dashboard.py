from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import requests
import json
from datetime import datetime

app = FastAPI(title="Contact Form Admin Dashboard")

# Your API URL
API_BASE_URL = "https://portfolioapi-production-95b0.up.railway.app"

@app.get("/", response_class=HTMLResponse)
async def admin_dashboard():
    """
    Admin dashboard to view contact form submissions
    """
    try:
        # Get all submissions from your API
        response = requests.get(f"{API_BASE_URL}/contacts")
        if response.status_code == 200:
            data = response.json()
            submissions = data.get("submissions", [])
        else:
            submissions = []
            print(f"Error fetching submissions: {response.status_code}")
    except Exception as e:
        submissions = []
        print(f"Error: {e}")

    # Create HTML table
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Contact Form Submissions - Admin Dashboard</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 20px;
                background-color: #f5f5f5;
            }}
            .container {{
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }}
            h1 {{
                color: #333;
                text-align: center;
                margin-bottom: 30px;
            }}
            .stats {{
                display: flex;
                justify-content: space-around;
                margin-bottom: 30px;
                padding: 20px;
                background: #f8f9fa;
                border-radius: 8px;
            }}
            .stat {{
                text-align: center;
            }}
            .stat-number {{
                font-size: 2em;
                font-weight: bold;
                color: #007bff;
            }}
            .stat-label {{
                color: #666;
                margin-top: 5px;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }}
            th, td {{
                padding: 12px;
                text-align: left;
                border-bottom: 1px solid #ddd;
            }}
            th {{
                background-color: #007bff;
                color: white;
                font-weight: bold;
            }}
            tr:hover {{
                background-color: #f5f5f5;
            }}
            .message-cell {{
                max-width: 300px;
                overflow: hidden;
                text-overflow: ellipsis;
                white-space: nowrap;
            }}
            .message-cell:hover {{
                white-space: normal;
                overflow: visible;
                background: white;
                position: relative;
                z-index: 1;
            }}
            .timestamp {{
                color: #666;
                font-size: 0.9em;
            }}
            .refresh-btn {{
                background: #28a745;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                cursor: pointer;
                font-size: 16px;
            }}
            .refresh-btn:hover {{
                background: #218838;
            }}
            .no-submissions {{
                text-align: center;
                color: #666;
                font-style: italic;
                padding: 40px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📧 Contact Form Submissions</h1>
            
            <div class="stats">
                <div class="stat">
                    <div class="stat-number">{len(submissions)}</div>
                    <div class="stat-label">Total Submissions</div>
                </div>
                <div class="stat">
                    <div class="stat-number">{len([s for s in submissions if s.get('status') == 'received'])}</div>
                    <div class="stat-label">New Messages</div>
                </div>
            </div>
            
            <button class="refresh-btn" onclick="location.reload()">🔄 Refresh</button>
            
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Email</th>
                        <th>Topic</th>
                        <th>Message</th>
                        <th>Date</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
    """
    
    if submissions:
        for submission in submissions:
            # Format timestamp
            timestamp = submission.get('timestamp', '')
            if timestamp:
                try:
                    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    formatted_time = dt.strftime('%Y-%m-%d %H:%M:%S')
                except:
                    formatted_time = timestamp
            else:
                formatted_time = 'N/A'
            
            html_content += f"""
                    <tr>
                        <td><strong>{submission.get('id', 'N/A')}</strong></td>
                        <td><a href="mailto:{submission.get('email', '')}">{submission.get('email', 'N/A')}</a></td>
                        <td>{submission.get('topic', 'N/A')}</td>
                        <td class="message-cell" title="{submission.get('message', 'N/A')}">{submission.get('message', 'N/A')}</td>
                        <td class="timestamp">{formatted_time}</td>
                        <td><span style="color: #28a745;">{submission.get('status', 'received')}</span></td>
                    </tr>
            """
    else:
        html_content += """
                    <tr>
                        <td colspan="6" class="no-submissions">No submissions yet. Check back later!</td>
                    </tr>
        """
    
    html_content += """
                </tbody>
            </table>
            
            <div style="margin-top: 30px; text-align: center; color: #666;">
                <p>💡 <strong>Tip:</strong> Click on any message to see the full text</p>
                <p>📧 <strong>Email:</strong> Click on email addresses to open your email client</p>
            </div>
        </div>
        
        <script>
            // Auto-refresh every 30 seconds
            setTimeout(function() {
                location.reload();
            }, 30000);
        </script>
    </body>
    </html>
    """
    
    return html_content

@app.get("/api/submissions")
async def get_submissions_api():
    """
    API endpoint to get submissions in JSON format
    """
    try:
        response = requests.get(f"{API_BASE_URL}/contacts")
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "Failed to fetch submissions", "status_code": response.status_code}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8081) 