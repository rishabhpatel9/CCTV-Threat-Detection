import streamlit as st
import cv2
import requests
from PIL import Image
import io
import time
import threading

st.set_page_config(page_title="Real-Time Threat Detection", layout="wide")
st.title("Live Webcam Threat Detection")
st.write("This app captures live webcam feed and sends frames to the fusion layer API.")

# Option to start/stop the webcam
run = st.checkbox("Turn on Webcam")

# Two columns: one for the video feed and one for the results
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Live Feed")
    # Video frame placeholder
    frame_window = st.image([])

with col2:
    st.subheader("Real-Time Analysis")
    # Placeholders for metrics to update dynamically
    decision_placeholder = st.empty()
    st.write("---")
    weapon_placeholder = st.empty()
    violence_placeholder = st.empty()
    anomaly_placeholder = st.empty()

# Open the default camera (index 0)
camera = cv2.VideoCapture(0)

# To avoid sending every single frame and overloading the API, adding a small delay
frame_skip = 5  # send every 5th frame to the API
frame_count = 0

# Keep track of the last known boxes to draw them smoothly between API calls
latest_boxes = []

# Container to hold results from the background thread
result_container = {"result": None, "error": False, "new_data": False}
api_thread = None

def fetch_api(files_data):
    try:
        response = requests.post("http://localhost:8000/predict", files=files_data, timeout=2.0)
        if response.status_code == 200:
            result_container["result"] = response.json()
            result_container["error"] = False
            result_container["new_data"] = True
    except requests.exceptions.RequestException:
        result_container["error"] = True
        result_container["new_data"] = True

while run:
    success, frame = camera.read()
    if not success:
        st.error("Failed to read from webcam.")
        break
    
    # Convert color space from BGR (OpenCV default) to RGB (Streamlit/Image default)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    for box in latest_boxes:
        x1, y1, x2, y2 = box['x1'], box['y1'], box['x2'], box['y2']
        conf = box['conf']
        class_name = box.get('class_name', 'Weapon').capitalize()
        
        # Draw red rectangle for weapon, green for person
        color = (0, 255, 0) if class_name.lower() == 'person' else (255, 0, 0)
        
        cv2.rectangle(frame_rgb, (x1, y1), (x2, y2), color, 2)
        # Add confidence label
        cv2.putText(frame_rgb, f"{class_name}: {conf:.2f}", (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    # Update image placeholder with the current frame
    frame_window.image(frame_rgb)
    
    # Process only every N frames to keep it running smoothly
    if frame_count % frame_skip == 0:
        # Only start a new thread if one isn't currently running
        if api_thread is None or not api_thread.is_alive():
            # Convert frame to bytes and send to the current API
            img = Image.fromarray(frame_rgb)
            buf = io.BytesIO()
            img.save(buf, format="JPEG")
            file_bytes = buf.getvalue()
            
            files = {"file": ("frame.jpg", file_bytes, "image/jpeg")}
            
            api_thread = threading.Thread(target=fetch_api, args=(files,))
            api_thread.start()

    # Update UI based on whatever the latest result is
    if result_container["new_data"]:
        if result_container["error"]:
            decision_placeholder.error("API disconnected or timed out.")
        elif result_container["result"]:
            result = result_container["result"]
            decision = result.get("fusion_decision", "Unknown")
            latest_boxes = result.get("weapon_boxes", [])
            
            # Update UI with color coding based on severity
            if "Safe" in decision:
                decision_placeholder.success(f"**Status:** {decision}")
            elif "Warning" in decision:
                decision_placeholder.warning(f"**Status:** {decision}")
            else:
                decision_placeholder.error(f"**Status:** {decision}")
            
            # Update metrics dynamically
            weapon_placeholder.metric("Weapon Confidence", f"{result.get('weapon_conf', 0.0):.2f}")
            violence_placeholder.metric("Violence Confidence", f"{result.get('violence_conf', 0.0):.2f}")
            anomaly_placeholder.metric("Anomaly Score", f"{result.get('anomaly_score', 0.0):.2f}")
            
        result_container["new_data"] = False
            
    frame_count += 1
    
    # Add a tiny sleep to let Streamlit catch its breath and render the UI
    time.sleep(0.01)

else:
    st.write("Webcam stopped.")
    if camera.isOpened():
        camera.release()
