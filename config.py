"""Dashboard configuration."""

SHEET_ID = "1OcoSO3L3G2nuDnYL-QSTFfMJa8YAzM4U5D55_c0MQg8"
SUMMARY_CSV = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Summary"
HISTORY_CSV = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=fund_history"

CACHE_TTL = 300  # 5 min — refresh on browser reload

# Colors (Blue theme)
PRIMARY = "#1B3A5C"
ACCENT = "#2E86DE"
LIGHT = "#85C1E9"
BG = "#F8F9FA"
TEXT = "#2C3E50"
MUTED = "#7F8C8D"

DIVISION_COLORS = {
    "1본부": "#1B3A5C",
    "2본부": "#2E86DE",
    "3본부": "#85C1E9",
}
