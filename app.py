"""
A7DO Genesis Mind — Full Interactive Dashboard
Streamlit application covering all 36 sheets and 7 developmental phases.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import openpyxl
import math
import json
from pathlib import Path

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="A7DO Genesis Mind",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Load workbook ─────────────────────────────────────────────────────────────
XLSX = Path("excel_report/a7do-final/A7DO_DNA_Master_v5_FINAL.xlsx")

@st.cache_resource
def load_workbook():
    return openpyxl.load_workbook(XLSX, data_only=True)

@st.cache_data
def sheet_to_df(sheet_name, header_row=None):
    wb = load_workbook()
    ws = wb[sheet_name]
    rows = []
    for row in ws.iter_rows(values_only=True):
        if any(c is not None for c in row):
            rows.append(list(row))
    if not rows:
        return pd.DataFrame()
    if header_row is not None and header_row < len(rows):
        cols = [str(c) if c is not None else f"Col{i}" for i, c in enumerate(rows[header_row])]
        data = rows[header_row+1:]
        return pd.DataFrame(data, columns=cols)
    return pd.DataFrame(rows)

# ── Organism formulas (pure Python — tick-driven) ─────────────────────────────
def organism_state(tick):
    week = round(tick / 80)
    height = 50 if week < 40 else min(50 + (177-50)*(1-math.exp(-0.005*(week-40))), 177)
    mass   = 3.5 if week < 40 else min(3.5 + (70-3.5)*(1-math.exp(-0.004*(week-40))), 70)
    hr     = 140 if week < 40 else max(70, 140-(140-70)*((week-40)/1160))
    vocab  = round(50000/(1+math.exp(-0.05*(week-156)))) if week > 0 else 0
    motor  = 5 if week>=400 else (4 if week>=260 else (3 if week>=160 else (2 if week>=80 else 1)))
    tom    = 5 if week>=624 else (4 if week>=312 else (3 if week>=208 else (2 if week>=156 else 1)))
    perm   = 3 if week>=52  else (2 if week>=44  else (1 if week>=36  else 0))
    birth  = tick >= 3200
    phase7 = tick >= 96000
    wisdom = min(0.1+((week-1200)/800)*0.9, 1.0) if week >= 1200 else 0.0
    if   week >= 1200: stage = "Mature Adult"
    elif week >= 1100: stage = "Mid Adult"
    elif week >= 1000: stage = "Adult"
    elif week >= 936:  stage = "Young Adult"
    elif week >= 624:  stage = "Adolescent"
    elif week >= 260:  stage = "Pre-Adolescent"
    elif week >= 156:  stage = "Child"
    elif week >= 80:   stage = "Toddler"
    elif week >= 52:   stage = "Infant"
    elif week >= 40:   stage = "Newborn"
    elif week >= 28:   stage = "Fetal Late"
    elif week >= 12:   stage = "Fetal Mid"
    elif week >= 4:    stage = "Fetal Early"
    else:              stage = "Embryo"
    if tick % 800 == 0:  ll_phase = "💤 Sleep Consolidation"
    elif tick % 10 == 0: ll_phase = "🔁 Repetition"
    elif tick % 5 == 0:  ll_phase = "🤝 Interaction"
    else:                ll_phase = "👁️ Exposure"
    C = min(0.05 + week/3000, 1.0)
    pred_err = max(0.1, 1.0 * math.exp(-0.0001*tick))
    ltm = min(int(tick * 0.96), 200000)
    return dict(tick=tick, week=week, stage=stage, height=round(height,1),
                mass=round(mass,2), hr=round(hr,1), vocab=vocab,
                motor=motor, tom=tom, perm=perm, birth=birth,
                phase7=phase7, wisdom=round(wisdom,3), ll_phase=ll_phase,
                C=round(C,3), pred_err=round(pred_err,3), ltm=ltm)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
[data-testid="stSidebar"] { background: #0d1117; }
[data-testid="stSidebar"] * { color: #e6edf3 !important; }
.metric-card {
    background: linear-gradient(135deg, #1f2937, #111827);
    border: 1px solid #374151;
    border-radius: 12px;
    padding: 16px;
    text-align: center;
    margin: 4px;
}
.metric-val { font-size: 2rem; font-weight: 700; color: #60a5fa; }
.metric-lbl { font-size: 0.75rem; color: #9ca3af; margin-top: 4px; }
.phase-badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
    margin: 2px;
}
.section-hdr {
    font-size: 1.1rem; font-weight: 700;
    border-left: 4px solid #60a5fa;
    padding-left: 10px; margin: 16px 0 8px 0;
    color: #e2e8f0;
}
</style>
""", unsafe_allow_html=True)

# ── Page list (navigation) ─────────────────────────────────────────────────────
pages = [
    "🏠 Mission Control",
    "📈 Growth Timeline",
    "🧬 Biology",
    "🧠 Cognition & Phase 4",
    "🔄 Learning Loop"
]

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🧬 A7DO Genesis Mind")
    st.markdown("**v5 FINAL · 36 sheets · 337 formulas**")
    st.divider()

    tick = st.slider("⚡ Current Tick", 0, 160000, 10000, step=80,
                     help="Drag to advance A7DO through its entire lifecycle")
    st.caption(f"Week {round(tick/80)} · {organism_state(tick)['stage']}")
    st.divider()

    page = st.radio("Navigate", pages, label_visibility="collapsed")
    st.divider()

    st.markdown("**
