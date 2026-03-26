import streamlit as st
import streamlit.components.v1 as components
import json, os, math, pandas as pd
from datetime import datetime

# --- KONFIGŪRACIJA ---
st.set_page_config(page_title="Jorės Mokykla", page_icon="🏫", layout="wide")


def load_data():
    if not os.path.exists("tasks.json"): return {}
    with open("tasks.json", "r", encoding="utf-8") as f: return json.load(f)


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


# --- PROGRAMA ---
data = load_data()
if not data:
    st.error("Nerastas tasks.json!")
    st.stop()

st.sidebar.title("🎮 Valdymas")
mode = st.sidebar.radio("Režimas:", ["📖 Jorės pamokos", "👨‍🏫 Tėčio kambarys"])

if mode == "👨‍🏫 Tėčio kambarys":
    st.title("👨‍🏫 Apžvalga")
    t1, t2 = st.tabs(["📋 Atsakymai", "🔤 Žodynas"])
    with t1:
        if os.path.exists("detalus_atsakymai.csv"):
            df = pd.read_csv("detalus_atsakymai.csv")
            st.dataframe(df.iloc[::-1], use_container_width=True)
            if st.button("Trinti istoriją"):
                os.remove("detalus_atsakymai.csv")
                st.rerun()
    with t2:
        vocab = []
        for r in data:
            for d in data[r]:
                for t in data[r][d]:
                    if t["type"] == "translation":
                        for lt, en in zip(t["lt_words"], t["en_answers"]):
                            vocab.append({"Lietuviškai": lt, "Angliškai": en, "Šaltinis": f"{r}-{d}"})
        if vocab:
            st.table(pd.DataFrame(vocab).drop_duplicates())
        else:
            st.info("Žodynas tuščias")

else:
    sel_week = st.sidebar.selectbox("📦 Rinkinys:", list(data.keys()))
    sel_day = st.sidebar.selectbox("📅 Diena:", list(data[sel_week].keys()))

    st.title(f"🌟 {sel_week} — {sel_day}")
    tasks = data[sel_week][sel_day]
    score, total = 0, 0

    for s_idx, sec in enumerate(tasks):
        with st.container(border=True):
            st.subheader(f"{sec.get('symbol', '📝')} {sec['subject']}")

            # --- Dinaminis stulpelių valdymas matematikai ---
            # Jei užduočių daug (pvz. sekmadienį), skaidome į 4 stulpelius
            prompts = sec.get("prompts", [])
            is_math_heavy = len(prompts) > 4 and sec["type"] == "text"

            if is_math_heavy:
                cols = st.columns(4)

            for i, p in enumerate(prompts):
                total += 1
                key = f"{sel_week}_{sel_day}_{s_idx}_{i}"

                # Pasirenkame, kur dėti laukelį
                target = cols[i % 4] if is_math_heavy else st

                if sec["type"] == "translation":
                    st.write(f"**{sec['lt_words'][i]}**")
                    ans = st.text_input("Atsakymas anglų k.", key=f"tr_{key}", label_visibility="collapsed").strip()
                    correct = sec["en_answers"][i]

                elif sec["type"] == "clock":
                    draw_clock(sec["times"][i])
                    ans = st.text_input("Laikas (HH:MM)", key=f"cl_{key}", label_visibility="collapsed").strip()
                    correct = sec["times"][i]

                elif sec["type"] == "sequence":
                    st.write(p)
                    sq_cols = st.columns(4)
                    u_vals = []
                    for j in range(4):
                        v = sq_cols[j].text_input(f"Seka {j}", key=f"sq_{key}_{j}",
                                                  label_visibility="collapsed").strip()
                        u_vals.append(v)
                    ans, correct = str(u_vals), str(sec["answers"][i])

                elif sec["type"] == "area":
                    st.write(f"**{p}**")
                    ans = st.text_area("Tavo istorija", key=f"ar_{key}", label_visibility="collapsed")
                    correct = "Laisvas tekstas"

                else:  # Standartinis text/math
                    target.write(p)
                    ans = target.text_input("Atsakymas", key=f"tx_{key}", label_visibility="collapsed").strip()
                    correct = sec["answers"][i] if sec.get("check") else "Laisvas"

                # Tikrinimas
                is_correct = False
                if sec["type"] == "sequence":
                    is_correct = [v.lower() for v in u_vals] == [c.lower() for c in sec["answers"][i]]
                elif sec.get("check", True) and correct != "Laisvas tekstas":
                    is_correct = ans.lower().replace(',', '.') == str(correct).lower().replace(',', '.')
                else:
                    is_correct = len(ans.strip()) > 2  # Jei laisvas tekstas, užtenka kelių simbolių

                if is_correct: score += 1

                # Mažas išsaugojimo mygtukas po kiekvienu (tik jei ne matematinė "paklodė")
                if not is_math_heavy:
                    if st.button("Išsaugoti", key=f"btn_{key}"):
                        save_detailed_log(sel_week, sel_day, p or sec['subject'], ans, correct)
                        st.toast("Išsaugota!")

    # --- ŠONINĖS JUOSTOS PROGRESAS ---
    st.sidebar.divider()
    st.sidebar.metric("Surinkti Taškai", f"{score} / {total}")
    if total > 0: st.sidebar.progress(score / total)

    # --- PABAIGOS MYGTUKAS ---
    st.divider()
    if st.button("BAIGTI ŠIOS DIENOS UŽDUOTIS 🏆", use_container_width=True, type="primary"):
        # Išsaugom galutinį rezultatą į logus
        save_detailed_log(sel_week, sel_day, "DIENOS REZULTATAS", f"{score}/{total}", "---")
        if score == total:
            st.balloons()
            st.success("Tobula! Viskas teisingai! 🎉")
        else:
            st.warning(f"Baigta! Rezultatas: {score} iš {total}. Pasitaisyk klaidas, jei nori balionų! 🎈")