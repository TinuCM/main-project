import customtkinter as ctk
from tkinter import messagebox

class LoginWindow(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        
        # Valid credentials
        self.VALID_CREDENTIALS = {
            "admin": "admin123",
            "user1": "user123",
            "": ""
        }
        
        self.setup_ui()

    def setup_ui(self):
        # Create a centered frame for the login form
        frame = ctk.CTkFrame(self, width=400, height=400, corner_radius=15)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        # Title
        ctk.CTkLabel(frame, text="Login", font=("Helvetica", 24, "bold")).pack(pady=20)

        # Username input
        ctk.CTkLabel(frame, text="Username:", font=("Helvetica", 14)).pack(pady=5)
        self.login_username = ctk.CTkEntry(frame, font=("Helvetica", 14), width=300)
        self.login_username.pack(pady=5)
        
        # Password input
        ctk.CTkLabel(frame, text="Password:", font=("Helvetica", 14)).pack(pady=5)
        self.login_password = ctk.CTkEntry(frame, show="*", font=("Helvetica", 14), width=300)
        self.login_password.pack(pady=5)
        
        # Login button
        login_button = ctk.CTkButton(
            frame, 
            text="Login", 
            font=("Helvetica", 14), 
            command=self.handle_login
        )
        login_button.pack(pady=20)

    def handle_login(self):
        username = self.login_username.get()
        password = self.login_password.get()

        if username in self.VALID_CREDENTIALS and self.VALID_CREDENTIALS[username] == password:
            self.master.show_home_window()
        else:
            messagebox.showerror("Error", "Invalid username or password!") 