import tkinter as tk
from home import HomePage
from add_member import AddMemberPage
from member_list import MemberListPage

# Create the main window
root = tk.Tk()
root.title("Robotics Club Member App")
root.configure(bg="#2b2b2b")  # Dark background

# Set the window to full screen
root.attributes("-fullscreen", True)
root.bind("<F11>", lambda event: root.attributes("-fullscreen", not root.attributes("-fullscreen")))  # Toggle fullscreen with F11
root.bind("<Escape>", lambda event: root.attributes("-fullscreen", False))  # Exit fullscreen with Escape

# Create a container for the frames
container = tk.Frame(root, bg="#2b2b2b")
container.pack(fill="both", expand=True)

# Create HomePage, AddMemberPage, and MemberListPage
home_page = HomePage(container)
add_member_page = AddMemberPage(container, home_page.home_frame)
member_list_page = MemberListPage(container, home_page.home_frame)

# Start with the home page
home_page.show_frame(home_page.home_frame)

# Run the application
root.mainloop()