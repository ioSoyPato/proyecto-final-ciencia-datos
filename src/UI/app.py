import streamlit as st
import requests
import json

st.write("""
# Se calcula la predicción de la temperatura en grados centígrados 
""")

st.sidebar.header('User Input Parameters')

def user_input_features():
    ts = st.sidebar.number_input("ts", value=1594512094.9, min_value=1594512094.385975, max_value=1595203417.264313)
    co = st.sidebar.number_input("co", value=0.001171, min_value=0.001171, max_value=0.01442)
    humidity = st.sidebar.number_input("humidity", value=1.1, min_value=1.1, max_value=99.900002)
    lpg = st.sidebar.number_input("lpg", value=0.002693, min_value=0.002693, max_value=0.016567)
    smoke = st.sidebar.number_input("smoke", value=0.006692, min_value=0.006692, max_value=0.04659)
    light = st.sidebar.radio("light", [True, False], index=0)  # Campo booleano
    motion = st.sidebar.radio("motion", [True, False], index=0)  # Campo booleano

    input_dict = {
        "ts": ts,
        "co": co,
        "humidity": humidity,
        "lpg": lpg,
        "smoke": smoke,
        "light": light,
        "motion": motion
    }

    return input_dict

input_dict = user_input_features()

if st.button('Predict'):
    response = requests.post(
        url="http://localhost:8000/predict",  
        headers={"Content-Type": "application/json"},
        data=json.dumps(input_dict)  
    )

    if response.status_code == 200:
        st.write(f"La temperatura predicha es: **{response.json()['prediction']} grados centígrados**")
    else:
        st.write("Error en la predicción.")
        st.write(f"Detalle del error: {response}")
