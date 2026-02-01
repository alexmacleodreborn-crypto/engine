"""
sim.py
Sandy's Law simulation harness
"""

import numpy as np
from engine import SandysLawEngine, SystemState


class SandysLawSimulator:
    def __init__(self, engine: SandysLawEngine):
        self.engine = engine

    def run(self,
            Z0: float,
            Sigma0: float,
            entropy_start: float,
            entropy_end: float,
            steps: int = 200,
            soften_Z: bool = True):
        """
        Time-evolve a trapped system
        """

        time = np.linspace(0, 1, steps)
        entropy = np.linspace(entropy_start, entropy_end, steps)

        Z = Z0
        Sigma = Sigma0

        log = {
            "time": [],
            "Z": [],
            "Sigma": [],
            "entropy_grad": [],
            "portal_score": [],
            "tau_rate": [],
            "gamma": [],
            "regime": [],
            "regime_code": []
        }

        for i, h in enumerate(entropy):

            # Optional trap softening
            if soften_Z:
                Z = max(0.0, Z0 * (1.0 - 0.7 * time[i]))

            state = SystemState(
                Z=Z,
                Sigma=Sigma,
                entropy_grad=h
            )

            out = self.engine.evaluate(state)

            log["time"].append(time[i])
            log["Z"].append(Z)
            log["Sigma"].append(Sigma)
            log["entropy_grad"].append(h)
            log["portal_score"].append(out.portal_score)
            log["tau_rate"].append(out.tau_rate)
            log["gamma"].append(out.gamma_eff)
            log["regime"].append(out.regime)
            log["regime_code"].append(out.regime_code)

        return log


# quick test
if __name__ == "__main__":
    engine = SandysLawEngine()
    sim = SandysLawSimulator(engine)

    data = sim.run(
        Z0=0.98,
        Sigma0=0.05,
        entropy_start=0.0,
        entropy_end=5.0
    )

    print("Simulation complete")
