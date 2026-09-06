import json
import calendar
import math
import os
import random
import re
import unicodedata
from datetime import datetime
from decimal import Decimal, InvalidOperation
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

.answer-hint {
  align-items: flex-start;
  background: #fff7ed;
  border: 2px solid #fed7aa;
  border-radius: 8px;
  color: #7c2d12;
  display: flex;
  gap: .45rem;
  font-size: .98rem;
  font-weight: 900;
  line-height: 1.35;
  margin: .45rem 0 .75rem;
  padding: .55rem .7rem;
}

.answer-hint span {
  color: #7c2d12 !important;
  -webkit-text-fill-color: #7c2d12 !important;
}

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

.stTextInput,
.stTextArea,
[data-testid="stTextInput"],
[data-testid="stTextArea"] {
  opacity: 1 !important;
}

.stTextInput > div,
.stTextArea > div,
[data-testid="stTextInput"] > div,
[data-testid="stTextArea"] > div {
  opacity: 1 !important;
}

.stTextInput input,
.stTextArea textarea,
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea,
[data-baseweb="input"] input,
[data-baseweb="textarea"] textarea {
  background: #ffffff !important;
  border-radius: 8px !important;
  border: 2px solid #d0d5dd !important;
  color: var(--ink) !important;
  caret-color: #0f172a !important;
  -webkit-text-fill-color: var(--ink) !important;
  font-size: 1.05rem !important;
  opacity: 1 !important;
  text-shadow: none !important;
}

.stTextInput input:focus,
.stTextArea textarea:focus,
[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus,
[data-baseweb="input"] input:focus,
[data-baseweb="textarea"] textarea:focus {
  background: #ffffff !important;
  border-color: var(--accent) !important;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, .18) !important;
  color: var(--ink) !important;
  caret-color: #0f172a !important;
  -webkit-text-fill-color: var(--ink) !important;
}

.stTextInput input::placeholder,
.stTextArea textarea::placeholder,
[data-testid="stTextInput"] input::placeholder,
[data-testid="stTextArea"] textarea::placeholder {
  color: #8a94a6 !important;
  -webkit-text-fill-color: #8a94a6 !important;
  opacity: 1 !important;
}

[data-testid="stSidebar"] .stTextInput input,
[data-testid="stSidebar"] [data-testid="stTextInput"] input,
[data-testid="stSidebar"] [data-baseweb="input"] input {
  background: #ffffff !important;
  color: var(--ink) !important;
  caret-color: #0f172a !important;
  -webkit-text-fill-color: var(--ink) !important;
}

input::selection,
textarea::selection {
  background: rgba(37, 99, 235, .28) !important;
  color: #0f172a !important;
  -webkit-text-fill-color: #0f172a !important;
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

[data-testid="stSidebar"] [data-testid="stSelectbox"] div[data-baseweb="select"] *,
[data-testid="stSidebar"] [data-testid="stSelectbox"] div[data-baseweb="select"] input,
[data-testid="stSidebar"] input[aria-label^="Selected"] {
  color: var(--ink) !important;
  -webkit-text-fill-color: var(--ink) !important;
}

[data-baseweb="popover"] [role="option"],
[data-baseweb="popover"] [role="listbox"] * {
  color: var(--ink) !important;
  -webkit-text-fill-color: var(--ink) !important;
}

[data-baseweb="popover"] [role="listbox"],
[data-baseweb="popover"] [role="option"] {
  background: #ffffff !important;
}

[data-baseweb="popover"] [role="option"]:hover,
[data-baseweb="popover"] [aria-selected="true"] {
  background: #eaf1ff !important;
  color: var(--ink) !important;
  -webkit-text-fill-color: var(--ink) !important;
}

[data-baseweb="popover"] {
  color: var(--ink) !important;
}

[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] label,
[data-testid="stWidgetLabel"] {
  color: var(--ink) !important;
  font-weight: 800 !important;
}

[data-testid="stRadio"] label,
[data-testid="stRadio"] label *,
[data-testid="stRadio"] p,
[data-testid="stRadio"] span {
  color: var(--ink) !important;
  -webkit-text-fill-color: var(--ink) !important;
  font-weight: 800 !important;
  opacity: 1 !important;
}

[data-testid="stRadio"] div[role="radiogroup"] {
  gap: 1.25rem !important;
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

.sidebar-progress-card {
  background: #ffffff;
  border: 2px solid #cbd5e1;
  border-radius: 8px;
  margin: .6rem 0 1rem;
  padding: .8rem;
  position: sticky;
  top: .75rem;
  z-index: 10;
}

.sidebar-progress-card h3 {
  color: #172033 !important;
  font-size: 1rem !important;
  margin: 0 0 .55rem !important;
}

.sidebar-progress-bar {
  background: #e5e7eb;
  border-radius: 999px;
  height: .75rem;
  margin-bottom: .6rem;
  overflow: hidden;
}

.sidebar-progress-fill {
  background: var(--accent);
  border-radius: inherit;
  height: 100%;
}

.sidebar-progress-card strong,
.sidebar-progress-card span {
  color: #172033 !important;
}

.sidebar-progress-card p {
  color: #5f6b7a !important;
  font-weight: 800 !important;
  margin: .35rem 0 0 !important;
}

.lesson-progress-card {
  background: #ffffff;
  border: 2px solid #cbd5e1;
  border-radius: 8px;
  box-shadow: 0 14px 30px rgba(16, 24, 40, .16);
  bottom: 1.25rem;
  margin: 0;
  max-width: 34rem;
  padding: .85rem 1rem;
  position: fixed;
  right: 1.5rem;
  width: min(34rem, calc(100vw - 24rem));
  z-index: 9999;
}

.lesson-progress-card h3 {
  color: #172033 !important;
  font-size: 1.05rem !important;
  margin: 0 0 .55rem !important;
}

.lesson-progress-meta {
  align-items: center;
  display: flex;
  flex-wrap: wrap;
  gap: .45rem;
}

.lesson-progress-meta strong,
.lesson-progress-meta span {
  color: #172033 !important;
  font-weight: 900 !important;
}

.lesson-progress-meta p {
  color: #5f6b7a !important;
  font-weight: 800 !important;
  margin: 0 !important;
}

@media (max-width: 900px) {
  .lesson-progress-card {
    bottom: .75rem;
    left: .75rem;
    right: .75rem;
    width: auto;
  }
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
        return {"completed_rinkiniai": [], "completed_lessons": []}
    try:
        with SETTINGS_FILE.open("r", encoding="utf-8") as f:
            settings = json.load(f)
    except (json.JSONDecodeError, OSError):
        return {"completed_rinkiniai": [], "completed_lessons": []}

    completed = settings.get("completed_rinkiniai", [])
    if not isinstance(completed, list):
        completed = []
    completed_lessons = settings.get("completed_lessons", [])
    if not isinstance(completed_lessons, list):
        completed_lessons = []
    return {"completed_rinkiniai": completed, "completed_lessons": completed_lessons}


def save_settings(settings):
    safe_settings = {
        "completed_rinkiniai": sorted(set(settings.get("completed_rinkiniai", []))),
        "completed_lessons": sorted(set(settings.get("completed_lessons", []))),
    }
    with SETTINGS_FILE.open("w", encoding="utf-8") as f:
        json.dump(safe_settings, f, ensure_ascii=False, indent=2)


def lesson_key(class_name: str, week: str, day: str) -> str:
    return f"{class_name}|{week}|{day}"


def start_lesson_timer(current_lesson_key: str, reset: bool = False):
    timer_key = f"lesson_started_at_{current_lesson_key}"
    if reset or st.session_state.get("active_lesson_key") != current_lesson_key or timer_key not in st.session_state:
        st.session_state.active_lesson_key = current_lesson_key
        st.session_state[timer_key] = datetime.now().isoformat()
    return timer_key


def lesson_elapsed_seconds(current_lesson_key: str) -> int:
    timer_key = f"lesson_started_at_{current_lesson_key}"
    started_raw = st.session_state.get(timer_key)
    if not started_raw:
        return 0
    try:
        started = datetime.fromisoformat(started_raw)
    except ValueError:
        return 0
    return max(0, int((datetime.now() - started).total_seconds()))


def format_duration(seconds: int) -> str:
    minutes, remainder = divmod(max(0, int(seconds)), 60)
    hours, minutes = divmod(minutes, 60)
    if hours:
        return f"{hours} val. {minutes} min."
    if minutes:
        return f"{minutes} min. {remainder} sek."
    return f"{remainder} sek."


def selected_study_date(prefix: str):
    today = datetime.now().date()
    year_options = list(range(today.year - 1, today.year + 2))
    year_default = year_options.index(today.year)

    date_cols = st.columns([1, 1, 1, 3])
    with date_cols[0]:
        year = st.selectbox("Metai", year_options, index=year_default, key=f"{prefix}_year")
    with date_cols[1]:
        month = st.selectbox("Mėnuo", list(range(1, 13)), index=today.month - 1, key=f"{prefix}_month")
    max_day = calendar.monthrange(int(year), int(month))[1]
    default_day = min(today.day, max_day)
    with date_cols[2]:
        day = st.selectbox("Diena", list(range(1, max_day + 1)), index=default_day - 1, key=f"{prefix}_calendar_day")

    return datetime(int(year), int(month), int(day)).date()


def render_daily_start_form(class_name: str, week: str, weekday: str, current_lesson_key: str):
    prefix = f"daily_meta_{class_name}_{week}_{weekday}"
    stage_key = f"{prefix}_stage"
    metadata_key = f"{prefix}_metadata"
    st.session_state.setdefault(stage_key, "date")

    if st.session_state[stage_key] == "tasks" and metadata_key in st.session_state:
        return st.session_state[metadata_key]

    with st.container(border=True):
        st.markdown('<div class="task-title"><span>📅</span><span>Dienos pradžia</span></div>', unsafe_allow_html=True)

        if st.session_state[stage_key] == "date":
            solved_date = selected_study_date(prefix)
            if st.button("Toliau", type="primary", key=f"{prefix}_date_next"):
                st.session_state[f"{prefix}_solved_date"] = solved_date.isoformat()
                st.session_state[stage_key] = "reading"
                st.rerun()
            return None

        solved_date = st.session_state.get(f"{prefix}_solved_date", datetime.now().date().isoformat())
        st.caption(f"Sprendimo data: {solved_date}")
        st.markdown("#### Skaitymas")
        read_key = f"{prefix}_read"
        st.markdown("**Ar skaitei?**")
        yes_col, no_col, _ = st.columns([0.7, 0.7, 4.6])
        with yes_col:
            if st.button(
                "Taip",
                key=f"{prefix}_read_yes",
                type="primary" if st.session_state.get(read_key) == "Taip" else "secondary",
                use_container_width=True,
            ):
                st.session_state[read_key] = "Taip"
                st.rerun()
        with no_col:
            if st.button(
                "Ne",
                key=f"{prefix}_read_no",
                type="primary" if st.session_state.get(read_key) == "Ne" else "secondary",
                use_container_width=True,
            ):
                st.session_state[read_key] = "Ne"
                st.rerun()
        read_today = st.session_state.get(read_key)
        if read_today is None:
            st.info("Pasirink, ar šiandien skaitei.")
            return None

        book_title = ""
        pages = 0
        minutes = 0
        if read_today == "Taip":
            read_cols = st.columns([2, 1, 1])
            with read_cols[0]:
                book_title = st.text_input("Knyga", key=f"{prefix}_book", placeholder="Knygos pavadinimas")
            with read_cols[1]:
                pages = st.number_input("Kiek puslapių skaitei?", min_value=0, step=1, key=f"{prefix}_pages")
            with read_cols[2]:
                minutes = st.number_input("Kiek minučių skaitei?", min_value=0, step=1, key=f"{prefix}_minutes")
        else:
            st.caption("Gerai, šiandien skaitymo laukų pildyti nereikia.")

        if st.button("Pradėti užduotis", type="primary", key=f"{prefix}_reading_next"):
            metadata = {
                "solved_date": solved_date,
                "read_today": read_today,
                "book_title": book_title.strip() if read_today == "Taip" else "",
                "reading_pages": int(pages) if read_today == "Taip" else 0,
                "reading_minutes": int(minutes) if read_today == "Taip" else 0,
            }
            st.session_state[metadata_key] = metadata
            st.session_state[stage_key] = "tasks"
            start_lesson_timer(current_lesson_key, reset=True)
            st.rerun()
        return None


def daily_reading_log_row(week: str, day: str, metadata: dict):
    read_today = metadata.get("read_today", "Ne")
    book_title = metadata.get("book_title", "")
    minutes = int(metadata.get("reading_minutes", 0))
    pages = int(metadata.get("reading_pages", 0))
    done = read_today == "Taip" and bool(book_title or minutes or pages)
    answer = f"{read_today}; {book_title}; {minutes} min.; {pages} psl."
    row = log_row("Pamokos", week, day, "Skaitymas", "Skaitymo žymėjimas", answer, "Tėvų / vaiko žymėjimas", done or read_today == "Ne")
    row["Knyga"] = book_title
    row["Skaitymo minutės"] = minutes
    row["Skaitymo puslapiai"] = pages
    row["Kaip sekėsi"] = "dienos pradžia"
    return row


def with_daily_metadata(rows, metadata: dict):
    enriched = []
    for row in rows:
        updated = dict(row)
        updated["Sprendimo data"] = metadata.get("solved_date", "")
        updated["Sprendimo trukmė sek."] = int(metadata.get("duration_seconds", 0))
        updated["Sprendimo trukmė"] = metadata.get("duration_text", "")
        updated["Ar skaitei"] = metadata.get("read_today", "")
        updated["Knyga"] = updated.get("Knyga", metadata.get("book_title", ""))
        updated["Skaitymo minutės"] = updated.get("Skaitymo minutės", metadata.get("reading_minutes", 0))
        updated["Skaitymo puslapiai"] = updated.get("Skaitymo puslapiai", metadata.get("reading_pages", 0))
        enriched.append(updated)
    return enriched


def normalize_answer(value: str) -> str:
    value = str(value).strip().lower().replace(",", ".")
    value = unicodedata.normalize("NFKD", value)
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    value = re.sub(r"[^\w\s.:-]", "", value)
    return re.sub(r"\s+", " ", value).strip()


def parse_decimal_answer(value: str):
    normalized = normalize_answer(value)
    if re.fullmatch(r"-?\d+(\.\d+)?", normalized):
        try:
            return Decimal(normalized)
        except InvalidOperation:
            return None
    return None


def normalize_comparison_symbol(value: str) -> str:
    return str(value).strip().replace("＜", "<").replace("＞", ">")


def is_eur_ct_answer(correct: str) -> bool:
    return bool(re.fullmatch(r"\s*\d+\s*eur\s+\d+\s*ct\s*", str(correct).strip(), flags=re.IGNORECASE))


def parse_eur_ct_answer(value: str):
    match = re.fullmatch(r"\s*(\d+)\s*eur\s+(\d+)\s*ct\s*", str(value).strip(), flags=re.IGNORECASE)
    if not match:
        return None
    return int(match.group(1)) * 100 + int(match.group(2))


def render_eur_ct_inputs(key: str) -> str:
    eur_col, ct_col, _ = st.columns([0.75, 0.75, 4.5])
    with eur_col:
        eur = st.text_input("Eur", key=f"{key}_eur", placeholder="0", max_chars=4)
    with ct_col:
        ct = st.text_input("ct", key=f"{key}_ct", placeholder="0", max_chars=2)

    if eur.strip() and ct.strip():
        return f"{eur.strip()} Eur {ct.strip()} ct"
    return ""


def render_compact_answer_input(label: str, key: str, placeholder: str = "Tavo atsakymas", max_chars: int = 12) -> str:
    answer_col, _ = st.columns([1.15, 4.85])
    with answer_col:
        return st.text_input(label, key=key, placeholder=placeholder, max_chars=max_chars)


def is_largest_smallest_number_question(subject: str, correct: str) -> bool:
    return (
        "did" in normalize_answer(subject)
        and "maz" in normalize_answer(subject)
        and bool(re.fullmatch(r"\s*\d+\s*,\s*\d+\s*", str(correct)))
    )


def render_largest_smallest_inputs(key: str, correct: str) -> str:
    expected_parts = split_expected_parts(correct)
    expected_largest = expected_parts[0] if len(expected_parts) > 0 else ""
    expected_smallest = expected_parts[1] if len(expected_parts) > 1 else ""

    largest_col, smallest_col, _ = st.columns([0.95, 0.95, 4.1])
    with largest_col:
        largest = st.text_input("Didžiausias", key=f"{key}_largest", placeholder="000", max_chars=3)
        if largest.strip() and expected_largest:
            show_feedback(check_answer(largest, expected_largest))
    with smallest_col:
        smallest = st.text_input("Mažiausias", key=f"{key}_smallest", placeholder="000", max_chars=3)
        if smallest.strip() and expected_smallest:
            show_feedback(check_answer(smallest, expected_smallest))

    if largest.strip() and smallest.strip():
        return f"{largest.strip()}, {smallest.strip()}"
    return ""


def check_answer(answer: str, correct: str) -> bool:
    answer_symbol = normalize_comparison_symbol(answer)
    correct_symbol = normalize_comparison_symbol(correct)
    if answer_symbol in {"<", ">", "="} or correct_symbol in {"<", ">", "="}:
        return answer_symbol == correct_symbol

    answer_money = parse_eur_ct_answer(answer)
    correct_money = parse_eur_ct_answer(correct)
    if answer_money is not None and correct_money is not None:
        return answer_money == correct_money

    answer_number = parse_decimal_answer(answer)
    correct_number = parse_decimal_answer(correct)
    if answer_number is not None and correct_number is not None:
        return answer_number == correct_number
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
        st.markdown(
            f'<div class="answer-hint"><span>🔐</span><span>Atsakymas: {correct}</span></div>',
            unsafe_allow_html=True,
        )


def progress_panel(score: int, total: int, label: str, target=None, variant: str = "sidebar"):
    target = target or st.sidebar
    pct = int(score / total * 100) if total else 0
    if pct == 100 and total:
        message = "Puikus darbas!"
    elif pct >= 70:
        message = "Labai gerai. Liko truputis."
    elif total:
        message = "Ramu. Mokomės po vieną žingsnį."
    else:
        message = "Pradėkime."

    card_class = "lesson-progress-card" if variant == "main" else "sidebar-progress-card"
    meta_class = ' class="lesson-progress-meta"' if variant == "main" else ""
    target.markdown(
        f"""
<div class="{card_class}">
  <h3>{label}</h3>
  <div class="sidebar-progress-bar"><div class="sidebar-progress-fill" style="width:{pct}%"></div></div>
  <div{meta_class}><strong>{score}/{total}</strong><span> teisingai · {pct}%</span><p>{message}</p></div>
</div>
""",
        unsafe_allow_html=True,
    )


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
        if not old_df.empty and not new_df.empty:
            duplicate_columns = ["Režimas", "Rinkinys", "Savaitė", "Diena", "Užduotis", "Klausimas"]

            def duplicate_keys(df):
                parts = [df.get("Laikas", pd.Series([""] * len(df))).astype(str).str[:10]]
                parts.extend(df.get(col, pd.Series([""] * len(df))).fillna("").astype(str) for col in duplicate_columns)
                return set(zip(*parts))

            existing_keys = duplicate_keys(old_df)
            new_keys = list(
                zip(
                    new_df.get("Laikas", pd.Series([""] * len(new_df))).astype(str).str[:10],
                    new_df.get("Režimas", pd.Series([""] * len(new_df))).fillna("").astype(str),
                    new_df.get("Rinkinys", pd.Series([""] * len(new_df))).fillna("").astype(str),
                    new_df.get("Savaitė", pd.Series([""] * len(new_df))).fillna("").astype(str),
                    new_df.get("Diena", pd.Series([""] * len(new_df))).fillna("").astype(str),
                    new_df.get("Užduotis", pd.Series([""] * len(new_df))).fillna("").astype(str),
                    new_df.get("Klausimas", pd.Series([""] * len(new_df))).fillna("").astype(str),
                )
            )

            keep_rows = []
            seen_new_keys = set()
            for key in new_keys:
                keep = key not in existing_keys and key not in seen_new_keys
                keep_rows.append(keep)
                if keep:
                    seen_new_keys.add(key)
            new_df = new_df[keep_rows]

            reading_mask = (
                new_df.get("Režimas", pd.Series([""] * len(new_df))).astype(str).eq("Vasaros užduotys")
                & new_df.get("Užduotis", pd.Series([""] * len(new_df))).astype(str).eq("Skaitymas")
                & new_df.get("Klausimas", pd.Series([""] * len(new_df))).astype(str).eq("Skaitymo žymėjimas")
            )
            if not new_df.empty and reading_mask.any():
                old_reading = old_df[
                    old_df.get("Režimas", pd.Series([""] * len(old_df))).astype(str).eq("Vasaros užduotys")
                    & old_df.get("Užduotis", pd.Series([""] * len(old_df))).astype(str).eq("Skaitymas")
                    & old_df.get("Klausimas", pd.Series([""] * len(old_df))).astype(str).eq("Skaitymo žymėjimas")
                ].copy()
                existing_reading_keys = set()
                if not old_reading.empty:
                    existing_reading_keys = set(
                        zip(
                            old_reading.get("Laikas", pd.Series([""] * len(old_reading))).astype(str).str[:10],
                            old_reading.get("Rinkinys", pd.Series([""] * len(old_reading))).astype(str),
                            old_reading.get("Savaitė", pd.Series([""] * len(old_reading))).astype(str),
                            old_reading.get("Diena", pd.Series([""] * len(old_reading))).astype(str),
                        )
                    )
                new_reading_keys = list(
                    zip(
                        new_df.get("Laikas", pd.Series([""] * len(new_df))).astype(str).str[:10],
                        new_df.get("Rinkinys", pd.Series([""] * len(new_df))).astype(str),
                        new_df.get("Savaitė", pd.Series([""] * len(new_df))).astype(str),
                        new_df.get("Diena", pd.Series([""] * len(new_df))).astype(str),
                    )
                )
                keep_reading = [
                    (not is_reading) or (key not in existing_reading_keys)
                    for is_reading, key in zip(reading_mask.tolist(), new_reading_keys)
                ]
                new_df = new_df[keep_reading]
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
    if "Sprendimo data" not in detailed.columns:
        detailed["Sprendimo data"] = ""
    if "Sprendimo trukmė" not in detailed.columns:
        detailed["Sprendimo trukmė"] = ""

    grouped = (
        detailed.groupby("Sesija", dropna=False)
        .agg(
            Laikas=("Laikas", "first"),
            Sprendimo_data=("Sprendimo data", "first"),
            Sprendimo_trukmė=("Sprendimo trukmė", "first"),
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


def render_daily_lessons(classrooms, child_name: str, show_answers: bool, settings):
    if (
        "daily_class" not in st.session_state
        or (
            not st.session_state.get("daily_class_user_selected", False)
            and st.session_state.daily_class == "1 klasė"
            and classrooms.get("2 klasė")
        )
    ):
        st.session_state.daily_class = "2 klasė" if classrooms.get("2 klasė") else "1 klasė"

    st.sidebar.markdown("### Klasė")
    class_cols = st.sidebar.columns(2)
    class_labels = list(classrooms.keys())
    for idx, class_label in enumerate(class_labels):
        with class_cols[idx % len(class_cols)]:
            if st.button(
                class_label.replace(" klasė", ""),
                key=f"class_{class_label}",
                type="primary" if st.session_state.daily_class == class_label else "secondary",
                use_container_width=True,
            ):
                st.session_state.daily_class = class_label
                st.session_state.daily_class_user_selected = True
                st.rerun()

    class_name = st.session_state.daily_class
    data = classrooms.get(class_name, {})

    if not data:
        hero(f"{child_name}: {class_name}", "Šiai klasei užduočių banką dar kursime.")
        st.info("Dabar visi turimi rinkiniai perkelti į „1 klasė“. „2 klasė“ paruošta naujai logikai ir būsimoms užduotims.")
        return

    completed_rinkiniai = set(settings.get("completed_rinkiniai", [])) if class_name == "1 klasė" else set()
    completed_lessons = set(settings.get("completed_lessons", []))
    show_completed_lessons = st.sidebar.checkbox("Rodyti atliktas dienas", value=False)
    active_weeks = []
    for week_name, week_days in data.items():
        if week_name in completed_rinkiniai:
            continue
        visible_days = [
            day_name
            for day_name in week_days.keys()
            if show_completed_lessons or lesson_key(class_name, week_name, day_name) not in completed_lessons
        ]
        if visible_days:
            active_weeks.append(week_name)

    if not data:
        st.error("Nerastas arba tuščias tasks.json failas.")
        return

    if not active_weeks:
        hero(f"{child_name}: {class_name}", "Visi rinkiniai pažymėti kaip užbaigti.")
        st.info("Atidarykite „Papildomai“ → „Tėvų nustatymai“ ir grąžinkite bent vieną rinkinį, kad jis vėl būtų rodomas vaikui.")
        return

    st.sidebar.markdown("### Pamoka")
    week = st.sidebar.selectbox("Rinkinys", active_weeks, key=f"week_{class_name}")
    available_days = [
        day_name
        for day_name in data[week].keys()
        if show_completed_lessons or lesson_key(class_name, week, day_name) not in completed_lessons
    ]
    day = st.sidebar.selectbox("Diena", available_days, key=f"day_{class_name}_{week}")
    sections = data[week][day]
    current_lesson_key = lesson_key(class_name, week, day)
    lesson_done = current_lesson_key in completed_lessons
    repeat_key = f"repeat_done_{current_lesson_key}"
    daily_meta_prefix = f"daily_meta_{class_name}_{week}_{day}"

    hero(f"{child_name}: {week} · {day}", "Kasdienės užduotys ir pamokos viename lange.")
    if lesson_done:
        st.success("Ši diena jau pažymėta kaip atlikta.")
        if not st.session_state.get(repeat_key, False):
            st.warning("Šitas rinkinys ir diena jau spręsti. Ar nori spręsti iš naujo?")
            c_repeat, c_skip = st.columns([1, 2])
            with c_repeat:
                if st.button("Spręsti iš naujo", type="primary", use_container_width=True):
                    st.session_state[repeat_key] = True
                    st.session_state[f"{daily_meta_prefix}_stage"] = "date"
                    st.session_state.pop(f"{daily_meta_prefix}_metadata", None)
                    start_lesson_timer(current_lesson_key, reset=True)
                    st.rerun()
            with c_skip:
                st.info("Jei nenori kartoti, šone pasirink kitą dieną arba nuimk „Rodyti atliktas dienas“.")
            return
    daily_metadata = render_daily_start_form(class_name, week, day, current_lesson_key)
    if daily_metadata is None:
        return
    start_lesson_timer(current_lesson_key)
    progress_slot = st.empty()

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

            elif sec_type == "multiple_choice":
                options_list = sec.get("options", [])
                answers_list = sec.get("answers", [])
                for i, prompt in enumerate(prompts):
                    total += 1
                    key = f"mc_{week}_{day}_{s_idx}_{i}"
                    correct = answers_list[i] if i < len(answers_list) else ""
                    options = options_list[i] if i < len(options_list) else []
                    max_attempts = int(sec.get("max_attempts", 2))
                    if options == ["<", ">", "="]:
                        show_correct_answer(correct, show_answers)
                        answer = render_comparison_buttons(prompt, correct, key, max_attempts=max_attempts)
                    else:
                        st.markdown(f'<div class="question">{prompt}</div>', unsafe_allow_html=True)
                        show_correct_answer(correct, show_answers)
                        answer = render_option_buttons(options, correct, key, max_attempts=max_attempts) if options else ""
                    if answer:
                        ok = check_answer(answer, correct)
                        if options != ["<", ">", "="]:
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
                        correct = sec.get("answers", [""])[i] if i < len(sec.get("answers", [])) else "Laisvas atsakymas"
                        key = f"tx_{week}_{day}_{s_idx}_{i}"
                        if "__ Eur __ ct" in str(prompt) and is_eur_ct_answer(correct):
                            answer = render_eur_ct_inputs(key)
                        elif is_largest_smallest_number_question(subject, correct):
                            answer = render_largest_smallest_inputs(key, correct)
                        elif checkable and subject.lower().startswith("matematika") and not cols:
                            answer = render_compact_answer_input("Atsakymas", key=key, placeholder="0")
                        else:
                            answer = st.text_input("Atsakymas", key=key, placeholder="Tavo atsakymas")
                        if checkable:
                            show_correct_answer(correct, show_answers)
                        if answer:
                            ok = check_answer(answer, correct) if checkable else len(answer.strip()) >= 3
                            show_feedback(ok, free=not checkable and ok)
                            score += int(ok)
                            rows_to_log.append(log_row("Pamokos", week, day, subject, prompt, answer, correct, ok))

    with progress_slot.container():
        progress_panel(score, total, "Dienos pažanga", target=st, variant="main")

    st.divider()
    col1, col_done, col2 = st.columns([1, 1, 2])
    with col1:
        if st.button("Išsaugoti dienos rezultatą", type="primary", use_container_width=True):
            duration_seconds = lesson_elapsed_seconds(current_lesson_key)
            daily_metadata["duration_seconds"] = duration_seconds
            daily_metadata["duration_text"] = format_duration(duration_seconds)
            daily_rows = rows_to_log or [log_row("Pamokos", week, day, "Dienos rezultatas", "-", f"{score}/{total}", "-", score == total)]
            daily_rows.append(daily_reading_log_row(week, day, daily_metadata))
            append_log(with_daily_metadata(daily_rows, daily_metadata))
            st.success(f"Išsaugota: {score}/{total}")
            st.caption(f"Sprendimo trukmė: {daily_metadata['duration_text']}")
            if total and score == total:
                settings["completed_lessons"] = sorted(completed_lessons | {current_lesson_key})
                save_settings(settings)
                st.success("Diena automatiškai pažymėta kaip atlikta.")
                st.balloons()
    with col_done:
        done_label = "Atlikta" if lesson_done else "Pažymėti atlikta"
        if st.button(done_label, disabled=lesson_done, use_container_width=True):
            settings["completed_lessons"] = sorted(completed_lessons | {current_lesson_key})
            save_settings(settings)
            st.success("Diena pažymėta kaip atlikta.")
            st.rerun()
    with col2:
        render_metric("Šios dienos rezultatas", f"{score}/{total}", "Rezultatas skaičiuojamas pagal įrašytus atsakymus.")


def summer_log_row(rinkinys, week, day, task, question, answer, correct, result):
    row = log_row("Vasaros užduotys", rinkinys, day, task.get("subject", ""), question, answer, correct, result)
    row["Savaitė"] = week
    row["Įgūdis"] = task.get("skill", "")
    row["Tracking tags"] = ", ".join(task.get("tracking_tags", []))
    return row


def render_hint_and_explanation(question, has_answer: bool, ok: bool, show_answers: bool):
    if show_answers and question.get("hint"):
        with st.expander("Užuomina", expanded=False):
            st.write(question["hint"])
    if has_answer and (ok or show_answers) and question.get("explanation"):
        st.info(question["explanation"])


def check_summer_answer(answer, correct, exact: bool = False):
    answer_text = str(answer).strip()
    correct_text = str(correct).strip()

    if exact:
        return answer_text == correct_text

    lt_letters = "ąčęėįšųūžĄČĘĖĮŠŲŪŽ"
    if len(correct_text) == 1 or any(ch in correct_text for ch in lt_letters):
        answer_clean = re.sub(r"\s+", " ", answer_text).strip().lower()
        correct_clean = re.sub(r"\s+", " ", correct_text).strip().lower()
        return answer_clean == correct_clean

    if correct_text in {".", "?", "!", "<", ">", "="}:
        return answer_text == correct_text

    if "," in correct_text:
        answer_parts = [normalize_answer(part) for part in re.split(r"[,;|]", answer_text) if part.strip()]
        correct_parts = [normalize_answer(part) for part in re.split(r"[,;|]", correct_text) if part.strip()]
        return answer_parts == correct_parts

    return check_answer(answer_text, correct_text)


def render_reading_tracker(rinkinys, week, day, task, task_key):
    st.markdown(f'<div class="task-title"><span>📚</span><span>{task.get("title", "Skaitymo žymėjimas")}</span></div>', unsafe_allow_html=True)
    st.write(task.get("instructions", "Pažymėk, kaip šiandien sekėsi skaityti."))

    read_today = st.selectbox("Ar šiandien skaitei?", ["Taip", "Ne"], key=f"{task_key}_read")
    book_title = st.text_input("Knygos pavadinimas", key=f"{task_key}_book")
    minutes = st.number_input("Kiek minučių skaitei?", min_value=0, step=1, key=f"{task_key}_minutes")
    pages = st.number_input("Kiek puslapių perskaitei?", min_value=0, step=1, key=f"{task_key}_pages")
    feeling = st.selectbox("Kaip sekėsi?", ["lengva", "normalu", "sunku"], key=f"{task_key}_feeling")

    done = read_today == "Taip" and bool(book_title.strip() or minutes or pages)
    if done:
        show_feedback(True, free=True)
    elif read_today == "Ne":
        st.caption("Nieko tokio. Pažymėta, kad šiandien skaitymo nebuvo.")

    answer = f"{read_today}; {book_title}; {minutes} min.; {pages} psl.; {feeling}"
    row = summer_log_row(rinkinys, week, day, task, "Skaitymo žymėjimas", answer, "Tėčio / vaiko žymėjimas", done)
    row["Knyga"] = book_title.strip()
    row["Skaitymo minutės"] = int(minutes)
    row["Skaitymo puslapiai"] = int(pages)
    row["Kaip sekėsi"] = feeling
    return int(done), 1, [row]


def parse_old_reading_answer(value):
    parts = [part.strip() for part in str(value).split(";")]
    book = parts[1] if len(parts) > 1 else ""
    minutes = 0
    pages = 0
    feeling = parts[4] if len(parts) > 4 else ""
    if len(parts) > 2:
        match = re.search(r"\d+", parts[2])
        minutes = int(match.group()) if match else 0
    if len(parts) > 3:
        match = re.search(r"\d+", parts[3])
        pages = int(match.group()) if match else 0
    return book, minutes, pages, feeling


def load_reading_progress():
    if not LOG_FILE.exists():
        return pd.DataFrame()

    try:
        df = repair_dataframe(pd.read_csv(LOG_FILE))
    except (OSError, pd.errors.ParserError):
        return pd.DataFrame()

    required = {"Režimas", "Užduotis", "Klausimas", "Laikas"}
    if not required.issubset(df.columns):
        return pd.DataFrame()

    reading = df[
        df["Užduotis"].astype(str).eq("Skaitymas")
        & df["Klausimas"].astype(str).eq("Skaitymo žymėjimas")
    ].copy()
    if reading.empty:
        return reading

    if not {"Knyga", "Skaitymo minutės", "Skaitymo puslapiai", "Kaip sekėsi"}.issubset(reading.columns):
        parsed = reading["Vaiko atsakymas"].map(parse_old_reading_answer)
        reading["Knyga"] = parsed.map(lambda item: item[0])
        reading["Skaitymo minutės"] = parsed.map(lambda item: item[1])
        reading["Skaitymo puslapiai"] = parsed.map(lambda item: item[2])
        reading["Kaip sekėsi"] = parsed.map(lambda item: item[3])

    reading["Skaitymo minutės"] = pd.to_numeric(reading["Skaitymo minutės"], errors="coerce").fillna(0).astype(int)
    reading["Skaitymo puslapiai"] = pd.to_numeric(reading["Skaitymo puslapiai"], errors="coerce").fillna(0).astype(int)
    if "Sprendimo data" in reading.columns:
        solved_dates = pd.to_datetime(reading["Sprendimo data"], errors="coerce")
        logged_dates = pd.to_datetime(reading["Laikas"], errors="coerce")
        reading["Data"] = solved_dates.fillna(logged_dates).dt.date
    else:
        reading["Data"] = pd.to_datetime(reading["Laikas"], errors="coerce").dt.date
    return reading.dropna(subset=["Data"])


def render_reading_progress_chart():
    reading = load_reading_progress()
    if reading.empty:
        st.info("Skaitymo statistikos dar nėra. Ji atsiras išsaugojus vasaros rezultatą.")
        return

    daily = (
        reading.groupby("Data", as_index=False)
        .agg(
            Puslapiai=("Skaitymo puslapiai", "sum"),
            Minutės=("Skaitymo minutės", "sum"),
        )
        .sort_values("Data")
    )
    st.line_chart(daily.set_index("Data")[["Puslapiai", "Minutės"]])

    latest = reading[["Laikas", "Diena", "Knyga", "Skaitymo minutės", "Skaitymo puslapiai", "Kaip sekėsi"]].tail(10)
    st.dataframe(latest.iloc[::-1], use_container_width=True, hide_index=True)


def should_split_missing_parts_question(prompt, correct, options):
    return not options and "_" in str(prompt) and "," in str(correct)


def split_expected_parts(correct):
    return [part.strip() for part in str(correct).split(",") if part.strip()]


def is_comparison_symbol_question(correct, options):
    return not options and str(correct).strip() in {"<", ">", "="}


def render_missing_parts_inputs(correct, key):
    expected_parts = split_expected_parts(correct)
    columns = st.columns(min(len(expected_parts), 4))
    answer_parts = []
    part_results = []

    for index, expected in enumerate(expected_parts):
        with columns[index % len(columns)]:
            answer_part = st.text_input(
                f"{index + 1} dalis",
                key=f"{key}_part_{index}",
                placeholder="raide / dalis",
            )
            answer_parts.append(answer_part)
            if answer_part.strip():
                part_ok = check_summer_answer(answer_part, expected)
                part_results.append(part_ok)
                show_feedback(part_ok)
            else:
                part_results.append(False)

    return ", ".join(part.strip() for part in answer_parts), part_results


def render_option_buttons(options, correct, key, max_attempts=2, labels=None):
    answer_key = f"{key}_button_answer"
    attempts_key = f"{key}_button_attempts"
    solved_key = f"{key}_button_solved"

    st.session_state.setdefault(answer_key, "")
    st.session_state.setdefault(attempts_key, 0)
    st.session_state.setdefault(solved_key, False)

    locked = st.session_state[attempts_key] >= max_attempts or st.session_state[solved_key]
    attempts_left = max(0, max_attempts - st.session_state[attempts_key])
    st.caption(f"Liko bandymų: {attempts_left}")

    columns = st.columns(min(len(options), 3))
    button_labels = labels or [str(option) for option in options]
    for index, option in enumerate(options):
        option_text = str(option)
        with columns[index % len(columns)]:
            if st.button(
                button_labels[index],
                key=f"{key}_option_{index}",
                use_container_width=True,
                disabled=locked,
            ):
                st.session_state[answer_key] = option_text
                st.session_state[attempts_key] = min(max_attempts, st.session_state[attempts_key] + 1)
                st.session_state[solved_key] = check_summer_answer(option_text, correct, exact=True)

    if st.session_state[answer_key]:
        st.caption(f"Pasirinkta: {st.session_state[answer_key]}")
    if st.session_state[attempts_key] >= max_attempts and not st.session_state[solved_key]:
        st.caption("Bandymų nebėra.")

    return st.session_state[answer_key]


def render_comparison_buttons(prompt, correct, key, max_attempts=2):
    answer_key = f"{key}_button_answer"
    attempts_key = f"{key}_button_attempts"
    solved_key = f"{key}_button_solved"

    st.session_state.setdefault(answer_key, "")
    st.session_state.setdefault(attempts_key, 0)
    st.session_state.setdefault(solved_key, False)

    locked = st.session_state[attempts_key] >= max_attempts or st.session_state[solved_key]
    prompt_col, less_col, greater_col, equal_col, status_col = st.columns([4.2, 0.55, 0.55, 0.55, 1.25])
    with prompt_col:
        st.markdown(f'<div class="question" style="margin:.12rem 0;padding:.55rem .75rem;">{prompt}</div>', unsafe_allow_html=True)

    for col, label, value in [(less_col, "<", "<"), (greater_col, "＞", ">"), (equal_col, "=", "=")]:
        with col:
            if st.button(label, key=f"{key}_comparison_{value}", disabled=locked, use_container_width=True):
                st.session_state[answer_key] = value
                st.session_state[attempts_key] = min(max_attempts, st.session_state[attempts_key] + 1)
                st.session_state[solved_key] = check_answer(value, correct)

    with status_col:
        attempts_left = max(0, max_attempts - st.session_state[attempts_key])
        st.caption(f"Liko: {attempts_left}")
        if st.session_state[answer_key]:
            show_feedback(check_answer(st.session_state[answer_key], correct))

    return st.session_state[answer_key]


def render_summer_question(task_type, question, key, show_answers):
    prompt = question.get("text", "")
    correct = question.get("answer", "")
    options = question.get("options", [])
    st.markdown(f'<div class="question">{prompt}</div>', unsafe_allow_html=True)

    split_missing_parts = should_split_missing_parts_question(prompt, correct, options)
    part_results = []

    if split_missing_parts:
        answer, part_results = render_missing_parts_inputs(correct, key)
    elif task_type in {"multiple_choice", "punctuation_choice", "sentence_completion"} and options:
        answer = render_option_buttons(options, correct, key)
    elif is_comparison_symbol_question(correct, options):
        answer = render_option_buttons(
            ["<", ">", "="],
            correct,
            key,
            max_attempts=2,
            labels=["<", "＞", "="],
        )
    elif task_type == "number_input_check":
        answer = st.text_input("Atsakymas", key=key, placeholder="Įrašyk skaičių")
    else:
        placeholder = "Įrašyk atsakymą"
        if task_type == "sentence_order":
            placeholder = "Sudėk sakinį"
        elif task_type == "word_building":
            placeholder = "Sudėk žodį"
        answer = st.text_input("Atsakymas", key=key, placeholder=placeholder)

    show_correct_answer(correct, show_answers)
    if split_missing_parts:
        expected_count = len(split_expected_parts(correct))
        filled_count = sum(1 for part in answer.split(",") if str(part).strip())
        has_answer = filled_count == expected_count
    else:
        has_answer = bool(str(answer).strip())
    ok = check_summer_answer(answer, correct, exact=bool(options)) if has_answer else False
    if has_answer and not split_missing_parts:
        show_feedback(ok)
    render_hint_and_explanation(question, has_answer, ok, show_answers)
    return answer, correct, ok, has_answer


def render_summer_task(rinkinys, week, day, task, task_index, show_answers):
    task_type = task.get("type", "text_input_check")
    task_key = f"summer_{rinkinys}_{week}_{day}_{task_index}"

    if task_type == "reading_tracker":
        return render_reading_tracker(rinkinys, week, day, task, task_key)

    subject = task.get("subject", "Užduotis")
    symbol = section_icon(subject, "📌")
    st.markdown(f'<div class="task-title"><span>{symbol}</span><span>{subject}: {task.get("title", "Užduotis")}</span></div>', unsafe_allow_html=True)
    if task.get("goal"):
        st.caption(task["goal"])
    if task.get("instructions"):
        st.write(task["instructions"])

    score = 0
    total = 0
    rows = []
    render_type = "multiple_choice" if task_type == "mixed_review" else task_type

    for q_index, question in enumerate(task.get("questions", [])):
        total += 1
        answer, correct, ok, has_answer = render_summer_question(render_type, question, f"{task_key}_{q_index}", show_answers)
        if has_answer:
            score += int(ok)
            rows.append(summer_log_row(rinkinys, week, day, task, question.get("text", ""), answer, correct, ok))

    if task.get("parent_check"):
        st.checkbox("Patikrinta", key=f"{task_key}_parent_check", help="Pažymėkite, kai tėvų patikrinimas atliktas.")
        st.markdown("**Tėvų patikrinimas:**")
        st.caption(task["parent_check"])

    return score, total, rows


def render_summer_tasks(summer_data, child_name: str, show_answers: bool):
    if not summer_data:
        st.error("Nerastas arba tuščias summer_tasks.json failas.")
        return

    pick_rinkinys, pick_week, pick_day = st.columns([1, 1, 1])
    with pick_rinkinys:
        rinkinys = st.selectbox("Vasaros rinkinys", list(summer_data.keys()), key="summer_rinkinys")
    weeks = summer_data.get(rinkinys, {})
    with pick_week:
        week = st.selectbox("Savaitė", list(weeks.keys()), key=f"summer_week_{rinkinys}")
    days = weeks.get(week, {})
    with pick_day:
        day = st.selectbox("Diena", list(days.keys()), key=f"summer_day_{rinkinys}_{week}")

    hero(f"{child_name}: Vasaros užduotys", f"{rinkinys} · {week} · {day}")
    st.info(f"Pasirinkta: {rinkinys} → {week} → {day}")

    score = 0
    total = 0
    rows_to_log = []

    for task_index, task in enumerate(days.get(day, [])):
        with st.container(border=True):
            task_score, task_total, task_rows = render_summer_task(rinkinys, week, day, task, task_index, show_answers)
            score += task_score
            total += task_total
            rows_to_log.extend(task_rows)

    progress_panel(score, total, "Vasaros pažanga")

    st.divider()
    col1, col2 = st.columns([1, 2])
    with col1:
        if st.button("Išsaugoti vasaros rezultatą", type="primary", use_container_width=True):
            append_log(rows_to_log or [log_row("Vasaros užduotys", rinkinys, day, "Dienos rezultatas", "-", f"{score}/{total}", "-", score == total)])
            st.success(f"Išsaugota: {score}/{total}")
            if total and score == total:
                st.balloons()
    with col2:
        render_metric("Šios dienos rezultatas", f"{score}/{total}", "Skaitymas įskaitomas pagal pažymėjimą, kitos užduotys tikrinamos automatiškai.")

    with st.expander("Skaitymo statistika", expanded=False):
        render_reading_progress_chart()


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

    count = st.slider("Praktikos ilgis", 5, 20, 10)
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
                        session_df[["Laikas", "Sprendimo_data", "Sprendimo_trukmė", "Režimas", "Rinkinys", "Diena", "Teisingai", "Iš_viso", "Procentai"]],
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
        st.caption("Dabar šie rinkiniai priklauso „1 klasė“. „2 klasė“ bus pildoma atskirai, kai perdėliosime logiką.")
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

        st.markdown("#### Atliktos dienos")
        completed_lessons = settings.get("completed_lessons", [])
        st.caption(f"Pažymėta atliktų dienų: {len(completed_lessons)}")
        if completed_lessons:
            st.dataframe(pd.DataFrame({"Diena": completed_lessons}), use_container_width=True, hide_index=True)
            if st.button("Išvalyti atliktas dienas", use_container_width=True):
                settings["completed_lessons"] = []
                save_settings(settings)
                st.rerun()

        st.markdown("#### Nauji rinkiniai")
        st.info("Programoje jau yra Rinkinys 1-12. Nauji 1 klasės rinkiniai automatiškai atsiras čia ir bus rodomi vaikui, kol nepažymėsite jų užbaigtais.")

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


def switch_main_view(view: str):
    st.session_state.main_view = view


def render_top_navigation():
    if "main_view" not in st.session_state:
        st.session_state.main_view = "Kasdienės užduotys"

    st.sidebar.markdown("### Meniu")
    nav_items = ["Kasdienės užduotys", "Vasaros užduotys", "Papildomai"]
    for label in nav_items:
        st.sidebar.button(
            label,
            key=f"nav_{label}",
            type="primary" if st.session_state.main_view == label else "secondary",
            use_container_width=True,
            on_click=switch_main_view,
            args=(label,),
        )

    st.sidebar.divider()
    return st.session_state.main_view


def render_extra_tools(data, numbers_db, logic_db, reasoning_db, child_name: str, show_answers: bool, settings):
    hero("Papildomai", "Papildomos praktikos, logikos ir tėvų nustatymų vieta.")
    extra_mode = st.selectbox(
        "Papildomas langas",
        ["Greita praktika", "Matematika", "Samprotavimas", "Logika", "Tėvų nustatymai"],
        key="extra_mode",
    )

    if extra_mode == "Greita praktika":
        render_adaptive(data, numbers_db, logic_db, show_answers)
    elif extra_mode == "Matematika":
        render_drill("🧮 Matematikos laboratorija", "Trumpi skaičiavimo pratimai su greitu patikrinimu.", numbers_db, "Matematika", [8, 12, 16, 24], "math_drill", show_answers)
    elif extra_mode == "Samprotavimas":
        render_drill("🧠 Matematinis samprotavimas", "1 klasės užduotys apie korteles, monetas, sekas, statinius ir kryptis.", reasoning_db, "Samprotavimas", [6, 8, 10, 12], "reasoning_drill", show_answers)
    elif extra_mode == "Logika":
        render_drill("🧩 Logikos kampelis", "Mįslės ir gudrūs klausimai, lavinantys samprotavimą.", logic_db, "Logika", [3, 5, 8, 12, 15], "logic_drill", show_answers)
    else:
        render_parent_settings(data, child_name, settings)


data = load_json_file("tasks.json")
grade2_data = load_json_file("grade2_tasks.json")
summer_data = load_json_file("summer_tasks.json")
numbers_db = load_json_file("numbers.json")
logic_db = load_json_file("logic.json")
reasoning_db = load_json_file("reasoning.json")
settings = load_settings()
classrooms = {"1 klasė": data, "2 klasė": grade2_data}

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
main_view = render_top_navigation()

if main_view == "Kasdienės užduotys":
    render_daily_lessons(classrooms, child_name, show_answers, settings)
elif main_view == "Vasaros užduotys":
    render_summer_tasks(summer_data, child_name, show_answers)
else:
    render_extra_tools(data, numbers_db, logic_db, reasoning_db, child_name, show_answers, settings)
