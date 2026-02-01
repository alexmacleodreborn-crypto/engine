"""
sim.py
Sandy's Law simulation harness
Includes GR vs Sandy's Law proper time comparison
"""

import numpy as np
from engine import SandysLawEngine, SystemState


class SandysLawSimulator:
    def __init__(self, engine: SandysLawEngine):
        self.engine = engine

    def run(
        self,
        Z0: float,
        Sigma0: float,
        entropy_start: float,
        entropy_end: float,
        steps: int = 200,
        soften_Z: bool = True,
    ):
        """
        Time-evolve a trapped system
        """

        time = np.linspace(0.0, 1.0, steps)
        entropy = np.linspace(entropy_start, entropy_end, steps)

        Z = Z0
        Sigma = Sigma0

        log = {
            "time": [],
            "Z": [],
            "Sigma": [],
            "entropy_grad": [],
            "portal_scor_
