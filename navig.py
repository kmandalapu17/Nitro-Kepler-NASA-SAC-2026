#oh yeeah
import streamlit as st

homee = st.Page("pages/homepage.py", title="Home", icon=":material/thumb_up:")
manuall = st.Page("pages/manual_report.py", title="Manual Report", icon=":material/thumb_up:")
autoo = st.Page(
    "pages/semi_automated_report.py",
    title="Semi-Automated Report",
    icon=":material/thumb_up:",
)
profilee = st.Page("pages/profile.py", title="Profiles")
pg = st.navigation([homee, manuall, autoo, profilee])
pg.run() 