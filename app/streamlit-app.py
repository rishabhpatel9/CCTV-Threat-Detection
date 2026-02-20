import streamlit as st
import requests
from PIL import Image

st.title("CCTV Threat Detection Fusion Layer")

uploaded_file = st.file_uploader("Upload a video/frame", type=["mp4","avi","png","jpg","jpeg"])

if uploaded_file:
    if uploaded_file.type.startswith("video"):
        st.video(uploaded_file)
    else:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Frame", width=600)

    if st.button("Run Detection"):
        files = {"file": uploaded_file.getbuffer()}
        response = requests.post("http://localhost:8000/predict", files=files)

        try:
            result = response.json()
        except Exception:
            st.error("API did not return valid JSON. Check FastAPI logs for details.")
            st.stop()

        decision = result["fusion_decision"]

        st.subheader("Fusion Results")
        st.write("Weapon Confidence:", result["weapon_conf"])
        st.progress(int(result["weapon_conf"] * 100))
        st.write("Violence Confidence:", result["violence_conf"])
        st.progress(int(result["violence_conf"] * 100))
        st.write("Anomaly Score:", result["anomaly_score"])
        st.progress(int(result["anomaly_score"] * 100))

        # Color-coded badge
        if "Safe" in decision:
            st.success(f"Fusion Decision: {decision}")
        else:
            st.error(f"Fusion Decision: {decision}")
