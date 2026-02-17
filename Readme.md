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

