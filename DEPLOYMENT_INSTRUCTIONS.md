# 🚀 VPS Deployment - Complete Instructions
## For eai.synthomind.cloud on Hostinger VPS

---

## 📦 Files Added/Modified for Deployment

### ✅ New Files Created:
1. **`.env.example`** - Environment variables template
2. **`ecosystem.config.js`** - PM2 process manager configuration
3. **`nginx.conf`** - Nginx reverse proxy configuration
4. **`deploy.sh`** - Automated deployment script (Linux)
5. **`transfer_to_vps.bat`** - Windows file transfer helper
6. **`DEPLOYMENT_GUIDE.md`** - Detailed deployment instructions
7. **`.gitkeep`** files in uploads/, output/, logs/

### ✅ Modified Files:
1. **`server.js`** - Added dotenv support and production-ready configurations
2. **`package.json`** - Added dotenv dependency
3. **`README.md`** - Added comprehensive deployment section

---

## 🎯 Deployment Methods

### Method 1: Automated Deployment (Recommended)

**Requirements:**
- Hostinger VPS running Ubuntu/Debian
- SSH access
- Domain DNS configured

**Steps:**

1. **Update VPS IP in transfer script:**
   ```powershell
   # Edit transfer_to_vps.bat
   # Change: set VPS_IP=YOUR_VPS_IP_HERE
   ```

2. **Transfer files from Windows:**
   ```powershell
   # Double-click transfer_to_vps.bat
   # OR run in PowerShell:
   .\transfer_to_vps.bat
   ```

3. **SSH into VPS:**
   ```powershell
   ssh root@YOUR_VPS_IP
   ```

4. **Run deployment:**
   ```bash
   cd /root/eai
   chmod +x deploy.sh
   ./deploy.sh
   ```

5. **Done!** Visit: https://eai.synthomind.cloud

---

### Method 2: Git-Based Deployment

1. **Initialize Git repository (on Windows):**
   ```powershell
   cd "C:\Users\vipul\OneDrive\Desktop\web dev\Collage projects\eai"
   git init
   git add .
   git commit -m "Initial deployment commit"
   ```

2. **Push to GitHub/GitLab:**
   ```powershell
   git remote add origin YOUR_REPO_URL
   git push -u origin main
   ```

3. **Deploy from VPS:**
   ```bash
   # SSH into VPS
   ssh root@YOUR_VPS_IP
   
   # Clone repository
   git clone YOUR_REPO_URL /var/www/eai
   
   # Run deployment
   cd /var/www/eai
   chmod +x deploy.sh
   ./deploy.sh
   ```

---

## 🔧 Pre-Deployment Setup

### Step 1: Configure Domain DNS

In your Hostinger control panel or domain registrar:

```
Type: A
Host: eai.synthomind.cloud (or just 'eai')
Points to: YOUR_VPS_IP_ADDRESS
TTL: 3600
```

**Verify DNS propagation:**
```powershell
nslookup eai.synthomind.cloud
```

### Step 2: VPS Preparation

Connect to your VPS:
```powershell
ssh root@YOUR_VPS_IP
```

Basic setup:
```bash
# Update system
apt update && apt upgrade -y

# Set timezone
timedatectl set-timezone Asia/Kolkata

# Set hostname
hostnamectl set-hostname eai-server
```

---

## 📋 Deployment Checklist

### Before Deployment:
- [ ] VPS is accessible via SSH
- [ ] Domain DNS A record configured
- [ ] DNS propagated (nslookup works)
- [ ] Root or sudo access available
- [ ] Sufficient disk space (at least 2GB free)

### During Deployment:
- [ ] Files transferred to VPS
- [ ] deploy.sh executed successfully
- [ ] No errors in deployment logs
- [ ] PM2 status shows "online"
- [ ] Nginx test passes (`nginx -t`)
- [ ] SSL certificate obtained
- [ ] Firewall configured

### After Deployment:
- [ ] Website accessible via HTTPS
- [ ] Upload test works
- [ ] Detection processing works
- [ ] Live streaming works
- [ ] Logs are being written
- [ ] PM2 auto-start configured

---

## 🧪 Testing Your Deployment

### 1. Basic Connectivity
```bash
# Check if app is running
pm2 status

# Test localhost
curl http://localhost:5010

# Test domain
curl -I https://eai.synthomind.cloud
```

### 2. Upload Test
1. Visit: https://eai.synthomind.cloud
2. Upload a test image
3. Process it
4. Verify detection works

### 3. Live Stream Test
1. Visit: https://eai.synthomind.cloud/live.html
2. Check if interface loads
3. Test with phone camera app

### 4. Check Logs
```bash
# Application logs
pm2 logs eai-detection

# Nginx access logs
sudo tail -f /var/log/nginx/eai_access.log

# Nginx error logs
sudo tail -f /var/log/nginx/eai_error.log
```

---

## 🔐 Security Hardening (Post-Deployment)

### 1. Create Non-Root User
```bash
adduser deployuser
usermod -aG sudo deployuser
su - deployuser
```

### 2. Configure SSH Key Authentication
```powershell
# On Windows, generate SSH key
ssh-keygen -t ed25519 -C "your_email@example.com"

# Copy public key to VPS
type $env:USERPROFILE\.ssh\id_ed25519.pub | ssh root@YOUR_VPS_IP "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
```

### 3. Harden SSH
```bash
sudo nano /etc/ssh/sshd_config

# Add/modify:
PermitRootLogin no
PasswordAuthentication no
Port 2222  # Change from default 22

sudo systemctl restart ssh
```

### 4. Install Fail2Ban
```bash
sudo apt install fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

### 5. Setup Firewall
```bash
sudo ufw allow 2222/tcp  # SSH (if you changed port)
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

---

## 🔄 Update & Maintenance

### Regular Updates
```bash
# Update application
cd /var/www/eai
git pull  # or upload new files
npm install --production
source venv/bin/activate && pip install -r requirements.txt
pm2 restart eai-detection

# Update system
sudo apt update && sudo apt upgrade -y
```

### Backup Important Files
```bash
# Create backup directory
mkdir -p /root/backups

# Backup uploads and outputs
tar -czf /root/backups/eai-data-$(date +%Y%m%d).tar.gz /var/www/eai/uploads /var/www/eai/output

# Backup database (if you add one later)
# mysqldump -u root -p database_name > /root/backups/db-$(date +%Y%m%d).sql
```

### Monitor Resources
```bash
# Check disk space
df -h

# Check memory
free -h

# Check CPU
htop

# PM2 monitoring
pm2 monit
```

---

## 🐛 Troubleshooting Guide

### Issue: Cannot SSH to VPS
**Solutions:**
```powershell
# Test connection
Test-NetConnection -ComputerName YOUR_VPS_IP -Port 22

# Verify IP address
# Check Hostinger control panel
```

### Issue: Domain not resolving
**Solutions:**
```powershell
# Check DNS
nslookup eai.synthomind.cloud

# Check NS records
nslookup -type=NS synthomind.cloud

# Wait for DNS propagation (can take up to 48 hours)
```

### Issue: SSL certificate fails
**Solutions:**
```bash
# Make sure domain resolves first
ping eai.synthomind.cloud

# Try manual certificate
sudo certbot certonly --nginx -d eai.synthomind.cloud

# Check certbot logs
sudo tail -f /var/log/letsencrypt/letsencrypt.log
```

### Issue: Application won't start
**Solutions:**
```bash
# Check PM2 logs
pm2 logs eai-detection --lines 100

# Test Python environment
cd /var/www/eai
source venv/bin/activate
python -c "import ultralytics; print('OK')"

# Check dependencies
npm list
pip list

# Restart everything
pm2 restart all
sudo systemctl restart nginx
```

### Issue: 502 Bad Gateway
**Solutions:**
```bash
# Check if app is running
pm2 status

# Check if app is listening on correct port
sudo netstat -tulpn | grep 5010

# Check Nginx logs
sudo tail -f /var/log/nginx/eai_error.log

# Restart app
pm2 restart eai-detection
```

### Issue: Upload fails
**Solutions:**
```bash
# Check directory permissions
ls -la /var/www/eai/uploads
sudo chown -R $USER:$USER /var/www/eai/uploads
chmod 755 /var/www/eai/uploads

# Check disk space
df -h

# Check Nginx client_max_body_size
sudo nano /etc/nginx/sites-available/eai.synthomind.cloud
# Ensure: client_max_body_size 100M;
```

---

## 📊 Performance Optimization

### 1. Enable Nginx Gzip Compression
```nginx
# Add to nginx.conf
gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;
```

### 2. PM2 Cluster Mode (Multi-Core)
```javascript
// Update ecosystem.config.js
instances: 'max',  // Use all CPU cores
exec_mode: 'cluster'
```

### 3. Use Smaller YOLO Model
```python
# In detect.py, change:
model = YOLO("yolov8n.pt")  # Fastest
# model = YOLO("yolov8s.pt")  # Small
# model = YOLO("yolov8m.pt")  # Medium
```

### 4. Add Redis Caching (Optional)
```bash
sudo apt install redis-server
npm install redis
```

---

## 📞 Support & Resources

### Official Documentation:
- **PM2:** https://pm2.keymetrics.io/docs/
- **Nginx:** https://nginx.org/en/docs/
- **Let's Encrypt:** https://letsencrypt.org/docs/
- **YOLOv8:** https://docs.ultralytics.com/

### Useful Commands Reference:

```bash
# PM2
pm2 list
pm2 restart <id>
pm2 stop <id>
pm2 delete <id>
pm2 logs <id>
pm2 monit

# Nginx
sudo nginx -t
sudo systemctl status nginx
sudo systemctl restart nginx
sudo systemctl reload nginx

# System
df -h           # Disk space
free -h         # Memory
htop            # CPU/processes
sudo ufw status # Firewall

# Logs
journalctl -xe
tail -f /var/log/nginx/error.log
```

---

## ✅ Deployment Complete!

After successful deployment, your application will be accessible at:

🌐 **Main Application:** https://eai.synthomind.cloud
🎥 **Live Detection:** https://eai.synthomind.cloud/live.html

### Next Steps:
1. ✅ Test all features
2. ✅ Set up monitoring
3. ✅ Configure backups
4. ✅ Harden security
5. ✅ Optimize performance

---

**Need Help?**
- Check logs: `pm2 logs eai-detection`
- Review Nginx errors: `sudo tail -f /var/log/nginx/eai_error.log`
- Test Python: `source /var/www/eai/venv/bin/activate && python --version`

**Happy Deploying! 🚀**
