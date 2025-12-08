import cv2
import sys
import os
from ultralytics import YOLO
import numpy as np

def process_media(input_path, output_path):
    """
    Process image or video for pet and human detection
    """
    print(f"[INFO] Starting processing: {input_path}")
    
    # Load YOLOv8 model
    print("[INFO] Loading YOLOv8 model...")
    model = YOLO("yolov8n.pt")
    
    # Get class names
    class_names = model.names
    
    # Human and pet class IDs (COCO dataset)
    HUMAN_CLASSES = [0]  # person
    PET_CLASSES = [15, 16]  # cat, dog
    
    print(f"[INFO] Human classes: {[class_names[i] for i in HUMAN_CLASSES]}")
    print(f"[INFO] Pet classes: {[class_names[i] for i in PET_CLASSES]}")
    
    # Check if input is image or video
    is_image = input_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))
    
    if is_image:
        process_image(input_path, output_path, model, class_names, HUMAN_CLASSES, PET_CLASSES)
    else:
        process_video(input_path, output_path, model, class_names, HUMAN_CLASSES, PET_CLASSES)

def process_image(input_path, output_path, model, class_names, HUMAN_CLASSES, PET_CLASSES):
    """
    Process a single image
    """
    print("[INFO] Processing image...")
    
    # Read image
    frame = cv2.imread(input_path)
    if frame is None:
        print(f"[ERROR] Could not read image: {input_path}")
        sys.exit(1)
    
    # Run YOLO inference
    results = model(frame, verbose=False)
    detections = results[0].boxes.data.cpu().numpy()
    
    pets_detected = 0
    humans_detected = 0
    
    # Draw detections on the original frame (not the annotated one)
    for det in detections:
        x1, y1, x2, y2, conf, cls_id = det
        cls_id = int(cls_id)
        label = class_names.get(cls_id, "Unknown")
        
        if cls_id in HUMAN_CLASSES:
            color = (0, 255, 0)  # Green for humans
            humans_detected += 1
        elif cls_id in PET_CLASSES:
            color = (255, 0, 0)  # Blue for pets (BGR format)
            pets_detected += 1
        else:
            continue
        
        # Draw bounding box
        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, 3)
        
        # Draw label with background
        text = f"{label} {conf:.2f}"
        (text_width, text_height), baseline = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
        cv2.rectangle(frame, (int(x1), int(y1) - text_height - 10), 
                     (int(x1) + text_width, int(y1)), color, -1)
        cv2.putText(frame, text, (int(x1), int(y1) - 5),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    # Add summary text
    summary = f"Pets: {pets_detected} | Humans: {humans_detected}"
    cv2.putText(frame, summary, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    
    # Save output image
    cv2.imwrite(output_path, frame)
    
    print(f"[INFO] Total frames: 1")
    print(f"[INFO] Pet alerts: {pets_detected}")
    print(f"[INFO] Humans detected: {humans_detected}")
    print(f"[INFO] Output saved: {output_path}")

def process_video(input_path, output_path, model, class_names, HUMAN_CLASSES, PET_CLASSES):
    """
    Process a video file
    """
    print("[INFO] Processing video...")
    
    # Open video
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        print(f"[ERROR] Could not open video: {input_path}")
        sys.exit(1)
    
    # Get video properties
    fps = int(cap.get(cv2.CAP_PROP_FPS)) or 20
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    print(f"[INFO] Video properties: {width}x{height} @ {fps}fps, {total_frames} frames")
    
    # Create video writer with universally compatible codecs
    # Try codecs in order of compatibility
    codecs_to_try = [
        ('mp4v', 'MPEG-4'),
        ('MJPG', 'Motion JPEG'),
        ('XVID', 'Xvid'),
        ('X264', 'H.264')
    ]
    
    out = None
    used_codec = None
    
    for codec_name, codec_desc in codecs_to_try:
        try:
            fourcc = cv2.VideoWriter_fourcc(*codec_name)
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
            if out.isOpened():
                used_codec = codec_desc
                print(f"[INFO] Using codec: {codec_desc} ({codec_name})")
                break
            else:
                print(f"[INFO] {codec_desc} codec not available, trying next...")
        except:
            print(f"[INFO] Failed to initialize {codec_desc}, trying next...")
            continue
    
    if not out or not out.isOpened():
        print("[ERROR] Could not create video writer with any codec")
        cap.release()
        sys.exit(1)
    
    frame_count = 0
    pet_alert_count = 0
    human_count = 0
    
    # Process each frame
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame_count += 1
        
        # Run YOLO inference on original frame
        results = model(frame, verbose=False)
        detections = results[0].boxes.data.cpu().numpy()
        
        pets_in_frame = False
        humans_in_frame = False
        
        # Draw detections on the original frame (not on annotated result)
        for det in detections:
            x1, y1, x2, y2, conf, cls_id = det
            cls_id = int(cls_id)
            label = class_names.get(cls_id, "Unknown")
            
            if cls_id in HUMAN_CLASSES:
                color = (0, 255, 0)  # Green for humans
                humans_in_frame = True
            elif cls_id in PET_CLASSES:
                color = (255, 0, 0)  # Blue for pets
                pets_in_frame = True
            else:
                continue
            
            # Draw bounding box
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
            
            # Draw label
            text = f"{label} {conf:.2f}"
            cv2.putText(frame, text, (int(x1), int(y1) - 5),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        
        # Count alerts
        if pets_in_frame:
            pet_alert_count += 1
        if humans_in_frame:
            human_count += 1
        
        # Add frame counter
        cv2.putText(frame, f"Frame: {frame_count}/{total_frames}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Write frame
        out.write(frame)
        
        # Progress update
        if frame_count % 30 == 0:
            progress = (frame_count / total_frames) * 100
            print(f"[INFO] Progress: {progress:.1f}% ({frame_count}/{total_frames} frames)")
    
    # Cleanup
    cap.release()
    out.release()
    
    print(f"[INFO] Total frames: {frame_count}")
    print(f"[INFO] Pet alerts: {pet_alert_count}")
    print(f"[INFO] Humans detected: {human_count}")
    print(f"[INFO] Output saved: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python detect.py <input_path> <output_path>")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    
    if not os.path.exists(input_path):
        print(f"[ERROR] Input file not found: {input_path}")
        sys.exit(1)
    
    try:
        process_media(input_path, output_path)
    except Exception as e:
        print(f"[ERROR] Processing failed: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
