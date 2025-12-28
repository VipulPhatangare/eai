import cv2
import sys
import os
import subprocess
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
    
    # Use mp4v codec with MP4 container for best compatibility and compression
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    if not out.isOpened():
        print("[ERROR] Could not create video writer with mp4v codec")
        cap.release()
        sys.exit(1)
    
    print(f"[INFO] Using codec: MPEG-4 (mp4v) for MP4 output")
    print(f"[INFO] Note: For smaller file sizes, consider re-encoding with FFmpeg after processing")
    
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
    cv2.destroyAllWindows()
    
    print(f"[INFO] Total frames: {frame_count}")
    print(f"[INFO] Pet alerts: {pet_alert_count}")
    print(f"[INFO] Humans detected: {human_count}")
    print(f"[INFO] Codec used: MPEG-4 (mp4v)")
    
    # Get initial file size
    initial_size = os.path.getsize(output_path) if os.path.exists(output_path) else 0
    print(f"[INFO] Initial output size: {initial_size / (1024*1024):.2f} MB")
    
    # Try to compress with FFmpeg if available
    try:
        # Try to use bundled FFmpeg first (from imageio-ffmpeg package)
        try:
            import imageio_ffmpeg
            ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
            print(f"[INFO] Using bundled FFmpeg: {ffmpeg_path}")
        except ImportError:
            # Fall back to system FFmpeg
            ffmpeg_path = 'ffmpeg'
            # Check if system FFmpeg is available
            ffmpeg_check = subprocess.run([ffmpeg_path, '-version'], 
                                         capture_output=True, 
                                         timeout=2,
                                         creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
            if ffmpeg_check.returncode != 0:
                raise FileNotFoundError("FFmpeg not found")
            print("[INFO] Using system FFmpeg")
        
        print("[INFO] Compressing video with H.264 codec...")
        temp_output = output_path + '.temp.mp4'
        
        # Compress video with H.264 codec (much better compression and browser support)
        compress_cmd = [
            ffmpeg_path, '-i', output_path,
            '-c:v', 'libx264',  # H.264 codec for browser compatibility
            '-preset', 'medium',  # Balance between speed and compression
            '-crf', '23',  # Quality (18-28, lower = better quality, 23 is default)
            '-movflags', '+faststart',  # Enable web streaming
            '-y',  # Overwrite output
            temp_output
        ]
        
        result = subprocess.run(compress_cmd, 
                              capture_output=True, 
                              timeout=300,
                              creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
        
        if result.returncode == 0 and os.path.exists(temp_output):
            # Replace original with compressed version
            os.remove(output_path)
            os.rename(temp_output, output_path)
            
            final_size = os.path.getsize(output_path)
            compression_ratio = (1 - final_size / initial_size) * 100
            print(f"[INFO] ✅ Video compressed successfully with H.264!")
            print(f"[INFO] Final size: {final_size / (1024*1024):.2f} MB")
            print(f"[INFO] Compression: {compression_ratio:.1f}% smaller")
            print(f"[INFO] Video is now browser-compatible!")
        else:
            print(f"[WARNING] FFmpeg compression failed, using original video")
            print(f"[WARNING] Browser playback may not work with mp4v codec")
            if os.path.exists(temp_output):
                os.remove(temp_output)
            
    except (subprocess.TimeoutExpired, FileNotFoundError, Exception) as e:
        print(f"[WARNING] FFmpeg compression skipped: {type(e).__name__}")
        print(f"[INFO] Video uses mp4v codec - may not play in all browsers")
        print(f"[INFO] Install FFmpeg for H.264 encoding: pip install imageio-ffmpeg")
    
    # Final file verification
    if os.path.exists(output_path):
        file_size = os.path.getsize(output_path)
        print(f"[INFO] Output saved: {output_path}")
        print(f"[INFO] Final file size: {file_size / (1024*1024):.2f} MB")
        if file_size < 1024:
            print(f"[WARNING] Output file size is very small, video may be corrupted")
    else:
        print(f"[ERROR] Output file was not created: {output_path}")

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
