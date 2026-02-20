from fastapi import FastAPI, UploadFile
from pydantic import BaseModel
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from PIL import Image
import io
from ultralytics import YOLO

app = FastAPI()
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load Weapons detection model (YOLOv8)
weapon_model = YOLO("Notebooks/yolov8n.pt")

# Load Violence detection model (SlowFast)
violence_model = torch.hub.load('facebookresearch/pytorchvideo', 'slowfast_r50', pretrained=False)
violence_model.blocks[-1].proj = nn.Linear(violence_model.blocks[-1].proj.in_features, 3)
violence_model.load_state_dict(torch.load(r"Notebooks/violence-detection-slowfast-model.pth", map_location=device))
violence_model.eval().to(device)

# Load I3D feature extractor for anomaly detection
i3d = torch.hub.load('facebookresearch/pytorchvideo', 'i3d_r50', pretrained=True)
i3d.blocks[-1].proj = nn.Identity()  # remove classifier head
i3d = i3d.to(device)
i3d.eval()

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
anomaly_model = Autoencoder().to(device)
anomaly_model.load_state_dict(torch.load("Notebooks/autoencoder_ucfcrime_epoch10.pth", map_location=device))
anomaly_model.eval()

# Preprocessing
transform = transforms.Compose([
    transforms.Resize((224,224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.45,0.45,0.45], std=[0.225,0.225,0.225])
])

# def preprocess_image(contents):
#     image = Image.open(io.BytesIO(contents)).convert("RGB")
#     return transform(image).unsqueeze(0).to(device)  # (1, C, H, W)

# for testing images - to remove
def preprocess_image(contents, num_frames=8):
    image = Image.open(io.BytesIO(contents)).convert("RGB")
    frame = transform(image)  # shape (3, H, W)

    # Repeat the frame along the temporal dimension
    clip = frame.unsqueeze(1).repeat(1, num_frames, 1, 1)  # (3, T, H, W)

    return clip.unsqueeze(0).to(device)  # (1, 3, T, H, W)

# Inference Functions
def run_weapon_model(file_bytes):
    image = Image.open(io.BytesIO(file_bytes)).convert("RGB")
    results = weapon_model(image, device="cpu")
    confs = [box.conf.item() for box in results[0].boxes]
    return max(confs) if confs else 0.0

def run_violence_model(tensor):
    # with torch.no_grad():
    #     # SlowFast expects [slow_pathway, fast_pathway]
    #     inputs = [tensor, tensor]  
    #     logits = violence_model(inputs)  # shape (1,3)
    #     probs = torch.softmax(logits, dim=1)
    # return probs[0,1].item()  # violence probability    
    return 0.0

# def run_anomaly_model(tensor):
#     with torch.no_grad():
#         # Extract I3D features
#         features = i3d(tensor)              # shape (1, 2048)
#         features = features.view(features.size(0), -1)

#         # Autoencoder reconstruction
#         outputs = anomaly_model(features)
#         loss = torch.mean((outputs - features)**2, dim=1)

#     return loss.item()

# for testing images - to remove
def run_anomaly_model(tensor):
    with torch.no_grad():
        features = i3d(tensor)              # shape (1, 2048)
        features = features.view(features.size(0), -1)
        outputs = anomaly_model(features)
        loss = torch.mean((outputs - features)**2, dim=1)
    return loss.item()


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

# API Endpoint
@app.post("/predict", response_model=FusionResponse)
async def predict(file: UploadFile):
    try:
        contents = await file.read()

        # Preprocess
        tensor = preprocess_image(contents)

        # Run models
        weapon_conf = run_weapon_model(contents)

        # SlowFast expects a list of tensors (slow + fast pathways)
        violence_conf = run_violence_model([tensor, tensor])

        anomaly_score = run_anomaly_model(tensor)

        # Fusion
        decision = fusion_rule(weapon_conf, violence_conf, anomaly_score)

        return FusionResponse(
            weapon_conf=weapon_conf,
            violence_conf=violence_conf,
            anomaly_score=anomaly_score,
            fusion_decision=decision
        )
    except Exception as e:
        # Always return a valid FusionResponse, even on error
        return FusionResponse(
            weapon_conf=0.0,
            violence_conf=0.0,
            anomaly_score=0.0,
            fusion_decision=f"Error: {str(e)}"
        )
