import streamlit as st
import streamlit.components.v1 as components
import json
import os
import math
from datetime import datetime

# --- APP CONFIG ---
st.set_page_config(page_title="Jorės Mokykla", page_icon="🇱🇹", layout="centered")


def load_data():
    """Safe loading of tasks.json."""
    try:
        if not os.path.exists("tasks.json"):
            st.error("Nerastas 'tasks.json' failas!")
            return {}
        with open("tasks.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"JSON Klaida: {e}")
        return {}


def draw_clock(time_str):
    """Upgraded Analog Clock with 1-12 numbers and distinct hands."""
    try:
        h, m = map(int, time_str.split(':'))
        hour_angle = (h % 12) * 30 + m * 0.5
        min_angle = m * 6

        # Math for Number Placement
        nums = ""
        for i in range(1, 13):
            angle = math.radians(i * 30 - 90)
            x, y = 50 + 36 * math.cos(angle), 52 + 36 * math.sin(angle)
            nums += f'<text x="{x}" y="{y}" font-size="7" font-family="Arial" font-weight="bold" text-anchor="middle" fill="#333">{i}</text>'

        html = f"""
        <div style="display: flex; justify-content: center;">
            <svg width="200" height="200" viewBox="0 0 100 100">
                <circle cx="50" cy="50" r="48" stroke="#333" stroke-width="2" fill="#f8f9fa" />
                <circle cx="50" cy="50" r="44" stroke="white" stroke-width="1" fill="white" />
                {nums}
                <line x1="50" y1="50" x2="50" y2="28" stroke="#222" stroke-width="3.5" stroke-linecap="round" transform="rotate({hour_angle} 50 50)" />
                <line x1="50" y1="50" x2="50" y2="15" stroke="#D32F2F" stroke-width="2" stroke-linecap="round" transform="rotate({min_angle} 50 50)" />
                <circle cx="50" cy="50" r="2.5" fill="#333" />
            </svg>
        </div>
        """
        components.html(html, height=210)
    except:
        st.warning("Nepavyko pavaizduoti laikrodžio.")


# --- UI START ---
data = load_data()

if data:
    # Header Section
    c1, c2 = st.columns([5, 1])
    c1.title("🇱🇹 Jorės Mokymosi Centras")
    c2.image("https://flagcdn.com/w80/lt.png")

    days = list(data.keys())
    selected_day = st.selectbox("Pasirink savaitės dieną:", days)
    st.divider()

    day_tasks = data[selected_day]
    score, total_tasks = 0, 0

    for s_idx, sec in enumerate(day_tasks):
        st.header(f"{sec.get('symbol', '📝')} {sec['subject']}")

        # 1. TRANSLATION (Monday)
        if sec["type"] == "translation":
            for i, p in enumerate(sec["prompts"]):
                lt_word = sec["lt_words"][i]
                correct = sec["en_answers"][i]
                st.write(f"**{p}:** {lt_word}")
                ans = st.text_input("Angliškai:", key=f"tr_{s_idx}_{i}").strip()
                total_tasks += 1
                if ans.lower() == correct.lower():
                    st.success("Teisingai!")
                    score += 1

        # 2. SEQUENCE (Monday)
        elif sec["type"] == "sequence":
            for i, p in enumerate(sec["prompts"]):
                st.write(f"**{p}**")
                cols = st.columns(4)
                user_vals = [cols[j].text_input("", key=f"sq_{s_idx}_{i}_{j}", label_visibility="collapsed").strip() for
                             j in range(4)]
                total_tasks += 1
                if [v.lower() for v in user_vals] == [c.lower() for c in sec["answers"][i]]:
                    st.success("Puiku!")
                    score += 1

        # 3. TEXT / AREA (Sentences, Stories, Logic, Money)
        elif sec["type"] in ["text", "area"]:
            for i, p in enumerate(sec["prompts"]):
                if sec["type"] == "area":
                    ans = st.text_area(p, key=f"ar_{s_idx}_{i}", placeholder="Parašyk savo pasakojimą čia...").strip()
                else:
                    ans = st.text_input(p, key=f"tx_{s_idx}_{i}").strip()

                total_tasks += 1
                if ans:
                    if sec.get("check", True):  # Checks for exact answers (Math/Time)
                        if ans.lower().replace(',', '.') == sec["answers"][i].lower():
                            st.success("Teisingai! ✅")
                            score += 1
                    else:  # Checks for length/punctuation (Stories/Sentences)
                        # Verifies at least 2 punctuation marks for stories
                        punctuation = ans.count('.') + ans.count('!') + ans.count('?')
                        if sec["type"] == "area" and punctuation < 2:
                            st.warning("Parašyk šiek tiek daugiau (bent 2 sakinius)!")
                        else:
                            st.success("Šaunuolė! Atlikta. 👍")
                            score += 1

        # 4. CLOCK (Wednesday)
        elif sec["type"] == "clock":
            for i, p in enumerate(sec["prompts"]):
                st.write(f"**{p}**")
                draw_clock(sec["times"][i])
                ans = st.text_input("Laikas (pvz., 03:30):", key=f"cl_{s_idx}_{i}").strip()
                total_tasks += 1
                if ans == sec["times"][i]:
                    st.success("Laikas teisingas! 🕒")
                    score += 1

    # --- PROGRESS BAR ---
    st.sidebar.metric("Tavo taškai", f"{score} / {total_tasks}")
    if total_tasks > 0:
        st.sidebar.progress(score / total_tasks)

    # --- SAVE / FINISH ---
    st.divider()
    if st.button("Išsaugoti ir Baigti 🎉", use_container_width=True):
        if score == total_tasks:
            st.balloons()
            if "Friday" in selected_day or "Penktadienis" in selected_day:
                st.success("VALIO! Įveikei visą savaitę! Gero savaitgalio! 🍦")
            else:
                st.success("Šios dienos užduotys atliktos puikiai!")
        else:
            st.warning(f"Liko {total_tasks - score} nebaigtos užduotys.")