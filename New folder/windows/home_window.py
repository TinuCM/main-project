import customtkinter as ctk
import psutil
from datetime import datetime
from utils.resource_monitor import ResourceMonitor

class HomeWindow(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.resource_monitor = ResourceMonitor()
        
        self.setup_ui()
        self.start_monitoring()

    def setup_ui(self):
        # Create main container
        main_container = ctk.CTkFrame(self)
        main_container.pack(fill="both", expand=True)

        # Create sidebar
        self.setup_sidebar(main_container)

        # Main content area
        content_area = ctk.CTkFrame(main_container)
        content_area.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Welcome section
        self.setup_welcome_section(content_area)

        # Stats Overview
        self.setup_stats_overview(content_area)

        # Create grid for dashboard cards
        grid_frame = ctk.CTkFrame(content_area, fg_color="transparent")
        grid_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Configure grid columns and rows
        grid_frame.grid_columnconfigure((0, 1), weight=1)
        grid_frame.grid_rowconfigure((0, 1), weight=1)

        # Dashboard Cards
        self.setup_system_card(grid_frame, 0, 0)
        self.setup_alerts_card(grid_frame, 0, 1)
        self.setup_logs_card(grid_frame, 1, 0)
        self.setup_status_card(grid_frame, 1, 1)

    def setup_sidebar(self, parent):
        sidebar = ctk.CTkFrame(parent, width=200)
        sidebar.pack(side="left", fill="y", padx=10, pady=10)
        sidebar.pack_propagate(False)

        # App title in sidebar
        ctk.CTkLabel(
            sidebar,
            text="IDS Dashboard",
            font=("Helvetica", 20, "bold")
        ).pack(pady=20)

        # Navigation buttons with Home and Back at top
        top_buttons_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        top_buttons_frame.pack(fill="x", padx=10, pady=5)

        # Back button
        back_btn = ctk.CTkButton(
            top_buttons_frame,
            text="↩️",
            width=40,
            height=40,
            command=self.master.go_back,
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            font=("Helvetica", 14)
        )
        back_btn.pack(side="left", padx=2)

        # Home button
        home_btn = ctk.CTkButton(
            top_buttons_frame,
            text="🏠",
            width=40,
            height=40,
            command=self.master.show_home_window,
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            font=("Helvetica", 14)
        )
        home_btn.pack(side="left", padx=2)

        # Main navigation buttons
        buttons = [
            ("🖥️ System", self.master.show_system_window),
            ("🚨 Alerts", self.master.show_alerts_window),
            ("📝 Logs", self.master.show_logs_window),
            ("⚙️ Admin", self.master.show_admin_window),
            ("🚪 Logout", self.master.show_login_window)
        ]

        for text, command in buttons:
            btn = ctk.CTkButton(
                sidebar,
                text=text,
                command=command,
                width=160,
                height=40,
                fg_color="transparent",
                text_color=("gray10", "gray90"),
                hover_color=("gray70", "gray30"),
                anchor="w",
                font=("Helvetica", 14)
            )
            btn.pack(pady=5, padx=10)

    def setup_welcome_section(self, parent):
        welcome_frame = ctk.CTkFrame(parent, fg_color="transparent")
        welcome_frame.pack(fill="x", padx=20, pady=(0, 20))

        # Welcome message
        ctk.CTkLabel(
            welcome_frame,
            text="Welcome to IDS Dashboard",
            font=("Helvetica", 24, "bold")
        ).pack(side="left", anchor="w")

        # Current time and date
        time_frame = ctk.CTkFrame(welcome_frame, fg_color="transparent")
        time_frame.pack(side="right")

        self.time_label = ctk.CTkLabel(
            time_frame,
            text="",
            font=("Helvetica", 14)
        )
        self.time_label.pack(side="right")
        self.update_time()

    def setup_stats_overview(self, parent):
        stats_frame = ctk.CTkFrame(parent)
        stats_frame.pack(fill="x", padx=20, pady=(0, 20))

        # Quick stats in a row with view details buttons
        stats = [
            ("🔍 System Status", "Active", "#00CC00", self.master.show_system_window),
            ("⚠️ Active Alerts", f"{len(self.resource_monitor.alerts)}", "#FFA500", self.master.show_alerts_window),
            ("📊 CPU Usage", "0%", None, self.master.show_system_window),
            ("💾 Memory Usage", "0%", None, self.master.show_system_window)
        ]

        for title, value, color, command in stats:
            stat_box = ctk.CTkFrame(stats_frame)
            stat_box.pack(side="left", expand=True, fill="both", padx=5, pady=10)

            # Title and View Details button container
            header_frame = ctk.CTkFrame(stat_box, fg_color="transparent")
            header_frame.pack(fill="x", padx=5, pady=(5, 0))

            ctk.CTkLabel(
                header_frame,
                text=title,
                font=("Helvetica", 12)
            ).pack(side="left")

            view_btn = ctk.CTkButton(
                header_frame,
                text="View",
                command=command,
                width=60,
                height=25,
                font=("Helvetica", 11),
                fg_color="transparent",
                hover_color=("gray70", "gray30")
            )
            view_btn.pack(side="right")

            label = ctk.CTkLabel(
                stat_box,
                text=value,
                font=("Helvetica", 16, "bold"),
                text_color=color
            )
            label.pack(pady=(0, 5))

            if title == "📊 CPU Usage":
                self.cpu_stat_label = label
            elif title == "💾 Memory Usage":
                self.memory_stat_label = label

    def update_time(self):
        current_time = datetime.now().strftime("%I:%M:%S %p\n%B %d, %Y")
        self.time_label.configure(text=current_time)
        self.after(1000, self.update_time)

    def create_card(self, parent, title):
        """Helper function to create consistent card frames"""
        card = ctk.CTkFrame(parent)
        
        # Title
        ctk.CTkLabel(
            card,
            text=title,
            font=("Helvetica", 16, "bold")
        ).pack(pady=10, padx=10, anchor="w")
        
        return card

    def setup_system_card(self, parent, row, col):
        card = self.create_card(parent, "System Resources")
        card.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

        # Add View Details button
        view_btn = ctk.CTkButton(
            card,
            text="View Details",
            command=self.master.show_system_window,
            width=100,
            height=30,
            font=("Helvetica", 12),
            fg_color="transparent",
            hover_color=("gray70", "gray30")
        )
        view_btn.pack(anchor="e", padx=10)

        # CPU Usage
        cpu_frame = ctk.CTkFrame(card, fg_color="transparent")
        cpu_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(cpu_frame, text="CPU Usage:", font=("Helvetica", 12)).pack(side="left")
        self.cpu_label = ctk.CTkLabel(cpu_frame, text="0%", font=("Helvetica", 12))
        self.cpu_label.pack(side="right")
        
        self.cpu_progress = ctk.CTkProgressBar(card)
        self.cpu_progress.pack(fill="x", padx=10, pady=(0, 10))
        self.cpu_progress.set(0)

        # Memory Usage
        mem_frame = ctk.CTkFrame(card, fg_color="transparent")
        mem_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(mem_frame, text="Memory Usage:", font=("Helvetica", 12)).pack(side="left")
        self.memory_label = ctk.CTkLabel(mem_frame, text="0%", font=("Helvetica", 12))
        self.memory_label.pack(side="right")
        
        self.memory_progress = ctk.CTkProgressBar(card)
        self.memory_progress.pack(fill="x", padx=10, pady=(0, 10))
        self.memory_progress.set(0)

    def setup_alerts_card(self, parent, row, col):
        card = self.create_card(parent, "Recent Alerts")
        card.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

        # Add View Details button
        view_btn = ctk.CTkButton(
            card,
            text="View Details",
            command=self.master.show_alerts_window,
            width=100,
            height=30,
            font=("Helvetica", 12),
            fg_color="transparent",
            hover_color=("gray70", "gray30")
        )
        view_btn.pack(anchor="e", padx=10)

        # Create scrollable frame for alerts
        alerts_frame = ctk.CTkScrollableFrame(card, height=150)
        alerts_frame.pack(fill="x", padx=10, pady=10)

        # Show last 5 alerts
        alerts = self.resource_monitor.alerts[:5]
        print(f"Loading alerts: {len(alerts)} found")  # Debug print

        if not alerts:
            ctk.CTkLabel(
                alerts_frame,
                text="No recent alerts",
                font=("Helvetica", 12)
            ).pack(pady=10)
        else:
            for alert in alerts:
                print(f"Processing alert: {alert}")  # Debug print
                alert_frame = ctk.CTkFrame(alerts_frame)
                alert_frame.pack(fill="x", pady=2)
                
                ctk.CTkLabel(
                    alert_frame,
                    text=f"🚨 {alert['message']}",
                    font=("Helvetica", 12)
                ).pack(side="left", padx=5)
                
                ctk.CTkLabel(
                    alert_frame,
                    text=alert['time'],
                    font=("Helvetica", 12),
                    text_color="gray"
                ).pack(side="right", padx=5)

    def setup_logs_card(self, parent, row, col):
        card = self.create_card(parent, "Recent Logs")
        card.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

        # Add View Details button
        view_btn = ctk.CTkButton(
            card,
            text="View Details",
            command=self.master.show_logs_window,
            width=100,
            height=30,
            font=("Helvetica", 12),
            fg_color="transparent",
            hover_color=("gray70", "gray30")
        )
        view_btn.pack(anchor="e", padx=10)

        # Create scrollable frame for logs
        logs_frame = ctk.CTkScrollableFrame(card, height=150)
        logs_frame.pack(fill="x", padx=10, pady=10)

        # Show last 5 logs
        logs = self.resource_monitor.logs[:5]
        if not logs:
            ctk.CTkLabel(
                logs_frame,
                text="No recent logs",
                font=("Helvetica", 12)
            ).pack(pady=10)
        else:
            for log in logs:
                log_frame = ctk.CTkFrame(logs_frame)
                log_frame.pack(fill="x", pady=2)
                
                ctk.CTkLabel(
                    log_frame,
                    text=f"📝 {log['event']}",
                    font=("Helvetica", 12)
                ).pack(side="left", padx=5)
                
                ctk.CTkLabel(
                    log_frame,
                    text=log['timestamp'],
                    font=("Helvetica", 12),
                    text_color="gray"
                ).pack(side="right", padx=5)

    def setup_status_card(self, parent, row, col):
        card = self.create_card(parent, "System Status")
        card.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

        # Add View Details button
        view_btn = ctk.CTkButton(
            card,
            text="View Details",
            command=self.master.show_admin_window,
            width=100,
            height=30,
            font=("Helvetica", 12),
            fg_color="transparent",
            hover_color=("gray70", "gray30")
        )
        view_btn.pack(anchor="e", padx=10)

        # Resource Limits
        limits_frame = ctk.CTkFrame(card, fg_color="transparent")
        limits_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(
            limits_frame,
            text="Resource Limits",
            font=("Helvetica", 14, "bold")
        ).pack(anchor="w", pady=5)

        # CPU Limit
        cpu_limit = self.resource_monitor.resource_limits.get('cpu', 50)
        ctk.CTkLabel(
            limits_frame,
            text=f"CPU Limit: {cpu_limit}%",
            font=("Helvetica", 12)
        ).pack(anchor="w")

        # Memory Limit
        memory_limit = self.resource_monitor.resource_limits.get('memory', 70)
        ctk.CTkLabel(
            limits_frame,
            text=f"Memory Limit: {memory_limit}%",
            font=("Helvetica", 12)
        ).pack(anchor="w")

        # Whitelist Count
        whitelist_frame = ctk.CTkFrame(card, fg_color="transparent")
        whitelist_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(
            whitelist_frame,
            text="Whitelisted Processes",
            font=("Helvetica", 14, "bold")
        ).pack(anchor="w", pady=5)
        
        count = len(self.resource_monitor.process_whitelist)
        ctk.CTkLabel(
            whitelist_frame,
            text=f"Total: {count} processes",
            font=("Helvetica", 12)
        ).pack(anchor="w")

    def start_monitoring(self):
        self.update_resources()

    def update_resources(self):
        try:
            # Update CPU
            cpu_percent = psutil.cpu_percent()
            self.cpu_progress.set(cpu_percent / 100)
            self.cpu_label.configure(text=f"{cpu_percent:.1f}%")
            self.cpu_stat_label.configure(text=f"{cpu_percent:.1f}%")
            
            # Update Memory
            memory = psutil.virtual_memory()
            self.memory_progress.set(memory.percent / 100)
            self.memory_label.configure(text=f"{memory.percent:.1f}%")
            self.memory_stat_label.configure(text=f"{memory.percent:.1f}%")
            
        except Exception as e:
            print(f"Error updating dashboard resources: {e}")
        
        if self.winfo_exists():
            self.after(1000, self.update_resources)

    def on_close(self):
        # Cleanup code here
        pass 