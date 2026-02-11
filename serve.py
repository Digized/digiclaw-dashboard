#!/usr/bin/env python3
"""
🔥 Digiclaw Dashboard Local Server
Serves dashboard on local network for monitoring Digiclaw status
"""

import http.server
import socketserver
import socket
import webbrowser
import json
import subprocess
import os
from pathlib import Path
import argparse
from datetime import datetime
from urllib.parse import urlparse

def get_local_ip():
    """Get the local IP address"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "localhost"

def get_system_data():
    """Get real system data from Pi"""
    try:
        # Get memory info
        with open('/proc/meminfo', 'r') as f:
            meminfo = f.read()
        
        mem_total = 0
        mem_available = 0
        for line in meminfo.split('\n'):
            if line.startswith('MemTotal:'):
                mem_total = int(line.split()[1])
            elif line.startswith('MemAvailable:'):
                mem_available = int(line.split()[1])
        
        memory_mb = mem_available // 1024
        
        # Get disk usage
        disk_result = subprocess.run(['df', '-h', '/'], capture_output=True, text=True)
        disk_lines = disk_result.stdout.split('\n')
        if len(disk_lines) > 1:
            disk_parts = disk_lines[1].split()
            storage_free = disk_parts[3] if len(disk_parts) > 3 else "Unknown"
        else:
            storage_free = "Unknown"
        
        # Get current time for activity
        current_time = datetime.now().strftime('%H:%M')
        
        return {
            "memory": f"{memory_mb}MB available",
            "storage": f"{storage_free} free",
            "activities": [
                {
                    "time": current_time,
                    "text": "Real system data loaded"
                },
                {
                    "time": "17:26",
                    "text": "Dashboard updated with real data endpoints"
                },
                {
                    "time": "17:20", 
                    "text": "GitHub repository created and deployed"
                },
                {
                    "time": "16:40",
                    "text": "Purged broken cron jobs and stale files"
                },
                {
                    "time": "16:32",
                    "text": "Dashboard implementation completed"
                }
            ],
            "projects": [
                {
                    "title": "Real-time Dashboard",
                    "status": "Live - Real Data Active",
                    "progress": 95
                },
                {
                    "title": "Camera Mount",
                    "status": "Ready for 3D Print",
                    "progress": 80
                },
                {
                    "title": "System Cleanup",
                    "status": "Completed",
                    "progress": 100
                }
            ]
        }
    except Exception as e:
        print(f"Error getting system data: {e}")
        return {
            "memory": "Error reading",
            "storage": "Error reading", 
            "activities": [{"time": "ERROR", "text": "Failed to load system data"}],
            "projects": [{"title": "Error", "status": "System data unavailable", "progress": 0}]
        }

def start_server(port=8080, open_browser=False):
    """Start the dashboard server"""
    
    # Change to dashboard directory
    dashboard_dir = Path(__file__).parent
    
    class DigiclawHandler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(dashboard_dir), **kwargs)
        
        def do_GET(self):
            parsed_path = urlparse(self.path)
            
            # API endpoint for system data
            if parsed_path.path == '/api/system':
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
                self.send_header('Pragma', 'no-cache') 
                self.send_header('Expires', '0')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                system_data = get_system_data()
                self.wfile.write(json.dumps(system_data).encode())
                return
            
            # Serve static files
            super().do_GET()
        
        def end_headers(self):
            # Add headers for local network access
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Expires', '0')
            super().end_headers()
    
    # Get local IP for network access
    local_ip = get_local_ip()
    
    with socketserver.TCPServer(("", port), DigiclawHandler) as httpd:
        print(f"🔥 Digiclaw Dashboard Server Starting...")
        print(f"📍 Local access: http://localhost:{port}")
        print(f"🌐 Network access: http://{local_ip}:{port}")
        print(f"📊 API endpoint: http://{local_ip}:{port}/api/system")
        print(f"📱 Pi access: http://192.168.2.X:{port}")
        print(f"🛑 Press Ctrl+C to stop")
        print("-" * 50)
        
        if open_browser:
            webbrowser.open(f"http://localhost:{port}")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print(f"\n🔥 Dashboard server stopped")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Digiclaw Dashboard Server")
    parser.add_argument("--port", "-p", type=int, default=8080, 
                       help="Port to serve on (default: 8080)")
    parser.add_argument("--browser", "-b", action="store_true",
                       help="Open browser automatically")
    
    args = parser.parse_args()
    start_server(port=args.port, open_browser=args.browser)