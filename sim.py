"""
sim.py
Sandy’s Law Simulator
NONLINEAR entropy release (critical upgrade)

This models:
- shock breakout
- decoherence cascades
- phase transitions
- runaway escape once channels open
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
        Time-evolve a trapped system with NONLINEAR entropy release
        """

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

            # -------------------------
            # Trap softening (gradual)
            # -------------------------
            if soften_Z:
                Z = max(0.0, Z0 * (1.0 - 0.7 * time[i]))
            else:
                Z = Z0

            # -----------------------------------
            # NONLINEAR entropy escape (CRITICAL)
            # -----------------------------------
            # Cubic activation once entropy channels open
            # This creates runaway behavior near portal
            Sigma = Sigma0 * (1.0 + 4.0 * (h / max(entropy_end, 1e-6)) ** 3)

            # System state
            state = SystemState(
                Z=Z,
                Sigma=Sigma,
                entropy_grad=h,
            )

            out = self.engine.evaluate(state)

            # -------------------------
            # GR proper time (weak-field proxy)
            # -------------------------
            phi = -0.1 * Z
            tau_gr = np.sqrt(max(0.0, 1.0 + 2.0 * phi))

            # -------------------------
            # Log everything
            # -------------------------
            log["time"].append(time[i])
            log["Z"].append(Z)
            log["Sigma"].append(Sigma)
            log["entropy_grad"].append(h)
            log["portal_score"].append(out.portal_score)
            log["tau_rate"].append(out.tau_rate)
            log["gamma"].append(out.gamma_eff)
            log["tau_gr"].append(tau_gr)
            log["regime"].append(out.regime)

        return log


# -------------------------
# Standalone sanity test
# -------------------------
if __name__ == "__main__":
    engine = SandysLawEngine()
    sim = SandysLawSimulator(engine)

    data = sim.run(
        Z0=0.98,
        Sigma0=0.05,
        entropy_start=0.0,
        entropy_end=5.0,
        steps=200,
    )

    print("Final portal score:", data["portal_score"][-1])
    print("Final regime:", data["regime"][-1])
