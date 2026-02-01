"""
streamlit.py
Sandy’s Law – Live Simulation Dashboard
"""

import streamlit as st
import pandas as pd

from engine import SandysLawEngine
from sim import SandysLawSimulator


# --------------------
# PAGE CONFIG
# --------------------
st.set_page_config(
    page_title="Sandy’s Law Engine",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------
# SIDEBAR
# --------------------
st.sidebar.title("Sandy’s Law Controls")

Z0 = st.sidebar.slider("Initial Trap Strength Z", 0.0, 1.0, 0.98, 0.01)
Sigma0 = st.sidebar.slider("Entropy Export Σ", 0.0, 5.0, 0.05, 0.01)
entropy_start = st.sidebar.slider("Entropy Gradient Start", 0.0, 5.0, 0.0, 0.1)
entropy_end = st.sidebar.slider("Entropy Gradient End", 0.0, 10.0, 5.0, 0.1)
steps = st.sidebar.slider("Simulation Steps", 50, 500, 200, 50)
soften_Z = st.sidebar.checkbox("Trap Softening Enabled", True)

# --------------------
# RUN SIM
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
# DISPLAY
# --------------------
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

# --------------------
# GR vs SANDY
# --------------------
st.subheader("Proper Time: GR vs Sandy’s Law")

compare = df.set_index("time")[["tau_gr", "tau_rate"]]
compare.columns = ["GR dτ/dt", "Sandy’s Law dτ/dt"]
st.line_chart(compare)

# --------------------
# FINAL STATE
# --------------------
final = df.iloc[-1]

st.subheader("Final Regime")
st.metric("Regime", final["regime"])
st.metric("Portal Score", f"{final['portal_score']:.3f}")

if final["portal_score"] >= engine.portal_threshold:
    st.success("Portal OPEN — system transitions")
else:
    st.warning("System remains trapped")

with st.expander("Raw data"):
    st.dataframe(df)
