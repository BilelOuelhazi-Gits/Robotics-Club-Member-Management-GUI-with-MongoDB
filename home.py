import customtkinter as ctk
from add_member import AddMemberPage
from member_list import MemberListPage

class HomePage:
    def __init__(self, container):
        self.container = container

        # Set appearance mode and theme
        ctk.set_appearance_mode("dark")  # "light" for light mode
        ctk.set_default_color_theme("dark-blue")  # Options: "blue", "green", "dark-blue"

        # Configure the container (main window) to stretch and center the content
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Create home frame with a gradient-style background
        self.home_frame = ctk.CTkFrame(container, fg_color="#1a1a1a")
        self.home_frame.grid(row=0, column=0, sticky="nsew")  # Stretch the frame to fill the window

        # Centering the home_frame content using grid configuration
        self.home_frame.grid_rowconfigure(0, weight=1)
        self.home_frame.grid_rowconfigure(1, weight=1)
        self.home_frame.grid_rowconfigure(2, weight=1)
        self.home_frame.grid_columnconfigure(0, weight=1)

        # Add a title label with a modern font
        title_label = ctk.CTkLabel(
            self.home_frame,
            text="Robotics Club Management",
            font=ctk.CTkFont("Arial", size=24, weight="bold"),
            text_color="#ffffff",
        )
        title_label.grid(row=0, column=0, pady=(30, 10), sticky="nsew")  # Center title

        # Button frame for better alignment
        button_frame = ctk.CTkFrame(self.home_frame, fg_color="#1a1a1a")
        button_frame.grid(row=1, column=0, pady=30, sticky="nsew")  # Stretch button frame

        # Add Member button with hover effect (adjusted size)
        add_member_btn = ctk.CTkButton(
            button_frame,
            text="Add Member",
            command=lambda: self.show_frame(self.add_member_page.add_member_frame),
            width=200,  # Adjusted width
            height=40,  # Adjusted height
            font=ctk.CTkFont("Arial", size=14, weight="bold"),  # Smaller font
            fg_color="#005f73",
            hover_color="#0a9396",  # Slightly brighter on hover
            corner_radius=8,
        )
        add_member_btn.pack(padx=20, pady=10)  # Center button within its frame

        # View Members button with hover effect (adjusted size)
        view_members_btn = ctk.CTkButton(
            button_frame,
            text="View Members",
            command=lambda: self.show_frame(self.member_list_page.member_list_frame),
            width=200,  # Adjusted width
            height=40,  # Adjusted height
            font=ctk.CTkFont("Arial", size=14, weight="bold"),  # Smaller font
            fg_color="#005f73",
            hover_color="#0a9396",
            corner_radius=8,
        )
        view_members_btn.pack(padx=20, pady=10)  # Center button within its frame

        # Add a decorative footer label
        footer_label = ctk.CTkLabel(
            self.home_frame,
            text="© 2024 NEXT-GEN TEKUP",
            font=ctk.CTkFont("Arial", size=12),
            text_color="#888888",
        )
        footer_label.grid(row=2, column=0, pady=(20, 10), sticky="nsew")  # Center footer

        # Initialize AddMemberPage and MemberListPage
        self.add_member_page = AddMemberPage(self.container, self.home_frame)
        self.member_list_page = MemberListPage(self.container, self.home_frame)

    def show_frame(self, frame):
        frame.tkraise()
