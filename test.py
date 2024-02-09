import streamlit as st

def main():
    st.title("Ravinder Gulla's Portfolio")
    st.write("Welcome to my portfolio web app! Here, you can learn more about me and my projects.")

    # About Me section
    st.header("About Me")
    st.write("I am a passionate developer interested in creating amazing web applications.")

    # My Projects section
    st.header("My Projects")

    project1 = {
        "name": "Project 1",
        "description": "Description of Techin510 Lab 1.",
        "link": "https://github.com/rgulla16/Techin510"
    }

    project2 = {
        "name": "Project 2",
        "description": "Description of Techin510 Lab 2.",
        "link": "https://github.com/rgulla16/Techin510"
    }

    display_project(project1)
    display_project(project2)

    # Contact Me section
    st.header("Contact Me")
    st.write("Feel free to reach out to me via email: rgulla@uw.edu")

def display_project(project):
    st.subheader(project["name"])
    st.write(project["description"])
    st.write("GitHub Repository:", project["link"])

if __name__ == "__main__":
    main()