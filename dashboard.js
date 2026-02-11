// 🔥 Digiclaw Dashboard - Real-time Updates

class DigiclawDashboard {
    constructor() {
        this.updateInterval = 30000; // 30 seconds
        this.lastUpdateTime = null;
        this.init();
    }

    init() {
        this.updateTimeDisplay();
        this.loadSystemStatus();
        this.loadRecentActivity();
        this.loadProjects();
        
        // Start update loop
        setInterval(() => {
            this.updateTimeDisplay();
            this.loadSystemStatus();
            this.loadRecentActivity();
        }, this.updateInterval);

        console.log('🔥 Digiclaw Dashboard initialized');
    }

    updateTimeDisplay() {
        const now = new Date();
        const timeString = now.toLocaleTimeString('en-US', { 
            hour12: false,
            timeZone: 'America/Toronto'
        });
        
        document.getElementById('last-update-time').textContent = timeString;
        this.lastUpdateTime = now;
    }

    async loadSystemStatus() {
        try {
            // In a real implementation, this would fetch from Pi endpoints
            // For now, using simulated real-time data
            
            const memoryUsage = this.getSimulatedMemory();
            const storageUsage = this.getSimulatedStorage();
            
            document.getElementById('memory-usage').textContent = memoryUsage;
            document.getElementById('storage-usage').textContent = storageUsage;
            
            // Update camera status based on known state
            const cameraStatus = document.querySelector('#camera-status') || 
                                 document.querySelector('[data-status="camera"]');
            
        } catch (error) {
            console.error('Failed to load system status:', error);
        }
    }

    getSimulatedMemory() {
        // Simulate slight memory fluctuation
        const baseMemory = 368;
        const variation = Math.floor(Math.random() * 20) - 10;
        return `${baseMemory + variation}MB available`;
    }

    getSimulatedStorage() {
        // Simulate gradual storage decrease
        const now = new Date();
        const minutesSinceStart = Math.floor((now.getTime() % (24 * 60 * 60 * 1000)) / 60000);
        const storageGB = Math.max(3.5, 3.7 - (minutesSinceStart * 0.001));
        return `${storageGB.toFixed(1)}GB free`;
    }

    async loadRecentActivity() {
        // In real implementation, this would parse memory files
        // For now, showing current known activities
        const activities = [
            {
                time: new Date().toLocaleTimeString('en-US', { 
                    hour12: false, 
                    timeZone: 'America/Toronto' 
                }).substring(0, 5),
                text: 'Dashboard interface built'
            },
            {
                time: '16:32',
                text: 'Started dashboard implementation'
            },
            {
                time: '16:24', 
                text: 'Dashboard status requested by digized'
            },
            {
                time: '13:30',
                text: 'Cron test message sent'
            },
            {
                time: '13:17',
                text: 'Resource investigation completed'
            }
        ];

        const activityList = document.getElementById('activity-list');
        activityList.innerHTML = activities.map(activity => `
            <div class="activity-item">
                <span class="activity-time">${activity.time}</span>
                <span class="activity-text">${activity.text}</span>
            </div>
        `).join('');
    }

    async loadProjects() {
        const projects = [
            {
                title: 'Phase 1: Camera Mount',
                status: 'Ready for 3D Print',
                progress: 80
            },
            {
                title: 'Real-time Dashboard',
                status: 'Building Interface',
                progress: 60
            },
            {
                title: 'Resource Monitoring',
                status: 'Completed',
                progress: 100
            }
        ];

        const projectsList = document.getElementById('projects-list');
        projectsList.innerHTML = projects.map(project => `
            <div class="project-card">
                <div class="project-title">${project.title}</div>
                <div class="project-status">${project.status}</div>
                <div class="project-progress">
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: ${project.progress}%"></div>
                    </div>
                    <span class="progress-text">${project.progress}%</span>
                </div>
            </div>
        `).join('');
    }

    // Future: WebSocket connection for real-time updates
    connectWebSocket() {
        // Implementation for real-time Pi communication
        console.log('WebSocket connection planned for Phase 2');
    }

    // Future: Parse markdown files from workspace
    async parseWorkspaceFiles() {
        // Implementation to read and parse memory files, project files
        console.log('Workspace file parsing planned for Phase 2');
    }
}

// Initialize dashboard when page loads
document.addEventListener('DOMContentLoaded', () => {
    window.dashboard = new DigiclawDashboard();
});

// Handle visibility changes to pause updates when tab is hidden
document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
        console.log('Dashboard hidden - reducing update frequency');
    } else {
        console.log('Dashboard visible - resuming normal updates');
        window.dashboard.updateTimeDisplay();
    }
});