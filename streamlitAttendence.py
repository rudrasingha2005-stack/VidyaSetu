# attendance_app_online.py

import streamlit as st
import datetime
import pandas as pd

# ---------- Session State ----------
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'role' not in st.session_state:
    st.session_state.role = 'Student'
if 'attendance' not in st.session_state:
    st.session_state.attendance = pd.DataFrame(columns=['Name', 'Role', 'Timestamp'])


# ---------- Login Page ----------
def login_page():
    st.title("📚 School Attendance System")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "user1" and password == "pass1":
            st.session_state.logged_in = True
            st.session_state.role = "Student"
        elif username == "admin" and password == "admin":
            st.session_state.logged_in = True
            st.session_state.role = "Admin"
        else:
            st.error("❌ Invalid Username or Password")

    if st.button("Login as Admin"):
        st.session_state.logged_in = True
        st.session_state.role = "Admin"


# ---------- Main Dashboard ----------
def main_dashboard():
    st.sidebar.title(f"Welcome, {st.session_state.role}!")

    page = st.sidebar.radio("Navigation",
                            ["Mark Attendance", "Records / Analytics", "Student Profile", "Midday Meal Scheme",
                             "Logout"])

    if page == "Mark Attendance":
        mark_attendance()
    elif page == "Records / Analytics":
        view_records()
    elif page == "Student Profile":
        st.info("📝 Student profile page (placeholder)")
    elif page == "Midday Meal Scheme":
        midday_meal()
    elif page == "Logout":
        st.session_state.logged_in = False
        st.session_state.role = "Student"


# ---------- Mark Attendance ----------
def mark_attendance():
    st.header("📌 Mark Attendance")
    name = st.text_input("Enter your Name")
    # Simulate face scan by uploading an image
    uploaded_file = st.file_uploader("Upload a face image to scan", type=["jpg", "png"])
    if st.button("✅ Capture Attendance") and uploaded_file and name:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.attendance = pd.concat([st.session_state.attendance,
                                                 pd.DataFrame([[name, st.session_state.role, timestamp]],
                                                              columns=['Name', 'Role', 'Timestamp'])],
                                                ignore_index=True)
        st.success(f"Attendance recorded for {name} at {timestamp}")


# ---------- Attendance Records ----------
def view_records():
    st.header("📊 Attendance Records")
    if st.session_state.attendance.empty:
        st.info("No attendance recorded yet.")
    else:
        st.dataframe(st.session_state.attendance)


# ---------- Midday Meal ----------
def midday_meal():
    st.header("🍽️ Midday Meal Scheme")
    if st.session_state.role != "Admin":
        st.error("🔒 Access Denied: Only school administration can access this page.")
    else:
        st.info("Midday Meal info for school admin (placeholder)")


# ---------- App Runner ----------
if not st.session_state.logged_in:
    login_page()
else:
    main_dashboard()
