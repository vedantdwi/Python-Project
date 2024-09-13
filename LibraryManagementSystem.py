import sqlite3
import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta

# Database Setup
def setup_database():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()

    # Drop tables if they exist to avoid conflicts
    cursor.execute('DROP TABLE IF EXISTS users')
    cursor.execute('DROP TABLE IF EXISTS books')
    cursor.execute('DROP TABLE IF EXISTS issues')
    cursor.execute('DROP TABLE IF EXISTS transactions')

    # Recreate tables with user_id and book_id
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT NOT NULL -- "admin" or "user"
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER UNIQUE,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            available BOOLEAN DEFAULT 1
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS issues (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER,
            user_id INTEGER,
            issue_date TEXT,
            return_date TEXT,
            FOREIGN KEY(book_id) REFERENCES books(book_id),
            FOREIGN KEY(user_id) REFERENCES users(user_id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            issue_id INTEGER,
            fine REAL DEFAULT 0,
            paid BOOLEAN DEFAULT 0,
            FOREIGN KEY(issue_id) REFERENCES issues(id)
        )
    ''')

    # Insert predefined data
    cursor.executescript('''
        INSERT OR IGNORE INTO users (username, password, role, user_id) VALUES
            ('admin', 'adminpass', 'admin', 1),
            ('user1', 'userpass', 'user', 2),
            ('user2', 'user2pass', 'user', 3);

        INSERT OR IGNORE INTO books (title, author, available, book_id) VALUES
            ('The Great Gatsby', 'F. Scott Fitzgerald', 1, 101),
            ('To Kill a Mockingbird', 'Harper Lee', 1, 102),
            ('1984', 'George Orwell', 1, 103),
            ('Moby Dick', 'Herman Melville', 1, 104);

        INSERT OR IGNORE INTO issues (book_id, user_id, issue_date, return_date) VALUES
            (101, 2, '2024-08-01', '2024-08-15'),
            (102, 3, '2024-07-15', '2024-08-10'),
            (103, 2, '2024-07-20', '2024-08-25');

        INSERT OR IGNORE INTO transactions (issue_id, fine, paid) VALUES
            (1, 10.00, 0),
            (2, 0.00, 1);
    ''')

    conn.commit()
    conn.close()

# Main Application Class
class LibraryApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Library Management System")
        self.geometry("400x300")
        self.frames = {}

        for F in (LoginPage, AdminPage, UserPage, AddBookPage, IssueBookPage, ReturnBookPage, ReportsPage):
            page_name = F.__name__
            frame = F(parent=self, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

# Login Page
class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Login Page", font=("Arial", 16))
        label.pack(pady=10)

        tk.Label(self, text="Username").pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        tk.Label(self, text="Password").pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        login_button = tk.Button(self, text="Login", command=self.check_login)
        login_button.pack(pady=10)

    def check_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, role FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()

        if user:
            user_id, role = user
            self.controller.user_id = user_id
            if role == "admin":
                self.controller.show_frame("AdminPage")
            else:
                self.controller.show_frame("UserPage")
        else:
            messagebox.showerror("Login Failed", "Invalid credentials")
        conn.close()

# Admin Homepage
class AdminPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Admin Homepage", font=("Arial", 16))
        label.pack(pady=10)

        add_book_btn = tk.Button(self, text="Add Book", command=lambda: controller.show_frame("AddBookPage"))
        add_book_btn.pack(pady=5)

        issue_book_btn = tk.Button(self, text="Issue Book", command=lambda: controller.show_frame("IssueBookPage"))
        issue_book_btn.pack(pady=5)

        return_book_btn = tk.Button(self, text="Return Book", command=lambda: controller.show_frame("ReturnBookPage"))
        return_book_btn.pack(pady=5)

        reports_btn = tk.Button(self, text="Reports", command=lambda: controller.show_frame("ReportsPage"))
        reports_btn.pack(pady=5)

        logout_btn = tk.Button(self, text="Logout", command=lambda: controller.show_frame("LoginPage"))
        logout_btn.pack(pady=5)

# User Homepage
class UserPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="User Homepage", font=("Arial", 16))
        label.pack(pady=10)

        issue_book_btn = tk.Button(self, text="Issue Book", command=lambda: controller.show_frame("IssueBookPage"))
        issue_book_btn.pack(pady=5)

        return_book_btn = tk.Button(self, text="Return Book", command=lambda: controller.show_frame("ReturnBookPage"))
        return_book_btn.pack(pady=5)

        reports_btn = tk.Button(self, text="Reports", command=lambda: controller.show_frame("ReportsPage"))
        reports_btn.pack(pady=5)

        logout_btn = tk.Button(self, text="Logout", command=lambda: controller.show_frame("LoginPage"))
        logout_btn.pack(pady=5)

# Add Book Page
class AddBookPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Add Book", font=("Arial", 16))
        label.pack(pady=10)

        tk.Label(self, text="Title").pack()
        self.title_entry = tk.Entry(self)
        self.title_entry.pack()

        tk.Label(self, text="Author").pack()
        self.author_entry = tk.Entry(self)
        self.author_entry.pack()

        submit_btn = tk.Button(self, text="Add Book", command=self.add_book)
        submit_btn.pack(pady=10)

        back_btn = tk.Button(self, text="Back", command=lambda: controller.show_frame("AdminPage"))
        back_btn.pack()

    def add_book(self):
        title = self.title_entry.get()
        author = self.author_entry.get()

        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO books (title, author, available) VALUES (?, ?, ?)", (title, author, True))
        conn.commit()

        messagebox.showinfo("Success", f"Book '{title}' added successfully!")
        conn.close()

# Issue Book Page
class IssueBookPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Issue Book", font=("Arial", 16))
        label.pack(pady=10)

        tk.Label(self, text="Book ID").pack()
        self.book_id_entry = tk.Entry(self)
        self.book_id_entry.pack()

        tk.Label(self, text="User ID").pack()
        self.user_id_entry = tk.Entry(self)
        self.user_id_entry.pack()

        issue_btn = tk.Button(self, text="Issue Book", command=self.issue_book)
        issue_btn.pack(pady=10)

        back_btn = tk.Button(self, text="Back", command=lambda: controller.show_frame("AdminPage"))
        back_btn.pack()

    def issue_book(self):
        book_id = self.book_id_entry.get()
        user_id = self.user_id_entry.get()

        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()

        cursor.execute("SELECT available FROM books WHERE book_id=?", (book_id,))
        book = cursor.fetchone()

        if book and book[0]:
            issue_date = datetime.now().strftime('%Y-%m-%d')
            return_date = (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')
            cursor.execute("INSERT INTO issues (book_id, user_id, issue_date, return_date) VALUES (?, ?, ?, ?)", 
                           (book_id, user_id, issue_date, return_date))
            cursor.execute("UPDATE books SET available=0 WHERE book_id=?", (book_id,))
            conn.commit()
            messagebox.showinfo("Success", "Book issued successfully!")
        else:
            messagebox.showerror("Error", "Book is not available")
        
        conn.close()

# Return Book Page
class ReturnBookPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Return Book", font=("Arial", 16))
        label.pack(pady=10)

        tk.Label(self, text="Book ID").pack()
        self.book_id_entry = tk.Entry(self)
        self.book_id_entry.pack()

        return_btn = tk.Button(self, text="Return Book", command=self.return_book)
        return_btn.pack(pady=10)

        back_btn = tk.Button(self, text="Back", command=lambda: controller.show_frame("AdminPage"))
        back_btn.pack()

    def return_book(self):
        book_id = self.book_id_entry.get()

        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM issues WHERE book_id=? AND return_date IS NOT NULL", (book_id,))
        issue = cursor.fetchone()

        if issue:
            cursor.execute("UPDATE books SET available=1 WHERE book_id=?", (book_id,))
            cursor.execute("DELETE FROM issues WHERE book_id=?", (book_id,))
            conn.commit()
            messagebox.showinfo("Success", "Book returned successfully!")
        else:
            messagebox.showerror("Error", "No record of this book being issued")
        
        conn.close()

# Reports Page
class ReportsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Reports", font=("Arial", 16))
        label.pack(pady=10)

        back_btn = tk.Button(self, text="Back", command=lambda: controller.show_frame("AdminPage"))
        back_btn.pack()

# Main Execution
if __name__ == "__main__":
    setup_database()
    app = LibraryApp()
    app.mainloop()
