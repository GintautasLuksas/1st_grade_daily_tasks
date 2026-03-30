import streamlit as st
import streamlit.components.v1 as components
import json, os, math, random
import pandas as pd
from datetime import datetime
from typing import Tuple

st.set_page_config(page_title="Jorės Mokykla", page_icon="🌟", layout="wide")

# ─────────────────────────────────────────────────────────────────
# GLOBALŪS STILIAI
# ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');

/* === PAGRINDINIS FONAS IR TEKSTAS === */
html, body, [data-testid="stAppViewContainer"] {
    background-color: #0f172a !important; /* Labai tamsi mėlyna */
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    color: #f1f5f9 !important;
}

/* === ŠONINĖ JUOSTA (MODERNUS GRADIENTAS) === */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%) !important;
    border-right: 1px solid #334155 !important;
}
[data-testid="stSidebar"] * { color: #cbd5e1 !important; }

/* === UŽDUOČIŲ BLOKAI (GLASSMORPHISM) === */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(30, 41, 59, 0.7) !important; /* Permatomas tamsus fonas */
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 24px !important;
    padding: 24px !important;
    margin-bottom: 20px !important;
    box-shadow: 0 10px 30px rgba(0,0,0,0.3) !important;
    backdrop-filter: blur(10px);
}

/* === ANTRAŠTĖS === */
h1 {
    color: #f8fafc !important;
    font-weight: 800 !important;
    letter-spacing: -1px !important;
    background: linear-gradient(90deg, #818cf8, #34d399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    padding-bottom: 10px;
}
h2, h3 { color: #e2e8f0 !important; font-weight: 700 !important; }

/* === ĮVEDIMO LAUKAI (DARK MODE) === */
input[type="text"], textarea {
    background: #1e293b !important;
    border: 2px solid #334155 !important;
    color: #f8fafc !important;
    border-radius: 16px !important;
    padding: 12px 16px !important;
    transition: all 0.3s ease !important;
}
input[type="text"]:focus {
    border-color: #6366f1 !important;
    background: #1e293b !important;
    box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.2) !important;
}

/* === VERTIMO IR MATEMATIKOS KORTELĖS === */
.lt-card {
    background: rgba(99, 102, 241, 0.15);
    border: 1px solid rgba(99, 102, 241, 0.4);
    border-radius: 16px;
    padding: 15px;
    font-size: 1.6rem;
    font-weight: 800;
    color: #a5b4fc;
    text-shadow: 0 0 15px rgba(99, 102, 241, 0.5);
}
.math-q {
    background: rgba(52, 211, 153, 0.1);
    border: 1px solid rgba(52, 211, 153, 0.3);
    border-radius: 12px;
    padding: 12px;
    font-size: 1.3rem;
    color: #6ee7b7;
    font-weight: 700;
}

/* === REZULTATŲ KORTELĖ ŠONE === */
.score-card {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 20px;
    padding: 20px;
}
.score-num { color: #fbbf24 !important; font-size: 2.2rem; font-weight: 900; }

/* === MYGTUKAI === */
.stButton > button {
    background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 12px 24px !important;
    font-weight: 700 !important;
    box-shadow: 0 4px 15px rgba(79, 70, 229, 0.4) !important;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(79, 70, 229, 0.5) !important;
}

/* === FEEDBACK ŽENKLIUKAI === */
.fb-ok { background: #064e3b; color: #34d399; border-radius: 12px; padding: 4px 12px; font-weight: 700; }
.fb-err { background: #450a0a; color: #f87171; border-radius: 12px; padding: 4px 12px; font-weight: 700; }

/* === LAIKRODIS (SUDERINIMAS SU DARK MODE) === */
svg circle { fill: #1e293b !important; stroke: #334155 !important; }
svg text { fill: #94a3b8 !important; }
svg line[stroke="#1e1b4b"] { stroke: #f8fafc !important; } /* Valandos rodyklė */

</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────
# PAGALBINĖS FUNKCIJOS
# ─────────────────────────────────────────────────────────────────

def load_json(filename):
    if not os.path.exists(filename):
        return {} if filename == "tasks.json" else []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return {} if filename == "tasks.json" else []
            return json.loads(content)
    except:
        return {} if filename == "tasks.json" else []


def save_detailed_log(rinkinys, diena, task_name, user_ans, correct_ans):
    log_file = "detalus_atsakymai.csv"
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    new_entry = pd.DataFrame(
        [[now, rinkinys, diena, task_name, user_ans, correct_ans]],
        columns=["Laikas", "Rinkinys", "Diena", "Uzduotis", "Jores Atsakymas", "Teisingas Atsakymas"]
    )
    if os.path.exists(log_file):
        df = pd.read_csv(log_file)
        df = pd.concat([df, new_entry], ignore_index=True)
    else:
        df = new_entry
    df.to_csv(log_file, index=False)


def draw_clock(time_str):
    try:
        h, m = map(int, time_str.split(':'))
        hour_angle = (h % 12) * 30 + m * 0.5
        min_angle = m * 6
        ticks = "".join([
            f'<line x1="{50+43*math.cos(math.radians(a)):.1f}" y1="{50+43*math.sin(math.radians(a)):.1f}" '
            f'x2="{50+47*math.cos(math.radians(a)):.1f}" y2="{50+47*math.sin(math.radians(a)):.1f}" '
            f'stroke="#94a3b8" stroke-width="2" stroke-linecap="round"/>'
            for a in [i*30-90 for i in range(12)]
        ])
        nums = "".join([
            f'<text x="{50+36*math.cos(math.radians(i*30-90)):.1f}" '
            f'y="{54+36*math.sin(math.radians(i*30-90)):.1f}" '
            f'font-family="Nunito,sans-serif" font-size="9" font-weight="700" '
            f'text-anchor="middle" fill="#475569">{i}</text>'
            for i in range(1, 13)
        ])
        html = f"""
<div style="text-align:center;padding:6px 0;">
<svg width="165" height="165" viewBox="0 0 100 100">
  <circle cx="50" cy="50" r="47" fill="#f8fafc" stroke="#c7d2fe" stroke-width="2.5"/>
  <circle cx="50" cy="50" r="44" fill="none" stroke="#e0e7ff" stroke-width="0.5"/>
  {ticks}{nums}
  <line x1="50" y1="50" x2="50" y2="27" stroke="#1e1b4b" stroke-width="4.5"
        stroke-linecap="round" transform="rotate({hour_angle} 50 50)"/>
  <line x1="50" y1="50" x2="50" y2="13" stroke="#6c63ff" stroke-width="3"
        stroke-linecap="round" transform="rotate({min_angle} 50 50)"/>
  <circle cx="50" cy="50" r="3.5" fill="#6c63ff"/>
</svg>
<div style="font-size:0.75rem;color:#94a3b8;margin-top:2px;">violetine = minutes</div>
</div>"""
        components.html(html, height=190)
    except:
        st.error("Formatas: HH:MM")


def check_answer(ans: str, correct: str) -> bool:
    return ans.strip().lower().replace(',', '.') == str(correct).strip().lower().replace(',', '.')


def show_feedback(is_ok: bool, free: bool = False):
    if free:
        st.markdown('<span class="fb-ok">&#10003; Gerai!</span>', unsafe_allow_html=True)
    elif is_ok:
        st.markdown('<span class="fb-ok">&#10003; Teisingai!</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="fb-err">&#10007; Pamegink dar!</span>', unsafe_allow_html=True)


def sidebar_score(score: int, total: int, icon: str = "🌟"):
    pct = int(score / total * 100) if total else 0
    st.sidebar.markdown(f"""
<div class="score-card">
  <div class="score-num">{icon} {score}/{total}</div>
  <div class="score-pct">{pct}% teisingai</div>
</div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────
# DUOMENŲ UŽKROVIMAS
# ─────────────────────────────────────────────────────────────────
data       = load_json("tasks.json")
numbers_db = load_json("numbers.json")
logic_db   = load_json("logic.json")

# ─────────────────────────────────────────────────────────────────
# ŠONINĖ JUOSTA
# ─────────────────────────────────────────────────────────────────
st.sidebar.markdown("## 🌟 Jorės Mokykla")
mode = st.sidebar.radio(
    "Pasirink:",
    ["📖 Pamokos", "🧮 Matematika", "🧩 Logika", "👨‍🏫 Tėčiui"],
    label_visibility="collapsed"
)
st.sidebar.markdown("---")

# ═══════════════════════════════════════════════════════════════
#  🧩  LOGIKA
# ═══════════════════════════════════════════════════════════════
if mode == "🧩 Logika":
    st.markdown("# 🧩 Loginių mįslių kampelis")

    # Funkcija lietuviškų raidžių „nuvalymui“
    def simplify(text):
        mapping = str.maketrans("ąčęėįšųūž", "aceeisuuz")
        return text.lower().strip().translate(mapping)

    # --- PAGALBOS KODAS (MOKYTOJO REŽIMAS) ---
    with st.sidebar:
        st.markdown("---")
        secret_code = st.text_input("🔑 Pagalbos kodas", type="password", placeholder="Įvesk kodą...")
        show_hints = (secret_code == "2000")
        if show_hints:
            st.success("🔓 Atsakymai atidengti!")

    if not logic_db:
        st.warning("Užpildyk logic.json failą!")
    else:
        if 'logic_drill' not in st.session_state:
            st.session_state.logic_drill = []

        c1, c2 = st.columns([1, 2])
        kiek = c1.slider("Kiek mįslių?", 3, 15, 5)
        if c2.button("🎲 Naujos mįslės", type="primary"):
            st.session_state.logic_drill = random.sample(logic_db, min(kiek, len(logic_db)))

        st.markdown("")
        score = 0
        for i, task in enumerate(st.session_state.logic_drill):
            with st.container(border=True):
                st.markdown(f'<div class="q-text">🔎 {i + 1}.&nbsp; {task["q"]}</div>',
                            unsafe_allow_html=True)

                # Atsakymo laukas
                ans = st.text_input(
                    "Atsakymas", key=f"log_{i}",
                    label_visibility="collapsed",
                    placeholder="Įrašyk atsakymą..."
                )

                if show_hints:
                    st.markdown(
                        f'<p style="color:#6366f1; font-size:0.9rem; margin-top:5px;">💡 Teisingas atsakymas: <b>{task["a"]}</b></p>',
                        unsafe_allow_html=True)

                if ans:
                    # Lyginame supaprastintus variantus be LT raidžių
                    ok = (simplify(ans) == simplify(task['a']))
                    show_feedback(ok)
                    if ok: score += 1

        if st.session_state.logic_drill:
            sidebar_score(score, len(st.session_state.logic_drill), "🧩")
            if score == len(st.session_state.logic_drill) and score > 0:
                st.balloons()


# ═══════════════════════════════════════════════════════════════
#  🧮  MATEMATIKA
# ═══════════════════════════════════════════════════════════════
elif mode == "🧮 Matematika":
    st.markdown("# 🧮 Skaičių laboratorija")

    if not numbers_db:
        st.warning("numbers.json tuščias!")
    else:
        if 'math_drill' not in st.session_state:
            st.session_state.math_drill = []

        c1, c2 = st.columns([1, 2])
        kiek = c1.selectbox("Užduočių skaičius", [8, 12, 16, 24])
        if c2.button("🎲 Generuoti veiksmus", type="primary"):
            st.session_state.math_drill = random.sample(numbers_db, min(kiek, len(numbers_db)))

        st.markdown("")
        score = 0
        if st.session_state.math_drill:
            cols = st.columns(3)
            for i, t in enumerate(st.session_state.math_drill):
                with cols[i % 3]:
                    with st.container(border=True):
                        st.markdown(f'<div class="math-q">{t["q"]}</div>',
                                    unsafe_allow_html=True)
                        ans = st.text_input(
                            "=", key=f"m_{i}",
                            label_visibility="collapsed",
                            placeholder="?", max_chars=10
                        ).strip()
                        if ans:
                            ok = check_answer(ans, str(t['a']))
                            show_feedback(ok)
                            if ok: score += 1

            sidebar_score(score, len(st.session_state.math_drill), "🧮")
            if score == len(st.session_state.math_drill) and score > 0:
                st.balloons()


# ═══════════════════════════════════════════════════════════════
#  📖  PAMOKOS
# ═══════════════════════════════════════════════════════════════
elif mode == "📖 Pamokos":
    if not data:
        st.error("tasks.json nerastas arba tuščias!")
        st.stop()

    sel_week = st.sidebar.selectbox("📦 Rinkinys:", list(data.keys()))
    sel_day  = st.sidebar.selectbox("📅 Diena:",    list(data[sel_week].keys()))

    st.markdown(f"# 🌟 {sel_week} — {sel_day}")
    score, total = 0, 0

    for s_idx, sec in enumerate(data[sel_week][sel_day]):
        with st.container(border=True):
            st.markdown(f"### {sec.get('symbol','📝')}&nbsp; {sec['subject']}")

            prompts  = sec.get("prompts", [])
            sec_type = sec["type"]

            # ── VERTIMAS ─────────────────────────────────────
            if sec_type == "translation":
                cols = st.columns(len(prompts))
                for i in range(len(prompts)):
                    total += 1
                    key = f"tr_{sel_week}_{sel_day}_{s_idx}_{i}"
                    with cols[i]:
                        st.markdown(
                            f'<div class="lt-card">🇱🇹 {sec["lt_words"][i]}</div>',
                            unsafe_allow_html=True)
                        ans = st.text_input(
                            "Angliškai", key=key,
                            label_visibility="collapsed",
                            placeholder="English...", max_chars=30
                        ).strip()
                        correct = sec["en_answers"][i]
                        if ans:
                            ok = check_answer(ans, correct)
                            show_feedback(ok)
                            if ok: score += 1

            # ── SEKA ─────────────────────────────────────────
            elif sec_type == "sequence":
                for i, p in enumerate(prompts):
                    total += 1
                    key = f"sq_{sel_week}_{sel_day}_{s_idx}_{i}"
                    st.markdown(f'<div class="q-text">📈 {p}</div>',
                                unsafe_allow_html=True)
                    sq_cols = st.columns(4)
                    u_vals = []
                    for j in range(4):
                        with sq_cols[j]:
                            v = st.text_input(
                                f"#{j+1}", key=f"{key}_{j}",
                                label_visibility="collapsed",
                                placeholder=f"#{j+1}", max_chars=8
                            ).strip()
                            u_vals.append(v)
                    if all(v != "" for v in u_vals):
                        ok = [v.lower() for v in u_vals] == \
                             [c.lower() for c in sec["answers"][i]]
                        show_feedback(ok)
                        if ok: score += 1

            # ── LAIKRODIS ────────────────────────────────────
            elif sec_type == "clock":
                clock_cols = st.columns(len(sec["times"]))
                for i in range(len(prompts)):
                    total += 1
                    key = f"cl_{sel_week}_{sel_day}_{s_idx}_{i}"
                    with clock_cols[i]:
                        draw_clock(sec["times"][i])
                        ans = st.text_input(
                            "Laikas", key=key,
                            label_visibility="collapsed",
                            placeholder="HH:MM", max_chars=5
                        ).strip()
                        correct = sec["times"][i]
                        if ans:
                            ok = (ans == correct)
                            show_feedback(ok)
                            if ok: score += 1

            # ── LAISVAS TEKSTAS (area) ───────────────────────
            elif sec_type == "area":
                for i, p in enumerate(prompts):
                    total += 1
                    key = f"ar_{sel_week}_{sel_day}_{s_idx}_{i}"
                    st.markdown(f'<div class="q-text">✏️ {p}</div>',
                                unsafe_allow_html=True)
                    ans = st.text_area(
                        "Tekstas", key=key,
                        label_visibility="collapsed",
                        placeholder="Rašyk čia...", height=110
                    )
                    if len(ans.strip()) > 2:
                        show_feedback(True, free=True)
                        score += 1
                    elif ans.strip():
                        st.markdown(
                            '<span class="fb-warn">✎ Rašyk daugiau!</span>',
                            unsafe_allow_html=True)

            # ── TEKSTAS (text) ───────────────────────────────
            else:
                checkable = sec.get("check", False)

                # Daug checkable → 3 stulpeliai (matematika)
                if len(prompts) > 3 and checkable:
                    tx_cols = st.columns(3)
                    for i, p in enumerate(prompts):
                        total += 1
                        key = f"tx_{sel_week}_{sel_day}_{s_idx}_{i}"
                        with tx_cols[i % 3]:
                            with st.container(border=True):
                                st.markdown(
                                    f'<div class="math-q">{p}</div>',
                                    unsafe_allow_html=True)
                                ans = st.text_input(
                                    "=", key=key,
                                    label_visibility="collapsed",
                                    placeholder="?", max_chars=15
                                ).strip()
                                correct = sec["answers"][i] \
                                    if i < len(sec["answers"]) else ""
                                if ans:
                                    ok = check_answer(ans, correct)
                                    show_feedback(ok)
                                    if ok: score += 1
                else:
                    for i, p in enumerate(prompts):
                        total += 1
                        key = f"tx_{sel_week}_{sel_day}_{s_idx}_{i}"
                        st.markdown(f'<div class="q-text">👉 {p}</div>',
                                    unsafe_allow_html=True)
                        ans = st.text_input(
                            "Atsakymas", key=key,
                            label_visibility="collapsed",
                            placeholder="Tavo atsakymas...", max_chars=80
                        ).strip()

                        if checkable:
                            correct = sec["answers"][i] \
                                if i < len(sec["answers"]) else ""
                            if ans:
                                ok = check_answer(ans, correct)
                                show_feedback(ok)
                                if ok: score += 1
                        else:
                            if len(ans) > 2:
                                show_feedback(True, free=True)
                                score += 1
                            elif ans:
                                st.markdown(
                                    '<span class="fb-warn">✎ Rašyk daugiau!</span>',
                                    unsafe_allow_html=True)

    # ── Pažanga ──────────────────────────────────────────────
    sidebar_score(score, total, "📖")
    st.markdown("---")
    if st.button("💾 Išsaugoti rezultatą 🏆", use_container_width=True, type="primary"):
        save_detailed_log(sel_week, sel_day, "DIENOS PLANAS", f"{score}/{total}", "-")
        pct = int(score / total * 100) if total else 0
        st.success(f"✅ Išsaugota! {score}/{total} — {pct}%")
        if score == total and total > 0:
            st.balloons()


# ═══════════════════════════════════════════════════════════════
#  👨‍🏫  TĖČIUI
# ═══════════════════════════════════════════════════════════════
else:
    st.markdown("# 👨‍🏫 Tėčio žurnalas")
    if os.path.exists("detalus_atsakymai.csv"):
        df = pd.read_csv("detalus_atsakymai.csv")
        st.dataframe(df.iloc[::-1], use_container_width=True, hide_index=True)
        st.markdown("")
        c1, c2 = st.columns([1, 3])
        with c1:
            if st.button("🗑️ Išvalyti istoriją", type="secondary"):
                os.remove("detalus_atsakymai.csv")
                st.rerun()
        c2.metric("Iš viso sesijų", len(df))
    else:
        st.info("📭 Istorija tuščia — Jorė dar nesprendė užduočių!")