import requests
from bs4 import BeautifulSoup
import pandas as pd
from collections import defaultdict

### Attendance
def return_attendance(username, pwd):
    try:
        session = requests.Session()
        r = session.get("https://ecampus.psgtech.ac.in/studzone2/")
        loginpage = session.get(r.url)
        soup = BeautifulSoup(loginpage.text, "html.parser")

        viewstate = soup.select("#__VIEWSTATE")[0]["value"]
        eventvalidation = soup.select("#__EVENTVALIDATION")[0]["value"]
        viewstategen = soup.select("#__VIEWSTATEGENERATOR")[0]["value"]

        item_request_body = {
            "__EVENTTARGET": "",
            "__EVENTARGUMENT": "",
            "__LASTFOCUS": "",
            "__VIEWSTATE": viewstate,
            "__VIEWSTATEGENERATOR": viewstategen,
            "__EVENTVALIDATION": eventvalidation,
            "rdolst": "S",
            "txtusercheck": username,
            "txtpwdcheck": pwd,
            "abcd3": "Login",
        }

        response = session.post(
            url=r.url, data=item_request_body, headers={"Referer": r.url}
        )
        val = response.url

        if response.status_code == 200:
            defaultpage = "https://ecampus.psgtech.ac.in/studzone2/AttWfPercView.aspx"

            page = session.get(defaultpage)
            soup = BeautifulSoup(page.text, "html.parser")

            data = []
            column = []
            table = soup.find("table", attrs={"class": "cssbody"})

            if table == None:
                message = str(soup.find("span", attrs={"id": "Message"}))
                if "On Process" in message:
                    return "Table is being updated"

            try:
                rows = table.find_all("tr")
                for index, row in enumerate(rows):
                    cols = row.find_all("td")
                    cols = [ele.text.strip() for ele in cols]
                    # Get rid of empty val
                    data.append([ele for ele in cols if ele])

                # df = pd.DataFrame(data, columns=column)
                # res = df.to_json(orient="split")
                # return res
                return data, session
            except:
                return "Invalid password"
        else:
            return "Try again after some time"

    except:
        return "Try again after some time"

### CGPA
def return_results(username, pwd):
    try:
        session = requests.Session()
        r = session.get("https://ecampus.psgtech.ac.in/studzone2/")
        loginpage = session.get(r.url)
        soup = BeautifulSoup(loginpage.text, "html.parser")

        viewstate = soup.select("#__VIEWSTATE")[0]["value"]
        eventvalidation = soup.select("#__EVENTVALIDATION")[0]["value"]
        viewstategen = soup.select("#__VIEWSTATEGENERATOR")[0]["value"]

        item_request_body = {
            "__EVENTTARGET": "",
            "__EVENTARGUMENT": "",
            "__LASTFOCUS": "",
            "__VIEWSTATE": viewstate,
            "__VIEWSTATEGENERATOR": viewstategen,
            "__EVENTVALIDATION": eventvalidation,
            "rdolst": "S",
            "txtusercheck": username,
            "txtpwdcheck": pwd,
            "abcd3": "Login",
        }

        response = session.post(
            url=r.url, data=item_request_body, headers={"Referer": r.url}
        )
        val = response.url

        if response.status_code == 200:
            defaultpage = "https://ecampus.psgtech.ac.in/studzone2/AttWfStudCourseSelection.aspx"

            page = session.get(defaultpage)
            soup = BeautifulSoup(page.text, "html.parser")

            data = []
            column = []
            table = soup.find("table", attrs={"id": "PDGCourse"})
            #print(table)

            if table == None:
                message = str(soup.find("span", attrs={"id": "Message"}))
                if "On Process" in message:
                    return "Table is being updated"

            try:
                rows = table.find_all("tr")
                for index, row in enumerate(rows):
                    cols = row.find_all("td")
                    cols = [ele.text.strip() for ele in cols]
                    # Get rid of empty val
                    data.append([ele for ele in cols if ele])

                # df = pd.DataFrame(data, columns=column)
                # res = df.to_json(orient="split")
                # return res
                return data, session
            except:
                return "Invalid password"
        else:
            return "Try again after some time"

    except:
        return "Try again after some time"

def get_cgpa(username, pwd):
    data = return_results(username, pwd)
    if isinstance(data, str):
        return None

    data = data[0]

    columns = data[0]
    courses = data[1:]
    df = pd.DataFrame(columns=columns, index=list(range(0, len(courses))))

    for index, c in enumerate(courses):
        for i, j in enumerate(columns):
            if i >= len(c):
                break
            df.loc[index, j] = c[i]

    df.loc[:, ['S.No', 'COURSE SEM', 'CREDITS']] = df.loc[:, ['S.No', 'COURSE SEM', 'CREDITS']].astype(int)
    grades = defaultdict(int, {'O': 10, 'A+': 9, 'A': 8, 'B+': 7, 'B': 6, 'C': 5})

    gpa = 0.0

    for i in df.index:
        gpa += df.loc[i, 'CREDITS'] * grades[df.loc[i, 'GRADE']]

    cgpa = gpa / df.loc[:, 'CREDITS'].sum()

    return cgpa


import streamlit as st

st.title("CGPA Calculator")

# Create a form for login
with st.form("Ecampus Login"):
    st.subheader("Enter your credentials:")
    
    username = st.text_input("Username:")
    password = st.text_input("Password:", type="password")
    
    submitted = st.form_submit_button("Login")
    
    if submitted:
        cgpa = get_cgpa(username, password)
        if username and password and cgpa != None:
            st.success(f"Welcome, {username}!")
            st.write(f"Roll No: {username}")
            st.write(f"CGPA: {cgpa}")
        else:
            st.error("Please provide correct username and password.")
