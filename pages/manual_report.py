import streamlit as st

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
                       "Poor sleep", "Daytime sleepiness"],
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
    {"name": "Sleep loss / fatigue risk", "level": "yellow", "min": 2,
     "symptoms": ["Poor sleep", "Daytime sleepiness", "Trouble concentrating", "Fatigue"]},
    {"name": "Behavioral health risk", "level": "yellow", "min": 2,
     "symptoms": ["Low mood", "Anxiety", "Irritability"]},
    {"name": "Acute radiation effects", "level": "red", "min": 1, "context": "solar",
     "symptoms": ["Nausea", "Vomiting", "Fatigue", "Skin redness", "Fever or chills"]},
    {"name": "Injury from launch/landing loads", "level": "red", "min": 1, "context": "landing",
     "symptoms": ["Back pain", "Tingling or numbness", "Muscle weakness", "Headache"]},
]

# placeholder baselines: replace with each astronaut's own values
BASELINES = {"balance": 20, "grip": 40, "pulse": 65, "weight": 75,
             "sit_stand": 15, "pvt": 300, "digits": 7}

TESTS = {
    "amsler":   {"label": "Amsler grid: do any lines look wavy, broken or missing?",
                 "kind": "yesno", "abnormal": lambda v: v == "Yes"},
    "near":     {"label": "Near-vision card: can you read your usual smallest line?",
                 "kind": "yesno", "abnormal": lambda v: v == "No"},
    "balance":  {"label": "Tandem stance, eyes closed: seconds held", "kind": "number",
                 "abnormal": lambda v: v < 0.7 * BASELINES["balance"]},
    "finger":   {"label": "Finger-to-nose, eyes closed: did you miss or shake?",
                 "kind": "yesno", "abnormal": lambda v: v == "Yes"},
    "temp":     {"label": "Temperature (°C), if you have a thermometer", "kind": "number",
                 "abnormal": lambda v: v >= 38.0},
    "pulse":    {"label": "Pulse count: beats in 30 s × 2", "kind": "number",
                 "abnormal": lambda v: abs(v - BASELINES["pulse"]) > 15},
    "touch":    {"label": "Light touch on both sides (hands, feet): does one side feel numb or different?",
                 "kind": "yesno", "abnormal": lambda v: v == "Yes"},
    "grip":     {"label": "Grip strength (kg), weaker side", "kind": "number",
                 "abnormal": lambda v: v < 0.85 * BASELINES["grip"]},
    "resp":     {"label": "Breaths per minute, counted over 60 s", "kind": "number",
                 "abnormal": lambda v: v > 20},
    "pvt":      {"label": "Reaction-time test: median (ms)", "kind": "number",
                 "abnormal": lambda v: v > 1.2 * BASELINES["pvt"]},
    "digits":   {"label": "Digit recall: longest list repeated back", "kind": "number",
                 "abnormal": lambda v: v < BASELINES["digits"] - 1},
    "orthostat":{"label": "Stand up from lying down: did you feel lightheaded?",
                 "kind": "yesno", "abnormal": lambda v: v == "Yes"},
    "weight":   {"label": "Body weight (kg)", "kind": "number",
                 "abnormal": lambda v: v < 0.97 * BASELINES["weight"]},
    "sit_stand":{"label": "Sit-to-stand: reps in 30 s", "kind": "number",
                 "abnormal": lambda v: v < 0.8 * BASELINES["sit_stand"]},
}

# keys must match the condition names in CONDITIONS exactly
CONDITION_TESTS = {
    "Spaceflight Associated Neuro-ocular Syndrome (SANS)": ["amsler", "near"],
    "Sensorimotor / vestibular adaptation": ["balance", "finger"],
    "Immune change or infection (e.g. viral reactivation)": ["temp", "pulse"],
    "Decompression sickness": ["touch", "grip", "finger"],
    "Hypoxia or high CO2 exposure": ["resp", "pulse", "pvt", "digits"],
    "Cardiovascular adaptation": ["orthostat", "pulse"],
    "Inadequate nutrition": ["weight", "grip"],
    "Bone or muscle loss / reduced fitness": ["grip", "sit_stand"],
    "Sleep loss / fatigue risk": ["pvt", "digits"],
    "Acute radiation effects": ["temp"],
    "Injury from launch/landing loads": ["touch", "grip", "finger"],
    # no entry = no safe or objective test: clot, behavioral health
}

def tests_to_run(results):
    ids = []
    for r in results:
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
    order = {"supported": 0, "tests normal, still report": 1, "no test available": 2,
             "not tested": 3, "less likely": 4}
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

def evaluate(selected, events):
    results = []
    for c in CONDITIONS:
        if "context" in c and c["context"] not in events:
            continue
        matched = [s for s in c["symptoms"] if s in selected]
        if len(matched) < c["min"]:
            continue
        if "requires" in c and not any(s in selected for s in c["requires"]):
            continue
        results.append({"name": c["name"], "level": c["level"], "matched": matched})
    # red first, then most matched symptoms
    results.sort(key=lambda r: (r["level"] != "red", -len(r["matched"])))
    return results

# ---------- CALLBACKS ----------

def submit_symptoms():
    chosen = [s for items in SYMPTOM_GROUPS.values() for s in items
              if st.session_state.get(f"sym_{s}")]
    events = [k for k in EVENTS if st.session_state.get(f"event_{k}")]
    if not chosen:
        st.session_state.no_symptoms = True     # stay on this screen
        return
    st.session_state.no_symptoms = False
    st.session_state.selected = chosen
    st.session_state.events = events
    st.session_state.step = "results"

def start_over():
    for items in SYMPTOM_GROUPS.values():
        for s in items:
            st.session_state.pop(f"sym_{s}", None)
    for k in EVENTS:
        st.session_state.pop(f"event_{k}", None)
    st.session_state.step = "start"

# Page Logic
st.set_page_config(page_title="Manual Report", page_icon=":material/thumb_up:", layout="wide")

if "step" not in st.session_state:
    st.session_state.step = "start"      # start -> fine -> confirm_home

def set_step(name):
    st.session_state.step = name

st.write("## Manual report portal.")
st.write("# How are you feeling today?")

if st.session_state.step == "start":
    st.button("Everything is good.", on_click=set_step, args=("fine",))
    st.button("I feel unwell.", on_click=set_step, args=("unwell",))

elif st.session_state.step == "fine":
    if st.button("Perform Automatic Checks (Recommended)"):
        st.session_state.step = "start"          # reset for next time
        st.switch_page("pages/semi_automated_report.py")
    st.button("Return to Home", on_click=set_step, args=("confirm_home",))

elif st.session_state.step == "confirm_home":
    st.write("## Are you sure?")
    if st.button("Yes"):
        st.session_state.step = "start"
        st.switch_page("pages/homepage.py")
    st.button("No", on_click=set_step, args=("fine",))

elif st.session_state.step == "unwell":
    st.write("### What symptoms do you have?")

    st.write("**Has any of this happened recently?**")
    for key, label in EVENTS.items():
        st.checkbox(label, key=f"event_{key}")

    cols = st.columns(3)
    for i, (group, items) in enumerate(SYMPTOM_GROUPS.items()):
        with cols[i % 3]:
            st.write(f"**{group}**")
            for s in items:
                st.checkbox(s, key=f"sym_{s}")

    if st.session_state.get("no_symptoms"):
        st.warning("Please select at least one symptom.")

    st.button("Submit Symptoms", on_click=submit_symptoms)
    st.button("Back", on_click=set_step, args=("start",))

elif st.session_state.step == "results":
    selected = st.session_state.get("selected", [])
    events = st.session_state.get("events", [])
    results = evaluate(selected, events)

    st.write("### Possible conditions")

    if any(r["level"] == "red" for r in results):
        st.error("# EMERGENCY. GET HELP IMMEDIATELY.")

    if not results:
        st.info("Your symptoms don't match a known disease.")

    for r in results:
        box = st.error if r["level"] == "red" else st.warning
        box(f"**{r['name']}**  \Symptoms: {', '.join(r['matched'])}")
        ids = tests_to_run(results)
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
        extra = f"  \nUnusual tests: {', '.join(r['unusual'])}" if r["unusual"] else ""
        box(f"**{r['name']}** ({r['status']}){extra}")
    st.button("Return to Home", on_click=set_step, args=("confirm_home",))