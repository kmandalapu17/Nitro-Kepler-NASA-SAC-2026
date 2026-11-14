import streamlit as st

st.set_page_config(page_title="homepage", page_icon=":material/thumb_up:", layout="wide")
import streamlit as st

st.markdown(
    """
    <style>
    @import url('https://googleapis.com');

    [data-testid="stMarkdownContainer"] h1 a, 
    [data-testid="stMarkdownContainer"] h2 a, 
    [data-testid="stMarkdownContainer"] h3 a {
    display: none !important;
    }

    /* Base styles */
    .stApp, p, [data-testid="stMarkdownContainer"] p {
        font-family: 'Rufina', serif !important;
        font-weight: 400;
    }

    .stButton > button {
    border-width: 8px !important;  /* Change this value to adjust thickness */
    border-style: solid !important;
    border-color: #62A77A !important; /* Optional: Sets the color of the border */
    font-size: 18px !important;
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
        font-family: 'Rufina', serif;
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

# Title implementation using custom tooltip inside the HTML string
st.markdown(
    """
    <div class="title-container">
        <h1>ToolNameHere</h1>
        <div class="custom-tooltip">
            <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.25" stroke-linecap="round" stroke-linejoin="round" class="feather feather-info">
                <circle cx="6" cy="6" r="5"></circle>
                <line x1="6" y1="8" x2="6" y2="6"></line>
                <line x1="6" y1="4" x2="6.005" y2="4"></line>
            </svg>
            <span class="tooltip-text">
                This is the health checkin and diagnosis application. You can choose to generate a manual report or a semi-automated report by clicking the respective buttons below.
            </span>
        </div>
    </div>
    """, 
    unsafe_allow_html=True,
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