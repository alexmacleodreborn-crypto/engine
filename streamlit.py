"""
streamlit.py
Sandy’s Law – Live Simulation Dashboard
Includes NORMALIZED GR vs Sandy’s Law comparison
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

Z0 = st.sidebar.slider("Initial Trap Strength Z", 0.0, 1.0, 0.98, 0.01)
Sigma0 = st.sidebar.slider("Entropy Export Σ", 0.0, 5.0, 0.05, 0.01)
entropy_start = st.sidebar.slider("Entropy Gradient Start", 0.0, 5.0, 0.0, 0.1)
entropy_end = st.sidebar.slider("Entropy Gradient End", 0.0, 10.0, 5.0, 0.1)
steps = st.sidebar.slider("Simulation Steps", 50, 500, 200, 50)
soften_Z = st.sidebar.checkbox("Trap Softening Enabled", True)

# --------------------
# ENGINE + SIMULATION
# --------------------
engine = SandysLawEngine()
sim = SandysLawSimulator(engine)

d
