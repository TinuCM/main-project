import customtkinter as ctk
from tkinter import messagebox

class AdminWindow(ctk.CTkFrame):
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

        # Title
        ctk.CTkLabel(
            content_area,
            text="Admin Panel",
            font=("Helvetica", 24, "bold")
        ).pack(pady=(0, 20), padx=10, anchor="w")

        # Create scrollable content frame
        self.content_frame = ctk.CTkScrollableFrame(content_area)
        self.content_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Resource Limits Section
        self.setup_resource_limits_section()
        
        # Process Whitelist Section
        self.setup_process_whitelist_section()

    def setup_resource_limits_section(self):
        # Resource Limits Frame
        limits_frame = ctk.CTkFrame(self.content_frame)
        limits_frame.pack(fill="x", pady=10, padx=5)

        # Title with line separator
        ctk.CTkLabel(
            limits_frame,
            text="Resource Limits",
            font=("Helvetica", 16, "bold")
        ).pack(pady=10, padx=10)

        # CPU Limit
        cpu_frame = ctk.CTkFrame(limits_frame)
        cpu_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(
            cpu_frame,
            text="CPU Usage Limit (%)",
            font=("Helvetica", 12)
        ).pack(side="left", padx=5)

        self.cpu_limit = ctk.CTkEntry(
            cpu_frame,
            width=100,
            placeholder_text="e.g. 80"
        )
        self.cpu_limit.pack(side="right", padx=5)
        self.cpu_limit.insert(0, str(self.resource_monitor.resource_limits.get('cpu', 50)))

        # Memory Limit
        memory_frame = ctk.CTkFrame(limits_frame)
        memory_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(
            memory_frame,
            text="Memory Usage Limit (%)",
            font=("Helvetica", 12)
        ).pack(side="left", padx=5)

        self.memory_limit = ctk.CTkEntry(
            memory_frame,
            width=100,
            placeholder_text="e.g. 90"
        )
        self.memory_limit.pack(side="right", padx=5)
        self.memory_limit.insert(0, str(self.resource_monitor.resource_limits.get('memory', 70)))

        # Update Limits Button
        ctk.CTkButton(
            limits_frame,
            text="Update Limits",
            command=self.update_resource_limits
        ).pack(pady=10)

    def setup_process_whitelist_section(self):
        # Process Whitelist Frame
        whitelist_frame = ctk.CTkFrame(self.content_frame)
        whitelist_frame.pack(fill="x", pady=10, padx=5)

        # Title
        ctk.CTkLabel(
            whitelist_frame,
            text="Process Whitelist",
            font=("Helvetica", 16, "bold")
        ).pack(pady=10, padx=10)

        # Add Process Frame
        add_frame = ctk.CTkFrame(whitelist_frame)
        add_frame.pack(fill="x", padx=10, pady=5)

        self.process_entry = ctk.CTkEntry(
            add_frame,
            placeholder_text="Enter process name (e.g., chrome.exe)",
            width=300
        )
        self.process_entry.pack(side="left", padx=5, expand=True)

        ctk.CTkButton(
            add_frame,
            text="Add Process",
            command=self.add_process
        ).pack(side="right", padx=5)

        # Whitelist Display Frame
        self.whitelist_display = ctk.CTkScrollableFrame(whitelist_frame, height=200)
        self.whitelist_display.pack(fill="x", padx=10, pady=5)

        self.refresh_whitelist()

    def refresh_whitelist(self):
        # Clear existing widgets
        for widget in self.whitelist_display.winfo_children():
            widget.destroy()

        # Add header
        header_frame = ctk.CTkFrame(self.whitelist_display)
        header_frame.pack(fill="x", pady=2)

        ctk.CTkLabel(
            header_frame,
            text="Whitelisted Processes",
            font=("Helvetica", 12, "bold")
        ).pack(side="left", padx=5)

        # Add processes
        for process in self.resource_monitor.process_whitelist:
            process_frame = ctk.CTkFrame(self.whitelist_display)
            process_frame.pack(fill="x", pady=2)

            ctk.CTkLabel(
                process_frame,
                text=process,
                font=("Helvetica", 12)
            ).pack(side="left", padx=5)

            ctk.CTkButton(
                process_frame,
                text="Remove",
                command=lambda p=process: self.remove_process(p),
                width=80,
                height=25
            ).pack(side="right", padx=5)

    def update_resource_limits(self):
        try:
            cpu = float(self.cpu_limit.get())
            memory = float(self.memory_limit.get())

            if not (0 <= cpu <= 100 and 0 <= memory <= 100):
                messagebox.showerror("Error", "Limits must be between 0 and 100")
                return

            self.resource_monitor.resource_limits['cpu'] = cpu
            self.resource_monitor.resource_limits['memory'] = memory

            # Save to file
            with open('resource_limits.txt', 'w') as f:
                f.write(f"cpu,{cpu}\n")
                f.write(f"memory,{memory}\n")

            messagebox.showinfo("Success", "Resource limits updated successfully")

        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers")

    def add_process(self):
        process = self.process_entry.get().strip()
        if not process:
            messagebox.showerror("Error", "Please enter a process name")
            return

        if process in self.resource_monitor.process_whitelist:
            messagebox.showerror("Error", "Process already in whitelist")
            return

        self.resource_monitor.process_whitelist.append(process)
        
        # Save to file
        with open('process_whitelist.txt', 'a') as f:
            f.write(f"{process}\n")

        self.process_entry.delete(0, 'end')
        self.refresh_whitelist()
        messagebox.showinfo("Success", f"Added {process} to whitelist")

    def remove_process(self, process):
        if messagebox.askyesno("Confirm", f"Remove {process} from whitelist?"):
            self.resource_monitor.process_whitelist.remove(process)
            
            # Save updated list to file
            with open('process_whitelist.txt', 'w') as f:
                for p in self.resource_monitor.process_whitelist:
                    f.write(f"{p}\n")
            
            self.refresh_whitelist()
            messagebox.showinfo("Success", f"Removed {process} from whitelist")

    def on_close(self):
        # Cleanup code here
        pass 