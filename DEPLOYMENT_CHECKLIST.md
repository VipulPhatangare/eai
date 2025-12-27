# ✅ VPS Deployment Checklist
## eai.synthomind.cloud on Hostinger VPS

Use this checklist to track your deployment progress.

---

## 📋 Pre-Deployment

### Local Setup (Windows)
- [ ] All project files are present
- [ ] VPS IP address obtained from Hostinger
- [ ] SSH credentials ready (username/password or SSH key)
- [ ] OpenSSH Client installed on Windows
- [ ] Domain DNS configured (A record)

### VPS Access
- [ ] Can SSH into VPS: `ssh root@YOUR_VPS_IP`
- [ ] Have root or sudo privileges
- [ ] VPS has at least 2GB free disk space
- [ ] VPS has Ubuntu/Debian OS

### Domain Configuration
- [ ] Domain `eai.synthomind.cloud` registered
- [ ] A record points to VPS IP address
- [ ] DNS propagation verified: `nslookup eai.synthomind.cloud`
- [ ] Domain resolves to correct IP

---

## 🚀 Deployment Process

### Step 1: File Transfer
- [ ] Updated VPS_IP in `transfer_to_vps.bat`
- [ ] Ran `.\transfer_to_vps.bat` successfully
- [ ] Files transferred to `/root/eai` on VPS
- [ ] No transfer errors

### Step 2: SSH Connection
- [ ] Connected to VPS: `ssh root@YOUR_VPS_IP`
- [ ] Navigated to project: `cd /root/eai`
- [ ] Verified files are present: `ls -la`
- [ ] Made deploy script executable: `chmod +x deploy.sh`

### Step 3: Run Deployment
- [ ] Executed: `./deploy.sh`
- [ ] Node.js installed successfully
- [ ] Python installed successfully
- [ ] PM2 installed successfully
- [ ] Nginx installed successfully
- [ ] Certbot installed successfully
- [ ] Application directory created
- [ ] Dependencies installed (npm)
- [ ] Python venv created
- [ ] Python packages installed
- [ ] Nginx configured
- [ ] SSL certificate obtained
- [ ] PM2 started application
- [ ] Firewall configured
- [ ] No deployment errors

---

## ✅ Post-Deployment Verification

### Application Status
- [ ] PM2 shows status "online": `pm2 status`
- [ ] Application logs look good: `pm2 logs eai-detection`
- [ ] No errors in PM2 logs
- [ ] Process auto-restart configured: `pm2 startup`

### Nginx Status
- [ ] Nginx is active: `sudo systemctl status nginx`
- [ ] Nginx config test passes: `sudo nginx -t`
- [ ] Nginx access logs working: `ls -la /var/log/nginx/`
- [ ] No errors in Nginx logs

### SSL Certificate
- [ ] Certificate obtained successfully
- [ ] Certificate valid: `sudo certbot certificates`
- [ ] HTTPS works without warnings
- [ ] Auto-renewal configured

### Firewall
- [ ] UFW is active: `sudo ufw status`
- [ ] Ports 80 and 443 allowed
- [ ] SSH port allowed (22 or custom)

---

## 🧪 Functionality Testing

### Website Access
- [ ] Site loads via HTTP: `http://eai.synthomind.cloud`
- [ ] HTTP redirects to HTTPS
- [ ] Site loads via HTTPS: `https://eai.synthomind.cloud`
- [ ] No SSL certificate warnings
- [ ] All static assets load correctly
- [ ] No console errors in browser

### Upload & Detection
- [ ] Upload page loads
- [ ] Can select a file
- [ ] File preview shows
- [ ] "Process File" button works
- [ ] Processing completes successfully
- [ ] Processed file displays
- [ ] Detection boxes visible
- [ ] Detection counts accurate
- [ ] Download button works

### Live Streaming
- [ ] Live page loads: `https://eai.synthomind.cloud/live.html`
- [ ] No WebSocket errors
- [ ] Can connect to phone stream
- [ ] Real-time detection works
- [ ] Frame updates smoothly

---

## 🔒 Security Hardening

### User Management
- [ ] Created non-root user: `adduser deployuser`
- [ ] Added user to sudo group
- [ ] Tested sudo access
- [ ] SSH key added for new user

### SSH Hardening
- [ ] Changed SSH port (optional)
- [ ] Disabled root login
- [ ] Disabled password authentication
- [ ] Restarted SSH service

### Additional Security
- [ ] Fail2ban installed: `sudo apt install fail2ban`
- [ ] Fail2ban configured and running
- [ ] Regular update schedule set
- [ ] Backup system configured

---

## 📊 Monitoring Setup

### Application Monitoring
- [ ] PM2 monitoring accessible: `pm2 monit`
- [ ] PM2 startup configured
- [ ] Log rotation configured
- [ ] Application metrics baseline recorded

### System Monitoring
- [ ] Disk usage checked: `df -h`
- [ ] Memory usage checked: `free -h`
- [ ] CPU usage checked: `htop`
- [ ] Baseline metrics recorded

### Log Monitoring
- [ ] Application logs location known
- [ ] Nginx logs location known
- [ ] Log retention policy set
- [ ] Log monitoring alerts (optional)

---

## 📚 Documentation Review

- [ ] Read DEPLOYMENT_INSTRUCTIONS.md
- [ ] Read DEPLOYMENT_GUIDE.md
- [ ] Read CHANGES_SUMMARY.md
- [ ] Bookmarked useful commands
- [ ] Understand update procedure

---

## 🎓 Knowledge Transfer

### Commands to Remember
- [ ] Restart app: `pm2 restart eai-detection`
- [ ] View logs: `pm2 logs eai-detection`
- [ ] Check status: `pm2 status`
- [ ] Monitor resources: `pm2 monit`
- [ ] Reload Nginx: `sudo systemctl reload nginx`
- [ ] Check Nginx: `sudo systemctl status nginx`
- [ ] Renew SSL: `sudo certbot renew`

### File Locations
- [ ] Application: `/var/www/eai/`
- [ ] Nginx config: `/etc/nginx/sites-available/eai.synthomind.cloud`
- [ ] PM2 logs: `/var/www/eai/logs/`
- [ ] Nginx logs: `/var/log/nginx/`
- [ ] SSL certificates: `/etc/letsencrypt/live/eai.synthomind.cloud/`

---

## 🔄 Maintenance Schedule

### Daily
- [ ] Check application status: `pm2 status`
- [ ] Monitor disk space: `df -h`
- [ ] Review error logs if any

### Weekly
- [ ] Review all logs
- [ ] Check for updates: `sudo apt update`
- [ ] Monitor resource usage
- [ ] Test all features

### Monthly
- [ ] Update system: `sudo apt upgrade`
- [ ] Update npm packages: `npm update`
- [ ] Update Python packages: `pip install -U -r requirements.txt`
- [ ] Review SSL certificate status
- [ ] Backup data
- [ ] Review security logs

---

## 🐛 Troubleshooting Reference

### Quick Fixes
- [ ] Know how to restart app
- [ ] Know how to restart Nginx
- [ ] Know how to check logs
- [ ] Know how to test Python environment
- [ ] Have rollback plan

### Emergency Contacts
- [ ] Hostinger support contact saved
- [ ] Domain registrar support saved
- [ ] Technical support contact identified

---

## 🎉 Deployment Complete!

### Final Checks
- [ ] All features tested and working
- [ ] Performance is acceptable
- [ ] Security measures in place
- [ ] Monitoring configured
- [ ] Documentation reviewed
- [ ] Team/stakeholders notified

### Success Metrics
- [ ] Application accessible at: https://eai.synthomind.cloud
- [ ] Uptime: ____% (target: 99%+)
- [ ] Response time: ____ms (target: <2000ms)
- [ ] No critical errors
- [ ] All tests passing

---

## 📝 Notes & Issues

Use this space to record any issues encountered or notes for future reference:

```
Date: ___________
Issue: _________________________________
Resolution: ____________________________
_______________________________________

Date: ___________
Note: __________________________________
_______________________________________
```

---

## 🎯 Next Steps

After successful deployment:

1. [ ] Announce go-live to users
2. [ ] Monitor for first 24 hours
3. [ ] Set up automated backups
4. [ ] Configure monitoring alerts
5. [ ] Plan for scaling if needed
6. [ ] Document any custom configurations
7. [ ] Schedule regular maintenance

---

**Deployment Date:** _______________
**Deployed By:** ___________________
**Status:** ⬜ Planning ⬜ In Progress ⬜ Complete ⬜ Verified

---

**Congratulations on your deployment! 🎊**
