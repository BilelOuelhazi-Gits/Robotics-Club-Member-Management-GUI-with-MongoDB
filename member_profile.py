import customtkinter as ctk
import pymongo
from tkinter import messagebox


class MemberProfilePage:
    def __init__(self, container, member_list_frame):
        self.container = container
        self.member_list_frame = member_list_frame
        self.current_member = None  # Store the current member's data

        # Create Member Profile Page Frame
        self.profile_frame = ctk.CTkFrame(container, fg_color="#2b2b2b")
        self.profile_frame.grid(row=0, column=0, sticky="nsew")

        # Back Button
        back_btn = ctk.CTkButton(self.profile_frame, text="Back", command=self.go_back, **{
            'fg_color': '#444', 'text_color': 'white', 'font': ctk.CTkFont('Arial', 12, 'bold'), 'width': 12, 'height': 2,
            'corner_radius': 8, 'hover_color': '#555'
        })
        back_btn.grid(row=0, column=0, padx=20, pady=20, sticky="w")

        # Title Label
        self.title_label = ctk.CTkLabel(self.profile_frame, text="", font=ctk.CTkFont('Arial', 18, 'bold'), text_color="white")
        self.title_label.grid(row=1, column=0, columnspan=2, pady=10)

        # Data Labels and Entry Fields
        self.fields = ["Name", "Last Name", "Email", "Payment Done"]
        self.entries = {}
        for i, field in enumerate(self.fields, start=2):
            label = ctk.CTkLabel(self.profile_frame, text=f"{field}:", font=ctk.CTkFont('Arial', 12), text_color="white")
            label.grid(row=i, column=0, padx=10, pady=5, sticky="e")

            entry = ctk.CTkEntry(self.profile_frame, font=ctk.CTkFont('Arial', 12), width=250)
            entry.grid(row=i, column=1, padx=20, pady=5)
            self.entries[field.lower().replace(" ", "_")] = entry

        # Role Dropdown Menu
        role_label = ctk.CTkLabel(self.profile_frame, text="Role:", font=ctk.CTkFont('Arial', 12), text_color="white")
        role_label.grid(row=len(self.fields) + 2, column=0, padx=10, pady=5, sticky="e")

        self.roles = [
            "Member",
            "Core Team - President", "Core Team - Vice President", "Core Team - Secretary", "Core Team - Treasurer",
            "Operational Team - Planning and Logistics Coordinator",
            "Operational Team - Content and Program Coordinator",
            "Operational Team - Promotion and Outreach Coordinator", "Operational Team - Technical Lead",
            "Operational Team - Training Coordinator",
            "Support Team - Marketing Manager", "Support Team - Social Media Manager",
            "Support Team - Sponsorship and Fundraising Manager"
        ]
        self.role_var = ctk.StringVar(value="Member")
        self.role_dropdown = ctk.CTkComboBox(self.profile_frame, variable=self.role_var, values=self.roles, font=ctk.CTkFont('Arial', 12))
        self.role_dropdown.grid(row=len(self.fields) + 2, column=1, padx=20, pady=5)

        # Points Section: Activity-based point addition
        self.points_label = ctk.CTkLabel(self.profile_frame, text="Add Points Based on Activities", font=ctk.CTkFont('Arial', 14, 'bold'), text_color="white")
        self.points_label.grid(row=len(self.fields) + 4, column=0, columnspan=2, pady=10)

        # Dropdown menu for selecting activity
        self.activities = {
            "Attending Club Meetings": 3,
            "Contributing to Team Projects": 10,
            "Leading a Project/Team": 30,
            "Mentoring New Members": 20,
            "Presenting Work": 30,
            "Developing New Ideas or Systems": 30,
            "Participating in Local/Regional Competitions": 5,
            "1st Place in Local/Regional Competition": 20,
            "2nd Place in Local/Regional Competition": 15,
            "3rd Place in Local/Regional Competition": 10,
            "Participating in National/International Competitions": 10,
            "1st Place in National/International Competition": 50,
            "2nd Place in National/International Competition": 35,
            "3rd Place in National/International Competition": 20,
            "Community Outreach or Volunteer Work": 10,
            "Recruiting New Members": 10,
            "Active Participation in Discussions or Decisions": 5
        }

        self.activity_var = ctk.StringVar(value="Select Activity")
        self.activity_dropdown = ctk.CTkComboBox(self.profile_frame, variable=self.activity_var, values=list(self.activities.keys()), font=ctk.CTkFont('Arial', 12))
        self.activity_dropdown.grid(row=len(self.fields) + 5, column=0, columnspan=2, padx=20, pady=5)

        # Add Points Button
        add_points_btn = ctk.CTkButton(self.profile_frame, text="Add Points", command=self.add_points, **{
            'fg_color': '#1e824c', 'text_color': 'white', 'font': ctk.CTkFont('Arial', 12, 'bold'), 'width': 12, 'height': 2,
            'corner_radius': 8, 'hover_color': '#2ecc71'
        })
        add_points_btn.grid(row=len(self.fields) + 6, column=0, columnspan=2, padx=20, pady=10)

        # Save Button
        save_btn = ctk.CTkButton(self.profile_frame, text="Save", command=self.save_changes, **{
            'fg_color': '#1e824c', 'text_color': 'white', 'font': ctk.CTkFont('Arial', 12, 'bold'), 'width': 12, 'height': 2,
            'corner_radius': 8, 'hover_color': '#2ecc71'
        })
        save_btn.grid(row=len(self.fields) + 7, column=1, padx=20, pady=20, sticky="e")

    def update_member_data(self, member):
        """Update the profile page with the selected member's data."""
        self.current_member = member  # Store the current member data
        self.title_label.configure(text=f"Profile of {member['name']} {member['last_name']}")


        # Populate fields with existing data
        for field in self.entries:
            self.entries[field].delete(0, ctk.END)
            self.entries[field].insert(0, member[field])

        # Set the role dropdown value
        self.role_var.set(member["role"])

    def add_points(self):
        """Add points to the current member based on the selected activity."""
        selected_activity = self.activity_var.get()
        if selected_activity == "Select Activity":
            messagebox.showerror("Error", "Please select a valid activity.")
            return

        points_to_add = self.activities.get(selected_activity)
        if points_to_add is None:
            messagebox.showerror("Error", "Error in retrieving points for selected activity.")
            return

        if self.current_member is None:
            messagebox.showerror("Error", "No member selected.")
            return

        # Update points
        current_points = self.current_member.get("points", 0)
        new_points = current_points + points_to_add
        self.current_member["points"] = new_points

        # Update the points display in the member profile
        messagebox.showinfo("Points Added",
                            f"{points_to_add} points added for {selected_activity}. Total points: {new_points}")

    def save_changes(self):
        """Save changes to the database."""
        updated_data = {
            "name": self.entries["name"].get(),
            "last_name": self.entries["last_name"].get(),
            "email": self.entries["email"].get(),
            "role": self.role_var.get(),
            "payment_done": self.entries["payment_done"].get(),
            "points": self.current_member.get("points", 0),  # Ensure points are saved
        }

        try:
            client = pymongo.MongoClient("mongodb://localhost:27017/")
            db = client["robotics_club"]
            collection = db["members"]

            # Update the database
            result = collection.update_one(
                {"_id": self.current_member["_id"]},  # Find member by their unique ID
                {"$set": updated_data}  # Update fields with new data
            )

            if result.modified_count > 0:
                messagebox.showinfo("Success", "Member information updated successfully!")
            else:
                messagebox.showinfo("No Changes", "No changes were made to the member information.")

            # Update the local current_member data
            self.current_member.update(updated_data)

        except pymongo.errors.ConnectionError as e:
            messagebox.showerror("Database Error", f"Could not update data in the database: {str(e)}")

    def go_back(self):
        """Return to the member list."""
        self.member_list_frame.tkraise()

    def show_frame(self, frame):
        """Show the given frame."""
        self.container.configure(bg="#2b2b2b")
        self.container.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()
