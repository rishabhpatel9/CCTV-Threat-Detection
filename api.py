from fastapi import FastAPI, UploadFile
from pydantic import BaseModel
import torch
import torch.nn as nn
from ultralytics import YOLO

app = FastAPI()

# Load Weapons detection model (YOLOv8)
weapon_model = YOLO("Notebooks/yolov8n.pt")

# Load Violence detection model (SlowFast)
violence_model = torch.hub.load('facebookresearch/pytorchvideo', 'slowfast_r50', pretrained=False)
violence_model.blocks[-1].proj = nn.Linear(violence_model.blocks[-1].proj.in_features, 3)
violence_model.load_state_dict(torch.load(r"Notebooks/violence-detection-slowfast-model.pth"))
violence_model.eval()

# Define Autoencoder for Anomaly detection
class Autoencoder(nn.Module):
    def __init__(self, input_dim=2048, hidden_dim=512):
        super(Autoencoder, self).__init__()
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim//2),
            nn.ReLU()
        )
        self.decoder = nn.Sequential(
            nn.Linear(hidden_dim//2, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, input_dim)
        )

    def forward(self, x):
        z = self.encoder(x)
        return self.decoder(z)

# Load Anomaly detection model (Autoencoder)
anomaly_model = Autoencoder()
anomaly_model.load_state_dict(torch.load("Notebooks/autoencoder_ucfcrime_epoch10.pth"))
anomaly_model.eval()

# Rule-based fusion
def fusion_rule(weapon_conf, violence_conf, anomaly_score,
                weapon_thresh=0.5, violence_thresh=0.5, anomaly_thresh=0.5):
    if weapon_conf >= weapon_thresh:
        return "Threat detected! : Weapon"
    elif violence_conf >= violence_thresh:
        return "Threat detected! : Violence"
    elif anomaly_score >= anomaly_thresh:
        return "Threat detected! : Anomaly"
    else:
        return "Safe"

class FusionResponse(BaseModel):
    weapon_conf: float
    violence_conf: float
    anomaly_score: float
    fusion_decision: str

@app.post("/predict", response_model=FusionResponse)
async def predict(file: UploadFile):
    try:
        # TODO: preprocess frames/video and run models
        # For now, return dummy values to avoid JSONDecodeError
        weapon_conf = 0.0
        violence_conf = 0.0
        anomaly_score = 0.0
        decision = fusion_rule(weapon_conf, violence_conf, anomaly_score)

        return FusionResponse(
            weapon_conf=weapon_conf,
            violence_conf=violence_conf,
            anomaly_score=anomaly_score,
            fusion_decision=decision
        )
    except Exception as e:
        return {"error": str(e)}
