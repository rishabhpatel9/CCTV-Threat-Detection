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

## Features to be added

- Smoke/Fire Detection (Environmental Safety): Could use datasets like FireNet or Smoke Detection Dataset (Kaggle).
- Abandoned Object Detection: use COCO/Open Images for “bag/backpack” detection and then apply anomaly logic (bag present without person).
- Restricted Zones / Tripwires: This is a post-processing feature to be added later by defining geofences in Streamlit/FastAPI pipeline.