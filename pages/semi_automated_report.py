import time
import pandas as pd
import streamlit as st
from vitals import BASELINE, SCENARIOS, read_vitals, assess

#Formatting
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rufina:wght@400;700&family=Playfair+Display:wght@400;700&family=Libre+Franklin:wght@400;700&display=swap');

    [data-testid="stMarkdownContainer"] h1 a, 
    [data-testid="stMarkdownContainer"] h2 a, 
    [data-testid="stMarkdownContainer"] h3 a {
    display: none !important;
    }

    /* Base styles */
    .stApp, p, label, li, button, input, textarea,
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stCaptionContainer"],
    [data-testid="stWidgetLabel"] p {
        font-family: 'Playfair Display', serif !important;
    }

    .stButton > button {
    border-width: 2px !important;  /* Change this value to adjust thickness */
    border-style: solid !important;
    border-color: #62A77A !important; /* Optional: Sets the color of the border */
    font-size: 18px !important;
    }

    .stButton > button p {
        font-family: 'Playfair Display', sans-serif !important;
        font-weight: 700 !important;
    }
    
    /* Headings and Title container styling */
    [data-testid="stMarkdownContainer"] h1, 
    [data-testid="stMarkdownContainer"] h2, 
    [data-testid="stMarkdownContainer"] h3, 
    [data-testid="stMarkdownContainer"] .title-container {
        font-family: 'Libre Franklin', sans-serif !important;
        font-weight: 700 !important;
    }

    /* Centers the title text and icon container */
    .title-container {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 5px; /* Gap between the text and the icon */
        margin: 0 auto;
    }

    /* Tooltip container positioning */
    .custom-tooltip {
        position: relative;
        display: inline-flex;
        cursor: pointer;
        color: #808495; /* Streamlit's default gray icon color */
        font-size: 18px;
        vertical-align: middle;
        user-select: none;
    }

    /* Tooltip text box styling */
    .custom-tooltip .tooltip-text {
        visibility: hidden;
        width: 600px;
        background-color: #FBE5C6; /* Dark background matching Streamlit tooltips */
        color: #33704A;
        text-align: center;
        border-radius: 4px;
        padding: 8px 12px;
        position: absolute;
        z-index: 99;
        bottom: 125%; /* Places it above the icon */
        left: 50%;
        transform: translateX(-50%);
        opacity: 0;
        transition: opacity 0.2s;
        font-family: 'Playfair Display', serif;
        font-weight: 400;
        font-size: 16px;
        line-height: 1.4;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.3);
    }

    /* Small arrow on the bottom of the tooltip */
    .custom-tooltip .tooltip-text::after {
        content: "";
        position: absolute;
        top: 100%;
        left: 50%;
        margin-left: -5px;
        border-width: 5px;
        border-style: solid;
        border-color: #33704A transparent transparent transparent;
    }

    /* Show the text box on hover */
    .custom-tooltip:hover .tooltip-text {
        visibility: visible;
        opacity: 1;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.set_page_config(page_title="Automatic Checks", layout="wide")
st.write("## Automatic health monitoring")
st.caption("Simulated sensor data for demonstration.")

N_READINGS = 15
TRIGGER = ("yellow", "red")      # which levels send the user to manual: your team decides

scenario = st.selectbox("Demo scenario", list(SCENARIOS))

if st.button("Start monitoring", key="start_auto"):
    history = []
    status = st.empty()
    cols = st.columns(len(BASELINE))
    slots = [c.empty() for c in cols]

    level, flags = "green", {}
    for tick in range(N_READINGS):
        history.append(read_vitals(scenario, tick))
        level, flags = assess(history)

        for slot, (name, v) in zip(slots, BASELINE.items()):
            with slot.container():
                st.metric(f"{name} ({v['unit']})", history[-1][name],
                          delta=round(history[-1][name] - v["base"], 1),
                          delta_color="off")
                st.line_chart(pd.DataFrame({name: [h[name] for h in history]}), height=120)

        status.write(f"Status: **{level.upper()}**" + (f" ({', '.join(flags)})" if flags else ""))

        if level in TRIGGER:
            break
        time.sleep(1)

    if level in TRIGGER:
        st.session_state.came_from_auto = True
        st.session_state.auto_flags = list(flags)
        st.session_state.step = "start"          # manual page starts at its first screen
        st.warning("Something looks off. Switching to a manual check...")
        time.sleep(2)
        st.switch_page("pages/manual_report.py")
    else:
        st.success("All readings normal.")
        st.button("Back to home", on_click=lambda: st.switch_page("pages/homepage.py"), key="auto_home")