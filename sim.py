"""
sim.py
Sandy’s Law Simulator + GR comparison
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

        time = np.linspace(0.0, 1.0, steps)
        entropy = np.linspace(entropy_start, entropy_end, steps)

        log = {
            "time": [],
            "Z": [],
            "Sigma": [],
            "entropy_grad": [],
            "portal_score": [],
            "tau_rate": [],
            "gamma": [],
            "tau_gr": [],
            "regime": [],
        }

        for i, h in enumerate(entropy):

            Z = Z0 * (1.0 - 0.7 * time[i]) if soften_Z else Z0
            Z = max(0.0, Z)

            state = SystemState(Z=Z, Sigma=Sigma0, entropy_grad=h)
            out = self.engine.evaluate(state)

            # Weak-field GR proper time proxy
            phi = -0.1 * Z
            tau_gr = np.sqrt(max(0.0, 1.0 + 2.0 * phi))

            log["time"].append(time[i])
            log["Z"].append(Z)
            log["Sigma"].append(Sigma0)
            log["entropy_grad"].append(h)
            log["portal_score"].append(out.portal_score)
            log["tau_rate"].append(out.tau_rate)
            log["gamma"].append(out.gamma_eff)
            log["tau_gr"].append(tau_gr)
            log["regime"].append(out.regime)

        return log
