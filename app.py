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
    # Life stage
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
    # Learning loop phase
    if tick % 800 == 0:  ll_phase = "💤 Sleep Consolidation"
    elif tick % 10 == 0: ll_phase = "🔁 Repetition"
    elif tick % 5 == 0:  ll_phase = "🤝 Interaction"
    else:                ll_phase = "👁️ Exposure"
    # Consciousness
    C = min(0.05 + week/3000, 1.0)
    # Prediction error (converges)
    pred_err = max(0.1, 1.0 * math.exp(-0.0001*tick))
    # LTM events
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
.ph-core    { background:#1e3a5f; color:#60a5fa; }
.ph-bio     { background:#1a3a2a; color:#4ade80; }
.ph-cog     { background:#3a1a3a; color:#c084fc; }
.ph-p3      { background:#3a2a1a; color:#fb923c; }
.ph-world   { background:#1a3a3a; color:#22d3ee; }
.ph-meta    { background:#2a2a1a; color:#facc15; }
.ph-loop    { background:#1a2a3a; color:#38bdf8; }
.ph-p7      { background:#2a1a1a; color:#f87171; }
.section-hdr {
    font-size: 1.1rem; font-weight: 700;
    border-left: 4px solid #60a5fa;
    padding-left: 10px; margin: 16px 0 8px 0;
    color: #e2e8f0;
}
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🧬 A7DO Genesis Mind")
    st.markdown("**v5 FINAL · 36 sheets · 337 formulas**")
    st.divider()

    tick = st.slider("⚡ Current Tick", 0, 160000, 10000, step=80,
                     help="Drag to advance A7DO through its entire lifecycle")
    st.caption(f"Week {round(tick/80)} · {organism_state(tick)['stage']}")
    st.divider()

    pages = [
        "🏠 Mission Control",
        "📈 Growth Timeline",
        "🧬 Biology",
        "🧠 Cognition & Phase 4",
        "🔄 Learning Loop",
        "🌍 World & Social",
        "⚙️ Engines & Runtime",
        "✨ Phase 7 — Wisdom",
        "📊 All Sheets Explorer",
    ]
    page = st.radio("Navigate", pages, label_visibility="collapsed")
    st.divider()
    st.markdown("**Source files merged:**")
    st.markdown("- Consolidated v17 (18 sheets)")
    st.markdown("- Master v3 (5 sheets)")
    st.markdown("- Consolidated v9 (5 sheets)")
    st.markdown("- Phase 7 NEW (4 sheets)")
    st.markdown("- Learning Loop + Spec (2 sheets)")

state = organism_state(tick)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: MISSION CONTROL
# ═══════════════════════════════════════════════════════════════════════════════
if page == "🏠 Mission Control":
    st.title("🧬 A7DO Genesis Mind — Mission Control")
    st.caption(f"Tick {tick:,} · Week {state['week']} · {state['stage']} · Learning Loop: {state['ll_phase']}")

    # ── Status banner ──
    if state['phase7']:
        st.success("🌟 PHASE 7 ACTIVE — Creative Synthesis · Wisdom Index · Career · Legacy engines online")
    elif state['birth']:
        st.info(f"🔄 Learning Loop active — {state['ll_phase']}")
    else:
        st.warning("⏳ Prenatal — Birth at Tick 3,200")

    # ── Key metrics ──
    cols = st.columns(8)
    metrics = [
        ("Height", f"{state['height']} cm", "📏"),
        ("Mass",   f"{state['mass']} kg",   "⚖️"),
        ("Heart Rate", f"{state['hr']} bpm","❤️"),
        ("Vocabulary", f"{state['vocab']:,}","💬"),
        ("Motor Stage", f"{state['motor']}/5","🦾"),
        ("ToM Stage",  f"{state['tom']}/5",  "🧠"),
        ("Consciousness", f"{state['C']}",   "✨"),
        ("Wisdom W(t)", f"{state['wisdom']}", "🦉"),
    ]
    for col, (lbl, val, icon) in zip(cols, metrics):
        col.markdown(f"""<div class="metric-card">
            <div class="metric-val">{icon}</div>
            <div class="metric-val" style="font-size:1.2rem">{val}</div>
            <div class="metric-lbl">{lbl}</div>
        </div>""", unsafe_allow_html=True)

    st.divider()

    # ── Growth curves ──
    col1, col2 = st.columns(2)
    ticks_range = list(range(0, 160001, 800))
    weeks_range = [t/80 for t in ticks_range]

    with col1:
        st.markdown('<div class="section-hdr">📏 Physical Growth</div>', unsafe_allow_html=True)
        heights = [organism_state(t)['height'] for t in ticks_range]
        masses  = [organism_state(t)['mass']   for t in ticks_range]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=weeks_range, y=heights, name="Height (cm)",
                                  line=dict(color="#60a5fa", width=2)))
        fig.add_trace(go.Scatter(x=weeks_range, y=masses, name="Mass (kg)",
                                  line=dict(color="#4ade80", width=2), yaxis="y2"))
        fig.add_vline(x=state['week'], line_dash="dash", line_color="#f87171",
                      annotation_text=f"Wk {state['week']}")
        fig.update_layout(
            template="plotly_dark", height=280, margin=dict(l=0,r=0,t=20,b=0),
            yaxis=dict(title="Height (cm)"),
            yaxis2=dict(title="Mass (kg)", overlaying="y", side="right"),
            legend=dict(orientation="h", y=1.1)
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="section-hdr">💬 Vocabulary Growth</div>', unsafe_allow_html=True)
        vocabs = [organism_state(t)['vocab'] for t in ticks_range]
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=weeks_range, y=vocabs, name="Vocabulary",
                                   fill="tozeroy", line=dict(color="#c084fc", width=2)))
        fig2.add_vline(x=state['week'], line_dash="dash", line_color="#f87171")
        fig2.update_layout(template="plotly_dark", height=280,
                           margin=dict(l=0,r=0,t=20,b=0),
                           yaxis=dict(title="Words"))
        st.plotly_chart(fig2, use_container_width=True)

    # ── Phase timeline ──
    st.markdown('<div class="section-hdr">🗺️ Developmental Phase Timeline</div>', unsafe_allow_html=True)
    phases = [
        dict(Phase="Phase 1 — Biology",      Start=0,     End=3200,  Color="#1e40af"),
        dict(Phase="Phase 2 — Sensorimotor", Start=3200,  End=6400,  Color="#065f46"),
        dict(Phase="Phase 3 — Core Cognition",Start=6400, End=12480, Color="#7c2d12"),
        dict(Phase="Phase 4 — Social Cog",   Start=12480, End=49920, Color="#581c87"),
        dict(Phase="Phase 5 — Cultural",     Start=49920, End=74880, Color="#713f12"),
        dict(Phase="Phase 6 — Identity",     Start=74880, End=96000, Color="#134e4a"),
        dict(Phase="Phase 7 — Wisdom",       Start=96000, End=160000,Color="#7f1d1d"),
    ]
    fig3 = go.Figure()
    for i, p in enumerate(phases):
        fig3.add_trace(go.Bar(
            x=[p['End']-p['Start']], y=[p['Phase']],
            base=[p['Start']], orientation='h',
            marker_color=p['Color'], name=p['Phase'],
            hovertemplate=f"{p['Phase']}<br>Tick {p['Start']:,}–{p['End']:,}<extra></extra>"
        ))
    fig3.add_vline(x=tick, line_color="#f87171", line_width=3,
                   annotation_text=f"Tick {tick:,}", annotation_position="top")
    fig3.update_layout(template="plotly_dark", height=280, showlegend=False,
                       barmode="overlay", margin=dict(l=0,r=0,t=20,b=0),
                       xaxis=dict(title="Tick"))
    st.plotly_chart(fig3, use_container_width=True)

    # ── Architecture completeness ──
    st.markdown('<div class="section-hdr">📊 Architecture Completeness (v1.0)</div>', unsafe_allow_html=True)
    domains = ["Biological body","Neural dynamics","Language & grounding","Cognitive architecture",
               "Energy & metabolism","Memory systems","Perception & vision","Motor intelligence",
               "Consciousness & self","Social & ToM","World & continuity","Temporal cognition"]
    scores  = [85,80,65,60,60,55,55,50,50,30,25,20]
    colors  = ["#4ade80" if s>=70 else "#facc15" if s>=50 else "#f87171" for s in scores]
    fig4 = go.Figure(go.Bar(x=scores, y=domains, orientation='h',
                             marker_color=colors,
                             text=[f"{s}%" for s in scores], textposition="outside"))
    fig4.update_layout(template="plotly_dark", height=380,
                       margin=dict(l=0,r=0,t=20,b=0),
                       xaxis=dict(range=[0,100], title="Completeness %"))
    st.plotly_chart(fig4, use_container_width=True)

    # ── Sheet index ──
    st.markdown('<div class="section-hdr">🗂️ All 36 Sheets</div>', unsafe_allow_html=True)
    sheet_cats = {
        "🏠 Master Dashboard":"Core","🧬 DNA Loop Engine":"Core","📈 Growth Timeline":"Core",
        "🧮 Mathematical Framework":"Core","⚙️ Parameters":"Core","📖 System Specification":"Core",
        "🧬 Prenatal & Genesis":"Biology","📐 Spatial Coordinates":"Biology","🫀 Body Systems":"Biology",
        "🔬 Subsystems":"Biology","⚡ Energy & Metabolism":"Biology","📏 Full Growth System":"Biology",
        "🧠 Mind & Cognition":"Cognition","🗣️ Language Grounding":"Phase 4","🧠 Theory of Mind":"Phase 4",
        "🔮 Predictive Simulation":"Phase 4","🗺️ Scene Graph & Places":"Phase 4",
        "👁️ Object Permanence":"Phase 3","🦴 Proprioception (P1)":"Phase 3",
        "💾 Episodic Memory (P3)":"Phase 3","🎯 Value System (P4)":"Phase 3","🦾 Motor Planning (P6)":"Phase 3",
        "🌍 World Systems":"World","🗺️ World Data":"World","📐 World & Space":"World",
        "🏥 Immersive Places":"World","👥 NPC Engine":"Social",
        "🔗 System Connections":"Meta","🔗 System Integration":"Meta",
        "🚀 v2.0 Architecture Audit":"Meta","⚙️ Runtime Patch v0.1":"Runtime",
        "🔄 Learning Loop":"Learning Loop",
        "✨ Creative Synthesis Engine":"Phase 7","🦉 Wisdom Index Engine":"Phase 7",
        "🎯 Career Specialisation Engine":"Phase 7","🌟 Legacy Projection Engine":"Phase 7",
    }
    cat_color = {"Core":"ph-core","Biology":"ph-bio","Cognition":"ph-cog","Phase 4":"ph-cog",
                 "Phase 3":"ph-p3","World":"ph-world","Social":"ph-world","Meta":"ph-meta",
                 "Runtime":"ph-meta","Learning Loop":"ph-loop","Phase 7":"ph-p7"}
    badges = ""
    for sheet, cat in sheet_cats.items():
        cls = cat_color.get(cat,"ph-core")
        badges += f'<span class="phase-badge {cls}">{sheet}</span>'
    st.markdown(badges, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: GROWTH TIMELINE
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "📈 Growth Timeline":
    st.title("📈 Growth Timeline")
    st.caption("292-row developmental lifecycle from conception to mature adult")

    col1, col2 = st.columns(2)
    ticks_r = list(range(0, 160001, 400))
    weeks_r  = [t/80 for t in ticks_r]

    with col1:
        st.subheader("Physical Development")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=weeks_r,
            y=[organism_state(t)['height'] for t in ticks_r],
            name="Height (cm)", line=dict(color="#60a5fa",width=2)))
        fig.add_trace(go.Scatter(x=weeks_r,
            y=[organism_state(t)['mass'] for t in ticks_r],
            name="Mass (kg)", line=dict(color="#4ade80",width=2), yaxis="y2"))
        fig.add_trace(go.Scatter(x=weeks_r,
            y=[organism_state(t)['hr'] for t in ticks_r],
            name="Heart Rate (bpm)", line=dict(color="#f87171",width=2), yaxis="y3"))
        fig.add_vline(x=state['week'], line_dash="dash", line_color="white")
        fig.update_layout(template="plotly_dark", height=350,
            yaxis=dict(title="Height cm"),
            yaxis2=dict(title="Mass kg", overlaying="y", side="right"),
            yaxis3=dict(title="HR bpm", overlaying="y", side="right", position=0.95),
            legend=dict(orientation="h", y=1.1), margin=dict(l=0,r=0,t=30,b=0))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Cognitive Development")
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=weeks_r,
            y=[organism_state(t)['vocab'] for t in ticks_r],
            name="Vocabulary", fill="tozeroy", line=dict(color="#c084fc",width=2)))
        fig2.add_trace(go.Scatter(x=weeks_r,
            y=[organism_state(t)['motor']*10000 for t in ticks_r],
            name="Motor Stage ×10k", line=dict(color="#fb923c",width=2,dash="dot")))
        fig2.add_trace(go.Scatter(x=weeks_r,
            y=[organism_state(t)['tom']*10000 for t in ticks_r],
            name="ToM Stage ×10k", line=dict(color="#22d3ee",width=2,dash="dot")))
        fig2.add_vline(x=state['week'], line_dash="dash", line_color="white")
        fig2.update_layout(template="plotly_dark", height=350,
            legend=dict(orientation="h", y=1.1), margin=dict(l=0,r=0,t=30,b=0))
        st.plotly_chart(fig2, use_container_width=True)

    # Lifecycle milestones table
    st.subheader("Key Lifecycle Milestones")
    milestones = [
        (0,0,"Embryo","Fertilisation / cell division begins"),
        (320,4,"Embryo","Neural plate formed"),
        (640,8,"Embryo","Heart chamber partition"),
        (960,12,"Fetal Early","Limb differentiation"),
        (1600,20,"Fetal Mid","Sensory organs activating"),
        (2240,28,"Fetal Late","Neural gain rising"),
        (2880,36,"Fetal Late","Reflex arcs active"),
        (3200,40,"Newborn","Birth — umbilical severed"),
        (4160,52,"Infant","Object permanence partial"),
        (6400,80,"Toddler","Crawling → standing"),
        (10000,125,"Toddler","Language accelerating"),
        (12480,156,"Child","Desire ToM onset"),
        (16640,208,"Child","Belief ToM onset"),
        (24960,312,"Pre-Adolescent","Second-order ToM onset"),
        (32000,400,"Pre-Adolescent","Skilled motor stage 5"),
        (49920,624,"Adolescent","Full ToM online"),
        (74880,936,"Young Adult","All adolescent systems 100%"),
        (80000,1000,"Adult","Strategic reasoning online"),
        (96000,1200,"Mature Adult","Phase 7 ACTIVATES — Wisdom Engine"),
        (160000,2000,"Mature Adult","W(t)=0.95 — Legacy curve L(t)=0.94"),
    ]
    df_m = pd.DataFrame(milestones, columns=["Tick","Week","Stage","Milestone"])
    df_m["Current"] = df_m["Tick"].apply(lambda t: "✅" if t <= tick else "⏳")
    st.dataframe(df_m, use_container_width=True, hide_index=True,
                 column_config={"Current": st.column_config.TextColumn("Status", width="small")})

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: BIOLOGY
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🧬 Biology":
    st.title("🧬 Biology — Body Systems & Growth")

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🫀 Body Systems", "🧬 Prenatal & Genesis",
        "⚡ Energy & Metabolism", "📏 Full Growth System", "🔬 Subsystems"
    ])

    with tab1:
        st.subheader("🫀 Body Systems")
        df = sheet_to_df("🫀 Body Systems")
        st.dataframe(df, use_container_width=True, hide_index=True)

    with tab2:
        st.subheader("🧬 Prenatal & Genesis")
        df = sheet_to_df("🧬 Prenatal & Genesis")
        st.dataframe(df, use_container_width=True, hide_index=True)

    with tab3:
        st.subheader("⚡ Energy & Metabolism")
        df = sheet_to_df("⚡ Energy & Metabolism")
        st.dataframe(df, use_container_width=True, hide_index=True)

        # ATP gauge
        atp = min(1.103, 0.5 + tick/200000)
        fig = go.Figure(go.Indicator(
            mode="gauge+number", value=atp,
            title={"text": "ATP Level"},
            gauge={"axis":{"range":[0,1.5]},
                   "bar":{"color":"#4ade80"},
                   "steps":[{"range":[0,0.5],"color":"#7f1d1d"},
                             {"range":[0.5,1.0],"color":"#713f12"},
                             {"range":[1.0,1.5],"color":"#14532d"}]}))
        fig.update_layout(template="plotly_dark", height=250)
        st.plotly_chart(fig, use_container_width=True)

    with tab4:
        st.subheader("📏 Full Growth System")
        df = sheet_to_df("📏 Full Growth System")
        st.dataframe(df, use_container_width=True, hide_index=True)

    with tab5:
        st.subheader("🔬 Subsystems")
        df = sheet_to_df("🔬 Subsystems")
        st.dataframe(df, use_container_width=True, hide_index=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: COGNITION & PHASE 4
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🧠 Cognition & Phase 4":
    st.title("🧠 Cognition & Phase 4 — Social Cognitive Engines")

    tab1,tab2,tab3,tab4,tab5,tab6,tab7 = st.tabs([
        "🧠 Mind & Cognition","🗣️ Language Grounding",
        "🧠 Theory of Mind","🔮 Predictive Simulation",
        "🗺️ Scene Graph","👁️ Object Permanence","💾 Episodic Memory"
    ])

    with tab1:
        st.subheader("🧠 Mind & Cognition")
        # Cognitive metrics live
        col1,col2,col3,col4 = st.columns(4)
        col1.metric("Vocabulary", f"{state['vocab']:,} words")
        col2.metric("Consciousness C", state['C'])
        col3.metric("Prediction Error", state['pred_err'])
        col4.metric("LTM Events", f"{state['ltm']:,}")
        df = sheet_to_df("🧠 Mind & Cognition")
        st.dataframe(df, use_container_width=True, hide_index=True)

    with tab2:
        st.subheader("🗣️ Language Grounding")
        st.info("G(word) = Σ_m w_m·f_m(percept) — Multimodal word-percept-action binding")
        # Vocab logistic curve
        weeks_r = list(range(0, 1300, 10))
        vocabs  = [round(50000/(1+math.exp(-0.05*(w-156)))) for w in weeks_r]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=weeks_r, y=vocabs, fill="tozeroy",
                                  line=dict(color="#c084fc",width=2), name="Vocabulary V(t)"))
        fig.add_vline(x=state['week'], line_dash="dash", line_color="#f87171",
                      annotation_text=f"Wk {state['week']}: {state['vocab']:,} words")
        fig.update_layout(template="plotly_dark", height=250,
                          xaxis_title="Week", yaxis_title="Words",
                          margin=dict(l=0,r=0,t=20,b=0))
        st.plotly_chart(fig, use_container_width=True)
        df = sheet_to_df("🗣️ Language Grounding")
        st.dataframe(df, use_container_width=True, hide_index=True)

    with tab3:
        st.subheader("🧠 Theory of Mind")
        # ToM stage gauge
        tom_stages = {1:"Proto-ToM (Wk 40–156)",2:"Desire inference (Wk 156–208)",
                      3:"False belief (Wk 208–312)",4:"Second-order (Wk 312–624)",
                      5:"Full social cognition (Wk 624+)"}
        st.success(f"**Current ToM Stage: {state['tom']} — {tom_stages[state['tom']]}**")
        fig = go.Figure(go.Indicator(
            mode="gauge+number", value=state['tom'],
            title={"text":"ToM Stage"},
            gauge={"axis":{"range":[0,5],"tickvals":[1,2,3,4,5]},
                   "bar":{"color":"#22d3ee"},
                   "steps":[{"range":[0,2],"color":"#1e3a5f"},
                             {"range":[2,4],"color":"#1a3a3a"},
                             {"range":[4,5],"color":"#134e4a"}]}))
        fig.update_layout(template="plotly_dark", height=250)
        st.plotly_chart(fig, use_container_width=True)
        df = sheet_to_df("🧠 Theory of Mind")
        st.dataframe(df, use_container_width=True, hide_index=True)

    with tab4:
        st.subheader("🔮 Predictive Simulation")
        st.info("F = Σ[εᵀ·Π·ε + log|Σ|] — Free energy minimisation")
        # Prediction error decay
        ticks_r = list(range(0, 160001, 800))
        errors  = [max(0.1, math.exp(-0.0001*t)) for t in ticks_r]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=ticks_r, y=errors, fill="tozeroy",
                                  line=dict(color="#f87171",width=2), name="Prediction Error"))
        fig.add_vline(x=tick, line_dash="dash", line_color="white")
        fig.update_layout(template="plotly_dark", height=250,
                          xaxis_title="Tick", yaxis_title="Error",
                          margin=dict(l=0,r=0,t=20,b=0))
        st.plotly_chart(fig, use_container_width=True)
        df = sheet_to_df("🔮 Predictive Simulation")
        st.dataframe(df, use_container_width=True, hide_index=True)

    with tab5:
        st.subheader("🗺️ Scene Graph & Places")
        # Place nodes map
        places = [
            ("Hospital (Birth)",0,0,"🏥"),("A7DO Home H8",1090,880,"🏠"),
            ("H1 — Alexis & Evelyn",1050,900,"🏡"),("H7 — James & Olivia",1100,870,"🏡"),
            ("BeenFore City",1000,1000,"🌆"),("BeenFore Lane",1090,860,"🛣️"),
        ]
        fig = go.Figure()
        for name,x,y,icon in places:
            fig.add_trace(go.Scatter(x=[x],y=[y],mode="markers+text",
                name=name, text=[f"{icon} {name}"], textposition="top center",
                marker=dict(size=14, color="#60a5fa")))
        fig.add_trace(go.Scatter(x=[1090],y=[880],mode="markers",
            name="A7DO (current)", marker=dict(size=20,color="#f87171",symbol="star")))
        fig.update_layout(template="plotly_dark", height=350,
                          xaxis_title="World X (m)", yaxis_title="World Y (m)",
                          showlegend=False, margin=dict(l=0,r=0,t=20,b=0))
        st.plotly_chart(fig, use_container_width=True)
        df = sheet_to_df("🗺️ Scene Graph & Places")
        st.dataframe(df, use_container_width=True, hide_index=True)

    with tab6:
        st.subheader("👁️ Object Permanence")
        st.metric("Current Stage", f"{state['perm']} / 3")
        df = sheet_to_df("👁️ Object Permanence")
        st.dataframe(df, use_container_width=True, hide_index=True)

    with tab7:
        st.subheader("💾 Episodic Memory")
        st.metric("LTM Events", f"{state['ltm']:,}")
        # Memory accumulation
        ticks_r = list(range(0, 160001, 800))
        ltms = [min(int(t*0.96), 200000) for t in ticks_r]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=ticks_r, y=ltms, fill="tozeroy",
                                  line=dict(color="#fb923c",width=2), name="LTM Events"))
        fig.add_vline(x=tick, line_dash="dash", line_color="white")
        fig.update_layout(template="plotly_dark", height=250,
                          xaxis_title="Tick", yaxis_title="Events",
                          margin=dict(l=0,r=0,t=20,b=0))
        st.plotly_chart(fig, use_container_width=True)
        df = sheet_to_df("💾 Episodic Memory (P3)")
        st.dataframe(df, use_container_width=True, hide_index=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: LEARNING LOOP
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🔄 Learning Loop":
    st.title("🔄 Learning Loop — Experience-First Architecture")
    st.caption("A7DO learns ONLY through interaction → repetition → sleep consolidation")

    # Current phase highlight
    phase_colors = {
        "👁️ Exposure":"#1e3a5f","🤝 Interaction":"#065f46",
        "🔁 Repetition":"#581c87","💤 Sleep Consolidation":"#1a1a2e"
    }
    col1,col2,col3,col4 = st.columns(4)
    for col, (ph, color) in zip([col1,col2,col3,col4], phase_colors.items()):
        active = ph == state['ll_phase']
        border = "3px solid #f87171" if active else "1px solid #374151"
        col.markdown(f"""<div style="background:{color};border:{border};border-radius:12px;
            padding:16px;text-align:center;">
            <div style="font-size:1.5rem">{ph.split()[0]}</div>
            <div style="font-weight:700;color:{'#f87171' if active else '#e2e8f0'}">{ph}</div>
            <div style="font-size:0.75rem;color:#9ca3af">{'← ACTIVE NOW' if active else ''}</div>
        </div>""", unsafe_allow_html=True)

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("4-Stage Cycle")
        stages_data = {
            "Stage": ["1 — Exposure","2 — Interaction","3 — Repetition","4 — Sleep Consolidation"],
            "Fires Every": ["Every tick","Every 5 ticks","Every 10 ticks","Every 800 ticks"],
            "Key Engines": [
                "EQ_SENS_06 · EQ_EMOT_07 · EQ_ATTN_09",
                "EQ_PRED_08 · Motor Planning · Value TD(λ)",
                "EQ_LANG_12 · G(word) · Scene Graph · ToM",
                "Episodic Memory · EQ_PRED_08 dream replay"
            ],
            "Output": [
                "Sensory vector · attention · emotional delta",
                "Reinforcement · motor update · error reduction",
                "Word-object bindings · concept formation",
                "Stable knowledge · grounded language · pruned LTM"
            ]
        }
        st.dataframe(pd.DataFrame(stages_data), use_container_width=True, hide_index=True)

    with col2:
        st.subheader("Word Learning Pipeline")
        word_steps = {
            "Step": ["1 Exposure","2 Attention","3 Prediction","4 Emotion",
                     "5 Episodic","6 Repetition","7 Sleep","8 Grounded"],
            "Process": [
                "Hears 'ball' while seeing round red object",
                "Attention spikes on novel object",
                "Prediction error spikes on unexpected outcome",
                "Emotional valence tags the event",
                "Event stored in episodic memory",
                "Multiple exposures strengthen binding",
                "Dream replay binds word→percept→motor→emotion",
                "Stable word-object binding emerges"
            ],
            "Engine": ["EQ_SENS_06","EQ_ATTN_09","EQ_PRED_08","EQ_EMOT_07",
                       "Episodic Mem","EQ_LANG_12","EQ_PRED_08","G(word)"],
            "Status": ["✅","✅","✅","✅","✅","🟡","✅","🟡"]
        }
        st.dataframe(pd.DataFrame(word_steps), use_container_width=True, hide_index=True)

    st.subheader("Concept Formation Types")
    concepts = {
        "Type": ["Object category","Action schema","Spatial relation","Social concept","Abstract concept","Self-concept"],
        "Example": ["'ball' = round+rolls+graspable","'eat' = mouth+food+satisfaction",
                    "'in' = object inside container","'friend' = NPC+positive bond",
                    "'justice' = fair+consistent+norm","'I' = self-model in consciousness"],
        "Onset Week": ["80–156","80–156","260–624","156–260","624+","624+"],
        "Required Systems": [
            "Object Permanence + Language + Scene Graph",
            "Motor Planning + Value System + Language",
            "Scene Graph + Language Grounding",
            "ToM + NPC Engine + Episodic Memory",
            "Language + ToM + Consciousness Loop",
            "Consciousness Loop + Episodic + Value System"
        ]
    }
    st.dataframe(pd.DataFrame(concepts), use_container_width=True, hide_index=True)

    st.subheader("Identity Emergence Components")
    identity = {
        "Component": ["Episodic self-history","Stable prediction patterns","Emotional history",
                      "Social bonds","Value system","Self-model","Skill identity","Wisdom & legacy"],
        "Source": ["Episodic Memory","Predictive Simulation","Emotion & Reinforcement",
                   "NPC Engine + ToM","Value System (P4)","Consciousness Loop",
                   "Motor Planning + Language","Phase 7 engines"],
        "Status": [f"✅ {state['ltm']:,} events",f"✅ Error={state['pred_err']}",
                   "✅ H(t) active",f"✅ Lorraine=0.95","✅ V(s)=1.0",
                   f"✅ C={state['C']}","🟡 Motor stage "+str(state['motor']),
                   "⏳ Wk 1200+" if not state['phase7'] else "✅ Active"]
    }
    st.dataframe(pd.DataFrame(identity), use_container_width=True, hide_index=True)

    st.subheader("Full Learning Loop Sheet")
    df = sheet_to_df("🔄 Learning Loop")
    st.dataframe(df, use_container_width=True, hide_index=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: WORLD & SOCIAL
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🌍 World & Social":
    st.title("🌍 World & Social — BeenFore City")

    tab1,tab2,tab3,tab4 = st.tabs(["🌍 World Systems","👥 NPC Engine","🗺️ World Data","🏥 Immersive Places"])

    with tab1:
        st.subheader("🌍 World Systems")
        # World map
        fig = go.Figure()
        locs = [
            ("Hospital",0,0,"#f87171"),("H8 Home",1090,880,"#4ade80"),
            ("H1",1050,900,"#60a5fa"),("H7",1100,870,"#60a5fa"),
            ("BeenFore City",1000,1000,"#facc15"),
        ]
        for name,x,y,color in locs:
            fig.add_trace(go.Scatter(x=[x],y=[y],mode="markers+text",
                text=[name],textposition="top center",
                marker=dict(size=16,color=color),name=name))
        fig.update_layout(template="plotly_dark",height=350,
                          xaxis_title="World X (m)",yaxis_title="World Y (m)",
                          margin=dict(l=0,r=0,t=20,b=0))
        st.plotly_chart(fig, use_container_width=True)
        df = sheet_to_df("🌍 World Systems")
        st.dataframe(df, use_container_width=True, hide_index=True)

    with tab2:
        st.subheader("👥 NPC Engine")
        npcs = [
            ("Lorraine","Primary caregiver",0.95,"Nurturing","✅"),
            ("Alexis","Secondary family",0.70,"Warm","✅"),
            ("Evelyn","Secondary family",0.65,"Playful","✅"),
            ("James","Neighbour",0.30,"Neutral","✅"),
        ]
        df_npc = pd.DataFrame(npcs, columns=["Name","Role","Bond Strength","Emotion","Status"])
        st.dataframe(df_npc, use_container_width=True, hide_index=True)
        # Bond strength chart
        fig = go.Figure(go.Bar(
            x=[n[0] for n in npcs], y=[n[2] for n in npcs],
            marker_color=["#4ade80","#60a5fa","#c084fc","#9ca3af"],
            text=[f"{n[2]}" for n in npcs], textposition="outside"
        ))
        fig.update_layout(template="plotly_dark", height=250,
                          yaxis=dict(range=[0,1.1],title="Bond Strength"),
                          margin=dict(l=0,r=0,t=20,b=0))
        st.plotly_chart(fig, use_container_width=True)
        df = sheet_to_df("👥 NPC Engine")
        st.dataframe(df, use_container_width=True, hide_index=True)

    with tab3:
        st.subheader("🗺️ World Data")
        df = sheet_to_df("🗺️ World Data")
        st.dataframe(df, use_container_width=True, hide_index=True)

    with tab4:
        st.subheader("🏥 Immersive Places")
        df = sheet_to_df("🏥 Immersive Places")
        st.dataframe(df, use_container_width=True, hide_index=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: ENGINES & RUNTIME
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "⚙️ Engines & Runtime":
    st.title("⚙️ Engines & Runtime — 20 Engine Architecture")

    tab1,tab2,tab3,tab4,tab5 = st.tabs([
        "🔗 System Connections","🔗 System Integration",
        "⚙️ Parameters","⚙️ Runtime Patch","🚀 Architecture Audit"
    ])

    with tab1:
        st.subheader("🔗 System Connections — 24-Engine Matrix")
        engines = [
            ("EQ_DNA_01","DNA Loop Engine","1 tick","Core","✅"),
            ("EQ_ANAT_02","Anatomy Growth","100 ticks","Core","✅"),
            ("EQ_NEUR_03","Neural Control","10 ticks","Core","✅"),
            ("EQ_CIRC_04","Circulatory","1 tick","Core","✅"),
            ("EQ_DIGE_05","Digestive & Energy","50 ticks","Core","✅"),
            ("EQ_SENS_06","Sensory Integration","1 tick","Core","✅"),
            ("EQ_EMOT_07","Emotion & Reinforcement","20 ticks","Core","✅"),
            ("EQ_PRED_08","Predictive Simulation","5 ticks","Core","✅"),
            ("EQ_ATTN_09","Attention Control","1 tick","Core","✅"),
            ("EQ_CONS_10","Consciousness Loop","100 ticks","Core","✅"),
            ("EQ_WRLD_11","World & NPC","50 ticks","Core","✅"),
            ("EQ_LANG_12","Language Acquisition","10 ticks","Core","✅"),
            ("Reflex ODE","Proprioception","1 tick","Phase 3","✅"),
            ("TD(λ)","Value / Motivation","5 ticks","Phase 3","✅"),
            ("Persistence ODE","Object Permanence","20 ticks","Phase 3","✅"),
            ("Power-law","Episodic Memory","10/100/800 ticks","Phase 3","✅"),
            ("G(word)","Language Grounding","10 ticks","Phase 4","🟡"),
            ("ToM_i(j)","Theory of Mind","200 ticks","Phase 4","🟡"),
            ("F=Σ[εᵀΠε]","Predictive Sim Full","5 ticks","Phase 4","🟡"),
            ("G={N,E}","Scene Graph","20 ticks","Phase 4","🟡"),
            ("EQ_CREAT_17","Creative Synthesis","500 ticks","Phase 7","⏳" if not state['phase7'] else "✅"),
            ("EQ_WISDOM_18","Wisdom Index","500 ticks","Phase 7","⏳" if not state['phase7'] else "✅"),
            ("EQ_CAREER_19","Career Specialisation","1000 ticks","Phase 7","⏳" if not state['phase7'] else "✅"),
            ("EQ_LEGACY_20","Legacy Projection","2000 ticks","Phase 7","⏳" if not state['phase7'] else "✅"),
        ]
        df_eng = pd.DataFrame(engines, columns=["Code","Engine","Fires Every","Phase","Status"])
        st.dataframe(df_eng, use_container_width=True, hide_index=True)

        # Engine fire frequency chart
        freq_map = {"1 tick":1,"5 ticks":5,"10 ticks":10,"20 ticks":20,"50 ticks":50,
                    "100 ticks":100,"200 ticks":200,"500 ticks":500,"1000 ticks":1000,
                    "2000 ticks":2000,"10/100/800 ticks":100}
        freqs = [freq_map.get(e[2],1) for e in engines]
        fig = go.Figure(go.Bar(
            x=[e[1] for e in engines], y=freqs,
            marker_color=["#4ade80" if e[3]=="Core" else "#60a5fa" if "Phase 3" in e[3]
                          else "#c084fc" if "Phase 4" in e[3] else "#f87171" for e in engines],
            text=freqs, textposition="outside"
        ))
        fig.update_layout(template="plotly_dark", height=300,
                          yaxis=dict(title="Ticks between fires", type="log"),
                          xaxis=dict(tickangle=45),
                          margin=dict(l=0,r=0,t=20,b=100))
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader("🔗 System Integration")
        df = sheet_to_df("🔗 System Integration")
        st.dataframe(df, use_container_width=True, hide_index=True)

    with tab3:
        st.subheader("⚙️ Parameters — 41 Biological Constants")
        df = sheet_to_df("⚙️ Parameters")
        st.dataframe(df, use_container_width=True, hide_index=True)

    with tab4:
        st.subheader("⚙️ Runtime Patch v0.1")
        df = sheet_to_df("⚙️ Runtime Patch v0.1")
        st.dataframe(df, use_container_width=True, hide_index=True)

    with tab5:
        st.subheader("🚀 v2.0 Architecture Audit")
        df = sheet_to_df("🚀 v2.0 Architecture Audit")
        st.dataframe(df, use_container_width=True, hide_index=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: PHASE 7 — WISDOM
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "✨ Phase 7 — Wisdom":
    st.title("✨ Phase 7 — Creative Synthesis & Wisdom Engine")

    if not state['phase7']:
        weeks_left = 1200 - state['week']
        ticks_left = 96000 - tick
        st.warning(f"⏳ Phase 7 activates at Tick 96,000 (Week 1,200). "
                   f"Currently {ticks_left:,} ticks ({weeks_left} weeks) away. "
                   f"Drag the tick slider to 96,000+ to activate.")
    else:
        st.success("🌟 PHASE 7 ACTIVE — All 4 wisdom engines online")

    # Wisdom index trajectory
    st.subheader("🦉 Wisdom Index W(t) Trajectory")
    weeks_r = list(range(1200, 2100, 10))
    wisdoms = [min(0.1+((w-1200)/800)*0.9, 1.0) for w in weeks_r]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=weeks_r, y=wisdoms, fill="tozeroy",
                              line=dict(color="#f87171",width=3), name="W(t)"))
    if state['week'] >= 1200:
        fig.add_vline(x=state['week'], line_dash="dash", line_color="white",
                      annotation_text=f"W={state['wisdom']}")
    fig.update_layout(template="plotly_dark", height=280,
                      xaxis_title="Week", yaxis_title="Wisdom W(t)",
                      yaxis=dict(range=[0,1.1]), margin=dict(l=0,r=0,t=20,b=0))
    st.plotly_chart(fig, use_container_width=True)

    tab1,tab2,tab3,tab4 = st.tabs([
        "✨ Creative Synthesis","🦉 Wisdom Index",
        "🎯 Career Specialisation","🌟 Legacy Projection"
    ])

    with tab1:
        st.subheader("✨ EQ_CREAT_17 — Creative Synthesis Engine")
        st.code("C_new(t) = α_c·(M_episodic ⊕ M_semantic) + β_c·(P_sim ⊗ S_skills) + γ_c·Noise_stochastic",
                language="text")
        col1,col2,col3 = st.columns(3)
        col1.metric("α_c (memory blend)", "0.4")
        col2.metric("β_c (skill-prediction)", "0.4")
        col3.metric("γ_c (stochastic noise)", "0.2")
        # Idea candidate table
        ideas = [
            ("IDEA_001","Novel tool use combining reach + object permanence",0.82,0.74,0.91,1),
            ("IDEA_002","Social strategy: delay gratification for NPC reward",0.76,0.68,0.88,2),
            ("IDEA_003","Spatial shortcut via scene graph recombination",0.71,0.85,0.79,3),
            ("IDEA_004","Emotional regulation via predictive reframing",0.65,0.72,0.95,4),
            ("IDEA_005","Language metaphor: abstract concept from concrete",0.88,0.55,0.83,5),
        ]
        df_ideas = pd.DataFrame(ideas, columns=["ID","Description","Novelty","Feasibility","Cultural Align","Rank"])
        st.dataframe(df_ideas, use_container_width=True, hide_index=True)
        df = sheet_to_df("✨ Creative Synthesis Engine")
        st.dataframe(df, use_container_width=True, hide_index=True)

    with tab2:
        st.subheader("🦉 EQ_WISDOM_18 — Wisdom Index Engine")
        st.code("W(t+1) = W(t) + η_w·[λ1·Consequence_50yr + λ2·EthicalWeight + λ3·EmpathyIndex − λ4·ImpulseDrive]",
                language="text")
        # Decision modulation
        w = state['wisdom']
        decision_data = {
            "Decision Type": ["Goal selection","Emotional regulation","Social decisions","Creative filtering","Career choices"],
            "Current Behaviour": [
                "Long-term consequence dominant" if w>0.6 else ("Balanced" if w>0.3 else "Short-term reward"),
                "Fully regulated, compassionate" if w>0.6 else ("Partially regulated" if w>0.3 else "Reactive, impulsive"),
                "Altruistic, legacy-aware" if w>0.6 else ("Reciprocal fairness" if w>0.3 else "Self-interest dominant"),
                "Ethics + consequence filtered" if w>0.6 else ("Feasibility-filtered" if w>0.3 else "All ideas pursued"),
                "Legacy-aligned specialisation" if w>0.6 else ("Skill-opportunity match" if w>0.3 else "Immediate reward"),
            ]
        }
        st.dataframe(pd.DataFrame(decision_data), use_container_width=True, hide_index=True)
        df = sheet_to_df("🦉 Wisdom Index Engine")
        st.dataframe(df, use_container_width=True, hide_index=True)

    with tab3:
        st.subheader("🎯 EQ_CAREER_19 — Career Specialisation Engine")
        st.code("Career(t+1) = Career(t) + η_car·[SkillVector · OpportunityMatrix · IdentityVector]",
                language="text")
        # 22-dim skill radar
        skills = ["Language","Logic","Spatial","Social ToM","Emotion Reg","Motor",
                  "Creative","Ethical","Long-term Plan","Memory","Pattern","Causal",
                  "Numerical","Narrative","Attention","Sensory","Predictive","Cultural",
                  "Self-Reg","Curiosity","Empathy","Legacy"]
        current = [0.72,0.68,0.81,0.65,0.59,0.88,0.45,0.52,0.41,0.77,0.74,0.63,
                   0.55,0.69,0.71,0.84,0.48,0.61,0.57,0.79,0.66,0.38]
        target  = [0.95,0.90,0.85,0.95,0.90,0.90,0.85,0.90,0.88,0.85,0.88,0.90,
                   0.85,0.88,0.90,0.88,0.90,0.88,0.92,0.85,0.95,0.90]
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(r=current+[current[0]], theta=skills+[skills[0]],
            fill="toself", name="Current Mastery", line_color="#60a5fa"))
        fig.add_trace(go.Scatterpolar(r=target+[target[0]], theta=skills+[skills[0]],
            fill="toself", name="Target", line_color="#4ade80", opacity=0.3))
        fig.update_layout(template="plotly_dark", height=400,
                          polar=dict(radialaxis=dict(range=[0,1])),
                          margin=dict(l=0,r=0,t=20,b=0))
        st.plotly_chart(fig, use_container_width=True)
        df = sheet_to_df("🎯 Career Specialisation Engine")
        st.dataframe(df, use_container_width=True, hide_index=True)

    with tab4:
        st.subheader("🌟 EQ_LEGACY_20 — Legacy Projection Engine")
        st.code("L(t+1) = L(t) + η_l·[Impact_direct + Impact_indirect + CulturalTransmission − Entropy_f·L(t)]",
                language="text")
        # Legacy curve
        weeks_r = [1200,1300,1400,1600,1800,2000,2400,3000]
        legacy  = [0.0,0.08,0.19,0.41,0.67,0.94,1.52,2.31]
        rememb  = [0.01,0.05,0.12,0.28,0.45,0.61,0.78,0.89]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=weeks_r, y=legacy, name="Legacy L(t)",
                                  fill="tozeroy", line=dict(color="#facc15",width=2)))
        fig.add_trace(go.Scatter(x=weeks_r, y=rememb, name="Remembrance Prob",
                                  line=dict(color="#c084fc",width=2,dash="dot"), yaxis="y2"))
        fig.update_layout(template="plotly_dark", height=280,
                          xaxis_title="Week", yaxis=dict(title="L(t)"),
                          yaxis2=dict(title="Remembrance", overlaying="y", side="right"),
                          legend=dict(orientation="h",y=1.1),
                          margin=dict(l=0,r=0,t=20,b=0))
        st.plotly_chart(fig, use_container_width=True)
        df = sheet_to_df("🌟 Legacy Projection Engine")
        st.dataframe(df, use_container_width=True, hide_index=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: ALL SHEETS EXPLORER
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "📊 All Sheets Explorer":
    st.title("📊 All Sheets Explorer")
    st.caption("Browse all 36 sheets from A7DO_DNA_Master_v5_FINAL.xlsx")

    wb = load_workbook()
    sheet_names = wb.sheetnames

    selected = st.selectbox("Select sheet", sheet_names)
    df = sheet_to_df(selected)

    col1,col2,col3 = st.columns(3)
    col1.metric("Rows", len(df))
    col2.metric("Columns", len(df.columns))
    col3.metric("Non-empty cells", df.notna().sum().sum())

    search = st.text_input("🔍 Search within sheet", "")
    if search:
        mask = df.apply(lambda col: col.astype(str).str.contains(search, case=False, na=False))
        df = df[mask.any(axis=1)]
        st.caption(f"{len(df)} rows matching '{search}'")

    st.dataframe(df, use_container_width=True, hide_index=True)

    # Download
    csv = df.to_csv(index=False)
    st.download_button(f"⬇️ Download {selected} as CSV",
                       data=csv, file_name=f"{selected}.csv", mime="text/csv")

# ── Footer ────────────────────────────────────────────────────────────────────
st.divider()
st.markdown(
    "<div style='text-align:center;color:#6b7280;font-size:0.8rem'>"
    "🧬 A7DO Genesis Mind · v5 FINAL · 36 sheets · 337 formulas · 0 errors · "
    "28 May 2026 · <em>This is the organism. There will be no more originals — only descendants.</em>"
    "</div>",
    unsafe_allow_html=True
)