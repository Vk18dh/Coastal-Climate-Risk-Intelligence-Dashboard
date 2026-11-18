import os

class RiskEngineConfig:
    """
    DEMO ONLY CONFIGURATION.
    These values are not scientifically validated and serve only as placeholders
    to demonstrate the mechanics of the Climate Risk Engine MVP.
    """
    
    METHODOLOGY_VERSION = "demo-1.0"
    NORMALIZATION_CONFIG_VERSION = "demo-1.0"

    # ── Normalization Thresholds (Demo Only) ──────────────────────────────────
    # Capped at 200 mm
    RAINFALL_MAX_MM = float(os.getenv("ENGINE_RAINFALL_MAX_MM", "200.0"))
    
    # Capped at 3.0 m
    TIDE_MAX_M = float(os.getenv("ENGINE_TIDE_MAX_M", "3.0"))
    
    # Inverted: 0 m is highest risk (1.0), 20 m is lowest risk (0.0)
    ELEVATION_MIN_M = float(os.getenv("ENGINE_ELEVATION_MIN_M", "0.0"))
    ELEVATION_MAX_M = float(os.getenv("ENGINE_ELEVATION_MAX_M", "20.0"))
    
    # Ordinal mapping for categorical flood severity
    FLOOD_SEVERITY_MAPPING = {
        "none": 0.0,
        "low": 0.25,
        "moderate": 0.5,
        "high": 0.75,
        "extreme": 1.0
    }

    # ── Component Weights (Demo Only) ─────────────────────────────────────────
    # Must sum to 1.0
    WEIGHTS = {
        "rainfall_score": 0.30,
        "tide_score": 0.30,
        "elevation_score": 0.20,
        "flood_score": 0.20
    }

    # ── Missing Data Mode ─────────────────────────────────────────────────────
    # "STRICT": Fails if any component is missing.
    # "RENORMALIZE": Proportionally redistributes missing weight among available.
    MISSING_DATA_MODE = os.getenv("ENGINE_MISSING_DATA_MODE", "RENORMALIZE").upper()

    # ── Risk Classification Thresholds (Demo Only) ────────────────────────────
    # Scale is 0.0 to 100.0
    CLASSIFICATION_THRESHOLDS = {
        "Low": 25.0,
        "Moderate": 50.0,
        "High": 75.0,
        "Critical": 100.0
    }
