# CCTV Threat Detection

![Python](https://img.shields.io/badge/python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-API-green)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-red)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Object%20Detection-blueviolet)
![Docker](https://img.shields.io/badge/Docker-Containerization-blue)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow)

## Overview

An intelligent end-to-end computer vision pipeline designed to analyze CCTV video feeds in real-time. By combining multiple AI models, the system automatically detects potential security threats such as drawn weapons, physical violence, and unusual activities, instantly flagging dangers and presenting the alerts through an easy-to-use web interface and robust API.

---

## Examples

<div align="center">

<table>
  <tr>
    <td align="center" width="33%"><img src="Example GIFs/Weapon-example-compressed.gif" width="100%" alt="Weapon Example" /></td>
    <td align="center" width="33%"><img src="Example GIFs/Violence-example-compressed.gif" width="100%" alt="Violence Example" /></td>
    <td align="center" width="33%"><img src="Example GIFs/Safe-example-compressed.gif" width="100%" alt="Safe Example" /></td>
  </tr>
  <tr>
    <td align="center"><b>Weapon Detection Example</b></td>
    <td align="center"><b>Violence Detection Example</b></td>
    <td align="center"><b>Safe Scenario Example</b></td>
  </tr>
  <tr>
    <td align="center" colspan="3"><img src="Example GIFs/webcam-example.gif" width="90%" alt="Webcam Live Stream Detection Example" /></td>
  </tr>
  <tr>
    <td align="center" colspan="3"><b>Webcam Live Stream Detection Example</b></td>
  </tr>
</table>

</div>

---

## Datasets & Capabilities

This project utilizes several datasets for model training and evaluation:\
1a. [Roboflow - Weapon Detection CCTV v3](https://universe.roboflow.com/weapon-detection-cctv/weapon-detection-cctv-v3-dataset) - **Weapons detection (in use)**\
1b. [Hugging Face - Simuletic/cctv-weapon-dataset](https://huggingface.co/datasets/Simuletic/cctv-weapon-dataset) - **Weapons detection (simuletic dataset) alternate model**\
2. [Kaggle - Smart-City CCTV Violence Detection Dataset (SCVD)](https://www.kaggle.com/datasets/toluwaniaremu/smartcity-cctv-violence-detection-dataset-scvd) - **Violence/fighting detection**\
3. [Kaggle - UCF Crime Dataset](https://www.kaggle.com/datasets/odins0n/ucf-crime-dataset) - **Anomaly detection** (e.g., assault, burglary, arson, etc.)

---

## Project Features

- **Spatial Object Detection (weapons/people):** Utilizes YOLOv8 to detect and track entities such as people and weapons in images.
- **Temporal Action Recognition (violence):** Employs a SlowFast model to analyze sequential motion and classify behaviors such as "violence" or "fighting".
- **Anomaly Detection:** Identifies unspecified unusual behaviors including Abuse, Arrest, Arson, Assault, Burglary, Explosion, RoadAccidents, Robbery, Shooting, Shoplifting, Stealing, and Vandalism.
- **Fusion Layer (Threat Scoring):** Features an intelligent rule based evaluation that synthesizes outputs from various detection modules into a final unified threat score.
- **FastAPI Inference Backend:** A robust, high performance API server processing images and executing simultaneous multi-model inferences.
- **Streamlit Frontend Applications:** Streamlit frontend for live stream analysis and an alternate UI to upload images and videos to see the detection in action.

---

## Project Architecture

```text
               ┌─────────────────────────────────────┐
               │      Streamlit Frontend Apps        │
               │    (Live Stream UI & Upload UI)     │
               └─────────────────┬───────────────────┘
                                 │
                                 ▼
               ┌─────────────────────────────────────┐
               │        FastAPI Inference API        │
               │ (Simultaneous multi-model inference)│
               └─────────────────┬───────────────────┘
                                 │
             ┌───────────────────┼───────────────────┐
             ▼                   ▼                   ▼
┌──────────────────────┐ ┌───────────────┐ ┌──────────────────┐
│     YOLOv8 Object    │ │   SlowFast    │ │      Anomaly     │
│      Detection       │ │    Action     │ │     Detection    │
│  (People, Weapons)   │ │  Recognition  │ │ (Abuse, Arson,   │
│                      │ │  (Violence)   │ │  Burglary, etc.) │
└────────────┬─────────┘ └───────┬───────┘ └─────────┬────────┘
             │                   │                   │
             └───────────────────┼───────────────────┘
                                 ▼
               ┌─────────────────────────────────────┐
               │     Fusion Layer Threat Scoring     │
               │   (Rules & Ensembled Threat Score)  │
               └─────────────────┬───────────────────┘
                                 │
                                 ▼
               ┌─────────────────────────────────────┐
               │      Alert & Monitoring System      │
               │      (UI feedback, logs, APIs)      │
               └─────────────────────────────────────┘
```

## Project Structure

```bash
CCTV-Threat-Detection/
├── app/
│   ├── streamlit-app.py                    # UI to upload images/videos
│   └── streamlit-webcam.py                 # Live stream analysis UI
├── Data/                                   # Data directory
├── Example GIFs/                           # Example GIFs for Readme.md
├── Notebooks/                              # Jupyter Notebooks and Models
│   ├── Rule-Based-Threat-Detection.ipynb
│   ├── anamoly-detection-model.ipynb
│   ├── violence-detection-i3d.ipynb
│   ├── violence-detection-slowfast.ipynb
│   ├── weapon-detection-model-mark2.ipynb
│   ├── weapon-detection-model-simuletic.ipynb
│   └── *.pth / *.pt                        # Pre-trained models (LFS)
├── .gitattributes
├── .gitignore
├── api.py                                  # FastAPI backend
├── LICENSE
├── Readme.md
└── requirements.txt
```

---

## Installation

### Local Installation

Clone the repo:

```bash
git clone https://github.com/rishabhpatel9/CCTV-Threat-Detection.git
cd CCTV-Threat-Detection
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run FastAPI backend:

```bash
uvicorn api:app --reload
```

Run Streamlit frontend:

```bash
streamlit run app/streamlit_app.py
```

### Deployment with Docker

You can easily spin up the entire pipeline (API + Frontend UIs) using the included `docker-compose.yml` file:

1. Build and run the containers:
   ```bash
   docker-compose up --build
   ```
2. The services will be available at:
   - **FastAPI Backend**: http://localhost:8000
   - **Streamlit Frontend (Image/Video Upload)**: http://localhost:8501
   - **Streamlit Frontend (Webcam Live Stream)**: http://localhost:8502
   
To stop the services, run:
```bash
docker-compose down
```

---

## Releases

* **v1.0.0** → Initial Version with core pipeline and Streamlit dashboard. Analyzes uploaded images for weapons, violence, and anomalies.
* **v2.0.0** → Updated Version with video processing + image processing pipeline and a secondary Streamlit dashboard for live stream analysis.

---

## Future Work


- **Dockerized Deployment**: Containerize the FastAPI backend and Streamlit frontend using Docker and Docker Compose for easier deployment and scalability.
- **Render Deployment**: Deploy the FastAPI backend and Streamlit frontend on Render for easy cloud hosting and public accessibility.
- **Improve violence-detection-slowfast model** by training on SCVD + UCF-Crime datasets.
- **Violence/Fighting Detection Model** - Use YOLOv8 as a preprocessing step to detect and crop people from frames before feeding them into an action recognition model. This can improve accuracy by focusing on human regions instead of background noise.
- **Anomaly/Loitering Detection Model** - YOLOv8 can again be used as a supporting module to detect people and track them with DeepSORT. Feed tracked trajectories into anomaly detection (e.g., loitering = person stays in same region too long). This helps with object/person localization.
- **Vehicle Detection**: use COCO/Open Images for “car,” “truck,” “bus” classes.
- **Smoke/Fire Detection (Environmental Safety)**: Could use datasets like FireNet or Smoke Detection Dataset (Kaggle).
- **Abandoned Object Detection**: use COCO/Open Images for “bag/backpack” detection and then apply anomaly logic (bag present without person).
- **Restricted Zones / Tripwires**: This is a post-processing feature to be added later by defining geofences in Streamlit/FastAPI pipeline.

---

## Contributing

Contributions are welcome!

* Fork the repo
* Create a feature branch
* Submit a pull request