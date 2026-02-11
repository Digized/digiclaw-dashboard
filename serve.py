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
import importlib.util
import sys

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

def get_comprehensive_data():
    """Get comprehensive status data"""
    try:
        # Load the API module
        spec = importlib.util.spec_from_file_location("api", Path(__file__).parent / "api.py")
        api_module = importlib.util.module_from_spec(spec)
        sys.modules["api"] = api_module
        spec.loader.exec_module(api_module)
        
        return api_module.get_comprehensive_status()
    except Exception as e:
        print(f"Error loading comprehensive data: {e}")
        # Fallback to basic data
        return {
            "timestamp": datetime.now().isoformat(),
            "system": {"error": "Failed to load comprehensive data"},
            "memory_summary": {"error": str(e)},
            "current_activity": {"status": "Error loading status", "last_update": datetime.now().strftime("%H:%M:%S")},
            "projects": [{"name": "Dashboard", "status": "Building comprehensive system", "progress": 50}],
            "recent_conversations": ["Working on comprehensive dashboard"],
            "autonomous_work": [{"action": "Building status system", "time": datetime.now().strftime("%H:%M")}],
            "next_actions": [{"action": "Fix comprehensive data loading", "priority": "high"}]
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
            
            # API endpoint for comprehensive status
            if parsed_path.path == '/api/status':
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
                self.send_header('Pragma', 'no-cache') 
                self.send_header('Expires', '0')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                status_data = get_comprehensive_data()
                self.wfile.write(json.dumps(status_data).encode())
                return
                
            # Legacy endpoint for backwards compatibility
            if parsed_path.path == '/api/system':
                self.send_response(200) 
                self.send_header('Content-type', 'application/json')
                self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
                self.send_header('Pragma', 'no-cache')
                self.send_header('Expires', '0')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                # Convert comprehensive data to legacy format
                comprehensive = get_comprehensive_data()
                legacy_data = {
                    "memory": comprehensive.get("system", {}).get("memory_available", "Unknown"),
                    "storage": comprehensive.get("system", {}).get("disk_free", "Unknown"),
                    "activities": [{"time": datetime.now().strftime("%H:%M"), "text": "Comprehensive status system active"}],
                    "projects": comprehensive.get("projects", [])
                }
                self.wfile.write(json.dumps(legacy_data).encode())
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