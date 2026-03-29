import streamlit as st
import streamlit.components.v1 as components
import json, os, math, random
import pandas as pd
from datetime import datetime

# --- KONFIGŪRACIJA ---
st.set_page_config(page_title="Jorės Mokykla", page_icon="🏫", layout="wide")


def load_json(filename):
    if not os.path.exists(filename):
        return {} if filename == "tasks.json" else []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content: return {} if filename == "tasks.json" else []
            return json.loads(content)
    except:
        return {} if filename == "tasks.json" else []


def save_detailed_log(rinkinys, diena, task_name, user_ans, correct_ans):
    log_file = "detalus_atsakymai.csv"
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    new_entry = pd.DataFrame([[now, rinkinys, diena, task_name, user_ans, correct_ans]],
                             columns=["Laikas", "Rinkinys", "Diena", "Užduotis", "Jorės Atsakymas",
                                      "Teisingas Atsakymas"])
    if os.path.exists(log_file):
        df = pd.read_csv(log_file)
        df = pd.concat([df, new_entry], ignore_index=True)
    else:
        df = new_entry
    df.to_csv(log_file, index=False)


def draw_clock(time_str):
    try:
        h, m = map(int, time_str.split(':'))
        hour_angle, min_angle = (h % 12) * 30 + m * 0.5, m * 6
        nums = "".join([
                           f'<text x="{50 + 36 * math.cos(math.radians(i * 30 - 90))}" y="{52 + 36 * math.sin(math.radians(i * 30 - 90))}" font-size="7" font-weight="bold" text-anchor="middle" fill="#333">{i}</text>'
                           for i in range(1, 13)])
        html = f"""<div style="text-align:center"><svg width="150" height="150" viewBox="0 0 100 100"><circle cx="50" cy="50" r="48" stroke="#333" stroke-width="2" fill="white"/>{nums}<line x1="50" y1="50" x2="50" y2="30" stroke="black" stroke-width="3" transform="rotate({hour_angle} 50 50)"/><line x1="50" y1="50" x2="50" y2="15" stroke="red" stroke-width="2" transform="rotate({min_angle} 50 50)"/></svg></div>"""
        components.html(html, height=160)
    except:
        st.error("Laikrodžio formatas HH:MM!")


# --- DUOMENŲ UŽKROVIMAS ---
data = load_json("tasks.json")
numbers_db = load_json("numbers.json")
logic_db = load_json("logic.json")

st.sidebar.title("🎮 Valdymas")
mode = st.sidebar.radio("Režimas:", ["📖 Pamokos", "🧮 Matematika", "🧩 Logika", "👨‍🏫 Tėčiui"])

# --- 🧩 LOGIKA ---
if mode == "🧩 Logika":
    st.title("🧩 Loginių mįslių kampelis")
    if not logic_db:
        st.warning("Užpildyk logic.json failą!")
    else:
        if 'logic_drill' not in st.session_state: st.session_state.logic_drill = []
        c1, c2 = st.columns([1, 2])
        kiek = c1.slider("Kiek mįslių?", 3, 10, 5)
        if c2.button("🎲 Naujos mįslės", type="primary"):
            st.session_state.logic_drill = random.sample(logic_db, min(kiek, len(logic_db)))

        if st.session_state.logic_drill:
            score = 0
            for i, task in enumerate(st.session_state.logic_drill):
                with st.container(border=True):
                    st.write(f"**{i + 1}. {task['q']}**")
                    ans = st.text_input("Tavo atsakymas", key=f"log_{i}", label_visibility="collapsed").strip().lower()
                    if ans == task['a'].lower():
                        st.success("Teisingai! ✨")
                        score += 1
            if score == len(st.session_state.logic_drill) and score > 0:
                st.balloons()

# --- 🧮 MATEMATIKA ---
elif mode == "🧮 Matematika":
    st.title("🧮 Skaičių laboratorija")
    if not numbers_db:
        st.warning("numbers.json tuščias!")
    else:
        if 'math_drill' not in st.session_state: st.session_state.math_drill = []
        c1, c2 = st.columns([1, 2])
        kiek = c1.selectbox("Užduočių skaičius", [8, 12, 16, 24])
        if c2.button("🎲 Generuoti veiksmus", type="primary"):
            st.session_state.math_drill = random.sample(numbers_db, min(kiek, len(numbers_db)))

        if st.session_state.math_drill:
            m_cols = st.columns(4)
            score = 0
            for i, t in enumerate(st.session_state.math_drill):
                col = m_cols[i % 4]
                col.write(f"**{t['q']}**")
                ans = col.text_input("Ats", key=f"m_{i}", label_visibility="collapsed").strip()
                if ans.replace(',', '.') == str(t['a']).replace(',', '.'): score += 1
            st.sidebar.metric("Progresas", f"{score}/{len(st.session_state.math_drill)}")
            if score == len(st.session_state.math_drill) and score > 0: st.balloons()

# --- 📖 PAMOKOS ---
elif mode == "📖 Pamokos":
    if not data: st.error("tasks.json nerastas arba tuščias!"); st.stop()

    sel_week = st.sidebar.selectbox("📦 Rinkinys:", list(data.keys()))
    sel_day = st.sidebar.selectbox("📅 Diena:", list(data[sel_week].keys()))
    st.title(f"🌟 {sel_week} — {sel_day}")

    score, total = 0, 0
    for s_idx, sec in enumerate(data[sel_week][sel_day]):
        with st.container(border=True):
            # Rodome simbolį ir temos pavadinimą aiškiai
            st.subheader(f"{sec.get('symbol', '📝')} {sec['subject']}")

            prompts = sec.get("prompts", [])
            is_math_heavy = len(prompts) > 4 and sec["type"] == "text"
            cols = st.columns(4) if is_math_heavy else [st]

            for i, p in enumerate(prompts):
                total += 1
                key = f"p_{sel_week}_{sel_day}_{s_idx}_{i}"
                target = cols[i % 4] if is_math_heavy else st

                if sec["type"] == "translation":
                    target.write(f"**{sec['lt_words'][i]}**")
                    ans = target.text_input("Vertimas", key=f"tr_{key}", label_visibility="collapsed").strip()
                    correct = sec["en_answers"][i]
                elif sec["type"] == "clock":
                    draw_clock(sec["times"][i])
                    ans = target.text_input("HH:MM", key=f"cl_{key}", label_visibility="collapsed").strip()
                    correct = sec["times"][i]
                elif sec["type"] == "sequence":
                    target.write(p)
                    sq_c = st.columns(4)
                    u_vals = [sq_c[j].text_input(f"s{j}", key=f"sq_{key}_{j}", label_visibility="collapsed").strip() for
                              j in range(4)]
                    ans, correct = str(u_vals), str(sec["answers"][i])
                elif sec["type"] == "area":
                    target.write(f"**{p}**")
                    ans = target.text_area("Tekstas", key=f"ar_{key}", label_visibility="collapsed")
                    correct = "Laisvas"
                else:
                    target.write(p)
                    ans = target.text_input("Atsakymas", key=f"tx_{key}", label_visibility="collapsed").strip()
                    correct = sec["answers"][i] if sec.get("check") else "Laisvas"

                # Tikrinimas
                is_ok = False
                if sec["type"] == "sequence":
                    is_ok = [v.lower() for v in u_vals] == [c.lower() for c in sec["answers"][i]]
                elif sec.get("check", True) and correct != "Laisvas":
                    is_ok = ans.lower().replace(',', '.') == str(correct).lower().replace(',', '.')
                else:
                    is_ok = len(ans.strip()) > 2

                if is_ok: score += 1

    st.sidebar.divider()
    st.sidebar.metric("Šios dienos progresas", f"{score}/{total}")
    if st.button("IŠSAUGOTI REZULTATĄ 🏆", use_container_width=True, type="primary"):
        save_detailed_log(sel_week, sel_day, "DIENOS PLANAS", f"{score}/{total}", "-")
        st.success("Rezultatas įrašytas į tėčio žurnalą!")
        if score == total and total > 0: st.balloons()

# --- 👨‍🏫 TĖČIUI ---
else:
    st.title("👨‍🏫 Administravimas")
    if os.path.exists("detalus_atsakymai.csv"):
        df = pd.read_csv("detalus_atsakymai.csv")
        st.dataframe(df.iloc[::-1], use_container_width=True)
        if st.button("Išvalyti istoriją"):
            os.remove("detalus_atsakymai.csv")
            st.rerun()
    else:
        st.info("Istorija tuščia. Jorė dar nesprendė užduočių!")