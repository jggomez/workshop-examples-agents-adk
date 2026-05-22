def calculate_risk_metrics(
    current_price: float, risk_profile: str = "balanced"
) -> dict:
    """Mathematically compute the risk index, implicit volatility, and
    suggested Stop-Loss thresholds based on current market price and user profile.

    Args:
        current_price: The active asset price retrieved from the market.
        risk_profile: User risk tolerance ('conservative', 'balanced', 'aggressive').
    """
    # Input validation (Zero Trust — Spec §5.2)
    if current_price <= 0:
        raise ValueError(
            f"current_price must be positive, got: {current_price}"
        )

    valid_profiles = ("conservative", "balanced", "aggressive")
    normalized_profile = risk_profile.strip().lower()
    if normalized_profile not in valid_profiles:
        raise ValueError(
            f"Invalid risk_profile: '{risk_profile}'. "
            f"Must be one of {valid_profiles}."
        )

    # Mapping risk profiles to volatility factors
    risk_factors = {
        "conservative": 0.02,
        "balanced": 0.05,
        "aggressive": 0.10,
    }

    volatility_factor = risk_factors[normalized_profile]

    expected_drawdown = current_price * volatility_factor
    stop_loss_level = current_price * (1 - (volatility_factor * 1.2))
    risk_score = (volatility_factor * 100) / 1.5  # Normalized score

    return {
        "risk_score": round(risk_score, 1),
        "classification": (
            "High Risk"
            if risk_score > 6
            else "Moderate Risk"
            if risk_score > 3
            else "Low Risk"
        ),
        "expected_24h_drawdown": round(expected_drawdown, 2),
        "suggested_stop_loss": round(stop_loss_level, 2),
        "applied_profile": normalized_profile,
    }
