import random, time
import streamlit as st

BASELINE = {   # placeholders: a clinician (or the astronaut's own data) sets real values
    "heart_rate": dict(base=65,  noise=2,   margin=15,  unit="bpm",  crit=(40, 130)),
    "spo2":       dict(base=97,  noise=0.5, margin=3,   unit="%",    crit=(90, None)),
    "temp":       dict(base=36.8,noise=0.1, margin=0.9, unit="°C",   crit=(None, 39.0)),
    "resp_rate":  dict(base=14,  noise=1,   margin=5,   unit="/min", crit=(8, 28)),
    "systolic":   dict(base=118, noise=3,   margin=20,  unit="mmHg", crit=(80, 180)),
}

# how far each vital drifts from baseline once the scenario kicks in
SCENARIOS = {
    "Normal": {},
    "Hypoxia / high CO2": {"spo2": -8, "heart_rate": +20, "resp_rate": +8},
    "Fever / infection": {"temp": +1.6, "heart_rate": +18},
    "Cardiovascular strain": {"heart_rate": +30, "systolic": -35},
    "Sensor glitch (one bad reading)": {},
}

def read_vitals(scenario, tick, ramp_start=5, ramp_len=5):
    frac = min(max((tick - ramp_start) / ramp_len, 0), 1)   # 0 -> 1 gradual change
    out = {}
    for name, v in BASELINE.items():
        shift = SCENARIOS[scenario].get(name, 0) * frac
        out[name] = round(random.gauss(v["base"] + shift, v["noise"]), 1)
    if scenario.startswith("Sensor glitch") and tick == 7:
        out["spo2"] = 92.0                                   # one blip, then back to normal
    return out

def classify(name, value):
    v = BASELINE[name]
    lo, hi = v["crit"]
    if (lo is not None and value < lo) or (hi is not None and value > hi):
        return "critical"
    if abs(value - v["base"]) > v["margin"]:
        return "out"
    return "ok"

WINDOW = 3   # consecutive readings needed before we trust a change

def assess(history):
    flags = {}   # vital -> "red" or "yellow"
    for name in BASELINE:
        recent = [classify(name, h[name]) for h in history[-WINDOW:]]
        last2 = recent[-2:]
        if len(last2) == 2 and all(r == "critical" for r in last2):
            flags[name] = "red"
        elif len(recent) == WINDOW and all(r != "ok" for r in recent):
            flags[name] = "yellow"

    if any(f == "red" for f in flags.values()) or len(flags) >= 2:
        level = "red"
    elif flags:
        level = "yellow"
    else:
        level = "green"
    return level, flags