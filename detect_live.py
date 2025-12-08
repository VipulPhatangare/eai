import cv2
import sys
import json
from ultralytics import YOLO
import numpy as np

def detect_live_frame(frame_path):
    """
    Process a single frame for real-time detection
    """
    # Load YOLOv8 model
    model = YOLO("yolov8n.pt")
    
    # Get class names
    class_names = model.names
    
    # Human and pet class IDs
    HUMAN_CLASSES = [0]  # person
    PET_CLASSES = [15, 16]  # cat, dog
    
    # Read frame
    frame = cv2.imread(frame_path)
    if frame is None:
        print(json.dumps({"error": "Could not read frame"}))
        sys.exit(1)
    
    # Run YOLO inference
    results = model(frame, verbose=False)
    detections = results[0].boxes.data.cpu().numpy()
    
    pets_count = 0
    humans_count = 0
    detection_list = []
    
    # Draw detections
    for det in detections:
        x1, y1, x2, y2, conf, cls_id = det
        cls_id = int(cls_id)
        label = class_names.get(cls_id, "Unknown")
        
        if cls_id in HUMAN_CLASSES:
            color = (0, 255, 0)  # Green for humans
            humans_count += 1
            detection_type = "human"
        elif cls_id in PET_CLASSES:
            color = (255, 0, 0)  # Blue for pets
            pets_count += 1
            detection_type = "pet"
        else:
            continue
        
        # Draw bounding box
        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
        
        # Draw label with background
        text = f"{label} {conf:.2f}"
        (text_width, text_height), baseline = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
        cv2.rectangle(frame, (int(x1), int(y1) - text_height - 5), 
                     (int(x1) + text_width, int(y1)), color, -1)
        cv2.putText(frame, text, (int(x1), int(y1) - 3),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        detection_list.append({
            "type": detection_type,
            "label": label,
            "confidence": float(conf),
            "bbox": [int(x1), int(y1), int(x2), int(y2)]
        })
    
    # Add live indicator
    cv2.putText(frame, "🔴 LIVE", (10, 30),
               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    
    # Add detection counts
    status_text = f"Pets: {pets_count} | Humans: {humans_count}"
    cv2.putText(frame, status_text, (10, 60),
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    # Save processed frame (overwrite input)
    cv2.imwrite(frame_path, frame)
    
    # Output detection info as JSON
    result = {
        "pets": pets_count,
        "humans": humans_count,
        "detections": detection_list
    }
    print(json.dumps(result))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(json.dumps({"error": "Usage: python detect_live.py <frame_path>"}))
        sys.exit(1)
    
    frame_path = sys.argv[1]
    
    try:
        detect_live_frame(frame_path)
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)
