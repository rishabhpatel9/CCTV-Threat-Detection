## Planned Architecture

### 1. Object Detection & Tracking (YOLOv8 + DeepSORT)
**Purpose:** Detect and track people, vehicles, and weapons.\
**Model:** YOLOv8 fine-tuned on [CCTV Weapon Dataset](https://huggingface.co/datasets/Simuletic/cctv-weapon-dataset)\
**Output:** Bounding boxes + IDs for individuals and objects.

Why separate? Object detection is spatial (bounding boxes), while behavior recognition is temporal (motion patterns).

### 2. Action Recognition (Violence, Fighting, Running, Loitering)
**Purpose:** Classify suspicious behaviors.\
**Model:** Action recognition networks (like SlowFast, I3D, ConvLSTM). (yet to be finalized)\
**Datasets:** Violence detection dataset (e.g., [UCF Crime Dataset](https://www.kaggle.com/datasets/odins0n/ucf-crime-dataset), [Smart-City CCTV Violence Detection Dataset (SCVD)](https://www.kaggle.com/datasets/toluwaniaremu/smartcity-cctv-violence-detection-dataset-scvd)).\
**Output:** Labels like “fighting,” “running,” “loitering.”

### 3. Anomaly Detection (Abandoned Objects, Unusual Motion)
**Purpose:** Detect anomalies not explicitly labeled.\
**Model:** Autoencoders or one-class SVMs trained on “normal” CCTV footage.\
**Output:** Flags unusual activity (e.g., bag left behind, erratic movement).

### 4. Fusion Layer (Threat Scoring)
**Purpose:** Combine outputs from all modules.\
**Implementation:** Lightweight rule-based system or ensemble classifier.\
**Logic Example:**
- Person + weapon → High threat.
- Group + aggressive gestures → Violence alert.
- Person + abnormal dwell time → Loitering alert.

### 5. Alert System (Deployment)

- FastAPI backend serves inference results.
- Streamlit frontend displays live CCTV feed + alerts.
- Dockerized for reproducibility


                ┌───────────────────────┐
                │   CCTV Video Stream   │
                └───────────┬───────────┘
                            │
                            ▼
                ┌───────────────────────┐
                │   YOLOv8 Object       │
                │   Detection           │
                │   (people, weapons,   │
                │   vehicles, objects)  │
                └───────────┬───────────┘
                            │
                            ▼
                ┌───────────────────────┐
                │   DeepSORT Tracking   │
                │   (IDs across frames) │
                └───────────┬───────────┘
                            │
                            ▼
                ┌───────────────────────┐
                │   Action Recognition  │
                │   (fighting, running, │
                │   loitering)          │
                └───────────┬───────────┘
                            │
                            ▼
                ┌───────────────────────┐
                │   Anomaly Detection   │
                │   (abandoned objects, │
                │   unusual motion)     │
                └───────────┬───────────┘
                            │
                            ▼
                ┌───────────────────────┐
                │   Fusion Layer        │
                │   Threat Scoring      │
                │   (rules + ensemble)  │
                └───────────┬───────────┘
                            │
                            ▼
                ┌───────────────────────┐
                │   Alert System        │
                │   (Streamlit UI,      │
                │   FastAPI API,        │
                │   logs, notifications)│
                └───────────────────────┘

## Datasets

1. [Hugging Face - Simuletic/cctv-weapon-dataset](https://huggingface.co/datasets/Simuletic/cctv-weapon-dataset)
2. [Kaggle - UCF Crime Dataset](https://www.kaggle.com/datasets/odins0n/ucf-crime-dataset)
3. [Kaggle - Smart-City CCTV Violence Detection Dataset (SCVD)](https://www.kaggle.com/datasets/toluwaniaremu/smartcity-cctv-violence-detection-dataset-scvd)

## Features covered by datasets

- Weapons detection → Simuletic dataset.
- Violence/fighting detection → SCVD + UCF-Crime.
- Loitering/anomaly detection → UCF-Crime (loitering, abnormal events).
- General suspicious behavior → UCF-Crime (multiple anomaly categories).

## Future Work

- Improve violence-detection-slowfast model by training on SCVD + UCF-Crime datasets.
- Violence/Fighting Detection Model - Use YOLOv8 as a preprocessing step to detect and crop people from frames before feeding them into an action recognition model. This can improve accuracy by focusing on human regions instead of background noise.
- Anomaly/Loitering Detection Model - YOLOv8 can again be used as a supporting module to detect people and track them with DeepSORT.Feed tracked trajectories into anomaly detection (e.g., loitering = person stays in same region too long). This helps with object/person localization.
- Vehicle Detection: use COCO/Open Images for “car,” “truck,” “bus” classes.
- Smoke/Fire Detection (Environmental Safety): Could use datasets like FireNet or Smoke Detection Dataset (Kaggle).
- Abandoned Object Detection: use COCO/Open Images for “bag/backpack” detection and then apply anomaly logic (bag present without person).
- Restricted Zones / Tripwires: This is a post-processing feature to be added later by defining geofences in Streamlit/FastAPI pipeline.