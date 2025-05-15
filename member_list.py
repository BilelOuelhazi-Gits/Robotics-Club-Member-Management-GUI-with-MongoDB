import customtkinter as ctk
import pymongo
from tkinter import messagebox
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from member_profile import MemberProfilePage  # Import the MemberProfilePage class

class MemberListPage:
    def __init__(self, container, home_frame):
        self.container = container
        self.home_frame = home_frame

        # Create Member List Page Frame
        self.member_list_frame = ctk.CTkFrame(container, fg_color="#2b2b2b")
        self.member_list_frame.grid(row=0, column=0, sticky="nsew")

        # Back Button
        back_btn = ctk.CTkButton(self.member_list_frame, text="Back", command=self.go_home, **{
            'fg_color': '#444', 'text_color': 'white', 'font': ctk.CTkFont('Arial', 12, 'bold'), 'width': 12, 'height': 2,
            'corner_radius': 8, 'hover_color': '#555'
        })
        back_btn.grid(row=0, column=0, padx=20, pady=20, sticky="w")

        # Refresh Button
        refresh_btn = ctk.CTkButton(self.member_list_frame, text="Refresh", command=self.refresh_data, **{
            'fg_color': '#444', 'text_color': 'white', 'font': ctk.CTkFont('Arial', 12, 'bold'), 'width': 12, 'height': 2,
            'corner_radius': 8, 'hover_color': '#555'
        })
        refresh_btn.grid(row=0, column=1, padx=20, pady=20, sticky="e")

        # Export to PDF Button
        export_btn = ctk.CTkButton(self.member_list_frame, text="Export to PDF", command=self.export_to_pdf, **{
            'fg_color': '#444', 'text_color': 'white', 'font': ctk.CTkFont('Arial', 12, 'bold'), 'width': 12, 'height': 2,
            'corner_radius': 8, 'hover_color': '#555'
        })
        export_btn.grid(row=0, column=2, padx=20, pady=20, sticky="e")

        # Title Label
        title_label = ctk.CTkLabel(self.member_list_frame, text="Member List", font=ctk.CTkFont('Arial', 18, 'bold'), text_color="white")
        title_label.grid(row=1, column=0, columnspan=5, pady=10)

        # Create the table headers
        headers = ["Name", "Last Name", "Email", "Role", "Payment Done", "Points", "Rank", "Add Points"]
        self.header_labels = []
        for i, header in enumerate(headers):
            header_label = ctk.CTkLabel(self.member_list_frame, text=header, text_color="white", font=ctk.CTkFont('Arial', 12, 'bold'))
            header_label.grid(row=2, column=i, padx=10, pady=5, sticky="nsew")
            self.header_labels.append(header_label)

        # Data container for dynamically added rows
        self.data_rows = []

        # Initialize the MemberProfilePage
        self.profile_page = MemberProfilePage(self.container, self.member_list_frame)

        # Fetch and display the data from MongoDB
        self.display_member_data()

    def go_home(self):
        self.home_frame.tkraise()

    def refresh_data(self):
        """Clear and reload the member data."""
        # Remove existing data rows
        for row in self.data_rows:
            for widget in row:
                widget.destroy()
        self.data_rows.clear()

        # Reload data from the database
        self.display_member_data()

    def display_member_data(self):
        try:
            client = pymongo.MongoClient("mongodb://localhost:27017/")
            db = client["robotics_club"]
            collection = db["members"]

            members = collection.find()

            # Add the members' data to the table
            row = 3  # Start from the 3rd row (below the headers)

            for member in members:
                member_row = []

                # Name Button (clickable)
                member_row.append(
                    ctk.CTkButton(self.member_list_frame, text=member['name'], fg_color="#2b2b2b", text_color="white", font=ctk.CTkFont('Arial', 12),
                                  command=lambda m=member: self.open_member_profile(m)))
                member_row[-1].grid(row=row, column=0, padx=10, pady=5)

                # Last Name Label
                member_row.append(ctk.CTkLabel(self.member_list_frame, text=member['last_name'], text_color="white", font=ctk.CTkFont('Arial', 12)))
                member_row[-1].grid(row=row, column=1, padx=10, pady=5)

                # Email Label
                member_row.append(ctk.CTkLabel(self.member_list_frame, text=member['email'], text_color="white", font=ctk.CTkFont('Arial', 12)))
                member_row[-1].grid(row=row, column=2, padx=10, pady=5)

                # Role Label
                member_row.append(
                    ctk.CTkLabel(self.member_list_frame, text=member['role'], text_color="white", font=ctk.CTkFont('Arial', 12)))
                member_row[-1].grid(row=row, column=3, padx=10, pady=5)

                # Payment Done Label
                member_row.append(
                    ctk.CTkLabel(self.member_list_frame, text=member['payment_done'], text_color="white", font=ctk.CTkFont('Arial', 12)))
                member_row[-1].grid(row=row, column=4, padx=10, pady=5)

                # Points Label
                points = member.get('points', 0)
                member_row.append(
                    ctk.CTkLabel(self.member_list_frame, text=str(points), text_color="white", font=ctk.CTkFont('Arial', 12)))
                member_row[-1].grid(row=row, column=5, padx=10, pady=5)

                # Rank Label
                rank = self.get_rank(points)
                member_row.append(
                    ctk.CTkLabel(self.member_list_frame, text=rank, text_color="white", font=ctk.CTkFont('Arial', 12)))
                member_row[-1].grid(row=row, column=6, padx=10, pady=5)

                # Add Points Button (adds 3 points)
                add_points_btn = ctk.CTkButton(self.member_list_frame, text="Add 3 Points", fg_color="#444", text_color="white", font=ctk.CTkFont('Arial', 12),
                                               command=lambda m=member: self.add_points(m))
                add_points_btn.grid(row=row, column=7, padx=10, pady=5)

                # Add the row to the list of data rows
                self.data_rows.append(member_row)
                row += 1

        except pymongo.errors.ConnectionError as e:
            messagebox.showerror("Database Error", f"Could not fetch data from the database: {str(e)}")

    def get_rank(self, points):
        """Return the rank based on points."""
        if points >= 500:
            return "Cyborg (Level 7)"
        elif points >= 350:
            return "Elite (Level 6)"
        elif points >= 200:
            return "Techsmith (Level 5)"
        elif points >= 115:
            return "Senior (Level 4)"
        elif points >= 60:
            return "Innovator (Level 3)"
        elif points >= 30:
            return "Assembler (Level 2)"
        else:
            return "Explorer (Level 1)"

    def open_member_profile(self, member):
        """Open the member's profile page."""
        self.profile_page.update_member_data(member)
        self.profile_page.show_frame(self.profile_page.profile_frame)

    def add_points(self, member):
        """Add 3 points to the selected member and update the database."""
        try:
            client = pymongo.MongoClient("mongodb://localhost:27017/")
            db = client["robotics_club"]
            collection = db["members"]

            # Increment points by 3
            new_points = member.get('points', 0) + 3
            collection.update_one({"_id": member["_id"]}, {"$set": {"points": new_points}})

            # Refresh the member list to show updated points
            self.refresh_data()

        except pymongo.errors.ConnectionError as e:
            messagebox.showerror("Database Error", f"Could not update data in the database: {str(e)}")

    def export_to_pdf(self):
        """Export the member data to a PDF file."""
        try:
            client = pymongo.MongoClient("mongodb://localhost:27017/")
            db = client["robotics_club"]
            collection = db["members"]
            members = collection.find()

            # Create a new PDF
            file_name = "member_list.pdf"
            c = canvas.Canvas(file_name, pagesize=letter)
            width, height = letter

            # Set up title and headers in PDF
            c.setFont("Helvetica-Bold", 16)
            c.drawString(30, height - 30, "Member List")
            c.setFont("Helvetica-Bold", 12)
            y_position = height - 60
            headers = ["Name", "Last Name", "Email", "Role", "Payment Done", "Points", "Rank"]
            for i, header in enumerate(headers):
                c.drawString(30 + (i * 80), y_position, header)

            # Add members' data to the PDF
            y_position -= 20
            for member in members:
                c.setFont("Helvetica", 12)
                c.drawString(30, y_position, member['name'])
                c.drawString(110, y_position, member['last_name'])
                c.drawString(190, y_position, member['email'])
                c.drawString(270, y_position, member['role'])
                c.drawString(350, y_position, str(member['payment_done']))
                c.drawString(430, y_position, str(member.get('points', 0)))
                c.drawString(510, y_position, self.get_rank(member.get('points', 0)))
                y_position -= 20

            # Save the PDF file
            c.save()
            messagebox.showinfo("Export Success", f"Member list exported to {file_name}")

        except pymongo.errors.ConnectionError as e:
            messagebox.showerror("Database Error", f"Could not fetch data from the database: {str(e)}")