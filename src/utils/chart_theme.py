import altair as alt
import streamlit as st
from src.utils import preferences
import src.utils.loaders as loaders
from src.utils.branding import add_chart_watermark

# -------------------------------
# Dark Theme
# -------------------------------
@alt.theme.register("streamiq_dark", enable=False)
def streamiq_dark_theme():
    return alt.theme.ThemeConfig({
        "config": {
            "background": "#0E1117",
            "view": {"stroke": "transparent"},
            "axis": {
                "domainColor": "#FAFAFA",
                "gridColor": "#262730",
                "labelColor": "#FAFAFA",
                "titleColor": "#FAFAFA"
            },
            "legend": {
                "labelColor": "#FAFAFA",
                "titleColor": "#FAFAFA",
                "orient": "bottom"
            },
            "title": {"color": "#FAFAFA"},
            "mark": {"color": "#4CAF50"}
        }
    })

# -------------------------------
# Light Theme
# -------------------------------
@alt.theme.register("streamiq_light", enable=False)
def streamiq_light_theme():
    return alt.theme.ThemeConfig({
        "config": {
            "background": "#FFFFFF",
            "view": {"stroke": "transparent"},
            "axis": {
                "domainColor": "#000000",
                "gridColor": "#F0F2F6",
                "labelColor": "#000000",
                "titleColor": "#000000"
            },
            "legend": {
                "labelColor": "#000000",
                "titleColor": "#000000",
                "orient": "bottom"
            },
            "title": {"color": "#000000"},
            "mark": {"color": "#4CAF50"}
        }
    })

# -------------------------------
# Theme Setter
# -------------------------------
def set_chart_theme(mode: str = "light", persist: bool = True):
    """Toggle chart theme between 'light' and 'dark', optionally persisting choice."""
    if mode.lower() == "dark":
        alt.theme.enable("streamiq_dark")
    else:
        alt.theme.enable("streamiq_light")
    if persist:
        try:
            preferences.set_preference("chart_theme", mode.lower())
        except Exception:
            pass  # fail gracefully if DB unavailable

def load_chart_theme():
    """Load persisted chart theme from preferences.db, fallback to light in demo mode."""
    if loaders.USE_DUMMY:
        set_chart_theme("light", persist=False)
        return
    try:
        saved = preferences.get_preference("chart_theme")
        if saved:
            set_chart_theme(saved, persist=False)
        else:
            set_chart_theme("light", persist=False)
    except Exception:
        set_chart_theme("light", persist=False)

# -------------------------------
# Smoke Test Confirmation
# -------------------------------
if __name__ == "__main__":
    import pandas as pd

    print("✅ StreamIQ chart themes registered successfully (dark & light).")

    # Demo dataset
    df = pd.DataFrame({"x": list(range(10)), "y": [i**2 for i in range(10)]})

    # Dark theme demo
    set_chart_theme("dark", persist=False)
    chart_dark = alt.Chart(df).mark_line().encode(x="x", y="y").properties(title="Dark Theme Demo")
    chart_dark = add_chart_watermark(chart_dark, mode="Dark")
    st.altair_chart(chart_dark, use_container_width=True)

    # Light theme demo
    set_chart_theme("light", persist=False)
    chart_light = alt.Chart(df).mark_line(color="green").encode(x="x", y="y").properties(title="Light Theme Demo")
    chart_light = add_chart_watermark(chart_light, mode="Light")
    st.altair_chart(chart_light, use_container_width=True)
