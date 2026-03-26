import streamlit as st
import streamlit.components.v1 as components
import json
import os
import math
import pandas as pd
from datetime import datetime

# --- KONFIGŪRACIJA ---
st.set_page_config(page_title="Jorės Mokykla", page_icon="🏫", layout="wide")


def load_data():
    if not os.path.exists("../tasks.json"):
        return {}
    with open("../tasks.json", "r", encoding="utf-8") as f:
        return json.load(f)


def save_detailed_log(rinkinys, diena, task_name, user_ans, correct_ans):
    """Išsaugo kiekvieną Jorės įvestą atsakymą į CSV failą."""
    log_file = "../detalus_atsakymai.csv"
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
    """Nupiešia analoginį laikrodį."""
    try:
        h, m = map(int, time_str.split(':'))
        hour_angle, min_angle = (h % 12) * 30 + m * 0.5, m * 6
        nums = "".join([
                           f'<text x="{50 + 36 * math.cos(math.radians(i * 30 - 90))}" y="{52 + 36 * math.sin(math.radians(i * 30 - 90))}" font-size="7" font-family="Arial" font-weight="bold" text-anchor="middle" fill="#333">{i}</text>'
                           for i in range(1, 13)])
        html = f"""<div style="display: flex; justify-content: center;"><svg width="180" height="180" viewBox="0 0 100 100"><circle cx="50" cy="50" r="48" stroke="#333" stroke-width="2" fill="#f8f9fa" /><circle cx="50" cy="50" r="44" stroke="white" stroke-width="1" fill="white" />{nums}<line x1="50" y1="50" x2="50" y2="28" stroke="#222" stroke-width="3.5" stroke-linecap="round" transform="rotate({hour_angle} 50 50)" /><line x1="50" y1="50" x2="50" y2="15" stroke="#D32F2F" stroke-width="2" stroke-linecap="round" transform="rotate({min_angle} 50 50)" /><circle cx="50" cy="50" r="2.5" fill="#333" /></svg></div>"""
        components.html(html, height=190)
    except:
        st.write("Laikrodžio klaida")


# --- PROGRAMOS PRADŽIA ---
data = load_data()
if not data:
    st.error("Klaida: Nerastas 'tasks.json' failas!")
    st.stop()

# --- ŠONINIS MENIU ---
st.sidebar.title("🎮 Valdymas")
mode = st.sidebar.radio("Pasirinkite rėžimą:", ["📖 Jorės pamokos", "👨‍🏫 Tėčio kambarys (Logai)"])

# --- 👨‍🏫 TĖČIO KAMBARYS (LOGAI IR ŽODYNAS) ---
if mode == "👨‍🏫 Tėčio kambarys (Logai)":
    st.title("👨‍🏫 Mokytojo apžvalga")

    tab1, tab2 = st.tabs(["📋 Visi Jorės atsakymai", "🔤 Sukauptas žodynas"])

    with tab1:
        st.subheader("Detalus atsakymų žurnalas")
        if os.path.exists("../detalus_atsakymai.csv"):
            log_df = pd.read_csv("../detalus_atsakymai.csv")
            st.dataframe(log_df.iloc[::-1], use_container_width=True)  # Naujausi viršuje
            if st.button("Išvalyti visą istoriją"):
                os.remove("../detalus_atsakymai.csv")
                st.rerun()
        else:
            st.info("Istorija tuščia. Jorė dar neišsaugojo jokių atsakymų.")

    with tab2:
        st.subheader("📚 Žodžiai, kuriuos mokomės")
        vocab = []
        for rink in data:
            for diena in data[rink]:
                for task in data[rink][diena]:
                    if task["type"] == "translation":
                        for lt, en in zip(task["lt_words"], task["en_answers"]):
                            vocab.append({"Lietuviškai": lt, "Angliškai": en, "Šaltinis": f"{rink} - {diena}"})
        if vocab:
            st.table(pd.DataFrame(vocab))
        else:
            st.info("Žodynas tuščias.")

# --- 📖 JORĖS PAMOKOS ---
else:
    all_weeks = list(data.keys())
    sel_week = st.sidebar.selectbox("📦 Pasirink Rinkinį:", all_weeks)

    all_days = list(data[sel_week].keys())
    sel_day = st.sidebar.selectbox("📅 Pasirink Dieną:", all_days)

    st.title(f"🌟 {sel_week} — {sel_day}")
    st.divider()

    tasks = data[sel_week][sel_day]
    score = 0
    total = 0

    for s_idx, sec in enumerate(tasks):
        with st.container(border=True):
            st.subheader(f"{sec.get('symbol', '📝')} {sec['subject']}")

            # 1. VERTIMAS
            if sec["type"] == "translation":
                for i, lt_w in enumerate(sec["lt_words"]):
                    total += 1
                    st.write(f"**Kaip angliškai:** {lt_w}?")
                    ans = st.text_input("Tavo atsakymas:", key=f"tr_{sel_week}_{sel_day}_{s_idx}_{i}").strip()

                    if ans.lower() == sec["en_answers"][i].lower():
                        score += 1

                    if st.button(f"Išsaugoti '{lt_w}'", key=f"btn_tr_{sel_week}_{sel_day}_{s_idx}_{i}"):
                        save_detailed_log(sel_week, sel_day, f"Vertimas: {lt_w}", ans, sec['en_answers'][i])
                        if ans.lower() == sec["en_answers"][i].lower():
                            st.success("Puiku! Teisingai. 🌟")
                        else:
                            st.error(f"Beveik! Teisingas žodis yra: {sec['en_answers'][i]}")

            # 2. TEKSTAS / MATEMATIKA
            elif sec["type"] in ["text", "area"]:
                for i, p in enumerate(sec["prompts"]):
                    total += 1
                    if sec["type"] == "area":
                        ans = st.text_area(p, key=f"ar_{sel_week}_{sel_day}_{s_idx}_{i}")
                    else:
                        ans = st.text_input(p, key=f"tx_{sel_week}_{sel_day}_{s_idx}_{i}")

                    correct = sec["answers"][i] if sec.get("check") else "Laisvas tekstas"

                    if sec.get("check"):
                        if ans.lower().replace(',', '.') == correct.lower().replace(',', '.'):
                            score += 1
                    elif ans.strip():  # Jei tai istorija ir laukelis netuščias, duodam tašką
                        score += 1

                    if st.button("Išsaugoti atsakymą", key=f"btn_tx_{sel_week}_{sel_day}_{s_idx}_{i}"):
                        save_detailed_log(sel_week, sel_day, p[:50], ans, correct)
                        if sec.get("check"):
                            if ans.lower().replace(',', '.') == correct.lower().replace(',', '.'):
                                st.success("Teisingai! ✅")
                            else:
                                st.error(f"Oi, turėtų būti: {correct}")
                        else:
                            st.success("Išsaugota! 👍")

            # 3. LAIKRODIS
            elif sec["type"] == "clock":
                for i, p in enumerate(sec["prompts"]):
                    total += 1
                    st.write(f"**{p}**")
                    draw_clock(sec["times"][i])
                    ans = st.text_input("Įrašyk laiką (HH:MM):", key=f"cl_{sel_week}_{sel_day}_{s_idx}_{i}").strip()

                    if ans == sec["times"][i]:
                        score += 1

                    if st.button("Išsaugoti laiką", key=f"btn_cl_{sel_week}_{sel_day}_{s_idx}_{i}"):
                        save_detailed_log(sel_week, sel_day, "Laikrodis", ans, sec["times"][i])
                        if ans == sec["times"][i]:
                            st.success("Tiksliai! 🕒")
                        else:
                            st.error(f"Ne visai. Laikrodis rodo {sec['times'][i]}")

            # 4. SEKOS
            elif sec["type"] == "sequence":
                for i, p in enumerate(sec["prompts"]):
                    total += 1
                    st.write(f"**Tęsk seką:** {p}")
                    cols = st.columns(4)
                    u_vals = [cols[j].text_input("", key=f"sq_{sel_week}_{sel_day}_{s_idx}_{i}_{j}",
                                                 label_visibility="collapsed").strip() for j in range(4)]

                    if [v.lower() for v in u_vals] == [c.lower() for c in sec["answers"][i]]:
                        score += 1

                    if st.button("Išsaugoti seką", key=f"btn_sq_{sel_week}_{sel_day}_{s_idx}_{i}"):
                        save_detailed_log(sel_week, sel_day, f"Seka: {p}", str(u_vals), str(sec["answers"][i]))
                        if [v.lower() for v in u_vals] == [c.lower() for c in sec["answers"][i]]:
                            st.success("Puiki seka! 🔢")
                        else:
                            st.error(f"Turėjo būti: {', '.join(sec['answers'][i])}")

    # --- ŠONINĖS JUOSTOS PROGRESAS ---
    st.sidebar.divider()
    st.sidebar.metric("Surinkti Taškai", f"{score} / {total}")
    if total > 0:
        st.sidebar.progress(score / total)

    # --- FINALINIS DIENOS PABAIGOS MYGTUKAS ---
    st.divider()
    st.write("### Baigei visas užduotis? 🎉")
    if st.button("BAIGTI ŠIOS DIENOS UŽDUOTIS 🏆", use_container_width=True, type="primary"):
        if score == total:
            st.balloons()
            st.success("Šaunuolė! Visos šios dienos užduotys atliktos tobulai! Eik ilsėtis! 🍦")
        else:
            st.warning(
                f"Diena baigta, bet surinkai {score} iš {total} taškų. Pasitikrink, ar viską atsakiai teisingai ir išsaugojai!")