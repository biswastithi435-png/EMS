
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


# Database Connection
conn = sqlite3.connect("employee.db")
cursor = conn.cursor()

# Create Employee Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    gender TEXT,
    age INTEGER,
    department TEXT,
    position TEXT,
    salary REAL,
    email TEXT,
    phone TEXT
)
""")
conn.commit()


# Main Window
root = tk.Tk()
root.title("Employment Management System")
root.geometry("1100x650")
root.config(bg="#f0f0f0")
root.resizable(True, True)


# Heading
heading = tk.Label(
    root,
    text="EMPLOYMENT MANAGEMENT SYSTEM",
    font=("Arial", 22, "bold"),
    bg="#1f4e78",
    fg="white",
    pady=15
)
heading.pack(fill=tk.X)


# Input Frame
input_frame = tk.LabelFrame(
    root,
    text="Employee Details",
    font=("Arial", 12, "bold"),
    bg="#f0f0f0",
    padx=15,
    pady=10
)
input_frame.pack(fill=tk.X, padx=20, pady=10)


# Variables
emp_id = tk.StringVar()
name = tk.StringVar()
gender = tk.StringVar()
age = tk.StringVar()
department = tk.StringVar()
position = tk.StringVar()
salary = tk.StringVar()
email = tk.StringVar()
phone = tk.StringVar()


# Input Fields
fields = [
    ("Employee ID", emp_id),
    ("Name", name),
    ("Gender", gender),
    ("Age", age),
    ("Department", department),
    ("Position", position),
    ("Salary", salary),
    ("Email", email),
    ("Phone", phone)
]

entries = {}

for index, (label, variable) in enumerate(fields):
    row = index // 3
    col = (index % 3) * 2

    tk.Label(
        input_frame,
        text=label,
        font=("Arial", 10, "bold"),
        bg="#f0f0f0"
    ).grid(row=row, column=col, padx=10, pady=8, sticky="w")

    if label == "Gender":
        entry = ttk.Combobox(
            input_frame,
            textvariable=variable,
            values=["Male", "Female", "Other"],
            state="readonly",
            width=22
        )
    else:
        entry = tk.Entry(
            input_frame,
            textvariable=variable,
            width=25,
            font=("Arial", 10)
        )

    entry.grid(row=row, column=col + 1, padx=10, pady=8)

    entries[label] = entry

# Employee ID is generated automatically
entries["Employee ID"].config(state="readonly")


# Clear Form
def clear_fields():
    for variable in [
        emp_id, name, gender, age, department,
        position, salary, email, phone
    ]:
        variable.set("")

    table.selection_remove(table.selection())


# Add Employee
def add_employee():
    if not name.get().strip():
        messagebox.showerror("Error", "Please enter employee name.")
        return

    try:
        employee_age = int(age.get())
        employee_salary = float(salary.get())

        if employee_age <= 0 or employee_salary < 0:
            raise ValueError

    except ValueError:
        messagebox.showerror(
            "Error",
            "Please enter a valid age and salary."
        )
        return

    try:
        cursor.execute("""
        INSERT INTO employees
        (name, gender, age, department, position, salary, email, phone)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            name.get().strip(),
            gender.get(),
            employee_age,
            department.get().strip(),
            position.get().strip(),
            employee_salary,
            email.get().strip(),
            phone.get().strip()
        ))

        conn.commit()
        messagebox.showinfo("Success", "Employee added successfully!")

        clear_fields()
        display_employees()

    except sqlite3.Error as error:
        messagebox.showerror("Database Error", str(error))


# Display Employees
def display_employees():
    for item in table.get_children():
        table.delete(item)

    cursor.execute("SELECT * FROM employees")
    records = cursor.fetchall()

    for record in records:
        table.insert("", tk.END, values=record)


# Select Employee
def select_employee(event):
    selected = table.focus()

    if not selected:
        return

    data = table.item(selected, "values")

    if data:
        emp_id.set(data[0])
        name.set(data[1])
        gender.set(data[2])
        age.set(data[3])
        department.set(data[4])
        position.set(data[5])
        salary.set(data[6])
        email.set(data[7])
        phone.set(data[8])


# Update Employee
def update_employee():
    if not emp_id.get():
        messagebox.showerror("Error", "Please select an employee.")
        return

    if not name.get().strip():
        messagebox.showerror("Error", "Employee name is required.")
        return

    try:
        employee_age = int(age.get())
        employee_salary = float(salary.get())

        if employee_age <= 0 or employee_salary < 0:
            raise ValueError

    except ValueError:
        messagebox.showerror("Error", "Enter valid age and salary.")
        return

    try:
        cursor.execute("""
        UPDATE employees SET
        name=?, gender=?, age=?, department=?,
        position=?, salary=?, email=?, phone=?
        WHERE id=?
        """, (
            name.get().strip(),
            gender.get(),
            employee_age,
            department.get().strip(),
            position.get().strip(),
            employee_salary,
            email.get().strip(),
            phone.get().strip(),
            emp_id.get()
        ))

        conn.commit()

        messagebox.showinfo("Success", "Employee updated successfully!")

        clear_fields()
        display_employees()

    except sqlite3.Error as error:
        messagebox.showerror("Database Error", str(error))


# Delete Employee
def delete_employee():
    if not emp_id.get():
        messagebox.showerror("Error", "Please select an employee.")
        return

    confirm = messagebox.askyesno(
        "Confirm Delete",
        "Are you sure you want to delete this employee?"
    )

    if confirm:
        cursor.execute(
            "DELETE FROM employees WHERE id=?",
            (emp_id.get(),)
        )

        conn.commit()

        messagebox.showinfo("Success", "Employee deleted successfully!")

        clear_fields()
        display_employees()


# Search Employee
def search_employee():
    keyword = search_var.get().strip()

    for item in table.get_children():
        table.delete(item)

    cursor.execute("""
    SELECT * FROM employees
    WHERE CAST(id AS TEXT) LIKE ?
    OR name LIKE ?
    """, (f"%{keyword}%", f"%{keyword}%"))

    records = cursor.fetchall()

    for record in records:
        table.insert("", tk.END, values=record)

    if not records:
        messagebox.showinfo("Search", "No employee found.")


# Button Frame
button_frame = tk.Frame(root, bg="#f0f0f0")
button_frame.pack(pady=10)

tk.Button(
    button_frame, text="Add Employee",
    command=add_employee, bg="#28a745",
    fg="white", width=15
).grid(row=0, column=0, padx=8)

tk.Button(
    button_frame, text="Update",
    command=update_employee, bg="#007bff",
    fg="white", width=15
).grid(row=0, column=1, padx=8)

tk.Button(
    button_frame, text="Delete",
    command=delete_employee, bg="#dc3545",
    fg="white", width=15
).grid(row=0, column=2, padx=8)

tk.Button(
    button_frame, text="Clear",
    command=clear_fields, bg="#6c757d",
    fg="white", width=15
).grid(row=0, column=3, padx=8)


# Search Frame
search_frame = tk.Frame(root, bg="#f0f0f0")
search_frame.pack(pady=10)

search_var = tk.StringVar()

tk.Label(
    search_frame,
    text="Search by ID or Name:",
    font=("Arial", 11, "bold"),
    bg="#f0f0f0"
).pack(side=tk.LEFT, padx=5)

tk.Entry(
    search_frame,
    textvariable=search_var,
    width=30
).pack(side=tk.LEFT, padx=5)

tk.Button(
    search_frame,
    text="Search",
    command=search_employee,
    bg="#17a2b8",
    fg="white",
    width=12
).pack(side=tk.LEFT, padx=5)

tk.Button(
    search_frame,
    text="Show All",
    command=display_employees,
    bg="#343a40",
    fg="white",
    width=12
).pack(side=tk.LEFT, padx=5)


# Employee Table
table_frame = tk.Frame(root)
table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

columns = (
    "ID", "Name", "Gender", "Age",
    "Department", "Position", "Salary",
    "Email", "Phone"
)

table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings"
)

for column in columns:
    table.heading(column, text=column)
    table.column(column, width=110, anchor=tk.CENTER)

scrollbar = ttk.Scrollbar(
    table_frame,
    orient=tk.VERTICAL,
    command=table.yview
)

table.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
table.pack(fill=tk.BOTH, expand=True)

table.bind("<ButtonRelease-1>", select_employee)


# Load Existing Records
display_employees()


# Run Application
root.mainloop()

# Close Database Connection
conn.close()
