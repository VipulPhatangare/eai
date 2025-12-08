# 🐾 Pets vs Humans Detection System

A full-stack web application that uses YOLOv8 for detecting pets and humans in images and videos.

## Features

- 📤 Upload images or videos through a beautiful web interface
- 🤖 AI-powered detection using YOLOv8
- 🎯 Detects pets (cats, dogs) and humans
- 📊 Real-time processing with progress tracking
- 📥 Download processed results
- 🎨 Modern, responsive UI with dark theme

## Tech Stack

### Frontend
- HTML5
- CSS3 (with modern animations)
- Vanilla JavaScript

### Backend
- Node.js
- Express.js
- Multer (file uploads)

### AI/ML
- Python 3.x
- YOLOv8 (Ultralytics)
- OpenCV
- PyTorch

## Installation

### 1. Install Node.js Dependencies

```powershell
npm install
```

### 2. Install Python Dependencies

```powershell
pip install -r requirements.txt
```

Or install individually:

```powershell
pip install ultralytics opencv-python numpy torch
```

## Usage

### 1. Start the Server

```powershell
npm start
```

Or for development with auto-reload:

```powershell
npm run dev
```

### 2. Open the Application

Open your browser and navigate to:
```
http://localhost:3000
```

### 3. Upload and Process

1. Click "Select File" or drag and drop an image/video
2. Preview your selection
3. Click "🚀 Process File"
4. Wait for AI processing
5. View results with detection statistics
6. Download the processed file

## Project Structure

```
eai/
├── public/                  # Frontend files
│   ├── index.html          # Main HTML page
│   ├── style.css           # Styling
│   └── script.js           # Client-side logic
├── uploads/                # Uploaded files (auto-created)
├── output/                 # Processed files (auto-created)
├── server.js               # Express.js server
├── detect.py               # Python detection script
├── package.json            # Node.js dependencies
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

## How It Works

1. **Upload**: User uploads image/video through the web interface
2. **Transfer**: Express.js receives the file via Multer
3. **Process**: Node.js spawns Python script to run YOLOv8 detection
4. **Detect**: YOLOv8 identifies pets and humans, draws bounding boxes
5. **Return**: Processed file is saved and sent back to the client
6. **Display**: Frontend shows original vs processed comparison

## Supported File Types

### Images
- JPG/JPEG
- PNG
- GIF
- BMP

### Videos
- MP4
- AVI
- MOV
- MKV

## Detection Classes

- **Humans**: Person (COCO class 0)
- **Pets**: Cat (class 15), Dog (class 16)

## Configuration

### Change Model

In `detect.py`, line 13:
```python
model = YOLO("yolov8n.pt")  # Options: yolov8n, yolov8s, yolov8m, yolov8l, yolov8x
```

### Change Port

In `server.js`, line 11:
```javascript
const PORT = 3000;  // Change to desired port
```

### File Size Limit

In `server.js`, line 29:
```javascript
limits: { fileSize: 100 * 1024 * 1024 }, // 100MB limit
```

## Troubleshooting

### Python Script Not Found
Make sure Python is in your PATH:
```powershell
python --version
```

### Module Not Found
Reinstall dependencies:
```powershell
pip install -r requirements.txt --force-reinstall
```

### Port Already in Use
Change the port in `server.js` or kill the process:
```powershell
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

### YOLO Model Download
First run will download YOLOv8 model (~6MB). Ensure internet connection.

## Performance Tips

- Use `yolov8n.pt` for faster processing (less accurate)
- Use `yolov8x.pt` for better accuracy (slower)
- For videos, consider reducing resolution before upload
- Process shorter videos for faster results

## Future Enhancements

- [ ] Real-time webcam detection
- [ ] Multiple file uploads
- [ ] Custom training for specific pets
- [ ] Alert notifications
- [ ] Database storage of results
- [ ] User authentication

## License

MIT License

## Credits

- YOLOv8 by Ultralytics
- COCO Dataset for pre-trained models

---

Made with ❤️ for pet lovers and AI enthusiasts!
