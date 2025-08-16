# detection/model.py
import os
from ultralytics import YOLO

best_model_path = os.path.join("main", "model", "xdet-v1-model.pt")

# load once when the app starts (fast inference)
model = YOLO(best_model_path)

def run_inference(image_path):
    """Run YOLO on an image and return prediction results."""
    results = model.predict(image_path, save=True)  # save=True will store results/runs
    output = []

    for r in results:
        if r.probs is not None:  # classification mode
            pred_index = r.probs.top1
            pred_name = r.names[pred_index]
            confidence = r.probs.top1conf.item()
            output.append({
                "label": pred_name,
                "confidence": confidence
            })
        else:  # detection mode (boxes)
            for box in r.boxes:
                cls_id = int(box.cls[0])
                label = r.names[cls_id]
                conf = float(box.conf[0])
                output.append({
                    "label": label,
                    "confidence": conf
                })
    return output
