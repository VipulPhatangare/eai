# 🐾 Pets vs Humans Detection System

A full-stack web application that uses YOLOv8 for detecting pets and humans in images and videos.

## 🚀 Quick Links

- **[Complete Deployment Guide](DEPLOYMENT_INSTRUCTIONS.md)** - Full instructions for Hostinger VPS
- **[Quick Start Guide](DEPLOYMENT_GUIDE.md)** - Fast deployment checklist
- **[Changes Summary](CHANGES_SUMMARY.md)** - All modifications made for deployment
- **Live Demo:** https://eai.synthomind.cloud (after deployment)

---

## 📦 VPS Deployment (3 Simple Steps)

### For Windows Users:

1. **Update VPS IP** in [transfer_to_vps.bat](transfer_to_vps.bat)
2. **Run:** `.\transfer_to_vps.bat`
3. **SSH & Deploy:**
   ```bash
   ssh root@YOUR_VPS_IP
   cd /root/eai
   chmod +x deploy.sh && ./deploy.sh
   ```

🎉 **Done!** Visit https://eai.synthomind.cloud

---

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
│   ├── live.js             # Live streaming client
│   ├── style.css           # Styling
│   └── script.js           # Client-side logic
├── uploads/                # Uploaded files (auto-created)
├── output/                 # Processed files (auto-created)
├── logs/                   # PM2 logs (auto-created)
├── server.js               # Express.js server
├── detect.py               # Python detection script
├── detect_live.py          # Python live detection script
├── package.json            # Node.js dependencies
├── requirements.txt        # Python dependencies
├── ecosystem.config.js     # PM2 configuration
├── nginx.conf              # Nginx configuration
├── deploy.sh               # Deployment script
├── .env.example            # Environment variables example
└── README.md               # This file
```

## Deployment to Hostinger VPS

This section provides step-by-step instructions to deploy your application on a Hostinger VPS with the domain **eai.synthomind.cloud**.

### Prerequisites

1. **VPS Access**: SSH access to your Hostinger VPS
2. **Domain**: Domain name pointed to your VPS IP address (eai.synthomind.cloud)
3. **Root/Sudo Access**: Ability to install packages and configure services

### Quick Deployment (Automated)

1. **Transfer files to VPS:**
   ```bash
   # From your local machine
   scp -r /path/to/eai root@your-vps-ip:/root/
   ```

2. **Connect to VPS:**
   ```bash
   ssh root@your-vps-ip
   ```

3. **Run deployment script:**
   ```bash
   cd /root/eai
   chmod +x deploy.sh
   ./deploy.sh
   ```

The script will automatically:
- Install Node.js, Python, PM2, Nginx, and Certbot
- Set up the application directory
- Install all dependencies
- Configure Nginx with SSL
- Start the application with PM2

### Manual Deployment Steps

If you prefer manual deployment or the automated script fails:

#### Step 1: System Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Node.js 20.x
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs

# Install Python and pip
sudo apt install -y python3 python3-pip python3-venv

# Install PM2 globally
sudo npm install -g pm2

# Install Nginx
sudo apt install -y nginx

# Install Certbot for SSL
sudo apt install -y certbot python3-certbot-nginx
```

#### Step 2: Application Setup

```bash
# Create application directory
sudo mkdir -p /var/www/eai
sudo chown -R $USER:$USER /var/www/eai

# Upload your project files to /var/www/eai
# You can use scp, git, or SFTP

cd /var/www/eai

# Install Node.js dependencies
npm install --production

# Create Python virtual environment
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
deactivate

# Create necessary directories
mkdir -p uploads output logs
chmod 755 uploads output logs
```

#### Step 3: Environment Configuration

```bash
# Create .env file
cat > .env << EOF
PORT=5010
NODE_ENV=production
DOMAIN=eai.synthomind.cloud
MAX_FILE_SIZE=100000000
SHOW_LOGS=false
EOF
```

#### Step 4: Python Wrapper Scripts

Create wrapper scripts to use the virtual environment:

```bash
# detect_wrapper.sh
cat > detect_wrapper.sh << 'EOF'
#!/bin/bash
cd /var/www/eai
source venv/bin/activate
python detect.py "$@"
EOF

# detect_live_wrapper.sh
cat > detect_live_wrapper.sh << 'EOF'
#!/bin/bash
cd /var/www/eai
source venv/bin/activate
python detect_live.py "$@"
EOF

chmod +x detect_wrapper.sh detect_live_wrapper.sh
```

Update [server.js](server.js) to use wrapper scripts (replace `'python'` with path to wrapper):

```javascript
// Line ~173 and ~391
const pythonProcess = spawn('./detect_wrapper.sh', ['detect.py', inputPath, outputPath]);
// or for live detection:
const pythonProcess = spawn('./detect_live_wrapper.sh', ['detect_live.py', tempFramePath]);
```

#### Step 5: Configure Nginx

```bash
# Copy Nginx configuration
sudo cp nginx.conf /etc/nginx/sites-available/eai.synthomind.cloud
sudo ln -sf /etc/nginx/sites-available/eai.synthomind.cloud /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Test Nginx configuration
sudo nginx -t

# Reload Nginx
sudo systemctl reload nginx
```

#### Step 6: SSL Certificate

Make sure your domain points to your VPS IP, then:

```bash
# Obtain SSL certificate
sudo certbot --nginx -d eai.synthomind.cloud

# Certificate will auto-renew. Test renewal:
sudo certbot renew --dry-run
```

#### Step 7: Start Application

```bash
# Start with PM2
pm2 start ecosystem.config.js

# Save PM2 configuration
pm2 save

# Setup PM2 to start on boot
pm2 startup
# Copy and run the command PM2 outputs

# Check status
pm2 status
pm2 logs eai-detection
```

#### Step 8: Configure Firewall

```bash
# Allow Nginx and SSH
sudo ufw allow 'Nginx Full'
sudo ufw allow OpenSSH
sudo ufw enable

# Check status
sudo ufw status
```

### Post-Deployment

**Access your application:**
- https://eai.synthomind.cloud

**Useful commands:**

```bash
# View logs
pm2 logs eai-detection

# Restart application
pm2 restart eai-detection

# Stop application
pm2 stop eai-detection

# Monitor resources
pm2 monit

# Nginx logs
sudo tail -f /var/log/nginx/eai_access.log
sudo tail -f /var/log/nginx/eai_error.log

# Check Nginx status
sudo systemctl status nginx

# Reload Nginx after config changes
sudo systemctl reload nginx
```

### Updating the Application

```bash
cd /var/www/eai

# Pull latest changes (if using git)
git pull

# Or upload new files via SCP/SFTP

# Update Node.js dependencies
npm install --production

# Update Python dependencies
source venv/bin/activate
pip install -r requirements.txt
deactivate

# Restart application
pm2 restart eai-detection
```

### Domain Configuration

Make sure your domain **eai.synthomind.cloud** has an A record pointing to your VPS IP:

```
Type: A
Name: eai.synthomind.cloud (or eai)
Value: YOUR_VPS_IP_ADDRESS
TTL: 3600 (or default)
```

### Troubleshooting Deployment

**Application not starting:**
```bash
pm2 logs eai-detection
# Check for errors in the logs
```

**Python errors:**
```bash
# Activate venv and test manually
cd /var/www/eai
source venv/bin/activate
python detect.py uploads/test.jpg output/test_processed.jpg
```

**Nginx errors:**
```bash
sudo nginx -t
sudo tail -f /var/log/nginx/error.log
```

**Port conflicts:**
```bash
# Check what's using port 5010
sudo netstat -tulpn | grep 5010
```

**SSL certificate issues:**
```bash
sudo certbot certificates
sudo certbot renew --force-renewal
```

### Security Recommendations

1. **Change default SSH port**
2. **Disable root login** (use sudo user)
3. **Install fail2ban** for brute-force protection
4. **Keep system updated** regularly
5. **Use strong passwords** and SSH keys
6. **Regular backups** of uploads and output folders
7. **Monitor logs** for suspicious activity

### Performance Optimization

1. **Enable Nginx gzip compression**
2. **Use PM2 cluster mode** for multiple cores
3. **Optimize YOLO model** (use smaller model if needed)
4. **Set up Redis** for caching (optional)
5. **CDN for static assets** (optional)



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
