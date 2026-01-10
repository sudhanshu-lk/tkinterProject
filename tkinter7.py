import pyodbc
import tkinter as tk
from tkinter import ttk, messagebox

# --- Database Connection ---
conn = pyodbc.connect(
            r'DRIVER={ODBC Driver 18 for SQL Server};'
            r'SERVER=HP\MYINSTANCE;'
            r'DATABASE=Bank1;'
            r'Trusted_Connection=yes;'
            r'TrustServerCertificate=yes;'
        )
cursor = conn.cursor()

# --- Main Window ---
root = tk.Tk()
root.title("Tkinter Project")
root.geometry("580x700")

def show_frame(frame):
    frame.tkraise()

# Frames
main_frame = ttk.Frame(root)
registration_frame = ttk.Frame(root)
crud_frame = ttk.Frame(root)

for frame in (main_frame, registration_frame, crud_frame):
    frame.grid(row=0, column=0, sticky='nsew', padx=600, pady=200)

# --- Main Frame ---
frame = tk.Frame(root, width=580, height=700, bg="green").grid(row=0, column=0)
tk.Label(main_frame, text="WELCOME TO THE MAIN PAGE", font=("Helvetica", 20, "bold")).pack(pady=20)
tk.Button(main_frame, text="Registration", bg="blue", fg="White", font=(20), command=lambda: show_frame(registration_frame)).pack(pady=10)
tk.Button(main_frame, text="CRUD Operation", bg="cyan", fg="white", font=(20), command=lambda: show_frame(crud_frame)).pack(pady=10)

# --- Registration Frame (Updated) ---
tk.Label(registration_frame, text="USER REGISTRATION", font=("Helvetica", 16, "bold")).pack(pady=10)

# 1. Username
tk.Label(registration_frame, text="Username", font=("Helvetica", 10, "bold")).pack()
reg_username = ttk.Entry(registration_frame)
reg_username.pack(fill='x', padx=50)

# 2. Password
ttk.Label(registration_frame, text="Password", font=("Helvetica", 10, "bold")).pack()
reg_password = ttk.Entry(registration_frame, show="")
reg_password.pack(fill='x', padx=50)

# 3. Gender
ttk.Label(registration_frame, text="Gender", font=("Helvetica", 10, "bold")).pack()
reg_gender_var = tk.StringVar(value="")
gender_frame = ttk.Frame(registration_frame)
gender_frame.pack()
ttk.Radiobutton(gender_frame, text="Male", variable=reg_gender_var, value="Male").pack(side=tk.LEFT, padx=10)
ttk.Radiobutton(gender_frame, text="Female", variable=reg_gender_var, value="Female").pack(side=tk.LEFT, padx=10)
ttk.Radiobutton(gender_frame, text="Other", variable=reg_gender_var, value="Other").pack(side=tk.LEFT, padx=10)

# 4. Phone Number
ttk.Label(registration_frame, text="Phone Number", font=("Helvetica", 10, "bold")).pack()
reg_phone = ttk.Entry(registration_frame)
reg_phone.pack(fill='x', padx=50)

# 5. Email
ttk.Label(registration_frame, text="Email", font=("Helvetica", 10, "bold")).pack()
reg_email = ttk.Entry(registration_frame)
reg_email.pack(fill='x', padx=50)

# 6. Qualification 
ttk.Label(registration_frame, text="Qualification", font=("Helvetica", 10, "bold")).pack()
qualification_options = ["10 pass", "12 pass", "BCA graduate"]
reg_qualification = ttk.Combobox(registration_frame, values=qualification_options, state="readonly")
reg_qualification.set("Select Qualification") 
reg_qualification.pack(fill='x', padx=50)


def register_user():
    username = reg_username.get().strip()
    password = reg_password.get()
    gender = reg_gender_var.get()
    phone = reg_phone.get().strip()
    email = reg_email.get().strip()
    qualification = reg_qualification.get()

    # --- Validation Checks ---
    if not all([username, password, phone, email, qualification, gender]):
        messagebox.showerror("Error", "All fields are required.")
        return

    if username.isnumeric():
        messagebox.showerror("Error", "Username cannot be numeric.")
        return
        
    if gender == "":
        messagebox.showerror("Error", "Please select a Gender.")
        return

    if not phone.isnumeric():
        messagebox.showerror("Error", "Phone Number must be numerical.")
        return

    if '@' not in email or '.' not in email:
        messagebox.showerror("Error", "Email must conatin both '@' aur '.'")
        return

    if qualification == "Select Qualification":
        messagebox.showerror("Error", "Please select your Qualification.")
        return

    # --- Database Insertion ---
    try:
        sql = """
            INSERT INTO user1 
            (username, email, password, gender, phone, qualification) 
            VALUES (?, ?, ?, ?, ?, ?)
        """
        cursor.execute(sql, (username, email, password, gender, phone, qualification))
        conn.commit()
        
        messagebox.showinfo("Success", "User registered successfully!")
        
        # Clear fields on success
        reg_username.delete(0, tk.END)
        reg_password.delete(0, tk.END)
        reg_email.delete(0, tk.END)
        reg_phone.delete(0, tk.END)
        reg_gender_var.set("")
        reg_qualification.set("Select Qualification")

    except pyodbc.IntegrityError:
        messagebox.showerror("Error", "Username already exists!")
    except Exception as e:
        messagebox.showerror("Database Error", f"An unexpected Database error occurred: {e}")


tk.Button(registration_frame, text="Submit", bg="Orange", fg="black", font=("Helvetica", 10, "bold"), command=register_user).pack(side=tk.LEFT, padx=18, pady=5)
tk.Button(registration_frame, text="Back", bg="black", fg="White", font=("Helvetica", 10, "bold"), command=lambda: show_frame(main_frame)).pack(side=tk.RIGHT, padx=18, pady=5)

# --- CRUD Frame (Updated to display all fields) ---
tk.Label(crud_frame, text="CRUD OPERATION", font=("Helvetica", 16, "bold")).pack(pady=10)
tk.Label(crud_frame, text="Enter only username to search the user", bg="green", fg="white", font=("Helvetica", 8, "bold")).pack()
ttk.Label(crud_frame, text="Search Username", font=("Helvetica", 10, "bold")).pack()
search_username = ttk.Entry(crud_frame)
search_username.pack(fill='x', padx=50)

# Fields to display and modify the fetched data
ttk.Label(crud_frame, text="Email", font=("Helvetica", 10, "bold")).pack()
crud_email = ttk.Entry(crud_frame)
crud_email.pack(fill='x', padx=50)

ttk.Label(crud_frame, text="Password", font=("Helvetica", 10, "bold")).pack()
crud_password = ttk.Entry(crud_frame, show="")
crud_password.pack(fill='x', padx=50)

ttk.Label(crud_frame, text="Gender", font=("Helvetica", 10, "bold")).pack()
crud_gender = ttk.Entry(crud_frame)
crud_gender.pack(fill='x', padx=50)

ttk.Label(crud_frame, text="Phone Number", font=("Helvetica", 10, "bold")).pack()
crud_phone = ttk.Entry(crud_frame)
crud_phone.pack(fill='x', padx=50)

ttk.Label(crud_frame, text="Qualification", font=("Helvetica", 10, "bold")).pack()
qualification_options = ["10 pass", "12 pass", "BCA graduate"]
crud_qualification = ttk.Combobox(crud_frame, values=qualification_options, state="readonly")
crud_qualification.pack(fill='x', padx=50)


def reset_fields():
    """Clears all entry fields in CRUD frame."""
    search_username.delete(0, tk.END)
    crud_email.delete(0, tk.END)
    crud_password.delete(0, tk.END)
    crud_gender.delete(0, tk.END)
    crud_phone.delete(0, tk.END)
    crud_qualification.set("") # Reset combobox


def search_user():
    """Searches by username and displays all details."""
    username = search_username.get()
    
    # Reset all fields before a new search
    reset_fields()
    search_username.insert(0, username)

    # Fetching all required columns
    sql = "SELECT email, password, gender, phone, qualification FROM user1 WHERE username = ?"
    cursor.execute(sql, (username,))
    result = cursor.fetchone()

    if result:
        # Populate all fields with fetched data
        crud_email.insert(0, result[0])      # email
        crud_password.insert(0, result[1])   # password
        crud_gender.insert(0, result[2])     # gender
        crud_phone.insert(0, result[3])      # phone
        crud_qualification.set(result[4])    # qualification (using set for Combobox)
    else:
        messagebox.showerror("Error", "Username not found!")
        reset_fields()


def update_user():
    """Updates all details for the current username."""
    username = search_username.get()
    email = crud_email.get()
    password = crud_password.get()
    gender = crud_gender.get()
    phone = crud_phone.get()
    qualification = crud_qualification.get()
    
    
    if not username:
        messagebox.showerror("Error", "Please search for a Username first.")
        return

    sql = """
        UPDATE user1 
        SET email = ?, password = ?, gender = ?, phone = ?, qualification = ? 
        WHERE username = ?
    """
    cursor.execute(sql, (email, password, gender, phone, qualification, username))
    
    if cursor.rowcount == 0:
        messagebox.showerror("Error", "Username not found!. Update failed.")
    else:
        conn.commit()
        messagebox.showinfo("Success", "User updated successfully!")


def delete_user():
    """Deletes the user entry."""
    username = search_username.get()
    cursor.execute("DELETE FROM user1 WHERE username = ?", (username,))
    if cursor.rowcount == 0:
        messagebox.showerror("Error", "Username not found!")
    else:
        conn.commit()
        reset_fields() # Clear all fields after deletion
        messagebox.showinfo("Deleted", "User deleted successfully!")


tk.Button(crud_frame, text="Search", bg="skyblue", fg="black", font=("Helvetica", 10, "bold"), command=search_user).pack(side=tk.LEFT, padx=28, pady=5)
tk.Button(crud_frame, text="Update", bg="lightgreen", fg="black", font=("Helvetica", 10, "bold"), command=update_user).pack(side=tk.LEFT, padx=15, pady=5)
tk.Button(crud_frame, text="Delete", bg="red", fg="black", font=("Helvetica", 10, "bold"), command=delete_user).pack(side=tk.LEFT, padx=15, pady=15)
tk.Button(crud_frame, text="Reset", bg="light gray", fg="black", font=("Helvetica", 10, "bold"), command=reset_fields).pack(side=tk.LEFT, padx=15, pady=5)
tk.Button(crud_frame, text="Back", bg="black", fg="White", font=("Helvetica", 10, "bold"), command=lambda: show_frame(main_frame)).pack(side=tk.LEFT, padx=15, pady=10)

# Start with main frame
show_frame(main_frame)
root.mainloop()

# Close connection
conn.close()
