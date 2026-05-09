import json
import math
import os
import random
import re
import unicodedata
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components


APP_DIR = Path(__file__).parent
LOG_FILE = APP_DIR / "detalus_atsakymai.csv"
SETTINGS_FILE = APP_DIR / "app_settings.json"

st.set_page_config(page_title="Kasdienės užduotys", page_icon="⭐", layout="wide")


st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:wght@400;700&family=Nunito:wght@600;700;800;900&display=swap');

:root {
  --ink: #172033;
  --muted: #5f6b7a;
  --paper: #f7f8fb;
  --panel: #ffffff;
  --line: #d9dee8;
  --accent: #2563eb;
  --accent-soft: #eaf1ff;
  --success: #0f8f63;
  --warning: #b45309;
  --danger: #dc2626;
}

html, body, [data-testid="stAppViewContainer"] {
  background: var(--paper) !important;
  color: var(--ink) !important;
  font-family: "Atkinson Hyperlegible", sans-serif !important;
}

[data-testid="stSidebar"] {
  background: #111827 !important;
  border-right: 0 !important;
}

[data-testid="stSidebar"] * {
  color: #f8fafc !important;
}

h1, h2, h3 {
  color: var(--ink) !important;
  font-family: "Nunito", sans-serif !important;
  letter-spacing: 0 !important;
}

h1 {
  font-size: clamp(2rem, 3.6vw, 3.5rem) !important;
  font-weight: 900 !important;
  line-height: 1.04 !important;
}

.hero {
  padding: 1rem 0 1.4rem;
}

.hero p {
  color: var(--muted);
  font-size: 1.08rem;
  max-width: 48rem;
}

.learning-card {
  background: var(--panel);
  border: 2px solid var(--line);
  border-radius: 8px;
  padding: 1.1rem;
  box-shadow: 0 10px 22px rgba(16, 24, 40, .06);
  min-height: 100%;
}

.task-title {
  align-items: center;
  display: flex;
  gap: .65rem;
  font-family: "Nunito", sans-serif;
  font-size: 1.18rem;
  font-weight: 900;
  margin-bottom: .9rem;
}

.pill {
  background: var(--accent-soft);
  border: 1px solid #c9dcff;
  border-radius: 999px;
  color: #1d4ed8;
  display: inline-block;
  font-size: .9rem;
  font-weight: 800;
  padding: .25rem .65rem;
}

.question {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  color: #243042;
  font-size: 1.2rem;
  font-weight: 800;
  margin: .3rem 0 .7rem;
  padding: .9rem;
}

.word-card {
  background: var(--accent-soft);
  border: 2px solid #c9dcff;
  border-radius: 8px;
  color: #1e3a8a;
  font-family: "Nunito", sans-serif;
  font-size: 1.6rem;
  font-weight: 900;
  padding: 1rem;
  text-align: center;
}

.success-note, .try-note, .free-note {
  border-radius: 8px;
  display: inline-block;
  font-weight: 900;
  margin-top: .2rem;
  padding: .35rem .7rem;
}

.success-note { background: #dcfce7; color: #166534; }
.try-note { background: #fee2e2; color: #991b1b; }
.free-note { background: #fef3c7; color: #92400e; }

.metric-card {
  background: var(--panel);
  border: 2px solid var(--line);
  border-radius: 8px;
  padding: 1rem;
}

.metric-card strong {
  display: block;
  font-family: "Nunito", sans-serif;
  font-size: 2rem;
  line-height: 1.1;
}

[data-testid="stMetric"] {
  background: var(--panel);
  border: 2px solid var(--line);
  border-radius: 8px;
  padding: 1rem;
}

[data-testid="stMetric"] * {
  color: var(--ink) !important;
}

.stButton > button {
  border-radius: 8px !important;
  border: 0 !important;
  background: var(--accent) !important;
  color: #ffffff !important;
  font-family: "Nunito", sans-serif !important;
  font-weight: 900 !important;
  min-height: 3rem;
}

.stTextInput input, .stTextArea textarea {
  background: #ffffff !important;
  border-radius: 8px !important;
  border: 2px solid #d0d5dd !important;
  color: var(--ink) !important;
  -webkit-text-fill-color: var(--ink) !important;
  font-size: 1.05rem !important;
}

.stTextInput input::placeholder, .stTextArea textarea::placeholder {
  color: #8a94a6 !important;
  -webkit-text-fill-color: #8a94a6 !important;
}

.stProgress > div > div > div > div {
  background-color: var(--accent) !important;
}

div[data-testid="stHorizontalBlock"] {
  gap: 1rem;
}

button[data-baseweb="tab"] {
  color: var(--muted) !important;
  font-weight: 800 !important;
}

button[data-baseweb="tab"] p {
  color: var(--muted) !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
  color: var(--accent) !important;
}

button[data-baseweb="tab"][aria-selected="true"] p {
  color: var(--accent) !important;
}

[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
  background: #ffffff !important;
  border-color: #cbd5e1 !important;
  color: var(--ink) !important;
}

[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] label,
[data-testid="stWidgetLabel"] {
  color: var(--ink) !important;
  font-weight: 800 !important;
}

[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p,
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] label,
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] {
  color: #e5e7eb !important;
}

[data-testid="stAlert"] {
  border-radius: 8px !important;
  border: 1px solid #bbf7d0 !important;
}

[data-testid="stAlert"] * {
  color: #14532d !important;
  font-weight: 800 !important;
}

[data-testid="stDataFrame"] {
  border: 1px solid var(--line);
  border-radius: 8px;
  overflow: hidden;
}
</style>
""",
    unsafe_allow_html=True,
)


def mojibake_score(text: str) -> int:
    markers = ("Ä", "Å", "Ã", "â", "ā", "�", "ļ", "")
    return sum(text.count(marker) for marker in markers)


def repair_text(text: str) -> str:
    """Repair common UTF-8 text that was accidentally decoded as Windows codepages."""
    if not isinstance(text, str) or not text:
        return text

    best = text
    best_score = mojibake_score(text)

    for encoding in ("cp1257", "cp1252", "latin1"):
        candidate = text
        for _ in range(2):
            try:
                candidate = candidate.encode(encoding).decode("utf-8")
            except UnicodeError:
                break
            score = mojibake_score(candidate)
            if score < best_score:
                best = candidate
                best_score = score

    return best


def repair_data(value):
    if isinstance(value, dict):
        return {repair_text(k): repair_data(v) for k, v in value.items()}
    if isinstance(value, list):
        return [repair_data(item) for item in value]
    if isinstance(value, str):
        return repair_text(value)
    return value


@st.cache_data
def load_json(filename: str, file_mtime: float = 0):
    path = APP_DIR / filename
    if not path.exists():
        return {} if filename == "tasks.json" else []
    with path.open("r", encoding="utf-8") as f:
        return repair_data(json.load(f))


def load_json_file(filename: str):
    path = APP_DIR / filename
    file_mtime = path.stat().st_mtime if path.exists() else 0
    return load_json(filename, file_mtime)


def load_settings():
    if not SETTINGS_FILE.exists():
        return {"completed_rinkiniai": []}
    try:
        with SETTINGS_FILE.open("r", encoding="utf-8") as f:
            settings = json.load(f)
    except (json.JSONDecodeError, OSError):
        return {"completed_rinkiniai": []}

    completed = settings.get("completed_rinkiniai", [])
    if not isinstance(completed, list):
        completed = []
    return {"completed_rinkiniai": completed}


def save_settings(settings):
    safe_settings = {
        "completed_rinkiniai": sorted(set(settings.get("completed_rinkiniai", [])))
    }
    with SETTINGS_FILE.open("w", encoding="utf-8") as f:
        json.dump(safe_settings, f, ensure_ascii=False, indent=2)


def normalize_answer(value: str) -> str:
    value = str(value).strip().lower().replace(",", ".")
    value = unicodedata.normalize("NFKD", value)
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    value = re.sub(r"[^\w\s.:-]", "", value)
    return re.sub(r"\s+", " ", value).strip()


def check_answer(answer: str, correct: str) -> bool:
    return normalize_answer(answer) == normalize_answer(correct)


def show_feedback(ok: bool, free: bool = False):
    if free:
        st.markdown('<span class="free-note">✓ Įskaityta</span>', unsafe_allow_html=True)
    elif ok:
        st.markdown('<span class="success-note">✓ Teisingai</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="try-note">Dar kartą</span>', unsafe_allow_html=True)


def show_correct_answer(correct, enabled: bool):
    if enabled and str(correct).strip():
        st.caption(f"Atsakymas: {correct}")


def progress_panel(score: int, total: int, label: str):
    pct = int(score / total * 100) if total else 0
    st.sidebar.markdown(f"### {label}")
    st.sidebar.progress(pct / 100 if total else 0)
    st.sidebar.markdown(f"**{score}/{total}** teisingai  \n**{pct}%**")
    if pct == 100 and total:
        st.sidebar.success("Puikus darbas!")
    elif pct >= 70:
        st.sidebar.info("Labai gerai. Liko truputis.")
    elif total:
        st.sidebar.warning("Ramu. Mokomės po vieną žingsnį.")


def draw_clock(time_str: str):
    try:
        h, m = map(int, str(time_str).split(":"))
        hour_angle = (h % 12) * 30 + m * 0.5
        min_angle = m * 6
        ticks = "".join(
            f'<line x1="{50 + 43 * math.cos(math.radians(a)):.1f}" '
            f'y1="{50 + 43 * math.sin(math.radians(a)):.1f}" '
            f'x2="{50 + 47 * math.cos(math.radians(a)):.1f}" '
            f'y2="{50 + 47 * math.sin(math.radians(a)):.1f}" '
            f'stroke="#8993a4" stroke-width="2" stroke-linecap="round"/>'
            for a in [i * 30 - 90 for i in range(12)]
        )
        nums = "".join(
            f'<text x="{50 + 36 * math.cos(math.radians(i * 30 - 90)):.1f}" '
            f'y="{54 + 36 * math.sin(math.radians(i * 30 - 90)):.1f}" '
            f'font-family="Nunito,sans-serif" font-size="9" font-weight="800" '
            f'text-anchor="middle" fill="#243042">{i}</text>'
            for i in range(1, 13)
        )
        html = f"""
<div style="text-align:center;padding:.2rem 0;">
<svg width="170" height="170" viewBox="0 0 100 100">
  <circle cx="50" cy="50" r="47" fill="#fffdf7" stroke="#243042" stroke-width="2.5"/>
  {ticks}{nums}
  <line x1="50" y1="50" x2="50" y2="27" stroke="#243042" stroke-width="4.5"
        stroke-linecap="round" transform="rotate({hour_angle} 50 50)"/>
  <line x1="50" y1="50" x2="50" y2="13" stroke="#38a3d1" stroke-width="3"
        stroke-linecap="round" transform="rotate({min_angle} 50 50)"/>
  <circle cx="50" cy="50" r="3.5" fill="#f8b84e"/>
</svg>
</div>"""
        components.html(html, height=180)
    except Exception:
        st.error("Laikrodžio formatas turi būti HH:MM")


def append_log(rows):
    if not rows:
        return
    session_id = datetime.now().strftime("%Y%m%d-%H%M%S")
    for row in rows:
        row.setdefault("Sesija", session_id)
    new_df = pd.DataFrame(rows)
    if LOG_FILE.exists():
        old_df = pd.read_csv(LOG_FILE)
        df = pd.concat([old_df, new_df], ignore_index=True)
    else:
        df = new_df
    df.to_csv(LOG_FILE, index=False, encoding="utf-8")


def log_row(mode, group, day, subject, question, answer, correct, result):
    return {
        "Laikas": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "Režimas": mode,
        "Rinkinys": group,
        "Diena": day,
        "Užduotis": subject,
        "Klausimas": question,
        "Vaiko atsakymas": answer,
        "Teisingas atsakymas": correct,
        "Rezultatas": result,
    }


def repair_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    fixed = df.copy()
    fixed.columns = [repair_text(str(col)) for col in fixed.columns]
    for col in fixed.columns:
        if fixed[col].dtype == object:
            fixed[col] = fixed[col].map(lambda value: repair_text(value) if isinstance(value, str) else value)
    return fixed


def first_available_series(df: pd.DataFrame, names, default=""):
    result = pd.Series([default] * len(df), index=df.index, dtype="object")
    for name in names:
        if name in df.columns:
            values = df[name]
            result = result.where(result.astype(str).str.strip().eq(default), result)
            result = result.mask(result.astype(str).str.strip().eq(default), values)
            result = result.fillna(default)
    return result


def build_progress_summary(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame()

    work = df.copy()
    result = first_available_series(work, ["Rezultatas"], "")
    answer = first_available_series(work, ["Vaiko atsakymas", "Jorės atsakymas", "Jores Atsakymas", "Atliktas Atsakymas"], "")
    mode = first_available_series(work, ["Režimas"], "Pamokos")
    day = first_available_series(work, ["Diena"], "")
    time = first_available_series(work, ["Laikas", "Data", "Data ir Laikas"], "")

    rows = []
    for idx in work.index:
        raw_result = str(result.loc[idx]).strip()
        raw_answer = str(answer.loc[idx]).strip()
        score_text = raw_answer if re.fullmatch(r"\d+\s*/\s*\d+", raw_answer) else raw_result
        match = re.fullmatch(r"(\d+)\s*/\s*(\d+)", score_text)

        if match:
            correct, total = int(match.group(1)), int(match.group(2))
            pct = round(correct / total * 100, 1) if total else 0
        elif raw_result.lower() in {"true", "1", "teisingai"}:
            correct, total, pct = 1, 1, 100
        elif raw_result.lower() in {"false", "0", "neteisingai"}:
            correct, total, pct = 0, 1, 0
        else:
            continue

        rows.append(
            {
                "Laikas": time.loc[idx],
                "Režimas": mode.loc[idx] if str(mode.loc[idx]).strip() else "Pamokos",
                "Diena": day.loc[idx],
                "Teisingai": correct,
                "Iš viso": total,
                "Procentai": pct,
            }
        )

    return pd.DataFrame(rows)


def detailed_log_rows(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty or "Klausimas" not in df.columns:
        return pd.DataFrame()

    detailed = df[df["Klausimas"].fillna("").astype(str).str.strip().ne("")].copy()
    if detailed.empty:
        return detailed

    if "Sesija" not in detailed.columns:
        detailed["Sesija"] = ""

    fallback_session = (
        first_available_series(detailed, ["Laikas"], "")
        + " | "
        + first_available_series(detailed, ["Režimas"], "Pamokos")
        + " | "
        + first_available_series(detailed, ["Rinkinys"], "")
        + " | "
        + first_available_series(detailed, ["Diena"], "")
    )
    detailed["Sesija"] = detailed["Sesija"].fillna("").astype(str)
    detailed["Sesija"] = detailed["Sesija"].where(detailed["Sesija"].str.strip().ne(""), fallback_session)
    detailed["Rezultatas"] = detailed["Rezultatas"].astype(str).str.lower().isin(["true", "1", "teisingai"])
    return detailed


def build_session_summary(df: pd.DataFrame) -> pd.DataFrame:
    detailed = detailed_log_rows(df)
    if detailed.empty:
        return pd.DataFrame()

    grouped = (
        detailed.groupby("Sesija", dropna=False)
        .agg(
            Laikas=("Laikas", "first"),
            Režimas=("Režimas", "first"),
            Rinkinys=("Rinkinys", "first"),
            Diena=("Diena", "first"),
            Teisingai=("Rezultatas", "sum"),
            Iš_viso=("Rezultatas", "size"),
        )
        .reset_index()
    )
    grouped["Procentai"] = (grouped["Teisingai"] / grouped["Iš_viso"] * 100).round(0).astype(int)
    return grouped.sort_values("Laikas", ascending=False)


def answer_detail_table(session_rows: pd.DataFrame) -> pd.DataFrame:
    if session_rows.empty:
        return pd.DataFrame()

    return pd.DataFrame(
        {
            "Užduotis": first_available_series(session_rows, ["Užduotis", "Uţduotis", "Uzduotis"], ""),
            "Klausimas": first_available_series(session_rows, ["Klausimas"], ""),
            "Vaiko atsakymas": first_available_series(
                session_rows,
                ["Vaiko atsakymas", "Jorės atsakymas", "Jorës atsakymas", "Jores Atsakymas"],
                "",
            ),
            "Teisingas atsakymas": first_available_series(
                session_rows,
                ["Teisingas atsakymas", "Teisingas Atsakymas"],
                "",
            ),
            "Rezultatas": session_rows["Rezultatas"].map(lambda ok: "Teisingai" if ok else "Klaida"),
        }
    )


def hero(title: str, subtitle: str):
    st.markdown(f'<div class="hero"><h1>{title}</h1><p>{subtitle}</p></div>', unsafe_allow_html=True)


def render_metric(label: str, value: str, note: str = ""):
    st.markdown(
        f'<div class="metric-card"><span>{label}</span><strong>{value}</strong><small>{note}</small></div>',
        unsafe_allow_html=True,
    )


def section_icon(subject: str, fallback: str = "📌") -> str:
    subject_key = normalize_answer(subject)
    if "anglu" in subject_key or "vertimas" in subject_key:
        return "🔤"
    if "matematika" in subject_key or "skaici" in subject_key or "sekos" in subject_key:
        return "🔢"
    if "laikas" in subject_key or "laikro" in subject_key:
        return "🕒"
    if "logika" in subject_key or "misle" in subject_key:
        return "🧩"
    if "tekstas" in subject_key or "sakin" in subject_key:
        return "✏️"
    if fallback in {"🇬🇧", "🇱🇹"}:
        return "🔤"
    return fallback


def render_daily_lessons(data, child_name: str, show_answers: bool, active_weeks):
    if not data:
        st.error("Nerastas arba tuščias tasks.json failas.")
        return

    if not active_weeks:
        hero(f"{child_name}: pamokos", "Visi rinkiniai pažymėti kaip užbaigti.")
        st.info("Atidarykite „Tėvų nustatymai“ ir grąžinkite bent vieną rinkinį, kad jis vėl būtų rodomas vaikui.")
        return

    week = st.sidebar.selectbox("Rinkinys", active_weeks)
    day = st.sidebar.selectbox("Diena", list(data[week].keys()))
    sections = data[week][day]

    hero(f"{child_name}: {week} · {day}", "Dienos užduotys su aiškiu grįžtamuoju ryšiu ir išsaugomu rezultatu.")

    score = 0
    total = 0
    rows_to_log = []

    for s_idx, sec in enumerate(sections):
        subject = sec.get("subject", "Užduotis")
        symbol = section_icon(subject, sec.get("symbol", "📌"))
        prompts = sec.get("prompts", [])
        sec_type = sec.get("type", "text")

        with st.container(border=True):
            st.markdown(f'<div class="task-title"><span>{symbol}</span><span>{subject}</span></div>', unsafe_allow_html=True)

            if sec_type == "translation":
                cols = st.columns(min(3, max(1, len(sec.get("lt_words", [])))))
                for i, lt_word in enumerate(sec.get("lt_words", [])):
                    total += 1
                    key = f"tr_{week}_{day}_{s_idx}_{i}"
                    correct = sec.get("en_answers", [""])[i]
                    with cols[i % len(cols)]:
                        st.markdown(f'<div class="word-card">{lt_word}</div>', unsafe_allow_html=True)
                        answer = st.text_input("Angliškai", key=key, placeholder="Įrašyk žodį")
                        show_correct_answer(correct, show_answers)
                        if answer:
                            ok = check_answer(answer, correct)
                            show_feedback(ok)
                            score += int(ok)
                            rows_to_log.append(log_row("Pamokos", week, day, subject, lt_word, answer, correct, ok))

            elif sec_type == "sequence":
                for i, prompt in enumerate(prompts):
                    total += 1
                    key = f"sq_{week}_{day}_{s_idx}_{i}"
                    st.markdown(f'<div class="question">{prompt}</div>', unsafe_allow_html=True)
                    expected = sec.get("answers", [[]])[i]
                    show_correct_answer(" | ".join(expected), show_answers)
                    cols = st.columns(len(expected))
                    answers = []
                    for j, _ in enumerate(expected):
                        with cols[j]:
                            answers.append(st.text_input(f"#{j + 1}", key=f"{key}_{j}", label_visibility="collapsed"))
                    if all(answer.strip() for answer in answers):
                        ok = [normalize_answer(a) for a in answers] == [normalize_answer(a) for a in expected]
                        show_feedback(ok)
                        score += int(ok)
                        rows_to_log.append(log_row("Pamokos", week, day, subject, prompt, " | ".join(answers), " | ".join(expected), ok))

            elif sec_type == "clock":
                cols = st.columns(min(3, max(1, len(sec.get("times", [])))))
                for i, prompt in enumerate(prompts):
                    total += 1
                    correct = sec.get("times", [""])[i]
                    with cols[i % len(cols)]:
                        st.markdown(f'<div class="question">{prompt}</div>', unsafe_allow_html=True)
                        draw_clock(correct)
                        answer = st.text_input("Koks laikas?", key=f"cl_{week}_{day}_{s_idx}_{i}", placeholder="HH:MM", max_chars=5)
                        show_correct_answer(correct, show_answers)
                        if answer:
                            ok = check_answer(answer, correct)
                            show_feedback(ok)
                            score += int(ok)
                            rows_to_log.append(log_row("Pamokos", week, day, subject, prompt, answer, correct, ok))

            elif sec_type == "area":
                for i, prompt in enumerate(prompts):
                    total += 1
                    st.markdown(f'<div class="question">{prompt}</div>', unsafe_allow_html=True)
                    answer = st.text_area("Tavo tekstas", key=f"ar_{week}_{day}_{s_idx}_{i}", height=120)
                    if answer.strip():
                        ok = len(answer.strip()) >= 3
                        show_feedback(ok, free=ok)
                        score += int(ok)
                        rows_to_log.append(log_row("Pamokos", week, day, subject, prompt, answer, "Laisvas atsakymas", ok))

            else:
                checkable = bool(sec.get("check", False))
                cols = st.columns(3) if checkable and len(prompts) > 3 else None
                for i, prompt in enumerate(prompts):
                    total += 1
                    if cols:
                        parent = cols[i % 3]
                    else:
                        parent = st.container()
                    with parent:
                        st.markdown(f'<div class="question">{prompt}</div>', unsafe_allow_html=True)
                        answer = st.text_input("Atsakymas", key=f"tx_{week}_{day}_{s_idx}_{i}", placeholder="Tavo atsakymas")
                        correct = sec.get("answers", [""])[i] if i < len(sec.get("answers", [])) else "Laisvas atsakymas"
                        if checkable:
                            show_correct_answer(correct, show_answers)
                        if answer:
                            ok = check_answer(answer, correct) if checkable else len(answer.strip()) >= 3
                            show_feedback(ok, free=not checkable and ok)
                            score += int(ok)
                            rows_to_log.append(log_row("Pamokos", week, day, subject, prompt, answer, correct, ok))

    progress_panel(score, total, "Dienos pažanga")

    st.divider()
    col1, col2 = st.columns([1, 2])
    with col1:
        if st.button("Išsaugoti dienos rezultatą", type="primary", use_container_width=True):
            append_log(rows_to_log or [log_row("Pamokos", week, day, "Dienos rezultatas", "-", f"{score}/{total}", "-", score == total)])
            st.success(f"Išsaugota: {score}/{total}")
            if total and score == total:
                st.balloons()
    with col2:
        render_metric("Šios dienos rezultatas", f"{score}/{total}", "Rezultatas skaičiuojamas pagal įrašytus atsakymus.")


def render_drill(title, subtitle, source, mode_name, count_options, sample_key, show_answers: bool):
    hero(title, subtitle)
    if not source:
        st.warning("Užduočių bankas tuščias.")
        return

    if sample_key not in st.session_state:
        st.session_state[sample_key] = []

    left, right = st.columns([1, 2])
    with left:
        count = st.selectbox("Kiek užduočių?", count_options)
    with right:
        if st.button("Naujas rinkinys", type="primary", use_container_width=True):
            st.session_state[sample_key] = random.sample(source, min(count, len(source)))

    score = 0
    total = len(st.session_state[sample_key])
    rows_to_log = []

    if st.session_state[sample_key]:
        cols = st.columns(2 if mode_name == "Logika" else 3)
        for i, item in enumerate(st.session_state[sample_key]):
            with cols[i % len(cols)]:
                with st.container(border=True):
                    st.markdown(f'<div class="question">{item["q"]}</div>', unsafe_allow_html=True)
                    answer = st.text_input("Atsakymas", key=f"{sample_key}_{i}", placeholder="Įrašyk atsakymą")
                    show_correct_answer(item["a"], show_answers)
                    if answer:
                        ok = check_answer(answer, item["a"])
                        show_feedback(ok)
                        score += int(ok)
                        rows_to_log.append(log_row(mode_name, "-", "-", item["q"], item["q"], answer, item["a"], ok))

        progress_panel(score, total, f"{mode_name} pažanga")
        if st.button("Išsaugoti pratimą", use_container_width=True):
            append_log(rows_to_log)
            st.success(f"Išsaugota: {score}/{total}")
            if total and score == total:
                st.balloons()
    else:
        st.info("Paspausk „Naujas rinkinys“, kad pradėtum.")


def collect_daily_weak_spots(data):
    items = []
    for week, days in data.items():
        for day, sections in days.items():
            for sec in sections:
                subject = sec.get("subject", "Užduotis")
                sec_type = sec.get("type", "text")
                prompts = sec.get("prompts", [])
                if sec_type == "translation":
                    for lt, en in zip(sec.get("lt_words", []), sec.get("en_answers", [])):
                        items.append({"q": f"{lt} angliškai?", "a": en, "source": f"{week} / {day} / {subject}"})
                elif sec.get("check", False):
                    for prompt, answer in zip(prompts, sec.get("answers", [])):
                        items.append({"q": prompt, "a": answer, "source": f"{week} / {day} / {subject}"})
    return items


def render_adaptive(data, numbers, logic, show_answers: bool):
    hero("🎯 Greita praktika", "Mišrus trumpas pratimas iš anglų kalbos, matematikos ir logikos.")
    bank = collect_daily_weak_spots(data)
    bank.extend({"q": item["q"], "a": item["a"], "source": "Matematika"} for item in numbers)
    bank.extend({"q": item["q"], "a": item["a"], "source": "Logika"} for item in logic)

    if "adaptive_drill" not in st.session_state:
        st.session_state.adaptive_drill = []

    count = st.sidebar.slider("Praktikos ilgis", 5, 20, 10)
    if st.button("Sukurti greitą praktiką", type="primary"):
        st.session_state.adaptive_drill = random.sample(bank, min(count, len(bank)))

    score = 0
    rows = []
    for i, item in enumerate(st.session_state.adaptive_drill):
        with st.container(border=True):
            st.markdown(f'<span class="pill">{item.get("source", "Praktika")}</span>', unsafe_allow_html=True)
            st.markdown(f'<div class="question">{item["q"]}</div>', unsafe_allow_html=True)
            answer = st.text_input("Atsakymas", key=f"adaptive_{i}", placeholder="Tavo atsakymas")
            show_correct_answer(item["a"], show_answers)
            if answer:
                ok = check_answer(answer, item["a"])
                show_feedback(ok)
                score += int(ok)
                rows.append(log_row("Greita praktika", item.get("source", "-"), "-", item["q"], item["q"], answer, item["a"], ok))

    total = len(st.session_state.adaptive_drill)
    progress_panel(score, total, "Praktikos pažanga")
    if total and st.button("Išsaugoti greitą praktiką", use_container_width=True):
        append_log(rows)
        st.success(f"Išsaugota: {score}/{total}")


def render_parent_settings(data, child_name: str, settings):
    hero("Tėvų nustatymai", f"{child_name} pažanga, rinkiniai ir mokymosi turinys vienoje vietoje.")

    if LOG_FILE.exists():
        df = repair_dataframe(pd.read_csv(LOG_FILE))
    else:
        df = pd.DataFrame()

    total_tasks = sum(len(sections) for days in data.values() for sections in days.values()) if data else 0
    vocab = []
    for week, days in data.items():
        for day, sections in days.items():
            for sec in sections:
                if sec.get("type") == "translation":
                    for lt, en in zip(sec.get("lt_words", []), sec.get("en_answers", [])):
                        vocab.append({"Lietuviškai": lt, "Angliškai": en, "Šaltinis": f"{week} / {day}"})

    c1, c2, c3 = st.columns(3)
    with c1:
        render_metric("Užduočių blokai", str(total_tasks), "Visuose rinkiniuose")
    with c2:
        render_metric("Žodyno žodžiai", str(len(vocab)), "Anglų kalbos kortelės")
    with c3:
        render_metric("Išsaugoti įrašai", str(len(df)), "Žurnale")

    tab1, tab2, tab3, tab4 = st.tabs(["Pažanga", "Rinkiniai", "Žodynas", "Duomenys"])

    with tab1:
        if df.empty:
            st.info("Istorija dar tuščia. Išsaugok pirmą pratimą, ir čia atsiras pažangos vaizdas.")
        else:
            session_df = build_session_summary(df)
            detailed_df = detailed_log_rows(df)

            if session_df.empty:
                st.info("Naujų detalių įrašų dar nėra. Išsaugok pamoką ar pratimą, tada čia matysi visus atsakymus.")
            else:
                avg_score = session_df["Procentai"].mean()
                total_answered = int(session_df["Iš_viso"].sum())
                total_correct = int(session_df["Teisingai"].sum())
                perfect_count = int((session_df["Procentai"] == 100).sum())

                m1, m2, m3 = st.columns(3)
                m1.metric("Vidurkis", f"{avg_score:.0f}%")
                m2.metric("Teisingai", f"{total_correct}/{total_answered}")
                m3.metric("Puikios sesijos", str(perfect_count))
                st.progress(min(max(avg_score, 0), 100) / 100)

                st.subheader("Sesijos")
                session_labels = {
                    (
                        f"{row['Laikas']} · {row['Režimas']} · {row['Diena']} · "
                        f"{int(row['Teisingai'])}/{int(row['Iš_viso'])} ({int(row['Procentai'])}%)"
                    ): row["Sesija"]
                    for _, row in session_df.iterrows()
                }
                selected_label = st.selectbox("Pasirink sesiją", list(session_labels.keys()))
                selected_session = session_labels[selected_label]
                session_rows = detailed_df[detailed_df["Sesija"] == selected_session].copy()

                wrong_rows = session_rows[~session_rows["Rezultatas"]]
                if wrong_rows.empty:
                    st.success("Visi atsakymai teisingi.")
                else:
                    st.warning(f"Klaidų: {len(wrong_rows)}")

                st.dataframe(
                    answer_detail_table(session_rows),
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "Rezultatas": st.column_config.TextColumn("Rezultatas", width="small"),
                    },
                )

                with st.expander("Klaidų sąrašas"):
                    if wrong_rows.empty:
                        st.info("Šioje sesijoje klaidų nėra.")
                    else:
                        st.dataframe(
                            answer_detail_table(wrong_rows),
                            use_container_width=True,
                            hide_index=True,
                        )

                with st.expander("Visos sesijos"):
                    st.dataframe(
                        session_df[["Laikas", "Režimas", "Rinkinys", "Diena", "Teisingai", "Iš_viso", "Procentai"]],
                        use_container_width=True,
                        hide_index=True,
                    )

            with st.expander("Seni žurnalo įrašai"):
                old_rows = df[df.get("Klausimas", pd.Series([""] * len(df))).fillna("").astype(str).str.strip().eq("")]
                if old_rows.empty:
                    st.info("Senų santraukinių įrašų nėra.")
                else:
                    st.dataframe(old_rows.iloc[::-1], use_container_width=True, hide_index=True)

    with tab2:
        all_weeks = list(data.keys())
        completed = [week for week in settings.get("completed_rinkiniai", []) if week in all_weeks]
        active = [week for week in all_weeks if week not in completed]

        st.subheader("Rinkinių valdymas")
        st.caption("Pažymėti rinkiniai laikomi užbaigtais ir vaikui neberodomi pamokų pasirinkime.")

        c_active, c_done = st.columns(2)
        c_active.metric("Rodomi vaikui", len(active))
        c_done.metric("Užbaigti / paslėpti", len(completed))

        selected_completed = st.multiselect(
            "Užbaigti rinkiniai",
            all_weeks,
            default=completed,
            key="completed_rinkiniai_multiselect",
            help="Pasirinkti rinkiniai bus paslėpti iš vaiko pamokų sąrašo.",
        )

        b1, b2, b3 = st.columns(3)
        with b1:
            if st.button("Išsaugoti rinkinių būseną", type="primary", use_container_width=True):
                settings["completed_rinkiniai"] = selected_completed
                save_settings(settings)
                st.success("Rinkinių būsena išsaugota.")
                st.rerun()
        with b2:
            if st.button("Pažymėti visus užbaigtus", use_container_width=True):
                settings["completed_rinkiniai"] = all_weeks
                save_settings(settings)
                st.rerun()
        with b3:
            if st.button("Rodyti visus", use_container_width=True):
                settings["completed_rinkiniai"] = []
                save_settings(settings)
                st.rerun()

        st.markdown("#### Aktyvūs rinkiniai")
        if active:
            st.dataframe(pd.DataFrame({"Rinkinys": active}), use_container_width=True, hide_index=True)
        else:
            st.warning("Visi rinkiniai paslėpti. Vaikas pamokų režime nematys pasirinkimų.")

        st.markdown("#### Nauji rinkiniai")
        st.info("Programoje jau yra Rinkinys 1-8. Kai į tasks.json pridėsite Rinkinys 9, 10 ir t. t., jie automatiškai atsiras čia ir bus rodomi vaikui, kol nepažymėsite jų užbaigtais.")

    with tab3:
        if vocab:
            st.dataframe(pd.DataFrame(vocab), use_container_width=True, hide_index=True)
        else:
            st.info("Žodyno dar nėra.")

    with tab4:
        st.caption("Atsargiai: istorijos valymas ištrina vietinį CSV žurnalą.")
        if LOG_FILE.exists() and st.button("Išvalyti istoriją", type="secondary"):
            os.remove(LOG_FILE)
            st.rerun()


data = load_json_file("tasks.json")
numbers_db = load_json_file("numbers.json")
logic_db = load_json_file("logic.json")
reasoning_db = load_json_file("reasoning.json")
settings = load_settings()

st.sidebar.markdown("## ⭐ Kasdienės užduotys")

if "child_name" not in st.session_state:
    st.session_state.child_name = ""

child_name_input = st.sidebar.text_input(
    "Vaiko vardas",
    value=st.session_state.child_name,
    placeholder="Pvz., Jorė",
)
st.session_state.child_name = child_name_input.strip()

answer_code = st.sidebar.text_input(
    "Atsakymų kodas",
    type="password",
    placeholder="Tik tėvams",
)
show_answers = answer_code == "2000"
if show_answers:
    st.sidebar.success("Atsakymai rodomi")

st.sidebar.divider()

if not st.session_state.child_name:
    hero("Kas mokysis šiandien?", "Įveskite vaiko vardą kairėje, kad užduotys ir pažanga būtų suasmenintos.")
    st.info("Vardas naudojamas tik šiame kompiuteryje veikiančioje programoje.")
    st.stop()

child_name = st.session_state.child_name
completed_rinkiniai = set(settings.get("completed_rinkiniai", []))
active_weeks = [week for week in data.keys() if week not in completed_rinkiniai]

mode = st.sidebar.radio(
    "Pasirink režimą",
    ["Pamokos", "Greita praktika", "Matematika", "Samprotavimas", "Logika", "Tėvų nustatymai"],
)
st.sidebar.divider()

if mode == "Pamokos":
    render_daily_lessons(data, child_name, show_answers, active_weeks)
elif mode == "Greita praktika":
    render_adaptive(data, numbers_db, logic_db, show_answers)
elif mode == "Matematika":
    render_drill("🧮 Matematikos laboratorija", "Trumpi skaičiavimo pratimai su greitu patikrinimu.", numbers_db, "Matematika", [8, 12, 16, 24], "math_drill", show_answers)
elif mode == "Samprotavimas":
    render_drill("🧠 Matematinis samprotavimas", "1 klasės užduotys apie korteles, monetas, sekas, statinius ir kryptis.", reasoning_db, "Samprotavimas", [6, 8, 10, 12], "reasoning_drill", show_answers)
elif mode == "Logika":
    render_drill("🧩 Logikos kampelis", "Mįslės ir gudrūs klausimai, lavinantys samprotavimą.", logic_db, "Logika", [3, 5, 8, 12, 15], "logic_drill", show_answers)
else:
    render_parent_settings(data, child_name, settings)
