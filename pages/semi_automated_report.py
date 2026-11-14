import time
import pandas as pd
import streamlit as st
from vitals import BASELINE, SCENARIOS, read_vitals, assess

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