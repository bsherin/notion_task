import customtkinter as ctk
from tkinter import messagebox


def submit_form():
    name = name_entry.get()
    start_date = date_entry.get()
    project = project_var.get()

    if not name or not start_date or not project:
        messagebox.showerror("Error", "All fields are required.")
        return

    print(f"Name: {name}")
    print(f"Start Date: {start_date}")
    print(f"Project: {project}")
    messagebox.showinfo("Submitted", f"Name: {name}\nStart Date: {start_date}\nProject: {project}")


ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Project Form")
app.geometry("400x250")

ctk.CTkLabel(app, text="Name:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
name_entry = ctk.CTkEntry(app, width=200)
name_entry.grid(row=0, column=1, padx=10, pady=5)

ctk.CTkLabel(app, text="Start Date (YYYY-MM-DD):").grid(row=1, column=0, padx=10, pady=5, sticky="w")
date_entry = ctk.CTkEntry(app, width=200)
date_entry.grid(row=1, column=1, padx=10, pady=5)

ctk.CTkLabel(app, text="Project:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
project_var = ctk.StringVar()
project_dropdown = ctk.CTkComboBox(app, variable=project_var, values=["Project A", "Project B", "Project C"], width=200)
project_dropdown.grid(row=2, column=1, padx=10, pady=5)

submit_button = ctk.CTkButton(app, text="Submit", command=submit_form)
submit_button.grid(row=3, column=1, pady=20)

app.mainloop()