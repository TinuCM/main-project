import customtkinter as ctk
from windows.home_window import HomeWindow
from windows.login_window import LoginWindow
from windows.system_window import SystemWindow
from windows.alerts_window import AlertsWindow
from windows.logs_window import LogsWindow
from windows.admin_window import AdminWindow

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window setup
        self.title("Intrusion Detection System")
        self.geometry("1024x720")
        
        # Global appearance settings
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("dark-blue")
        
        # Add page history
        self.page_history = []
        self.current_page = None

        # Show login window first
        self.current_window = None
        self.show_login_window()

    def navigate_to(self, window_class):
        """Navigate to a new page and store history"""
        if self.current_window:
            self.page_history.append(type(self.current_window))
        self.clear_current_window()
        self.current_window = window_class(self)
        self.current_window.pack(fill="both", expand=True)

    def go_back(self):
        """Navigate to previous page"""
        if self.page_history:
            previous_window = self.page_history.pop()
            self.clear_current_window()
            self.current_window = previous_window(self)
            self.current_window.pack(fill="both", expand=True)

    def show_login_window(self):
        self.page_history.clear()  # Clear history when logging out
        self.clear_current_window()
        self.current_window = LoginWindow(self)
        self.current_window.pack(fill="both", expand=True)

    def show_system_window(self):
        self.navigate_to(SystemWindow)

    def show_alerts_window(self):
        self.navigate_to(AlertsWindow)

    def show_logs_window(self):
        self.navigate_to(LogsWindow)

    def show_admin_window(self):
        self.navigate_to(AdminWindow)

    def show_home_window(self):
        self.navigate_to(HomeWindow)

    def clear_current_window(self):
        if self.current_window:
            self.current_window.destroy()

if __name__ == "__main__":
    app = MainApp()
    app.mainloop() 