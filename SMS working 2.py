import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3


# Function to create database and table if not exists
def Database():
    global conn, cursor
    conn = sqlite3.connect('student_records.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            sex TEXT NOT NULL,
            age INTEGER NOT NULL,
            major TEXT NOT NULL,
            sub_major TEXT NOT NULL,
            contact TEXT NOT NULL
        )
    ''')
    conn.commit()

# Function to close database connection
def close_db():
    conn.close()


# Function to add student record to the database
def register():
    if not (name.get() and sex.get() and age.get() and major.get() and sub_major.get() and contact.get()):
        messagebox.showwarning("Input Error", "All fields must be filled!")
        return

    if not contact.get().isdigit():
        messagebox.showwarning("Invalid Input", "Contact should contain only digits.")
        return

    cursor.execute('''
        INSERT INTO students (name, sex, age, major, sub_major, contact)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (name.get(), sex.get(), age.get(), major.get(), sub_major.get(), contact.get()))
    conn.commit()

    messagebox.showinfo("Success", "Student record added successfully.")
    clear_fields()


# Function to clear input fields after submission
def clear_fields():
    name.set("")
    sex.set("")
    age.set(16)  # Default to 16
    major.set("")
    sub_major.set("")
    contact.set("")


# Function to delete student record
def delete_student():
    delete_window = tk.Toplevel()
    delete_window.title("Delete Student")
    delete_window.geometry("400x300")
    delete_window.configure(bg="#e0f7fa")

    tk.Label(delete_window, text="Enter Student Name to Delete", font=("Arial", 14), bg="#e0f7fa", fg="Black").pack(pady=10)
    delete_name = tk.StringVar()
    tk.Entry(delete_window, textvariable=delete_name, font=("Arial", 14)).pack(pady=10)

    def confirm_delete():
        if not delete_name.get():
            messagebox.showwarning("Input Error", "Please enter Student Name to delete.")
            return

        cursor.execute('DELETE FROM students WHERE name = ?', (delete_name.get(),))
        conn.commit()

        if cursor.rowcount > 0:
            messagebox.showinfo("Success", "Record deleted successfully.")
        else:
            messagebox.showwarning("Not Found", "Student with this name not found.")
        delete_window.destroy()

    tk.Button(delete_window, text="Delete", command=confirm_delete, font=("Arial", 14), bg="#d32f2f", fg="black").pack(pady=10)
    add_home_button(delete_window)


# Function to display all student records
def view_all_students():
    cursor.execute("SELECT * FROM students")
    records = cursor.fetchall()

    if not records:
        messagebox.showinfo("No Records", "No student records found.")
        return

    view_window = tk.Toplevel()
    view_window.title("View All Students")
    view_window.geometry("1000x500")
    view_window.configure(bg="#e0f7fa")

    # Table header
    columns = ["ID", "Name", "Sex", "Age", "Major", "Sub Major", "Contact"]
    tree = ttk.Treeview(view_window, columns=columns, show="headings")
    tree.pack(fill="both", padx=20, pady=20)

    for col in columns:
        tree.heading(col, text=col, anchor="w")
        tree.column(col, width=140, anchor="w")

    for record in records:
        tree.insert("", "end", values=record)

    add_home_button(view_window)


# Function to search for a student by name
def search_student():
    search_window = tk.Toplevel()
    search_window.title("Search Student")
    search_window.geometry("400x300")
    search_window.configure(bg="#e0f7fa")

    tk.Label(search_window, text="Enter Student Name to Search", font=("Arial", 14), bg="#e0f7fa", fg="Black").pack(pady=10)
    search_name = tk.StringVar()
    tk.Entry(search_window, textvariable=search_name, font=("Arial", 14)).pack(pady=10)

    def perform_search():
        if not search_name.get():
            messagebox.showwarning("Input Error", "Please enter Student Name to search.")
            return

        cursor.execute("SELECT * FROM students WHERE name LIKE ?", ('%' + search_name.get() + '%',))
        records = cursor.fetchall()

        if not records:
            messagebox.showwarning("Not Found", "Student with this name not found.")
            return

        # Display search results in a new window
        result_window = tk.Toplevel()
        result_window.title("Search Results")
        result_window.geometry("1000x500")
        result_window.configure(bg="#e0f7fa")

        columns = ["ID", "Name", "Sex", "Age", "Major", "Sub Major", "Contact"]
        tree = ttk.Treeview(result_window, columns=columns, show="headings")
        tree.pack(fill="both", padx=20, pady=20)

        for col in columns:
            tree.heading(col, text=col, anchor="w")
            tree.column(col, width=140, anchor="w")

        for record in records:
            tree.insert("", "end", values=record)

        add_home_button(result_window)

    tk.Button(search_window, text="Search", command=perform_search, font=("Arial", 14), bg="#0288d1", fg="black").pack(pady=10)
    add_home_button(search_window)


# Major and sub-major options
school_majors = {
    "School of Business": ["Business Administration", "Communication", "e-Society (Digital Marketing)"],
    "School of Digital Technologies": [
        "Artificial Intelligence (AI)", "Computer Science", "Cybersecurity", "Data Analytics",
        "Digital Infrastructure", "Information and Communications Technology", "Interactive App Design and Development",
        "Software Development"
    ],
    "School of Law": ["Law"],
    "School of Social Sciences": ["General Education", "International Relations and Diplomacy/Political Science"]
}

# Function to auto update sub-majors based on the selected major
def update_sub_majors(*args):
    selected_major = major.get()
    sub_major_menu["values"] = school_majors.get(selected_major, [])
    sub_major.set("")  # Clear sub-major field whenever major is changed


# Function to add home button to any window
def add_home_button(window):
    home_button = tk.Button(window, text="Home", command=go_home, font=("Arial", 14), bg="#9c27b0", fg="black")
    home_button.pack(pady=20)


# Main page (Home page)
def main_page():
    global root, name, sex, age, major, sub_major, contact, sub_major_menu

    root = tk.Tk()
    root.title("Student Records")
    root.geometry("700x600")
    root.configure(bg="#e0f7fa")

    name = tk.StringVar()
    sex = tk.StringVar()
    age = tk.IntVar(value=15)  # Default to 15
    major = tk.StringVar()
    sub_major = tk.StringVar()
    contact = tk.StringVar()

    label = tk.Label(root, text="Tractor", font=("Verdana", 30, "bold"), fg="#00796b", bg="#e0f7fa")
    label.pack(pady=30)

    add_button = tk.Button(root, text="Add New Student", command=add_student_page, font=("Arial", 14), bg="#00796b",
                           fg="black", width=20, height=2)
    add_button.pack(pady=10)

    search_button = tk.Button(root, text="Search Student by Name", command=search_student, font=("Arial", 14),
                              bg="#0288d1", fg="black", width=20, height=2)
    search_button.pack(pady=10)

    view_button = tk.Button(root, text="View All Students", command=view_all_students, font=("Arial", 14),
                            bg="#0288d1", fg="black", width=20, height=2)
    view_button.pack(pady=10)

    delete_button = tk.Button(root, text="Delete Student", command=delete_student, font=("Arial", 14), bg="#d32f2f",
                              fg="black", width=20, height=2)
    delete_button.pack(pady=10)

    root.mainloop()


# Add Student Page
def add_student_page():
    global sub_major_menu  # Declare globally so it can be updated in the function

    add_screen = tk.Toplevel()
    add_screen.title("Add New Student")
    add_screen.geometry("400x600")  # Set consistent window size
    add_screen.configure(bg="#e0f7fa")

    # Name
    tk.Label(add_screen, text="Name", font=("Arial", 12), bg="#e0f7fa", fg="#004d40").pack(pady=5)
    tk.Entry(add_screen, textvariable=name, font=("Arial", 12)).pack(fill="x", padx=20, pady=5)

    # Sex
    tk.Label(add_screen, text="Sex", font=("Arial", 12), bg="#e0f7fa", fg="#004d40").pack(pady=5)
    sex_menu = ttk.Combobox(add_screen, textvariable=sex, font=("Arial", 12), state="readonly")
    sex_menu["values"] = ["Male", "Female"]
    sex_menu.pack(fill="x", padx=20, pady=5)

    # Age
    tk.Label(add_screen, text="Age", font=("Arial", 12), bg="#e0f7fa", fg="#004d40").pack(pady=5)
    age_menu = ttk.Spinbox(add_screen, from_=15, to=60, textvariable=age, font=("Arial", 12), width=5)
    age_menu.pack(padx=20, pady=5)

    # Major
    tk.Label(add_screen, text="Major", font=("Arial", 12), bg="#e0f7fa", fg="#004d40").pack(pady=5)
    major_menu = ttk.Combobox(add_screen, textvariable=major, font=("Arial", 12), state="readonly")
    major_menu["values"] = list(school_majors.keys())
    major_menu.pack(fill="x", padx=20, pady=5)
    major_menu.bind("<<ComboboxSelected>>", update_sub_majors)

    # Sub Major
    tk.Label(add_screen, text="Sub Major", font=("Arial", 12), bg="#e0f7fa", fg="#004d40").pack(pady=5)
    sub_major_menu = ttk.Combobox(add_screen, textvariable=sub_major, font=("Arial", 12), state="readonly")
    sub_major_menu.pack(fill="x", padx=20, pady=5)

    # Contact
    tk.Label(add_screen, text="Contact", font=("Arial", 12), bg="#e0f7fa", fg="#004d40").pack(pady=5)
    tk.Entry(add_screen, textvariable=contact, font=("Arial", 12)).pack(fill="x", padx=20, pady=5)

    # Buttons
    submit_button = tk.Button(add_screen, text="Submit", command=register, font=("Arial", 12), bg="#00796b", fg="black",
                              width=10)
    submit_button.pack(pady=10)

    clear_button = tk.Button(add_screen, text="Clear", command=clear_fields, font=("Arial", 12), bg="#00796b", fg="black",
                             width=10)
    clear_button.pack(pady=5)

    back_button = tk.Button(add_screen, text="Back", command=add_screen.destroy, font=("Arial", 12), bg="#9c27b0",
                            fg="black", width=10)
    back_button.pack(pady=5)


# Function to go back to the main page
def go_home():
    root.quit()
    main_page()


# Initialize Database and main page
Database()
main_page()
close_db()
