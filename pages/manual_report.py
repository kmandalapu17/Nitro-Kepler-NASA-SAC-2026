import streamlit as st
from profiles import get_test_baselines, profile_banner
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

# ---------- DATA----------

SYMPTOM_GROUPS = {
    "Head and eyes": ["Headache", "Blurred or changed vision",
                      "Trouble focusing up close", "Ringing or pulsing in ears"],
    "Balance": ["Dizziness", "Nausea", "Unsteadiness", "Clumsiness"],
    "Chest and breathing": ["Shortness of breath", "Palpitations",
                            "Chest discomfort", "Lightheaded when standing"],
    "Body": ["Joint pain", "Tingling or numbness", "Muscle weakness",
             "Back pain", "Swelling in one leg or neck"],
    "Skin and general": ["Rash", "Cold sores", "Fever or chills", "Fatigue",
                         "Poor appetite", "Vomiting", "Skin redness"],
    "Mind and sleep": ["Low mood", "Anxiety", "Irritability",
                       "Trouble concentrating", "Confusion",
                       "Poor sleep", "Daytime sleepiness",
                       "Loss of interest or motivation", "Feeling hopeless",
                       "Panic or racing thoughts", "Feeling lonely or isolated",
                       "Withdrawing from the crew", "Conflict with crewmates",
                       "Irregular sleep schedule", "Overwhelmed by workload",
                       "Making more mistakes than usual",
                       "Procedures or equipment hard to use",
                       "Feeling unsupported by ground team",
                       "Thoughts of harming myself"],
}

EVENTS = {
    "eva": "I just finished a spacewalk",
    "solar": "A solar storm alert was issued recently",
    "landing": "I recently launched or landed",
}

# symptoms: list that counts toward this condition
# min: how many of those symptoms must be selected
# requires: (optional) at least one of these must be selected
# context: (optional) an event that must be checked for this to show
CONDITIONS = [
    {"name": "Spaceflight Associated Neuro-ocular Syndrome (SANS)", "level": "red", "min": 2,
     "symptoms": ["Headache", "Blurred or changed vision", "Trouble focusing up close", "Ringing or pulsing in ears"],
     "requires": ["Blurred or changed vision", "Trouble focusing up close"]},
    {"name": "Sensorimotor / vestibular adaptation", "level": "yellow", "min": 2,
     "symptoms": ["Dizziness", "Nausea", "Unsteadiness", "Clumsiness"]},
    {"name": "Immune change or infection (e.g. viral reactivation)", "level": "yellow", "min": 2,
     "symptoms": ["Rash", "Cold sores", "Fever or chills", "Fatigue"],},
    {"name": "Decompression sickness", "level": "red", "min": 1, "context": "eva",
     "symptoms": ["Joint pain", "Tingling or numbness", "Fatigue", "Rash", "Headache"],
     "requires": ["Joint pain", "Tingling or numbness"]},
    {"name": "Hypoxia or high CO2 exposure", "level": "red", "min": 2,
     "symptoms": ["Headache", "Confusion", "Shortness of breath", "Trouble concentrating"],
     "requires": ["Confusion", "Shortness of breath"]},
    {"name": "Cardiovascular adaptation", "level": "yellow", "min": 1,
     "symptoms": ["Palpitations", "Chest discomfort", "Lightheaded when standing", "Shortness of breath", "Dizziness"]},
    {"name": "Possible blood clot (venous)", "level": "red", "min": 1,
     "symptoms": ["Swelling in one leg or neck"]},
    {"name": "Inadequate nutrition", "level": "yellow", "min": 2,
     "symptoms": ["Poor appetite", "Fatigue"]},
    {"name": "Bone or muscle loss / reduced fitness", "level": "yellow", "min": 2,
     "symptoms": ["Back pain", "Muscle weakness", "Fatigue"]},
    {"name": "Acute radiation effects", "level": "red", "min": 1, "context": "solar",
     "symptoms": ["Nausea", "Vomiting", "Fatigue", "Skin redness", "Fever or chills"]},
    {"name": "Injury from launch/landing loads", "level": "red", "min": 1, "context": "landing",
     "symptoms": ["Back pain", "Tingling or numbness", "Muscle weakness", "Headache"]},
    {"name": "Behavioral changes and psychiatric disorders", "level": "yellow", "min": 2,
     "symptoms": ["Low mood", "Loss of interest or motivation", "Feeling hopeless",
                  "Anxiety", "Panic or racing thoughts", "Irritability",
                  "Withdrawing from the crew"],
     "requires": ["Low mood", "Loss of interest or motivation", "Feeling hopeless",
                  "Anxiety", "Panic or racing thoughts"]},
    {"name": "Inadequate teamwork", "level": "yellow", "min": 2,
     "symptoms": ["Conflict with crewmates", "Withdrawing from the crew",
                  "Irritability", "Feeling lonely or isolated"],
     "requires": ["Conflict with crewmates", "Withdrawing from the crew"]},
    {"name": "Inadequate sleep and irregular schedules", "level": "yellow", "min": 2,
     "symptoms": ["Poor sleep", "Irregular sleep schedule", "Daytime sleepiness",
                  "Trouble concentrating", "Fatigue"],
     "requires": ["Poor sleep", "Irregular sleep schedule", "Daytime sleepiness"]},
    {"name": "Inadequate systems operations support", "level": "yellow", "min": 2,
     "symptoms": ["Overwhelmed by workload", "Making more mistakes than usual",
                  "Procedures or equipment hard to use", "Feeling unsupported by ground team",
                  "Trouble concentrating"],
     "requires": ["Overwhelmed by workload", "Procedures or equipment hard to use",
                  "Feeling unsupported by ground team"]},
]

BASELINES = get_test_baselines()   # comes from the active profile

TESTS = {
    "Amsler Grid":   {"label": "Amsler grid: do any lines look wavy, broken or missing?", "help": "Amsler grid JPG.png",
                 "kind": "yesno", "abnormal": lambda v: v == "Yes"},
    "Near Vision":     {"label": "Near-vision card: can you read your usual smallest line?",
                 "kind": "yesno", "abnormal": lambda v: v == "No"},
    "Balance":  {"label": "Tandem stance, eyes closed: seconds held", "kind": "number",
                 "abnormal": lambda v: v < 0.7 * BASELINES["balance"]},
    "Finger To Nose":   {"label": "Finger-to-nose, eyes closed: did you miss or shake?",
                 "kind": "yesno", "abnormal": lambda v: v == "Yes"},
    "Temperature":     {"label": "Temperature (°C), if you have a thermometer", "kind": "number",
                 "abnormal": lambda v: v >= 38.0},
    "Pulse Count":    {"label": "Pulse count: beats in 30 s × 2", "kind": "number",
                 "abnormal": lambda v: abs(v - BASELINES["pulse"]) > 15},
    "Touch":    {"label": "Light touch on both sides (hands, feet): does one side feel numb or different?",
                 "kind": "yesno", "abnormal": lambda v: v == "Yes"},
    "Grip Strength":     {"label": "Grip strength (kg), weaker side", "kind": "number",
                 "abnormal": lambda v: v < 0.85 * BASELINES["grip"]},
    "Breaths Per Minute":     {"label": "Breaths per minute, counted over 60 s", "kind": "number",
                 "abnormal": lambda v: v > 20},
    "Reaction Time":      {"label": "Reaction-time test: median (ms)", "kind": "number",
                 "abnormal": lambda v: v > 1.2 * BASELINES["pvt"]},
    "Digit Recall":   {"label": "Digit recall: longest list repeated back", "kind": "number",
                 "abnormal": lambda v: v < BASELINES["digits"] - 1},
    "Lying to Standing":{"label": "Stand up from lying down: did you feel lightheaded?",
                 "kind": "yesno", "abnormal": lambda v: v == "Yes"},
    "Weight (Kg)":   {"label": "Body weight (kg)", "kind": "number",
                 "abnormal": lambda v: v < 0.97 * BASELINES["weight"]},
    "Sit to Stand": {"label": "Sit-to-stand: reps in 30 s", "kind": "number",
                 "abnormal": lambda v: v < 0.8 * BASELINES["sit_stand"]},
}

# keys must match the condition names in CONDITIONS exactly
CONDITION_TESTS = {
    "Spaceflight Associated Neuro-ocular Syndrome (SANS)": ["Amsler Grid", "Near Vision"],
    "Sensorimotor / vestibular adaptation": ["Balance", "Finger To Nose"],
    "Immune change or infection (e.g. viral reactivation)": ["Temperature", "Pulse Count"],
    "Decompression sickness": ["Touch", "Grip Strength", "Finger To Nose"],
    "Hypoxia or high CO2 exposure": ["Breaths Per Minute", "Pulse Count", "Reaction Time", "Digit Recall"],
    "Cardiovascular adaptation": ["Lying to Standing", "Pulse Count"],
    "Inadequate nutrition": ["Weight (Kg)", "Grip Strength"],
    "Bone or muscle loss / reduced fitness": ["Grip Strength", "Sit to Stand"],
    "Inadequate sleep and irregular schedules": ["Reaction Time", "Digit Recall"],
    "Acute radiation effects": ["Temperature"],
    "Injury from launch/landing loads": ["Touch", "Grip Strength", "Finger To Nose"],
    # no entry = no safe or objective test: clot, behavioral health
}

CARE = {
    "Spaceflight Associated Neuro-ocular Syndrome (SANS)": {
        "do": ["Tell your Crew Medical Officer about any change in vision, even a mild one.",
               "Write down when it started and what changed (blur, distance, headache).",
               "Repeat the near-vision and Amsler grid checks once a day and log the results.",
               "Avoid long stretches of close-up screen work without breaks."],
        "escalate": ["Sudden vision loss, or lines on the Amsler grid look distorted or missing.",
                     "Vision keeps getting worse over several days."]},
    "Sensorimotor / vestibular adaptation": {
        "do": ["Move slowly and avoid sudden head movements.",
               "Stay close to handholds and rest until the dizziness fades.",
               "Hold off on demanding tasks (spacewalks, robotics) until you feel steady.",
               "Drink fluids and log how you feel each day."],
        "escalate": ["Vomiting that keeps you from holding down fluids.",
                     "Symptoms last more than a day or two, or get worse."]},
    "Immune change or infection (e.g. viral reactivation)": {
        "do": ["Rest and drink fluids.",
               "Take your temperature and log it twice a day.",
               "Take a photo of any rash or sore each day to show how it changes.",
               "Wash hands often and limit close contact."],
        "escalate": ["Fever above your mission's threshold, or fever lasting more than 1–2 days.",
                     "A rash that spreads quickly or you feel much worse."]},
    "Decompression sickness": {
        "do": ["Stop what you are doing and tell a crewmate and the ground team now.",
               "Rest. Do not do another spacewalk or strenuous activity.",
               "Follow your mission's decompression sickness procedure and the ground team's instructions.",
               "Note when symptoms started relative to the spacewalk."],
        "escalate": ["This is urgent. Do not wait for symptoms to settle on their own."]},
    "Hypoxia or high CO2 exposure": {
        "do": ["Check the cabin CO2 and oxygen readings and any active alarms.",
               "Tell your crewmates and the ground team right away.",
               "Follow your mission's procedure for cabin air problems, including moving to a well-ventilated area if directed.",
               "Don't do demanding tasks while confused or breathless."],
        "escalate": ["This is urgent. Confusion or breathlessness can get worse quickly."]},
    "Cardiovascular adaptation": {
        "do": ["Sit or lie down and rest.",
               "When you stand up, do it slowly.",
               "Drink fluids and follow your normal exercise plan unless told otherwise.",
               "Count your pulse and log it with how you feel."],
        "escalate": ["Chest pain or pressure, fainting, or breathlessness at rest.",
                     "A racing or irregular heartbeat that doesn't settle."]},
    "Possible blood clot (venous)": {
        "do": ["Contact your Crew Medical Officer now.",
               "Do not massage the swollen area and avoid strenuous exercise with that limb or neck.",
               "Note which side is affected, when it began, and any redness or warmth."],
        "escalate": ["This is urgent. Chest pain or sudden breathlessness makes it more so."]},
    "Inadequate nutrition": {
        "do": ["Log everything you eat and drink for the next few days.",
               "Eat meals on schedule even if your appetite is low.",
               "Tell the food or nutrition team about foods you can't face, so they can swap them.",
               "Weigh yourself weekly and log it."],
        "escalate": ["Weight keeps dropping, or you can't eat for several days."]},
    "Bone or muscle loss / reduced fitness": {
        "do": ["Complete your full exercise plan every day and log it.",
               "Tell the Crew Medical Officer about back pain or weakness that is new.",
               "Re-check grip strength and sit-to-stand once a week."],
        "escalate": ["Sharp back pain, numbness, or weakness that appears suddenly."]},
    "Acute radiation effects": {
        "do": ["If a solar storm alert is active, move to the most shielded area as your mission procedure directs.",
               "Tell the ground team and write down when each symptom started.",
               "Record your dosimeter reading.",
               "Rest and drink fluids."],
        "escalate": ["This is urgent. Vomiting or fever after a known event should be reported straight away."]},
    "Injury from launch/landing loads": {
        "do": ["Limit movement of your neck and back until you've been checked.",
               "Don't try to treat it yourself.",
               "Tell the ground or recovery team about every pain, numbness or weakness."],
        "escalate": ["This is urgent. Numbness, weakness or severe pain after launch or landing needs a medical check."]},
    "Behavioral changes and psychiatric disorders": {
        "do": ["Talk to someone you trust: a crewmate, family or friends on a call, or the behavioral health support team.",
               "Ask for a private conversation with your Crew Medical Officer or psychologist.",
               "Keep your routine: sleep, meals, exercise and some time to yourself.",
               "Write down how your mood changes through the day."],
        "escalate": ["You have thoughts of harming yourself or giving up. Contact your Crew Medical Officer or support protocol now.",
                     "Low mood or anxiety lasts more than a couple of weeks, or stops you doing your job."]},
    "Inadequate teamwork": {
        "do": ["Take a break from the argument and come back to it when you are both calm.",
               "Talk about specific tasks and needs, not about people.",
               "Use your crew's agreed conflict process, or ask the ground team or psychologist to help mediate.",
               "Keep sharing meals or downtime to rebuild trust."],
        "escalate": ["Conflict is affecting safety-critical tasks or someone feels unsafe."]},
    "Inadequate sleep and irregular schedules": {
        "do": ["Keep a consistent bedtime and wake time.",
               "Dim lights and cut screen time before sleep, and avoid caffeine late in your day.",
               "Log your sleep hours and sleepiness each day.",
               "Avoid safety-critical tasks when you are very drowsy."],
        "escalate": ["You can't stay awake during tasks, or sleep problems last more than a week or two."]},
    "Inadequate systems operations support": {
        "do": ["Write down exactly which procedure, tool or equipment is causing trouble.",
               "Report it to the ground team and ask for help prioritizing your workload.",
               "Don't skip a safety step to save time. Ask for clarification instead."],
        "escalate": ["The problem affects a safety-critical system or you can't get the support you need."]},
}

GENERIC_CARE = {
    "do": ["Rest and drink fluids.", "Write down your symptoms and when they started.",
           "Check again later today and tomorrow."],
    "escalate": ["Symptoms get worse, or new ones appear."]}


def show_care(r):
    """Show instructions under a condition. r is one item from results/refined."""
    care = CARE.get(r["name"], GENERIC_CARE)
    with st.expander(f"What to do: {r['name']}"):
        if r["level"] == "red":
            st.error("Contact your Crew Medical Officer now.")
        else:
            st.info("Rest, re-check, and report if things don't improve.")
        st.write("**What to do now**")
        for line in care["do"]:
            st.write(f"- {line}")
        st.write("**Contact Ground Control if:**")
        for line in care["escalate"]:
            st.write(f"- {line}")
        st.caption("General guidance only. Follow your mission procedures and the instructions of your Crew Medical Officer.")

def tests_to_run(results):
    ids = []
    for r in results:
        if len(r["matched"]) >= r["min"] + 1:
            for t in CONDITION_TESTS.get(r["name"], []):
                if t not in ids:
                    ids.append(t)
    return ids

def refine(results, test_results):
    # test_results: {test_id: True if abnormal, False if normal}; missing = not done
    refined = []
    for r in results:
        ran = [t for t in CONDITION_TESTS.get(r["name"], []) if t in test_results]
        abnormal = [t for t in ran if test_results[t]]
        if not CONDITION_TESTS.get(r["name"]):
            status = "no test available"
        elif not ran:
            status = "not tested"
        elif abnormal:
            status = "supported"
        elif r["level"] == "red":
            status = "tests normal, still report"     # never clear a red
        else:
            status = "less likely"
        refined.append({**r, "status": status, "abnormal": abnormal})
    order = {"supported": 0, "tests normal, still report": 2, "no test available": 3,
             "not tested": 1, "less likely": 4}
    refined.sort(key=lambda r: (r["level"] != "red", order[r["status"]]))
    return refined

def submit_tests():
    out = {}
    for t, spec in TESTS.items():
        v = st.session_state.get(f"test_{t}")
        if v is not None:
            out[t] = bool(spec["abnormal"](v))
    st.session_state.test_results = out
    st.session_state.step = "refined"

def evaluate(selected , events):
    results = []
    for c in CONDITIONS:
        if "context" in c and c["context"] not in events:
            continue
        matched = [s for s in c["symptoms"] if s in selected]
        if len(matched) < c["min"]:
            continue
        if "requires" in c and not any(s in selected for s in c["requires"]):
            continue
        # FIX: Add "min": c["min"] to the dictionary below
        results.append({"name": c["name"], "level": c["level"], "matched": matched, "min": c["min"]})
    
    results.sort(key=lambda r: -len(r["matched"]))
    return results

# ---------- CALLBACKS ----------

# Screen order: recent events first, then each symptom group
PAGES = ["Recent events"] + list(SYMPTOM_GROUPS.keys())

def init_wizard():
    if "group_idx" not in st.session_state:
        st.session_state.group_idx = 0
    if "picked_syms" not in st.session_state:
        st.session_state.picked_syms = set()
    if "picked_events" not in st.session_state:
        st.session_state.picked_events = set()

def save_page():
    """Copy this screen's checkboxes into the permanent store."""
    page = PAGES[st.session_state.group_idx]
    if page == "Recent events":
        for key in EVENTS:
            if st.session_state.get(f"event_{key}"):
                st.session_state.picked_events.add(key)
            else:
                st.session_state.picked_events.discard(key)
    else:
        for s in SYMPTOM_GROUPS[page]:
            if st.session_state.get(f"sym_{s}"):
                st.session_state.picked_syms.add(s)
            else:
                st.session_state.picked_syms.discard(s)

def next_page():
    save_page()
    st.session_state.group_idx += 1

def prev_page():
    save_page()
    st.session_state.group_idx -= 1

def submit_symptoms():
    save_page()
    if not st.session_state.picked_syms:
        st.session_state.no_symptoms = True      # stay on the last screen
        return
    st.session_state.no_symptoms = False
    # keep the order from SYMPTOM_GROUPS
    st.session_state.selected = [s for items in SYMPTOM_GROUPS.values()
                                 for s in items if s in st.session_state.picked_syms]
    st.session_state.events = [k for k in EVENTS if k in st.session_state.picked_events]
    st.session_state.step = "results"

def start_over():
    st.session_state.picked_syms = set()
    st.session_state.picked_events = set()
    st.session_state.group_idx = 0
    st.session_state.no_symptoms = False
    st.session_state.step = "start"
# Page Logic
st.set_page_config(page_title="Manual Report", page_icon=":material/thumb_up:", layout="wide")

if "step" not in st.session_state:
    st.session_state.step = "start"      # start -> fine -> confirm_home

def set_step(name):
    st.session_state.step = name



st.write("## Manual report portal.")
profile_banner()
if st.session_state.step == "start":
    st.write("# How are you feeling today?")
    if st.session_state.pop("came_from_auto", False):
        flags = st.session_state.pop("auto_flags", [])
        st.warning(f"The automatic check flagged: {', '.join(flags)}. Please complete a manual check.")

    st.button("Everything is good.", on_click=set_step, args=("fine",))
    st.button("I feel unwell.", on_click=set_step, args=("unwell",))

elif st.session_state.step == "fine":
    if st.button("Perform Automatic Checks (Recommended)"):
        st.session_state.step = "start"          # reset for next time
        st.switch_page("pages/semi_automated_report.py")
    st.button("Return to Home", on_click=set_step, args=("confirm_home",))

elif st.session_state.step == "confirm_home":
    st.session_state.step = "start"
    st.switch_page("pages/homepage.py")

elif st.session_state.step == "unwell":
    init_wizard()
    idx = st.session_state.group_idx
    page = PAGES[idx]
    last = idx == len(PAGES) - 1

    st.write("### What symptoms do you have?")
    st.progress((idx + 1) / len(PAGES), text=f"Step {idx + 1} of {len(PAGES)}: {page}")

    if page == "Recent events":
        st.write("**Has any of this happened recently?**")
        for key, label in EVENTS.items():
            st.checkbox(label, key=f"event_{key}",
                        value=key in st.session_state.picked_events)
    else:
        st.write(f"**{page}**")
        for s in SYMPTOM_GROUPS[page]:
            st.checkbox(s, key=f"sym_{s}",
                        value=s in st.session_state.picked_syms)

    if last and st.session_state.get("no_symptoms"):
        st.write("No symptoms selected. Sending for Automatic Checks.")
        if st.button("Perform Automatic Checks", key="no_sym_auto_btn"):
            st.switch_page("pages/semi_automated_report.py")

    col1, col2 = st.columns(2)
    with col1:
        if idx == 0:
            st.button("Back", on_click=set_step, args=("start",), key="wiz_back_start")
        else:
            st.button("Previous", on_click=prev_page, key="wiz_prev")
    with col2:
        if last:
            st.button("Submit Symptoms", on_click=submit_symptoms, key="wiz_submit")
        else:
            st.button("Next", on_click=next_page, key="wiz_next")

elif st.session_state.step == "results":
    selected = st.session_state.get("selected", [])
    events = st.session_state.get("events", [])
    results = evaluate(selected, events)

    st.write("### Possible conditions")

    if not results:
        st.write("Your symptoms don't match any known conditions.")
        st.write("Sending for Automatic Checks")
        if st.button("Perform Automatic Checks"):
            st.switch_page("pages/semi_automated_report.py")

    for r in results:
        box = st.error if r["level"] == "red" else st.warning
        box(f"**{r['name']}**  Symptoms: {', '.join(r['matched'])}")
        show_care(r)
    ids = tests_to_run(results)
    if ids:
        st.button("Run tests to narrow this down", on_click=set_step, args=("tests",))

    st.button("Start over", on_click=start_over)
    st.button("Return to Home", on_click=set_step, args=("confirm_home",))
elif st.session_state.step == "tests":
    results = evaluate(st.session_state.selected, st.session_state.events)
    st.write("### Function tests")
    st.caption("Do only the tests you can. Leave the rest blank.")
    for t in tests_to_run(results):
        spec = TESTS[t]
        if spec["kind"] == "yesno":
            st.radio(spec["label"], ["Yes", "No"], index=None, horizontal=True, key=f"test_{t}")
        else:
            st.number_input(spec["label"], value=None, key=f"test_{t}")
        if t == "Amsler Grid":
            with st.expander("Amsler Grid Diagram"):
                st.image("Amsler grid JPG.png", caption="Look at the center dot. Check if lines look wavy or broken.")
        if t == "Near Vision":
            with st.expander("Near Vision Card. Hold it at your usual reading distance."):
                st.image("nearvisioncard.jpeg", caption="Can you read your usual smallest line?")
        if t == "Balance":
            with st.expander("Balance test instructions"):
                st.image("tandemstance.jpeg", caption="Stand with one foot in front of the other, eyes closed. Time how long you can hold it.")
    st.button("See new results", on_click=submit_tests)
    st.button("Back", on_click=set_step, args=("results",))

elif st.session_state.step == "refined":
    results = evaluate(st.session_state.selected, st.session_state.events)
    refined = refine(results, st.session_state.get("test_results", {}))
    st.write("### Refined results")
    for r in refined:
        box = st.error if r["level"] == "red" else st.warning
        if r["status"] == "less likely":
            box = st.info
        extra = f"  \nUnusual tests: {', '.join(r['abnormal'])}" if r["abnormal"] else ""
        box(f"**{r['name']}** ({r['status']}){extra}")
        show_care(r)
    st.button("Return to Home", on_click=set_step, args=("confirm_home",))