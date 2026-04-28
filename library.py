import mysql.connector
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk

# ===== DB CONNECTION =====
con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="host",
    database="librarydb"
)

# ===== DB HELPER =====
def run_query(query, values=None):
    cur = con.cursor()
    cur.execute(query, values or ())
    if not query.strip().lower().startswith("select"):
        con.commit()
    return cur

# ===== WINDOW STYLE =====
def style_window(win, title, w=500, h=400):
    win.title(title)
    win.geometry(f"{w}x{h}")
    win.configure(bg="#0f172a")

    win.update_idletasks()
    x = (win.winfo_screenwidth() // 2) - (w // 2)
    y = (win.winfo_screenheight() // 2) - (h // 2)
    win.geometry(f"{w}x{h}+{x}+{y}")

# ===== ADD STUDENT =====
def add_student_gui():
    win = tk.Toplevel()
    style_window(win, "Add Student", 550, 520)

    labels = [
        "Name", "Course", "Department",
        "Year", "RollNo",
        "Entry Time (DD-MM HH:MM)",
        "Exit Time (DD-MM HH:MM) (optional)"
    ]

    entries = []

    for i, text in enumerate(labels):
        tk.Label(win, text=text, bg="#0f172a", fg="white").grid(row=i, column=0, padx=20, pady=10)
        e = tk.Entry(win, width=35)
        e.grid(row=i, column=1)
        entries.append(e)

    def submit():
        try:
            cur = run_query("SELECT COUNT(*) FROM Students")
            sno = cur.fetchone()[0] + 1

            current_year = datetime.now().year

            entry_time = datetime.strptime(entries[5].get(), "%d-%m %H:%M").replace(year=current_year)

            if entries[6].get() == "":
                exit_time = None
            else:
                exit_time = datetime.strptime(entries[6].get(), "%d-%m %H:%M").replace(year=current_year)

            run_query(
                """INSERT INTO Students
                (SNo, Name, Course, Department, Year, RollNo, EntryTime, ExitTime)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",
                (
                    sno,
                    entries[0].get(),
                    entries[1].get(),
                    entries[2].get(),
                    int(entries[3].get()),
                    int(entries[4].get()),
                    entry_time,
                    exit_time
                )
            )

            messagebox.showinfo("Success", "Student Added")
            win.destroy()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(win, text="Submit", bg="#3b82f6", fg="white",
              width=20, command=submit).grid(row=8, columnspan=2, pady=20)

# ===== ADD BOOK =====
def add_book_gui():
    win = tk.Toplevel()
    style_window(win, "Add Book", 500, 400)

    labels = ["Title", "Author", "Category", "Pages"]
    entries = []

    for i, text in enumerate(labels):
        tk.Label(win, text=text, bg="#0f172a", fg="white").grid(row=i, column=0, padx=20, pady=10)
        e = tk.Entry(win, width=30)
        e.grid(row=i, column=1)
        entries.append(e)

    def submit():
        try:
            run_query(
                "INSERT INTO Books(Title, Author, Category, Pages) VALUES (%s,%s,%s,%s)",
                (entries[0].get(), entries[1].get(), entries[2].get(), int(entries[3].get()))
            )
            messagebox.showinfo("Success", "Book Added")
            win.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(win, text="Submit", bg="#3b82f6", fg="white",
              width=20, command=submit).grid(row=5, columnspan=2, pady=20)

# ===== ISSUE BOOK =====
def issue_book_gui():
    win = tk.Toplevel()
    style_window(win, "Issue Book", 500, 350)

    labels = ["Student ID", "Book ID", "Issue Date (YYYY-MM-DD)"]
    entries = []

    for i, text in enumerate(labels):
        tk.Label(win, text=text, bg="#0f172a", fg="white").grid(row=i, column=0, padx=20, pady=10)
        e = tk.Entry(win, width=30)
        e.grid(row=i, column=1)
        entries.append(e)

    def submit():
        try:
            run_query(
                "INSERT INTO Issue(StudentID, BookID, IssueDate, ReturnDate, Fine) VALUES (%s,%s,%s,NULL,0)",
                (int(entries[0].get()), int(entries[1].get()), entries[2].get())
            )
            messagebox.showinfo("Success", "Book Issued")
            win.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(win, text="Submit", bg="#3b82f6", fg="white",
              width=20, command=submit).grid(row=4, columnspan=2, pady=20)

# ===== RETURN BOOK =====
def return_book_gui():
    win = tk.Toplevel()
    style_window(win, "Return Book", 450, 300)

    tk.Label(win, text="Issue ID", bg="#0f172a", fg="white").grid(row=0, column=0, padx=20, pady=10)
    tk.Label(win, text="Return Date (YYYY-MM-DD)", bg="#0f172a", fg="white").grid(row=1, column=0)

    issue_id = tk.Entry(win, width=30)
    rdate = tk.Entry(win, width=30)

    issue_id.grid(row=0, column=1)
    rdate.grid(row=1, column=1)

    def submit():
        try:
            cur = run_query("SELECT IssueDate FROM Issue WHERE IssueID=%s", (issue_id.get(),))
            result = cur.fetchone()

            if not result:
                messagebox.showerror("Error", "Invalid Issue ID")
                return

            d1 = datetime.strptime(str(result[0]), "%Y-%m-%d")
            d2 = datetime.strptime(rdate.get(), "%Y-%m-%d")

            days = (d2 - d1).days
            fine = max(0, (days - 7) * 5)

            run_query(
                "UPDATE Issue SET ReturnDate=%s, Fine=%s WHERE IssueID=%s",
                (rdate.get(), fine, issue_id.get())
            )

            messagebox.showinfo("Done", f"Returned. Fine = {fine}")
            win.destroy()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(win, text="Submit", bg="#3b82f6", fg="white",
              width=20, command=submit).grid(row=2, columnspan=2, pady=20)

# ===== SEARCH VIEW (EXCEL STYLE + HIDE StudentID) =====
def search_window(table):
    win = tk.Toplevel()
    style_window(win, f"{table} View", 850, 550)

    tk.Label(win, text=f"{table} Data",
             bg="#0f172a", fg="white",
             font=("Arial", 14)).pack(pady=10)

    search_entry = tk.Entry(win, width=40)
    search_entry.pack(pady=5)

    tree = ttk.Treeview(win)
    tree.pack(fill="both", expand=True)

    def show_data(data, columns):
        tree.delete(*tree.get_children())

        filtered_cols = [c for c in columns if c != "StudentID"]
        tree["columns"] = filtered_cols
        tree["show"] = "headings"

        for col in filtered_cols:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor="center")

        for row in data:
            filtered_row = [row[i] for i, c in enumerate(columns) if c != "StudentID"]
            tree.insert("", "end", values=filtered_row)

    def search():
        keyword = search_entry.get().lower()
        cur = run_query(f"SELECT * FROM {table}")
        data = cur.fetchall()
        columns = [desc[0] for desc in cur.description]

        filtered = [row for row in data if keyword in str(row).lower()]
        show_data(filtered, columns)

    def show_all():
        cur = run_query(f"SELECT * FROM {table}")
        data = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        show_data(data, columns)

    tk.Button(win, text="Search", command=search).pack(pady=5)
    tk.Button(win, text="Show All", command=show_all).pack(pady=5)

# ===== DELETE STUDENT =====
def delete_student_gui():
    win = tk.Toplevel()
    style_window(win, "Delete Student", 450, 350)

    tk.Label(win, text="Roll No",
             bg="#0f172a", fg="white").pack(pady=5)
    roll = tk.Entry(win, width=30)
    roll.pack()

    tk.Label(win, text="OR Department (bulk)",
             bg="#0f172a", fg="white").pack(pady=5)
    dept = tk.Entry(win, width=30)
    dept.pack()

    def delete():
        try:
            if roll.get():
                run_query("DELETE FROM Students WHERE RollNo=%s", (roll.get(),))
                messagebox.showinfo("Done", "Student deleted")

            elif dept.get():
                run_query("DELETE FROM Students WHERE Department=%s", (dept.get(),))
                messagebox.showinfo("Done", "Bulk students deleted")

            win.destroy()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(win, text="Delete", bg="red", fg="white",
              width=20, command=delete).pack(pady=20)

# ===== DELETE BOOK =====
def delete_book_gui():
    win = tk.Toplevel()
    style_window(win, "Delete Book", 450, 350)

    tk.Label(win, text="Title",
             bg="#0f172a", fg="white").pack(pady=5)
    title = tk.Entry(win, width=30)
    title.pack()

    tk.Label(win, text="OR Category (bulk)",
             bg="#0f172a", fg="white").pack(pady=5)
    cat = tk.Entry(win, width=30)
    cat.pack()

    def delete():
        try:
            if title.get():
                run_query("DELETE FROM Books WHERE Title=%s", (title.get(),))
                messagebox.showinfo("Done", "Book deleted")

            elif cat.get():
                run_query("DELETE FROM Books WHERE Category=%s", (cat.get(),))
                messagebox.showinfo("Done", "Bulk books deleted")

            win.destroy()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(win, text="Delete", bg="red", fg="white",
              width=20, command=delete).pack(pady=20)

# ===== MAIN GUI =====
def gui():
    root = tk.Tk()
    root.title("Library Management System")
    root.geometry("800x650")
    root.configure(bg="#0f172a")

    tk.Label(root, text="Library Management System",
             font=("Segoe UI", 22, "bold"),
             bg="#1e293b", fg="white", pady=15).pack(fill="x")

    frame = tk.Frame(root, bg="#0f172a")
    frame.pack(pady=30)

    btn = {"width": 30, "height": 2, "bg": "#3b82f6", "fg": "white"}

    tk.Button(frame, text="Add Student", command=add_student_gui, **btn).pack(pady=5)
    tk.Button(frame, text="Add Book", command=add_book_gui, **btn).pack(pady=5)
    tk.Button(frame, text="Issue Book", command=issue_book_gui, **btn).pack(pady=5)
    tk.Button(frame, text="Return Book", command=return_book_gui, **btn).pack(pady=5)

    tk.Button(frame, text="View Students", command=lambda: search_window("Students"), **btn).pack(pady=5)
    tk.Button(frame, text="View Books", command=lambda: search_window("Books"), **btn).pack(pady=5)

    tk.Button(frame, text="Delete Student", command=delete_student_gui, **btn).pack(pady=5)
    tk.Button(frame, text="Delete Book", command=delete_book_gui, **btn).pack(pady=5)

    tk.Button(root, text="Exit", command=root.quit,
              bg="red", fg="white", width=20).pack(pady=20)

    root.mainloop()

# ===== START =====
gui()
