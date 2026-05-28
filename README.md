# 🧬 A7DO Genesis Mind — Interactive Dashboard

## Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the app
```bash
streamlit run app.py
```

### 3. Open in browser
```
http://localhost:8501
```

---

## Requirements
- Python 3.9+
- The file `A7DO_DNA_Master_v5_FINAL.xlsx` must be at this relative path from where you run the app:
  ```
  excel_report/a7do-final/A7DO_DNA_Master_v5_FINAL.xlsx
  ```

## File structure
```
A7DO_App/
├── app.py                          ← Main Streamlit application
├── requirements.txt                ← Python dependencies
├── README.md                       ← This file
└── excel_report/
    └── a7do-final/
        └── A7DO_DNA_Master_v5_FINAL.xlsx  ← Master organism file
```

---

## Pages

| Page | Content |
|---|---|
| 🏠 Mission Control | Live tick slider · physical growth curves · phase timeline · architecture completeness |
| 📈 Growth Timeline | Full lifecycle milestones · height/mass/vocab/motor/ToM curves |
| 🧬 Biology | Body Systems · Prenatal & Genesis · Energy & Metabolism · Full Growth System · Subsystems |
| 🧠 Cognition & Phase 4 | Mind & Cognition · Language Grounding · Theory of Mind · Predictive Simulation · Scene Graph · Object Permanence · Episodic Memory |
| 🔄 Learning Loop | 4-stage cycle · word learning pipeline · concept formation · ToM emergence · identity components |
| 🌍 World & Social | World Systems · NPC Engine (bond strengths) · World Data · Immersive Places |
| ⚙️ Engines & Runtime | 24-engine matrix · Parameters · System Integration · Runtime Patch · Architecture Audit |
| ✨ Phase 7 — Wisdom | Creative Synthesis · Wisdom Index · Career Specialisation (22-dim radar) · Legacy Projection |
| 📊 All Sheets Explorer | Browse + search all 36 sheets · CSV download |

---

## Key features
- **Live tick slider** (0 → 160,000) — all formulas update in real time
- **Phase 7 activates** automatically when tick ≥ 96,000
- **Learning Loop phase** shown live (Exposure / Interaction / Repetition / Sleep)
- **All 36 sheets** browsable with search and CSV export
- **Dark theme** with colour-coded phase system