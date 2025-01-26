import customtkinter as ctk

class AlertsWindow(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.resource_monitor = self.master.current_window.resource_monitor
        
        self.setup_ui()
        self.start_monitoring()

    def setup_ui(self):
        # Create main container
        main_container = ctk.CTkFrame(self)
        main_container.pack(fill="both", expand=True)

        # Create sidebar
        sidebar = ctk.CTkFrame(main_container, width=200)
        sidebar.pack(side="left", fill="y", padx=10, pady=10)
        sidebar.pack_propagate(False)

        # App title in sidebar
        ctk.CTkLabel(
            sidebar,
            text="IDS Dashboard",
            font=("Helvetica", 20, "bold")
        ).pack(pady=20)

        # Navigation buttons in sidebar with Home and Back buttons at top
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

        # Main content area
        content_area = ctk.CTkFrame(main_container)
        content_area.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Title and refresh button
        header_frame = ctk.CTkFrame(content_area, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(
            header_frame,
            text="System Alerts",
            font=("Helvetica", 24, "bold")
        ).pack(side="left")

        refresh_btn = ctk.CTkButton(
            header_frame,
            text="Refresh",
            command=self.refresh_alerts,
            width=100
        )
        refresh_btn.pack(side="right")

        # Create alerts table
        self.setup_alerts_table(content_area)

    def setup_alerts_table(self, parent):
        if hasattr(self, 'table_frame'):
            self.table_frame.destroy()

        # Create table container
        self.table_frame = ctk.CTkFrame(parent)
        self.table_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Configure grid weights
        self.table_frame.grid_columnconfigure(0, weight=1)  # Time
        self.table_frame.grid_columnconfigure(1, weight=1)  # Priority
        self.table_frame.grid_columnconfigure(2, weight=2)  # Process
        self.table_frame.grid_columnconfigure(3, weight=3)  # Details

        # Headers
        headers = ["Time", "Priority", "Process", "Details"]
        header_bg = "gray25"
        
        for col, header in enumerate(headers):
            header_label = ctk.CTkLabel(
                self.table_frame,
                text=header,
                font=("Helvetica", 12, "bold"),
                fg_color=header_bg,
                corner_radius=6
            )
            header_label.grid(row=0, column=col, sticky="nsew", padx=2, pady=2)

        if not self.resource_monitor.alerts:
            no_alerts_label = ctk.CTkLabel(
                self.table_frame,
                text="No alerts found",
                font=("Helvetica", 12)
            )
            no_alerts_label.grid(row=1, column=0, columnspan=4, pady=20)
            return

        # Add alerts
        for row, alert in enumerate(self.resource_monitor.alerts, start=1):
            row_bg = "gray17" if row % 2 == 0 else "gray20"
            
            # Time
            time_label = ctk.CTkLabel(
                self.table_frame,
                text=alert["time"],
                font=("Helvetica", 12),
                fg_color=row_bg,
                corner_radius=6
            )
            time_label.grid(row=row, column=0, sticky="nsew", padx=2, pady=2)

            # Priority
            priority_color = "#FF4444" if alert["priority"] == "High" else "#FFA500"
            priority_label = ctk.CTkLabel(
                self.table_frame,
                text=alert["priority"],
                text_color=priority_color,
                font=("Helvetica", 12),
                fg_color=row_bg,
                corner_radius=6
            )
            priority_label.grid(row=row, column=1, sticky="nsew", padx=2, pady=2)

            # Process
            process_label = ctk.CTkLabel(
                self.table_frame,
                text=alert["process_name"],
                font=("Helvetica", 12),
                fg_color=row_bg,
                corner_radius=6
            )
            process_label.grid(row=row, column=2, sticky="nsew", padx=2, pady=2)

            # Details
            details_frame = ctk.CTkFrame(self.table_frame, fg_color=row_bg)
            details_frame.grid(row=row, column=3, sticky="nsew", padx=2, pady=2)
            details_frame.grid_columnconfigure(0, weight=1)

            details_text = alert["details"].replace('\n', ' | ')
            details_label = ctk.CTkLabel(
                details_frame,
                text=details_text,
                font=("Helvetica", 12),
                wraplength=400,  # Adjust based on your needs
                justify="left"
            )
            details_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)

    def refresh_alerts(self):
        self.setup_alerts_table(self.table_frame.master)

    def start_monitoring(self):
        self.check_alerts()

    def check_alerts(self):
        # Check for new alerts
        alerts = self.resource_monitor.check_resources()
        if alerts:
            self.refresh_alerts()
        
        # Schedule next check if window still exists
        if self.winfo_exists():
            self.after(2000, self.check_alerts)

    def on_close(self):
        # Cleanup code here
        pass 