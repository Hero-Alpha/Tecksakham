import streamlit as st
import sqlite3
from streamlit_option_menu import option_menu
import pandas as pd


# Connect to database
def connectdb():
    conn = sqlite3.connect("mydb.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS student (
            name TEXT,
            mail TEXT UNIQUE,
            password TEXT,
            roll INTEGER PRIMARY KEY,
            branch TEXT
        );
    """)
    conn.commit()
    return conn


# Add record
def addRecord(data):
    try:
        with connectdb() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO student (name, mail, password, roll, branch) VALUES (?, ?, ?, ?, ?)", data)
            conn.commit()
            return True
    except sqlite3.IntegrityError:
        st.error("A student with this Roll No or Email already exists.")
        return False


# Display records
def display():
    st.title("All Registered Students")

    with connectdb() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name, mail, roll, branch FROM student")
        records = cursor.fetchall()

    if records:
        df = pd.DataFrame(records, columns=["Name", "Email", "Roll No", "Branch"])
        st.dataframe(df, use_container_width=True)
        return df
    else:
        st.info("No records found.")
        return None


# Delete record
def delete():
    st.title("RECORD DELETION")
    st.subheader("Confirm the following information to delete the record")

    roll = st.number_input("Enter your roll no.", min_value=1, step=1)
    password = st.text_input("Enter your password", type="password")
    branch = st.selectbox("Branch", options=["CSE", "AIML", "IOT", "ECE"])

    if st.button("Delete Record"):
        with connectdb() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM student WHERE roll = ? AND password = ? AND branch = ?", (roll, password, branch))
            record = cursor.fetchone()

            if record:
                cursor.execute("DELETE FROM student WHERE roll = ?", (roll,))
                conn.commit()
                st.success("Record deleted successfully!")
            else:
                st.error("No matching record found! Please check your credentials.")


# Filtering according to branch
def filter_by_branch():
    st.title("FILTER RECORDS BY BRANCH")
    branch = st.selectbox("Select a branch to filter records", options=["CSE", "AIML", "IOT", "ECE"])

    if st.button("Filter Records"):
        with connectdb() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name, mail, roll FROM student WHERE branch = ?", (branch,))
            records = cursor.fetchall()

            if records:
                df = pd.DataFrame(records, columns=["Name", "Email", "Roll No"])
                st.success(f"Showing records for branch: {branch}")
                st.dataframe(df, use_container_width=True)
            else:
                st.warning(f"No records found for {branch} branch.")


# Signup Page
def signup():
    st.title("REGISTRATION PAGE")
    name = st.text_input("Enter your name")
    mail = st.text_input("Enter your email")
    password = st.text_input("Enter your password", type="password")
    repassword = st.text_input("Retype your password", type="password")
    roll = st.number_input("Enter your roll no.", min_value=1, step=1)
    branch = st.selectbox("Branch", options=["CSE", "AIML", "IOT", "ECE"])

    if st.button("Sign Up"):
        if password != repassword:
            st.warning("Password mismatch, please try again")
        elif not name or not mail or not password:
            st.warning("All fields are required!")
        else:
            if addRecord((name, mail, password, int(roll), branch)):
                st.success("Student registration successful!")


# Sidebar menu
with st.sidebar:
    selected = option_menu("My App", ["Signup", "Display All Records", "Delete Record", "Filter As Branch"])

# Routing based on sidebar selection
if selected == "Signup":
    signup()
elif selected == "Display All Records":
    display()
elif selected == "Delete Record":
    delete()
elif selected == "Filter As Branch":
    filter_by_branch()
