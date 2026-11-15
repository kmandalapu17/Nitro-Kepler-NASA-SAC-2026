import datetime
import streamlit as st
from profiles import (load_profiles, save_profiles, set_active,
                      DEFAULT_VITALS, DEFAULT_TESTS)

st.set_page_config(page_title="Astronaut Profiles", layout="wide")

# (paste your <style> block here)

# ---------- callbacks ----------
def create_cb():
    s = st.session_state
    name = s.get("new_profile_name", "").strip()
    if not name:
        s.profile_msg = ("error", "Enter a name first.")
        return
    profiles = load_profiles()
    if name in profiles:
        s.profile_msg = ("error", "That profile already exists.")
        return
    profiles[name] = {"vitals": dict(DEFAULT_VITALS), "tests": dict(DEFAULT_TESTS),
                      "baseline_set": False}
    save_profiles(profiles)
    set_active(name)
    s.profile_choice = name
    s.new_profile_name = ""
    s.profile_msg = ("success", f"Created {name}. Now enter your healthy baseline below.")


def save_cb(name):
    s = st.session_state
    if not s.get(f"healthy_{name}"):
        s.profile_msg = ("error", "Please confirm you are healthy and rested before saving a baseline.")
        return
    hr = s[f"hr_{name}"]
    profiles = load_profiles()
    profiles[name] = {
        "vitals": {"heart_rate": hr, "spo2": s[f"spo2_{name}"], "temp": s[f"temp_{name}"],
                   "resp_rate": s[f"resp_{name}"], "systolic": s[f"sys_{name}"]},
        "tests": {"pulse": hr, "balance": s[f"bal_{name}"], "grip": s[f"grip_{name}"],
                  "weight": s[f"wt_{name}"], "sit_stand": s[f"sts_{name}"],
                  "pvt": s[f"pvt_{name}"], "digits": s[f"dig_{name}"]},
        "baseline_set": True,
        "saved_on": datetime.date.today().isoformat(),
    }
    save_profiles(profiles)
    set_active(name)
    s.profile_msg = ("success", f"Baseline saved for {name}.")


def delete_cb(name):
    profiles = load_profiles()
    profiles.pop(name, None)
    save_profiles(profiles)
    st.session_state.pop("active_profile", None)
    st.session_state.pop("profile_choice", None)
    st.session_state.profile_msg = ("info", f"Deleted {name}.")


# ---------- page ----------
st.write("## Astronaut profiles")
st.caption("Record these values while you are healthy and rested. "
           "They become your personal baseline for the checks.")

msg = st.session_state.pop("profile_msg", None)
if msg:
    getattr(st, msg[0])(msg[1])

profiles = load_profiles()
names = list(profiles)

with st.expander("Create a new profile", expanded=not names):
    st.text_input("Astronaut name", key="new_profile_name")
    st.button("Create profile", on_click=create_cb, key="create_profile_btn")

if names:
    if st.session_state.get("profile_choice") not in names:
        active = st.session_state.get("active_profile")
        st.session_state.profile_choice = active if active in names else names[0]
    choice = st.selectbox("Profile", names, key="profile_choice")
    set_active(choice)

    cur = profiles[choice]
    v = {**DEFAULT_VITALS, **cur.get("vitals", {})}
    t = {**DEFAULT_TESTS, **cur.get("tests", {})}

    if cur.get("baseline_set"):
        st.caption(f"Baseline last saved: {cur.get('saved_on', 'unknown')}")
    else:
        st.info("This profile still has default values. Enter your own below.")

    with st.form(f"profile_form_{choice}"):
        c1, c2 = st.columns(2)
        with c1:
            st.write("**Resting vitals**")
            st.number_input("Resting heart rate (bpm)", 40.0, 120.0, float(v["heart_rate"]),
                            step=1.0, key=f"hr_{choice}")
            st.number_input("Oxygen saturation, SpO2 (%)", 85.0, 100.0, float(v["spo2"]),
                            step=1.0, key=f"spo2_{choice}")
            st.number_input("Body temperature (°C)", 35.0, 38.0, float(v["temp"]),
                            step=0.1, format="%.1f", key=f"temp_{choice}")
            st.number_input("Breathing rate (breaths/min)", 6.0, 30.0, float(v["resp_rate"]),
                            step=1.0, key=f"resp_{choice}")
            st.number_input("Systolic blood pressure (mmHg)", 80.0, 180.0, float(v["systolic"]),
                            step=1.0, key=f"sys_{choice}")
        with c2:
            st.write("**Function tests**")
            st.number_input("Tandem balance, eyes closed (seconds)", 0.0, 120.0, float(t["balance"]),
                            step=1.0, key=f"bal_{choice}")
            st.number_input("Grip strength (kg)", 5.0, 120.0, float(t["grip"]),
                            step=1.0, key=f"grip_{choice}")
            st.number_input("Body weight (kg)", 30.0, 200.0, float(t["weight"]),
                            step=0.5, key=f"wt_{choice}")
            st.number_input("Sit-to-stand (reps in 30 s)", 0.0, 50.0, float(t["sit_stand"]),
                            step=1.0, key=f"sts_{choice}")
            st.number_input("Reaction time, median (ms)", 150.0, 800.0, float(t["pvt"]),
                            step=5.0, key=f"pvt_{choice}")
            st.number_input("Digit recall (longest list)", 3.0, 15.0, float(t["digits"]),
                            step=1.0, key=f"dig_{choice}")

        st.checkbox("I am healthy and rested right now", key=f"healthy_{choice}")
        st.form_submit_button("Save baseline", on_click=save_cb, args=(choice,))

    with st.expander("Delete this profile"):
        ok = st.checkbox("Yes, delete it", key=f"del_{choice}")
        st.button("Delete profile", disabled=not ok, on_click=delete_cb,
                  args=(choice,), key="delete_profile_btn")

st.page_link("pages/homepage.py", label="Back to home")