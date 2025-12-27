#!/bin/bash

# Quick Start Script for VPS Deployment
# Run this after SSH into your VPS

echo "╔════════════════════════════════════════════╗"
echo "║   EAI Detection System - Quick Deploy     ║"
echo "║   Domain: eai.synthomind.cloud            ║"
echo "╚════════════════════════════════════════════╝"
echo ""

# Check if running on VPS
if [ ! -d "/root/eai" ] && [ ! -d "/var/www/eai" ]; then
    echo "❌ Project directory not found!"
    echo ""
    echo "Please upload your project files first:"
    echo "  scp -r /path/to/eai root@YOUR_VPS_IP:/root/"
    echo ""
    exit 1
fi

# Find project directory
if [ -d "/root/eai" ]; then
    PROJECT_DIR="/root/eai"
elif [ -d "/var/www/eai" ]; then
    PROJECT_DIR="/var/www/eai"
else
    echo "❌ Cannot locate project directory"
    exit 1
fi

echo "📁 Project directory: $PROJECT_DIR"
cd "$PROJECT_DIR"
echo ""

# Make deploy script executable
if [ -f "deploy.sh" ]; then
    chmod +x deploy.sh
    echo "✅ Found deploy.sh"
    echo ""
    echo "🚀 Starting automated deployment..."
    echo "⏳ This will take 5-10 minutes..."
    echo ""
    
    # Run deployment
    ./deploy.sh
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "╔════════════════════════════════════════════╗"
        echo "║          DEPLOYMENT SUCCESSFUL! 🎉         ║"
        echo "╚════════════════════════════════════════════╝"
        echo ""
        echo "🌐 Your application is now live at:"
        echo "   https://eai.synthomind.cloud"
        echo ""
        echo "📊 Check status:"
        echo "   pm2 status"
        echo "   pm2 logs eai-detection"
        echo ""
        echo "🔧 Useful commands:"
        echo "   pm2 restart eai-detection    # Restart app"
        echo "   pm2 logs eai-detection       # View logs"
        echo "   pm2 monit                    # Monitor resources"
        echo "   sudo systemctl status nginx  # Check Nginx"
        echo ""
    else
        echo ""
        echo "❌ Deployment failed!"
        echo "Check the error messages above."
        echo ""
        echo "Common issues:"
        echo "  1. Domain DNS not configured"
        echo "  2. Insufficient disk space"
        echo "  3. Network connectivity issues"
        echo ""
        echo "For help, see: DEPLOYMENT_INSTRUCTIONS.md"
    fi
else
    echo "❌ deploy.sh not found in $PROJECT_DIR"
    echo "Make sure all project files are uploaded."
fi
