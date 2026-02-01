"""
app.py
Sandy's Law Streamlit Dashboard
Full live simulation with GR vs Sandy's Law comparison
"""

import streamlit as st
import pandas as pd

from engine import SandysLawEngine
from sim import SandysLawSimulator


# --------------------
# PAGE CONFIG
# --------------------
st.set_page_config(
    page_title="Sandy's Law Engine",
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

# --------------------
# SIDEBAR CONTROLS
# --------------------
st.sidebar.title("Sandy’s Law Controls")

Z0 = st.sidebar.slider(
    "Initial Trap Strength Z", 0.0, 1.0, 0.98, 0.01
)

Sigma0 = st.sidebar.slider(
    "Entropy Export Σ", 0.0, 5.0, 0.05, 0.01
)

entropy_start = st.sidebar.slider(
    "Entropy Gradient Start", 0.0, 5.0, 0.0, 0.1
)

entropy_end = st.sidebar.slider(
    "Entropy Gradient End", 0.0, 10.0, 5.0, 0.1
)

steps = st.sidebar.slider(
    "Simulation Steps", 50, 500, 200, 50
)

soften_Z = st.sidebar.checkbox(
    "Trap Softening Enabled", value=True
)

# --------------------
# ENGINE + SIM
# --------------------
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

# --------------------
# MAIN DISPLAY
# --------------------
st.title("Sandy’s Law Engine — Live Simulation")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Portal Score")
    st.line_chart(
        df[["time", "portal_score"]].set_index("time")
    )

    st.subheader("Effective Time Rate (Sandy’s Law)")
    st.line_chart(
        df[["time", "tau_rate"]].set_index("time")
    )

with col2:
    st.subheader("Trap Strength Z")
    st.line_chart(
        df[["time", "Z"]].set_index("time")
    )

    st.subheader("Time Modulation γ")
    st.line_chart(
        df[["time", "gamma"]].set_index("time")
    )

# --------------------
# GR vs SANDY COMPARISON
# --------------------
st.subheader("Proper Time Comparison: GR vs Sandy’s Law")

compare_df = df[["time", "tau_rate", "tau_gr"]].set_index("time")
compare_df = compare_df.rename(
    columns={
        "tau_rate": "Sandy’s Law dτ/dt",
        "tau_gr": "GR dτ/dt",
    }
)

st.line_chart(compare_df)

# --------------------
# FINAL REGIME SUMMARY
# --------------------
st.subheader("Final Regime")

final_regime = df.iloc[-1]["regime"]
final_score = df.iloc[-1]["portal_score"]

st.metric("Regime", final_regime)
st.metric("Portal Score", f"{final_score:.3f}")

if final_score >= engine.portal_threshold:
    st.success("Portal OPEN — system transitions")
else:
    st.warning("System remains trapped")

# --------------------
# RAW DATA
# --------------------
with st.expander("Show raw data"):
    st.dataframe(df)
