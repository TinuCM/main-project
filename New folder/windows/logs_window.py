import customtkinter as ctk

class LogsWindow(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.resource_monitor = self.master.current_window.resource_monitor
        
        self.setup_ui()

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
            text="System Logs",
            font=("Helvetica", 24, "bold")
        ).pack(side="left")

        refresh_btn = ctk.CTkButton(
            header_frame,
            text="Refresh",
            command=self.refresh_logs,
            width=100
        )
        refresh_btn.pack(side="right")

        # Create logs table
        self.setup_logs_table(content_area)

    def setup_logs_table(self, content_area):
        if hasattr(self, 'table_frame'):
            self.table_frame.destroy()

        self.table_frame = ctk.CTkFrame(content_area)
        self.table_frame.pack(fill="x", pady=(0, 2))

        # Headers
        headers = ["Time", "Event", "Severity", "Status", "Action", "User"]
        header_frame = ctk.CTkFrame(self.table_frame, fg_color="gray25")
        header_frame.pack(fill="x", pady=1)

        for header in headers:
            cell = ctk.CTkLabel(
                header_frame,
                text=header,
                font=("Helvetica", 12, "bold")
            )
            cell.pack(side="left", expand=True, padx=5, pady=5)

        # Logs
        if not self.resource_monitor.logs:
            ctk.CTkLabel(
                self.table_frame,
                text="No logs found",
                font=("Helvetica", 12)
            ).pack(pady=20)
            return

        for i, log in enumerate(self.resource_monitor.logs):
            row_color = "gray17" if i % 2 == 0 else "gray20"
            row = ctk.CTkFrame(self.table_frame, fg_color=row_color)
            row.pack(fill="x", pady=1)

            # Time
            ctk.CTkLabel(
                row,
                text=log["timestamp"],
                font=("Helvetica", 12)
            ).pack(side="left", expand=True, padx=5, pady=5)

            # Event
            ctk.CTkLabel(
                row,
                text=log["event"],
                font=("Helvetica", 12)
            ).pack(side="left", expand=True, padx=5, pady=5)

            # Severity
            severity_color = "#FF4444" if log["severity"] == "High" else "#FFA500"
            ctk.CTkLabel(
                row,
                text=log["severity"],
                text_color=severity_color,
                font=("Helvetica", 12)
            ).pack(side="left", expand=True, padx=5, pady=5)

            # Status
            status_color = {
                "Alert": "#FF4444",
                "Warning": "#FFA500",
                "Info": "#00CC00"
            }.get(log["status"], None)
            
            ctk.CTkLabel(
                row,
                text=log["status"],
                text_color=status_color,
                font=("Helvetica", 12)
            ).pack(side="left", expand=True, padx=5, pady=5)

            # Action
            ctk.CTkLabel(
                row,
                text=log["action"],
                font=("Helvetica", 12)
            ).pack(side="left", expand=True, padx=5, pady=5)

            # User
            ctk.CTkLabel(
                row,
                text=log["user"],
                font=("Helvetica", 12)
            ).pack(side="left", expand=True, padx=5, pady=5)

    def refresh_logs(self):
        self.setup_logs_table()

    def on_close(self):
        # Cleanup code here
        pass 