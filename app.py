import streamlit as st
import json
import csv
import os
from datetime import datetime

st.set_page_config(page_title="Užduotys", page_icon="📚", layout="centered")


# --- LOAD DATA ---
# This function loads the tasks from your JSON file
def load_tasks(filepath="tasks.json"):
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        st.error("Nerastas tasks.json failas! Prašau sukurti failą su užduotimis.")
        return {}


# This function saves the answers to a CSV log file
def save_log(day, answers_dict):
    file_exists = os.path.isfile("log.csv")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("log.csv", mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        # Write headers if the file is brand new
        if not file_exists:
            writer.writerow(["Data ir Laikas", "Diena", "Užduotis", "Atliktas Atsakymas"])

        # Write each answer as a new row
        for question, answer in answers_dict.items():
            writer.writerow([timestamp, day, question, answer])


# --- MAIN APP LOGIC ---
st.title("📚 Jorės Dienos Užduotys")
st.write("Pasirink savaitės dieną ir atlik savo dienos užduotis!")

tasks_data = load_tasks()

if tasks_data:
    # Get the days available in the JSON file
    days_available = list(tasks_data.keys())

    # Try to guess today's day to set as default, otherwise pick the first one
    current_weekday = datetime.today().weekday()
    default_index = current_weekday if current_weekday < len(days_available) else 0

    selected_day = st.selectbox("Kokia šiandien diena?", days_available, index=default_index)

    st.divider()

    # We use a dictionary to temporarily store her answers on the screen
    current_answers = {}

    # Dynamically generate the layout based on the JSON file
    day_tasks = tasks_data[selected_day]

    for section in day_tasks:
        st.header(section["subject"])
        if section["description"]:
            st.write(section["description"])

        for prompt in section["prompts"]:
            # Create a unique key for Streamlit to track each input box
            unique_key = f"{selected_day}_{section['subject']}_{prompt}"
            # Show the text input and save what she types into our dictionary
            user_input = st.text_input(prompt, key=unique_key)
            current_answers[prompt] = user_input

    st.divider()

    # --- SAVE BUTTON ---
    if st.button("Išsaugoti ir Užbaigti Dienos Užduotis! 🎉"):
        # Check if all fields are filled out (optional, but good practice)
        if all(value.strip() != "" for value in current_answers.values()):
            save_log(selected_day, current_answers)
            st.success("Šaunuolė! Užduotys sėkmingai atliktos ir išsaugotos į žurnalą. 🌟")
            st.balloons()
        else:
            st.warning("Prieš išsaugant, prašau užpildyti visus laukelius! ✍️")