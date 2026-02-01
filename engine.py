"""
Sandy's Law Engine (SLE)
Core physics layer — Day 1

Author: Alexander Ormiston MacLeod
Purpose: Universal constraint engine for trapped systems
"""

import numpy as np
from dataclasses import dataclass


# =========================
# CONSTANTS (LOCKED v1)
# =========================

ALPHA_R = 0.15        # Ricci / entropy coupling
BETA_W = 0.05         # Weyl stiffness (reserved)
KB_NORM = 1.0         # Normalized Boltzmann constant

PORTAL_THRESHOLD = 1.51
PRE_TRANSITION = 1.45


# =========================
# DATA STRUCTURES
# =========================

@dataclass
class SystemState:
    """
    Minimal state vector for any system
    """
    Z: float          # Trap strength (0=open, 1=fully trapped)
    Sigma: float      # Entropy export rate
    entropy_grad: float  # dH/dt
    R: float = 0.0    # Ricci scalar (optional)
    W2: float = 0.0   # Weyl^2 (optional)


@dataclass
class EngineOutput:
    portal_score: float
    regime: str
    regime_code: int
    gamma_eff: float
    tau_rate: float
    flags: dict


# =========================
# CORE ENGINE
# =========================

class SandysLawEngine:
    """
    Universal constraint engine
    """

    def __init__(self,
                 alpha: float = ALPHA_R,
                 portal_threshold: float = PORTAL_THRESHOLD):
        self.alpha = alpha
        self.portal_threshold = portal_threshold

    # ---------------------
    # Omnium potential
    # ---------------------
    def omnium_potential(self, phi: float,
                         A: float = 1.0,
                         B: float = 0.2,
                         k: float = 10.0) -> float:
        """
        Washboard + double-well Omnium potential
        """
        return A * (phi**2 - 1.0)**2 - B * np.cos(k * phi)

    # ---------------------
    # Time modulation
    # ---------------------
    def temporal_modulation(self, entropy_grad: float) -> float:
        """
        Gamma_Q = 1 + alpha * (dH / kB)
        """
        return 1.0 + self.alpha * (entropy_grad / KB_NORM)

    # ---------------------
    # Sandy's Law time rate
    # ---------------------
    def effective_time_rate(self, Z: float, Sigma: float) -> float:
        """
        dτ_SL / dt = (1 - Z) * Sigma
        """
        return max(0.0, (1.0 - Z) * Sigma)

    # ---------------------
    # Portal score
    # ---------------------
    def portal_score(self, Z: float, Sigma: float,
                     entropy_grad: float) -> float:
        """
        Minimal portal score functional
        (expandable later)
        """
        return 1.0 + 0.15 * entropy_grad + 0.5 * (1.0 - Z) * Sigma

    # ---------------------
    # Regime classifier
    # ---------------------
    def classify_regime(self, K: float):
        if K < PRE_TRANSITION:
            return "Newtonian / Stable", 0
        elif PRE_TRANSITION <= K < self.portal_threshold:
            return "Transitional", 1
        else:
            return "Zeno / Modulated", 2

    # ---------------------
    # Main evaluation
    # ---------------------
    def evaluate(self, state: SystemState) -> EngineOutput:

        K = self.portal_score(state.Z,
                              state.Sigma,
                              state.entropy_grad)

        regime, code = self.classify_regime(K)

        gamma = self.temporal_modulation(state.entropy_grad)

        tau_rate = self.effective_time_rate(state.Z, state.Sigma)

        flags = {
            "fully_trapped": state.Z > 0.95,
            "silent_system": tau_rate < 1e-6,
            "portal_open": K >= self.portal_threshold
        }

        return EngineOutput(
            portal_score=K,
            regime=regime,
            regime_code=code,
            gamma_eff=gamma,
            tau_rate=tau_rate,
            flags=flags
        )


# =========================
# QUICK SELF-TEST
# =========================

if __name__ == "__main__":

    engine = SandysLawEngine()

    # Example: trapped core → breakout
    test_state = SystemState(
        Z=0.98,
        Sigma=0.05,
        entropy_grad=1.0
    )

    result = engine.evaluate(test_state)

    print("=== Sandy's Law Engine Test ===")
    print(result)
