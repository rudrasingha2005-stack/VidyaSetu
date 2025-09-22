import tkinter as tk
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk

# ---------------- Login Page ---------------- #
def login():
    username = entry_username.get()
    password = entry_password.get()
    if username == "student" and password == "1234":
        open_main_window("Student")
    elif username == "admin" and password == "admin":
        open_main_window("Admin")
    else:
        messagebox.showerror("Login Failed", "Invalid Username or Password")

# ---------------- Face Scan Attendance ---------------- #
def mark_attendance():
    cam_window = tk.Toplevel()
    cam_window.title("Face Scan Attendance")
    cam_window.geometry("500x400")

    label = tk.Label(cam_window)
    label.pack()

    cap = cv2.VideoCapture(0)

    def show_frame():
        ret, frame = cap.read()
        if ret:
            frame = cv2.flip(frame, 1)  # mirror image
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            label.imgtk = imgtk
            label.configure(image=imgtk)
        label.after(10, show_frame)

    def capture_attendance():
        messagebox.showinfo("Attendance Marked", "Attendance Recorded Successfully!")
        cap.release()
        cam_window.destroy()

    capture_btn = tk.Button(cam_window, text="✅ Capture Attendance", command=capture_attendance,
                            bg="#4CAF50", fg="white", font=("Arial", 12))
    capture_btn.pack(pady=10)

    show_frame()

# ---------------- Main Window ---------------- #
def open_main_window(role):
    login_window.destroy()  # close login page

    main_window = tk.Tk()
    main_window.title(f"Attendance App - {role}")
    main_window.geometry("400x500")
    main_window.configure(bg="white")

    # Top bar with profile button
    top_frame = tk.Frame(main_window, bg="#4CAF50", height=60)
    top_frame.pack(fill="x")

    profile_btn = tk.Button(top_frame, text="👤 Profile", font=("Arial", 12, "bold"),
                            bg="white", fg="black", relief="flat")
    profile_btn.pack(side="left", padx=10, pady=10)

    # Greeting
    greeting = tk.Label(main_window, text=f"Welcome, {role}!", font=("Arial", 16, "bold"), bg="white")
    greeting.pack(pady=20)

    # Main Options
    btn_attendance = tk.Button(main_window, text="📌 Mark Attendance",
                               font=("Arial", 14), width=20, height=2, bg="#2196F3", fg="white",
                               command=mark_attendance)
    btn_attendance.pack(pady=15)

    btn_record = tk.Button(main_window, text="📊 Records / Analytics",
                           font=("Arial", 14), width=20, height=2, bg="#FF9800", fg="white")
    btn_record.pack(pady=15)

    btn_profile = tk.Button(main_window, text="📝 Student Profile",
                            font=("Arial", 14), width=20, height=2, bg="#9C27B0", fg="white")
    btn_profile.pack(pady=15)

    main_window.mainloop()

# ---------------- Start Login Page ---------------- #
login_window = tk.Tk()
login_window.title("Attendance App - Login")
login_window.geometry("350x400")
login_window.configure(bg="white")

title_label = tk.Label(login_window, text="📚 School Attendance", font=("Arial", 18, "bold"), bg="white", fg="#333")
title_label.pack(pady=30)

lbl_username = tk.Label(login_window, text="Username:", font=("Arial", 12), bg="white")
lbl_username.pack(pady=5)
entry_username = tk.Entry(login_window, font=("Arial", 12))
entry_username.pack(pady=5)

lbl_password = tk.Label(login_window, text="Password:", font=("Arial", 12), bg="white")
lbl_password.pack(pady=5)
entry_password = tk.Entry(login_window, show="*", font=("Arial", 12))
entry_password.pack(pady=5)

btn_login = tk.Button(login_window, text="Login", font=("Arial", 14), width=12, bg="#4CAF50", fg="white", command=login)
btn_login.pack(pady=20)

btn_admin = tk.Button(login_window, text="Login as Admin", font=("Arial", 12), bg="#2196F3", fg="white",
                      command=lambda: open_main_window("Admin"))
btn_admin.pack()

login_window.mainloop()