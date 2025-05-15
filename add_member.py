import customtkinter as ctk
import pymongo
from tkinter import messagebox

class AddMemberPage:
    def __init__(self, container, home_frame):
        self.container = container
        self.home_frame = home_frame

        # Create Add Member Page Frame
        self.add_member_frame = ctk.CTkFrame(container, fg_color="#2b2b2b")
        self.add_member_frame.grid(row=0, column=0, sticky="nsew")

        # Back Button
        back_btn = ctk.CTkButton(self.add_member_frame, text="Back", command=self.go_home, **{
            'fg_color': '#444', 'text_color': 'white', 'font': ctk.CTkFont('Arial', 12, 'bold'), 'width': 12, 'height': 2,
            'corner_radius': 8, 'hover_color': '#555'
        })
        back_btn.grid(row=0, column=0, padx=20, pady=20, sticky="w")

        # Title Label
        title_label = ctk.CTkLabel(self.add_member_frame, text="Add Member", font=ctk.CTkFont('Arial', 18, 'bold'), text_color="white")
        title_label.grid(row=1, column=0, columnspan=2, pady=10)

        # Name Entry
        name_label = ctk.CTkLabel(self.add_member_frame, text="Name:", font=ctk.CTkFont('Arial', 12), text_color="white")
        name_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.name_entry = ctk.CTkEntry(self.add_member_frame, font=ctk.CTkFont('Arial', 12), width=250)
        self.name_entry.grid(row=2, column=1, padx=20, pady=5)

        # Last Name Entry
        last_name_label = ctk.CTkLabel(self.add_member_frame, text="Last Name:", font=ctk.CTkFont('Arial', 12), text_color="white")
        last_name_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.last_name_entry = ctk.CTkEntry(self.add_member_frame, font=ctk.CTkFont('Arial', 12), width=250)
        self.last_name_entry.grid(row=3, column=1, padx=20, pady=5)

        # Email Entry
        email_label = ctk.CTkLabel(self.add_member_frame, text="Email:", font=ctk.CTkFont('Arial', 12), text_color="white")
        email_label.grid(row=4, column=0, padx=10, pady=5, sticky="e")
        self.email_entry = ctk.CTkEntry(self.add_member_frame, font=ctk.CTkFont('Arial', 12), width=250)
        self.email_entry.grid(row=4, column=1, padx=20, pady=5)

        # Role Dropdown
        role_label = ctk.CTkLabel(self.add_member_frame, text="Role:", font=ctk.CTkFont('Arial', 12), text_color="white")
        role_label.grid(row=5, column=0, padx=10, pady=5, sticky="e")
        self.role_var = ctk.StringVar()
        role_options = [
            "Member", "Core Team - President", "Core Team - Vice President", "Core Team - Secretary", "Core Team - Treasurer",
            "Operational Team - Planning and Logistics Coordinator", "Operational Team - Content and Program Coordinator",
            "Operational Team - Promotion and Outreach Coordinator", "Operational Team - Technical Lead", "Operational Team - Training Coordinator",
            "Support Team - Marketing Manager", "Support Team - Social Media Manager", "Support Team - Sponsorship and Fundraising Manager"
        ]
        self.role_dropdown = ctk.CTkComboBox(self.add_member_frame, variable=self.role_var, values=role_options, font=ctk.CTkFont('Arial', 12))
        self.role_dropdown.grid(row=5, column=1, padx=20, pady=5)

        # Payment Done Dropdown
        payment_label = ctk.CTkLabel(self.add_member_frame, text="Payment Done:", font=ctk.CTkFont('Arial', 12), text_color="white")
        payment_label.grid(row=6, column=0, padx=10, pady=5, sticky="e")
        self.payment_var = ctk.StringVar()
        payment_options = ['Yes', 'No']
        self.payment_dropdown = ctk.CTkComboBox(self.add_member_frame, variable=self.payment_var, values=payment_options, font=ctk.CTkFont('Arial', 12))
        self.payment_dropdown.grid(row=6, column=1, padx=20, pady=5)

        # Submit Button
        submit_btn = ctk.CTkButton(self.add_member_frame, text="Submit", command=self.submit_member, **{
            'fg_color': '#444', 'text_color': 'white', 'font': ctk.CTkFont('Arial', 14, 'bold'), 'width': 20, 'height': 2,
            'corner_radius': 8, 'hover_color': '#555'
        })
        submit_btn.grid(row=7, column=0, columnspan=2, pady=20)

        # Adjust row and column configuration for resizing
        self.add_member_frame.grid_rowconfigure(1, weight=1)
        self.add_member_frame.grid_rowconfigure(7, weight=1)
        self.add_member_frame.grid_columnconfigure(1, weight=1)

    def show_frame(self, frame):
        frame.tkraise()

    def go_home(self):
        self.home_frame.tkraise()

    def submit_member(self):
        # Extracting data from the form fields
        name = self.name_entry.get()
        last_name = self.last_name_entry.get()
        email = self.email_entry.get()
        role = self.role_var.get()
        payment_done = self.payment_var.get()

        if not name or not last_name or not email or not role or not payment_done:
            messagebox.showerror("Error", "All fields must be filled out.")
            return

        # Insert member data into MongoDB, including default points (10 points)
        member_data = {
            "name": name,
            "last_name": last_name,
            "email": email,
            "role": role,
            "payment_done": payment_done,
            "points": 10  # Default points for new members
        }

        try:
            # Connect to MongoDB (ensure MongoDB is running and the database exists)
            client = pymongo.MongoClient("mongodb://localhost:27017/")
            db = client["robotics_club"]
            collection = db["members"]

            # Insert data into the collection
            collection.insert_one(member_data)
            messagebox.showinfo("Success", "Member added successfully!")

            # Clear the form fields after submission
            self.name_entry.delete(0, ctk.END)
            self.last_name_entry.delete(0, ctk.END)
            self.email_entry.delete(0, ctk.END)
            self.role_var.set('')
            self.payment_var.set('')

        except pymongo.errors.ConnectionError as e:
            messagebox.showerror("Database Error", f"Could not connect to the database: {str(e)}")
