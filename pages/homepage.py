import streamlit as st
st.set_page_config(page_title="homepage", page_icon=":material/thumb_up:", layout="wide")

#st.markdown("<h1>ToolNameHere</h1>", unsafe_allow_html=True, help="This is the health checkin and diagnosis application. You can choose to generate a manual report or a semi-automated report by clicking the respective buttons below.", width="auto",text_alignment="center", anchors=False, wrap = True)
st.title(
    "ToolNameHere", 
    help="This is the health checkin and diagnosis application. You can choose to generate a manual report or a semi-automated report by clicking the respective buttons below.", 
    text_alignment="center",
    anchor=False,
)
st.write("")


lefts, right = st.columns(2)
with lefts:
    with st.container(horizontal_alignment="center"):
        manual = st.button("Click here for a manual report.")
with right:
    with st.container(horizontal_alignment="center"):
        auto = st.button("Click here for the semi-automated report.")

if manual:
    st.write("You have selected the manual report option.")
    st.switch_page("pages/manual_report.py")
if auto:
    st.write("You have selected the semi-automated report option.")
    st.switch_page("pages/semi_automated_report.py")