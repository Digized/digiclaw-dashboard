#!/usr/bin/env python3
"""
🔥 Digiclaw DDNS Setup for digiclaw.digized.xyz
Automatically configures dynamic DNS to make dashboard accessible externally
"""

import subprocess
import requests
import socket
import json
import time
from pathlib import Path

def get_public_ip():
    """Get current public IP address"""
    try:
        response = requests.get('https://api.ipify.org?format=json', timeout=10)
        return response.json()['ip']
    except Exception as e:
        print(f"Failed to get public IP: {e}")
        try:
            # Fallback method
            response = requests.get('https://icanhazip.com', timeout=10)
            return response.text.strip()
        except Exception as e2:
            print(f"Fallback IP detection failed: {e2}")
            return None

def get_local_ip():
    """Get local IP address"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "192.168.2.22"  # Default based on known IP

def setup_ddns_config():
    """Setup DDNS configuration"""
    
    public_ip = get_public_ip()
    local_ip = get_local_ip()
    
    config = {
        "subdomain": "digiclaw",
        "domain": "digized.xyz",
        "full_domain": "digiclaw.digized.xyz",
        "public_ip": public_ip,
        "local_ip": local_ip,
        "dashboard_port": 8081,
        "last_updated": time.time(),
        "setup_instructions": {
            "namecheap": [
                "1. Log into Namecheap dashboard",
                "2. Go to Domain List → digized.xyz → Manage",
                "3. Advanced DNS → Add new record:",
                "   - Type: A Record",
                "   - Host: digiclaw", 
                "   - Value: " + (public_ip or "YOUR_PUBLIC_IP"),
                "   - TTL: 1 min (for testing, later 5 min)",
                "4. Save changes",
                "5. Wait 1-5 minutes for propagation",
                f"6. Test: http://digiclaw.digized.xyz:8081/"
            ],
            "router_port_forward": [
                "1. Access router admin (usually 192.168.1.1 or 192.168.2.1)",
                "2. Find Port Forwarding / NAT settings",
                f"3. Add rule: External port 8081 → Internal {local_ip}:8081",
                "4. Protocol: TCP",
                "5. Enable the rule",
                "6. Save router configuration"
            ],
            "alternative_local_access": [
                f"Local network: http://{local_ip}:8081/",
                f"Comprehensive dashboard: http://{local_ip}:8081/comprehensive.html"
            ]
        }
    }
    
    # Save config file
    config_file = Path(__file__).parent / "ddns-config.json"
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    return config

def print_setup_instructions(config):
    """Print setup instructions"""
    
    print("🔥 DDNS Setup for digiclaw.digized.xyz")
    print("=" * 50)
    print(f"Public IP: {config['public_ip']}")
    print(f"Local IP: {config['local_ip']}")  
    print(f"Dashboard: http://digiclaw.digized.xyz:8081/comprehensive.html")
    print()
    
    print("📍 NAMECHEAP DNS SETUP:")
    for step in config['setup_instructions']['namecheap']:
        print(f"   {step}")
    print()
    
    print("🌐 ROUTER PORT FORWARDING:")
    for step in config['setup_instructions']['router_port_forward']:
        print(f"   {step}")
    print()
    
    print("🏠 LOCAL ACCESS (No DDNS needed):")
    for option in config['setup_instructions']['alternative_local_access']:
        print(f"   {option}")
    print()
    
    print("⚡ QUICK TEST:")
    print("   1. Set up Namecheap DNS record (takes 1-5 minutes)")
    print("   2. Test local first: http://192.168.2.22:8081/comprehensive.html")
    print("   3. Test external: http://digiclaw.digized.xyz:8081/comprehensive.html") 
    print("   4. If external fails, check router port forwarding")

def check_ddns_status(config):
    """Check if DDNS is working"""
    
    try:
        # Test local access
        local_url = f"http://{config['local_ip']}:{config['dashboard_port']}/api/status"
        response = requests.get(local_url, timeout=5)
        local_working = response.status_code == 200
        
        # Test external access (this will fail until DNS propagates)
        external_url = f"http://{config['full_domain']}:{config['dashboard_port']}/api/status"
        try:
            response = requests.get(external_url, timeout=10)
            external_working = response.status_code == 200
        except:
            external_working = False
            
        return {
            "local_working": local_working,
            "external_working": external_working,
            "local_url": local_url,
            "external_url": external_url
        }
        
    except Exception as e:
        return {"error": str(e)}

def main():
    """Main setup function"""
    
    print("🔥 Setting up Digiclaw DDNS...")
    
    # Generate configuration
    config = setup_ddns_config()
    
    # Print instructions
    print_setup_instructions(config)
    
    # Test current status
    print("🔧 TESTING CURRENT STATUS:")
    status = check_ddns_status(config)
    
    if 'error' in status:
        print(f"   ❌ Error testing: {status['error']}")
    else:
        print(f"   📍 Local access: {'✅' if status['local_working'] else '❌'}")
        print(f"   🌐 External access: {'✅' if status['external_working'] else '⏳ (Pending DNS setup)'}")
    
    print()
    print("💡 Next: Set up the DNS record in Namecheap as shown above")
    print("   The comprehensive dashboard will then be accessible worldwide!")

if __name__ == "__main__":
    main()