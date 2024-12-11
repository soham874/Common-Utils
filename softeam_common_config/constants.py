from pathlib import Path

BASEDIR=Path(__file__).parent.parent

UPSTOX_AUTH_HEADERS='upstox_headers'
ZERODHA_AUTH_HEADERS='zerodha_auth_headers'

# Analysis strategies
SUPPORTED_ANALYSIS_STRATEGIES = [
    'analyst'
]