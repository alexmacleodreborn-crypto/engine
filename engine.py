"""
engine.py
Sandy’s Law Engine – Core Physics
"""

from dataclasses import dataclass


# =========================
# CONSTANTS (v1)
# =========================

ALPHA_R = 0.15
PORTAL_THRESHOLD = 1.51
PRE_TRANSITION = 1.45


# =========================
# DATA STRUCTURES
# =========================

@dataclass
class SystemState:
    Z: float                # Trap strength (0–1)
    Sigma: float            # Entropy export rate
    entropy_grad: float     # dH/dt


@dataclass
class EngineOutput:
    portal_score: float
    regime: str
    regime_code: int
    gamma_eff: float
    tau_rate: float
    flags: dict


# =========================
# ENGINE
# =========================

class SandysLawEngine:
    def __init__(self):
        self.portal_threshold = PORTAL_THRESHOLD

    # ---------------------
    # Time modulation
    # ---------------------
    def temporal_modulation(self, entropy_grad: float) -> float:
        return 1.0 + ALPHA_R * entropy_grad

    # ---------------------
    # Sandy time rate
    # ---------------------
    def effective_time_rate(self, Z: float, Sigma: float) -> float:
        return max(0.0, (1.0 - Z) * Sigma)

    # ---------------------
    # Portal score
    # ---------------------
    def portal_score(self, Z: float, Sigma: float, entropy_grad: float) -> float:
        return 1.0 + 0.15 * entropy_grad + 0.5 * (1.0 - Z) * Sigma

    # ---------------------
    # Regime classifier
    # ---------------------
    def classify_regime(self, K: float):
        if K < PRE_TRANSITION:
            return "Newtonian / Stable", 0
        elif K < self.portal_threshold:
            return "Transitional", 1
        else:
            return "Zeno / Modulated", 2

    # ---------------------
    # Evaluate system
    # ---------------------
    def evaluate(self, state: SystemState) -> EngineOutput:
        K = self.portal_score(state.Z, state.Sigma, state.entropy_grad)
        regime, code = self.classify_regime(K)
        gamma = self.temporal_modulation(state.entropy_grad)
        tau_rate = self.effective_time_rate(state.Z, state.Sigma)

        flags = {
            "fully_trapped": state.Z > 0.95,
            "silent_system": tau_rate < 1e-6,
            "portal_open": K >= self.portal_threshold,
        }

        return EngineOutput(
            portal_score=K,
            regime=regime,
            regime_code=code,
            gamma_eff=gamma,
            tau_rate=tau_rate,
            flags=flags,
        )
