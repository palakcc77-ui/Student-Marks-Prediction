import streamlit as st
import joblib
import sqlite3
import pandas as pd

conn = sqlite3.connect("students.db")
cursor=conn.cursor()

cursor.execute(""" CREATE TABLE IF NOT EXISTS students( id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, study_hours REAL, predicted_marks REAL)""")
conn.commit()

st.title("Student Marks Prediction")
student_name=st.text_input("Enter Student Name")
study_hour=st.number_input("Enter study hours")

btn=st.button("Predict!")
reset=st.button("Reset")
save=st.button("Save Record")
view=st.button("View Record")

update_id=st.number_input("Enter Record ID to Update",min_value=1,step=1)
new_name=st.text_input("New Student Name")
new_hours=st.number_input("New Student Hours",min_value=4.0,max_value=12.0,step=0.5)

update=st.button("Update Record")

delete_id=st.number_input("Enter Record ID to Delete",min_value=1,step=1,key="delete_id")
delete=st.button("Delete Record")


if btn:
    if study_hour>4 and study_hour<12:
        model=joblib.load("student_marks.pkl")
        res=model.predict([[study_hour]])[0][0].round(2)
        st.write(f"Predicted Marks: {res}")
        st.session_state["marks"]=res
        
    else:
        st.warning("Invalid")

if save:
    if "marks" in st.session_state:
        cursor.execute("INSERT INTO students(name, study_hours, predicted_marks) VALUES(?, ?, ?)",(student_name, study_hour, st.session_state["marks"]))
        conn.commit()
        st.success("Record Saved Successfully!")
    else:
        st.warning("Please predict the marks First!!")

if view:
    data=pd.read_sql_query("SELECT*FROM students",conn)
    if data.empty:
        st.warning("No Records Found!!")
    else:
        st.subheader("Student Records")
        st.dataframe(data)

if update:
    model=joblib.load("student_marks.pkl")
    new_marks=model.predict([[new_hours]])[0][0].round(2)
    cursor.execute("""UPDATE students SET name=?,study_hours=?,predicted_marks=? WHERE id=?""",(new_name,new_hours,new_marks,update_id))
    conn.commit()
    st.success("Record Update Successfully!")

if delete:
    cursor.execute("DELETE FROM students WHERE id=?",(delete_id,))
    conn.commit()
    if cursor.rowcount>0:
        st.success("Record Deleted Successfully!!")
    else:
        st.warning("Record ID not Found!!")

if reset:
    st.rerun()