import os
from huggingface_hub import hf_hub_download

def download_models():
    # Downloads the necessary large model files from Hugging Face Hub if they don't exist locally.
    repo_id = "rishp9/CCTV-Threat-Detection-Models"  # Updated repository name
    models_dir = os.path.join(os.path.dirname(__file__), "models")
    
    # List of required models to download
    models = [
        "violence-detection-slowfast-model.pth",
        "anamoly-detection-model-epoch10.pth",
        "weapon-detection-model-mark2.pt"
    ]
    
    if not os.path.exists(models_dir):
        os.makedirs(models_dir)
        
    print("Checking for required models...")
    for model_file in models:
        model_path = os.path.join(models_dir, model_file)
        if not os.path.exists(model_path):
            print(f"Downloading {model_file} from Hugging Face Hub...")
            try:
                hf_hub_download(
                    repo_id=repo_id,
                    filename=model_file,
                    local_dir=models_dir,
                    local_dir_use_symlinks=False
                )
                print(f"Successfully downloaded {model_file}")
            except Exception as e:
                print(f"Error downloading {model_file}: {e}")
                print(f"Please ensure {model_file} is available at huggingface.co/{repo_id}")
        else:
            print(f"Model {model_file} already exists.")

if __name__ == "__main__":
    download_models()
