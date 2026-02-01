"""
streamlit.py
Sandy’s Law – Live Simulation Dashboard

Includes:
- Nonlinear entropy dynamics (via sim.py)
- Normalized GR vs Sandy comparison
- Automatic portal-crossing marker
- Supernova Core Collapse preset
- Gravitational Wave Merger preset
"""

import streamlit as st
import pandas as pd

from engine import SandysLawEngine
from sim import SandysLawSimulator


# ====================
# PAGE CONFIG
# ====================
st.set_page_config(
    page_title="Sandy’s Law Engine",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    body {
        background-color: #0e1117;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ====================
# SIDEBAR – PRESETS
# ====================
st.sidebar.title("Sandy’s Law Controls")

st.sidebar.subheader("Presets")
preset = st.sidebar.selectbox(
    "Select system preset",
    [
        "Custom",
        "Supernova Core Collapse",
        "Gravitational Wave Merger",
    ],
)

# ====================
# SIDEBAR – PARAMETERS
# ====================
if preset == "Supernova Core Collapse":
    # --- SN CORE COLLAPSE ---
    Z0 = 0.995            # extreme confinement
    Sigma0 = 0.01         # neutrino trapping
    entropy_start = 0.0
    entropy_end = 6.0     # heating + bounce
    steps = 300
    soften_Z = True

    st.sidebar.markdown(
        """
        **Supernova Core Collapse preset active**

        • Near-total confinement  
        • Suppressed entropy escape  
        • Nonlinear neutrino release  
        • Shock revival via portal opening
        """
    )

elif preset == "Gravitational Wave Merger":
    # --- GW MERGER / RINGDOWN ---
    Z0 = 0.9995           # extreme spacetime trapping
    Sigma0 = 0.002        # almost no escape until ringdown
    entropy_start = 0.0
    entropy_end = 4.0     # brief, intense excitation
    steps = 200
    soften_Z = False     # trap does NOT soften during merger

    st.sidebar.markdown(
        """
        **Gravitational Wave Merger preset active**

        • Extreme spacetime trapping  
        • Brief portal opening at merger  
        • Ringdown as controlled energy release  
        • GR geometry + Sandy escape dynamics
        """
    )

else:
    # --- CUSTOM ---
    Z0 = st.sidebar.slider("Initial Trap Strength Z", 0.0, 1.0, 0.98, 0.01)
    Sigma0 = st.sidebar.slider("Entropy Export Σ", 0.0, 5.0, 0.05, 0.01)
    entropy_start = st.sidebar.slider("Entropy Gradient Start", 0.0, 5.0, 0.0, 0.1)
    entropy_end = st.sidebar.slider("Entropy Gradient End", 0.0, 10.0, 5.0, 0.1)
    steps = st.sidebar.slider("Simulation Steps", 50, 500, 200, 50)
    soften_Z = st.sidebar.checkbox("Trap Softening Enabled", True)

# ====================
# ENGINE + SIMULATION
# ====================
engine = SandysLawEngine()
sim = SandysLawSimulator(engine)

data = sim.run(
    Z0=Z0,
    Sigma0=Sigma0,
    entropy_start=entropy_start,
    entropy_end=entropy_end,
    steps=steps,
    soften_Z=soften_Z,
)

df = pd.DataFrame(data)

# ====================
# PORTAL CROSSING DETECTION
# ====================
portal_threshold = engine.portal_threshold

cross_idx = None
for i in range(len(df)):
    if df.loc[i, "portal_score"] >= portal_threshold:
        cross_idx = i
        break

portal_time = df.loc[cross_idx, "time"] if cross_idx is not None else None

# ====================
# MAIN DISPLAY
# ====================
st.title("Sandy’s Law Engine — Live Simulation")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Portal Score")
    st.line_chart(df.set_index("time")["portal_score"])

    st.subheader("Effective Time Rate (Sandy’s Law)")
    st.line_chart(df.set_index("time")["tau_rate"])

with col2:
    st.subheader("Trap Strength Z")
    st.line_chart(df.set_index("time")["Z"])

    st.subheader("Time Modulation γ")
    st.line_chart(df.set_index("time")["gamma"])

# ====================
# GR vs SANDY (NORMALIZED)
# ====================
st.subheader("Proper Time (Normalized): GR vs Sandy’s Law")

norm_df = df.copy()
norm_df["GR (normalized)"] = norm_df["tau_gr"] / norm_df["tau_gr"].max()
norm_df["Sandy (normalized)"] = (
    norm_df["tau_rate"] / max(norm_df["tau_rate"].max(), 1e-9)
)

st.line_chart(
    norm_df.set_index("time")[["GR (normalized)", "Sandy (normalized)"]]
)

if portal_time is not None:
    st.caption(f"🔴 Portal opens at t ≈ {portal_time:.3f}")

# ====================
# FINAL REGIME SUMMARY
# ====================
final = df.iloc[-1]

st.subheader("Final Regime")
st.metric("Regime", final["regime"])
st.metric("Portal Score", f"{final['portal_score']:.3f}")

if final["portal_score"] >= engine.portal_threshold:
    st.success("Portal OPEN — system transitions")
else:
    st.warning("System remains trapped")

# ====================
# RAW DATA
# ====================
with st.expander("Show raw data"):
    st.dataframe(df)
