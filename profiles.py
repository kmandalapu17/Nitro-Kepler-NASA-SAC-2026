import json
from pathlib import Path
import streamlit as st
from vitals import DEFAULT_BASELINE

PROFILE_FILE = Path(__file__).parent / "profiles.json"

# one source of truth for defaults
DEFAULT_VITALS = {k: v["base"] for k, v in DEFAULT_BASELINE.items()}
DEFAULT_TESTS = {"pulse": 65, "balance": 20, "grip": 40, "weight": 75,
                 "sit_stand": 15, "pvt": 300, "digits": 7}


def load_profiles():
    if PROFILE_FILE.exists():
        try:
            return json.loads(PROFILE_FILE.read_text())
        except json.JSONDecodeError:
            return {}
    return {}


def save_profiles(profiles):
    PROFILE_FILE.write_text(json.dumps(profiles, indent=2))


def set_active(name):
    st.session_state.active_profile = name


def get_active_profile():
    """Returns (name, profile_dict), or (None, None) if nothing is selected."""
    profiles = load_profiles()
    name = st.session_state.get("active_profile")
    if name in profiles:
        return name, profiles[name]
    return None, None


def get_vital_baselines():
    _, p = get_active_profile()
    base = dict(DEFAULT_VITALS)
    if p:
        base.update(p.get("vitals", {}))
    return base


def get_test_baselines():
    _, p = get_active_profile()
    base = dict(DEFAULT_TESTS)
    if p:
        base.update(p.get("tests", {}))
    return base


def profile_banner():
    """Call near the top of any page to show which profile is in use."""
    name, p = get_active_profile()
    if not name:
        st.warning("No astronaut profile selected. Using default values.")
        st.page_link("pages/profile.py", label="Set up a profile")
    elif not p.get("baseline_set"):
        st.warning(f"Profile **{name}** is still using default values. "
                   "Enter your healthy baseline.")
        st.page_link("pages/profile.py", label="Set baseline")
    else:
        st.caption(f"Active profile: {name}")