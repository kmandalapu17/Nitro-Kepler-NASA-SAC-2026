import streamlit as st

# Single-line text input
name = st.text_input("Enter your name:")

# Number input with constraints
age = st.number_input("Enter your age:", min_value=1, max_value=120, step=1)

# Display output
if name:
    st.write(f"No, {name}!")
if age:
    st.write(f"Your uncness is {age}.")

# Button to trigger specific action
if st.button("Submit"):
    st.write(f"Submitted: {name}, Uncness: {age}")