# 🔥 Digiclaw Control Dashboard

Real-time monitoring interface for Digiclaw autonomous operations.

## Features

- **Live Status Monitoring** - System resources, projects, activity feed
- **Terminal Aesthetic** - Green-on-black hacker style interface  
- **Local Network Access** - Monitor from any device on your network
- **Real-time Updates** - Auto-refreshes every 30 seconds
- **Project Tracking** - Current work status and progress
- **Activity Feed** - Recent autonomous decisions and actions

## Quick Start

```bash
# Start dashboard server
cd digiclaw-dashboard
python3 serve.py

# Access dashboard
# Local: http://localhost:8080
# Network: http://192.168.2.X:8080
```

## Server Options

```bash
# Custom port
python3 serve.py --port 9000

# Auto-open browser
python3 serve.py --browser

# Help
python3 serve.py --help
```

## Dashboard Sections

### 🎯 Current Projects
- Active project status
- Progress bars with completion percentage
- Next milestone indicators

### 📊 System Status
- **Memory**: Available RAM on Pi
- **Storage**: Free disk space
- **Camera**: Current orientation status
- **Nodes**: Connected device status

### ⚡ Recent Activity
- Real-time log of autonomous decisions
- Timestamped action history
- System events and milestones

### 🛠️ Skills Arsenal
- Installed capabilities
- Active/inactive skill status
- Skill availability indicators

### 🚀 Next Actions
- Prioritized task queue
- Scheduled activities
- Waiting dependencies

### 📋 Daily Summary
- Today's accomplishments
- Current priorities
- System health overview

## Network Access

**From any device on your network:**
- Find Pi IP: `ip addr show` or router admin panel
- Access: `http://PI_IP:8080`
- Bookmark for quick monitoring

**Typical local IPs:**
- Pi: `192.168.1.X` or `192.168.2.X`
- Dashboard: `http://192.168.X.X:8080`

## Architecture

```
digiclaw-dashboard/
├── index.html          # Main dashboard interface
├── style.css           # Terminal aesthetic styling
├── dashboard.js        # Real-time update logic
├── serve.py           # Local server script
└── README.md          # This file
```

## Development

**Real-time Data Sources** (Future phases):
- Pi system metrics endpoint
- Workspace markdown file parsing
- WebSocket connections
- Direct memory file access

**Current Implementation:**
- Static HTML/CSS/JS interface
- Simulated real-time data
- 30-second refresh cycle
- Local network HTTP server

## Browser Compatibility

- **Chrome/Edge**: Full support
- **Firefox**: Full support  
- **Safari**: Full support
- **Mobile**: Basic support (not optimized)

## Security

- **Local network only** - No external access
- **Read-only monitoring** - No control capabilities
- **Simple HTTP** - No authentication needed for local use

---

🔥 **Digiclaw Dashboard v1.0** - Built for local network monitoring of autonomous Pi operations.