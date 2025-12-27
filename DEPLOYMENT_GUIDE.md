# VPS Deployment Quick Guide for eai.synthomind.cloud

## 📋 Pre-Deployment Checklist

- [ ] VPS server running Ubuntu/Debian
- [ ] Root/sudo access to VPS
- [ ] Domain `eai.synthomind.cloud` A record pointing to VPS IP
- [ ] SSH access configured
- [ ] Git installed (optional, for version control)

## 🚀 Quick Deployment (3 Steps)

### Option 1: Using SCP (Simple Copy)

**Step 1: Transfer files from Windows to VPS**
```powershell
# From Windows PowerShell (in project directory)
scp -r "C:\Users\vipul\OneDrive\Desktop\web dev\Collage projects\eai" root@YOUR_VPS_IP:/root/
```

**Step 2: SSH into VPS**
```powershell
ssh root@YOUR_VPS_IP
```

**Step 3: Run deployment script**
```bash
cd /root/eai
chmod +x deploy.sh
./deploy.sh
```

### Option 2: Using Git (Recommended)

**Step 1: Initialize Git (on Windows)**
```powershell
cd "C:\Users\vipul\OneDrive\Desktop\web dev\Collage projects\eai"
git init
git add .
git commit -m "Initial commit"

# Push to GitHub/GitLab
git remote add origin YOUR_GIT_REPO_URL
git push -u origin main
```

**Step 2: SSH into VPS**
```bash
ssh root@YOUR_VPS_IP
```

**Step 3: Clone and deploy**
```bash
# Clone repository
git clone YOUR_GIT_REPO_URL /var/www/eai

# Run deployment
cd /var/www/eai
chmod +x deploy.sh
./deploy.sh
```

## 🔧 What the Deployment Script Does

1. ✅ Updates system packages
2. ✅ Installs Node.js 20.x
3. ✅ Installs Python 3 and pip
4. ✅ Installs PM2 (process manager)
5. ✅ Installs Nginx (web server)
6. ✅ Installs Certbot (SSL certificates)
7. ✅ Creates application directory
8. ✅ Installs all dependencies
9. ✅ Creates Python virtual environment
10. ✅ Configures Nginx with domain
11. ✅ Obtains SSL certificate
12. ✅ Starts application with PM2
13. ✅ Configures firewall

## 🌐 After Deployment

### Access Your Application
- **URL**: https://eai.synthomind.cloud
- **Live Stream**: https://eai.synthomind.cloud (live.html)

### Verify Deployment
```bash
# Check PM2 status
pm2 status

# View application logs
pm2 logs eai-detection

# Check Nginx status
sudo systemctl status nginx

# Test domain
curl -I https://eai.synthomind.cloud
```

## 📊 Management Commands

### Application Management
```bash
# Restart application
pm2 restart eai-detection

# Stop application
pm2 stop eai-detection

# View logs
pm2 logs eai-detection

# Monitor resources
pm2 monit
```

### Nginx Management
```bash
# Check configuration
sudo nginx -t

# Reload Nginx
sudo systemctl reload nginx

# View logs
sudo tail -f /var/log/nginx/eai_access.log
sudo tail -f /var/log/nginx/eai_error.log
```

### SSL Certificate
```bash
# Check certificate status
sudo certbot certificates

# Test renewal
sudo certbot renew --dry-run

# Force renewal (if needed)
sudo certbot renew --force-renewal
```

## 🔄 Update Application

### Git Method (Recommended)
```bash
cd /var/www/eai
git pull
npm install --production
source venv/bin/activate && pip install -r requirements.txt && deactivate
pm2 restart eai-detection
```

### SCP Method
```powershell
# From Windows
scp -r "C:\Users\vipul\OneDrive\Desktop\web dev\Collage projects\eai\*" root@YOUR_VPS_IP:/var/www/eai/
```

```bash
# On VPS
cd /var/www/eai
npm install --production
source venv/bin/activate && pip install -r requirements.txt && deactivate
pm2 restart eai-detection
```

## 🐛 Common Issues

### Issue: Domain not accessible
**Solution:**
1. Check DNS propagation: `nslookup eai.synthomind.cloud`
2. Verify Nginx is running: `sudo systemctl status nginx`
3. Check firewall: `sudo ufw status`

### Issue: SSL certificate error
**Solution:**
```bash
sudo certbot --nginx -d eai.synthomind.cloud --force-renewal
```

### Issue: Application not starting
**Solution:**
```bash
pm2 logs eai-detection
# Check logs for errors

# Test Python environment
cd /var/www/eai
source venv/bin/activate
python -c "import ultralytics; print('OK')"
```

### Issue: Upload fails
**Solution:**
```bash
# Check directory permissions
ls -la /var/www/eai/uploads
sudo chown -R $USER:$USER /var/www/eai/uploads
chmod 755 /var/www/eai/uploads
```

## 📱 Phone Live Stream Setup

To use the live detection feature with your phone:

1. Install a camera streaming app (like "IP Webcam" for Android)
2. Configure it to stream to: `wss://eai.synthomind.cloud/socket.io/`
3. Open https://eai.synthomind.cloud/live.html on any device

## 🔐 Security Best Practices

1. **Change SSH port**
   ```bash
   sudo nano /etc/ssh/sshd_config
   # Change Port 22 to Port 2222
   sudo systemctl restart ssh
   ```

2. **Install fail2ban**
   ```bash
   sudo apt install fail2ban
   sudo systemctl enable fail2ban
   ```

3. **Disable root login**
   ```bash
   # Create new user
   adduser deployuser
   usermod -aG sudo deployuser
   
   # In /etc/ssh/sshd_config
   PermitRootLogin no
   ```

4. **Regular updates**
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

## 📈 Performance Monitoring

### Check Resource Usage
```bash
# CPU and Memory
htop

# Disk usage
df -h

# Application stats
pm2 monit
```

### Nginx Performance
```bash
# Monitor connections
sudo netstat -plant | grep nginx

# Check worker processes
ps aux | grep nginx
```

## 📞 Support

If you encounter issues:
1. Check logs: `pm2 logs eai-detection`
2. Check Nginx logs: `sudo tail -f /var/log/nginx/eai_error.log`
3. Verify Python environment: `source /var/www/eai/venv/bin/activate && python --version`

## ✅ Deployment Complete!

Your application should now be live at:
**https://eai.synthomind.cloud** 🎉

Upload images or videos to detect pets and humans using AI!
