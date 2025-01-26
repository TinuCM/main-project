import psutil
import GPUtil
from datetime import datetime
import json

class ResourceMonitor:
    def __init__(self):
        # Define resource limits (in percentage)
        self.resource_limits = self.load_resource_limits()
        self.process_whitelist = self.load_process_whitelist()
        
        # Initialize alerts and logs
        self.alerts = []
        self.logs = []
        self.load_alerts_and_logs()
        
        print("\n=== Resource Monitor Initialized ===")
        print(f"Resource Limits: {self.resource_limits}")
        print(f"Whitelisted Processes: {self.process_whitelist}")

    def load_resource_limits(self):
        try:
            with open('resource_limits.txt', 'r') as f:
                limits = {}
                for line in f:
                    resource, limit = line.strip().split(',')
                    limits[resource] = float(limit)
                return limits
        except FileNotFoundError:
            return {'cpu': 50, 'memory': 70}

    def load_process_whitelist(self):
        try:
            whitelist = []
            with open('process_whitelist.txt', 'r') as f:
                for line in f:
                    process = line.strip()
                    if process:
                        whitelist.append(process)
            return whitelist
        except FileNotFoundError:
            default_whitelist = [
                "chrome.exe",
                "code.exe",
                "python.exe",
                "explorer.exe",
                "discord.exe",
                "whatsapp.exe"
            ]
            with open('process_whitelist.txt', 'w') as f:
                for process in default_whitelist:
                    f.write(f"{process}\n")
            return default_whitelist

    def load_alerts_and_logs(self):
        try:
            with open('alerts_logs.json', 'r') as f:
                data = json.load(f)
                self.alerts = data.get('alerts', [])
                self.logs = data.get('logs', [])
        except FileNotFoundError:
            self.alerts = []
            self.logs = []

    def save_alerts_and_logs(self):
        with open('alerts_logs.json', 'w') as f:
            json.dump({'alerts': self.alerts, 'logs': self.logs}, f)

    def check_resources(self):
        """Check system resources and processes, return any alerts"""
        alerts = []
        print("\n=== Checking System Resources ===")
        
        # Get system memory info for percentage calculations
        system_memory = psutil.virtual_memory()
        total_memory = system_memory.total
        
        # Track processes exceeding limits
        problematic_processes = []
        
        # Check all running processes
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
            try:
                # Get process info
                proc_info = proc.info
                proc_name = proc_info['name'].lower()
                
                # Calculate process resource usage
                cpu_percent = proc_info['cpu_percent'] / psutil.cpu_count()  # Normalize CPU percentage
                memory_percent = (proc_info['memory_info'].rss / total_memory) * 100
                
                # Print process info if using significant resources
                if cpu_percent > 1 or memory_percent > 1:
                    print(f"\nProcess: {proc_name}")
                    print(f"  PID: {proc_info['pid']}")
                    print(f"  CPU: {cpu_percent:.1f}%")
                    print(f"  Memory: {memory_percent:.1f}%")
                    print(f"  Whitelisted: {proc_name in [p.lower() for p in self.process_whitelist]}")
                
                # Check if process exceeds limits
                if (cpu_percent > self.resource_limits['cpu'] or 
                    memory_percent > self.resource_limits['memory']):
                    
                    # Only add to problematic processes if not in whitelist
                    if proc_name not in [p.lower() for p in self.process_whitelist]:
                        print(f"\n!!! Resource Limit Exceeded by {proc_name} !!!")
                        print(f"  CPU: {cpu_percent:.1f}% (Limit: {self.resource_limits['cpu']}%)")
                        print(f"  Memory: {memory_percent:.1f}% (Limit: {self.resource_limits['memory']}%)")
                        
                        problematic_processes.append({
                            'name': proc_name,
                            'pid': proc_info['pid'],
                            'cpu': cpu_percent,
                            'memory': memory_percent
                        })
                    else:
                        print(f"\nIgnoring whitelisted process {proc_name} exceeding limits")
                
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
                print(f"Error accessing process: {e}")
                continue
        
        # Generate alerts for problematic processes
        for proc in problematic_processes:
            alert = self.create_process_alert(proc)
            alerts.append(alert)
        
        return alerts

    def create_process_alert(self, process):
        """Create an alert for a problematic process"""
        current_time = datetime.now()
        
        # Create detailed message
        details = (
            f"Process Name: {process['name']}\n"
            f"PID: {process['pid']}\n"
            f"CPU Usage: {process['cpu']:.1f}% (Limit: {self.resource_limits['cpu']}%)\n"
            f"Memory Usage: {process['memory']:.1f}% (Limit: {self.resource_limits['memory']}%)"
        )
        
        alert = {
            "priority": "High",
            "message": f"Process {process['name']} exceeded resource limits",
            "details": details,
            "time": current_time.strftime("%H:%M:%S"),
            "process_name": process['name']
        }
        
        # Add to alerts list
        self.alerts.insert(0, alert)
        if len(self.alerts) > 100:
            self.alerts.pop()
        
        # Create log entry
        log_entry = {
            "timestamp": current_time.strftime("%Y-%m-%d %H:%M:%S"),
            "source_ip": "localhost",
            "event": f"Resource limit exceeded by {process['name']}",
            "severity": "High",
            "status": "Alert",
            "action": "Process Monitoring",
            "user": "system",
            "process": process['name']
        }
        
        # Add to logs list
        self.logs.insert(0, log_entry)
        if len(self.logs) > 100:
            self.logs.pop()
        
        # Save to file
        self.save_alerts_and_logs()
        
        print(f"\n=== Alert Generated ===")
        print(f"Time: {alert['time']}")
        print(f"Process: {process['name']}")
        print(f"Details:\n{details}")
        
        return alert 