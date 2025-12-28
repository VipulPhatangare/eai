// DOM Elements
const uploadBox = document.getElementById('uploadBox');
const fileInput = document.getElementById('fileInput');
const selectFileBtn = document.getElementById('selectFileBtn');
const filePreview = document.getElementById('filePreview');
const cancelBtn = document.getElementById('cancelBtn');
const processBtn = document.getElementById('processBtn');
const previewMedia = document.getElementById('previewMedia');
const fileName = document.getElementById('fileName');
const fileSize = document.getElementById('fileSize');

const processingSection = document.getElementById('processingSection');
const processingStatus = document.getElementById('processingStatus');
const progressFill = document.getElementById('progressFill');

const resultsSection = document.getElementById('resultsSection');
const newUploadBtn = document.getElementById('newUploadBtn');
const statFrames = document.getElementById('statFrames');
const statPets = document.getElementById('statPets');
const statHumans = document.getElementById('statHumans');
const originalMedia = document.getElementById('originalMedia');
const processedMedia = document.getElementById('processedMedia');
const downloadBtn = document.getElementById('downloadBtn');

const errorSection = document.getElementById('errorSection');
const errorMessage = document.getElementById('errorMessage');
const retryBtn = document.getElementById('retryBtn');

// State
let selectedFile = null;
let originalFileUrl = null;

// Event Listeners
selectFileBtn.addEventListener('click', () => fileInput.click());

uploadBox.addEventListener('click', (e) => {
    // Only trigger if clicking on the box itself, not the button
    if (e.target === uploadBox || uploadBox.contains(e.target) && e.target !== selectFileBtn) {
        fileInput.click();
    }
});

uploadBox.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadBox.style.borderColor = 'var(--primary-color)';
    uploadBox.style.transform = 'scale(1.02)';
});

uploadBox.addEventListener('dragleave', () => {
    uploadBox.style.borderColor = 'var(--border-color)';
    uploadBox.style.transform = 'scale(1)';
});

uploadBox.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadBox.style.borderColor = 'var(--border-color)';
    uploadBox.style.transform = 'scale(1)';
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFileSelect(files[0]);
    }
});

fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFileSelect(e.target.files[0]);
    }
}, { once: false });

cancelBtn.addEventListener('click', resetUpload);
newUploadBtn.addEventListener('click', resetUpload);
retryBtn.addEventListener('click', resetUpload);

processBtn.addEventListener('click', processFile);

// Functions
function handleFileSelect(file) {
    // Validate file type
    const validTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 
                       'video/mp4', 'video/avi', 'video/quicktime', 'video/x-matroska'];
    
    if (!validTypes.includes(file.type)) {
        alert('Please select a valid image or video file!');
        return;
    }

    // Validate file size (100MB max)
    const maxSize = 100 * 1024 * 1024;
    if (file.size > maxSize) {
        alert('File size must be less than 100MB!');
        return;
    }

    selectedFile = file;
    originalFileUrl = URL.createObjectURL(file);

    // Update UI
    uploadBox.style.display = 'none';
    filePreview.style.display = 'block';

    // Display file info
    fileName.textContent = `📄 ${file.name}`;
    fileSize.textContent = `💾 ${formatFileSize(file.size)}`;

    // Display preview
    previewMedia.innerHTML = '';
    if (file.type.startsWith('image/')) {
        const img = document.createElement('img');
        img.src = originalFileUrl;
        img.alt = 'Preview';
        previewMedia.appendChild(img);
    } else {
        const video = document.createElement('video');
        video.src = originalFileUrl;
        video.controls = true;
        video.muted = true;
        previewMedia.appendChild(video);
    }
}

async function processFile() {
    if (!selectedFile) {
        alert('No file selected!');
        return;
    }

    // Hide preview, show processing
    filePreview.style.display = 'none';
    processingSection.style.display = 'block';
    errorSection.style.display = 'none';
    resultsSection.style.display = 'none';

    // Prepare form data
    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
        // Upload and process
        processingStatus.textContent = 'Uploading file...';
        
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Processing failed');
        }

        processingStatus.textContent = 'Processing complete!';
        
        const result = await response.json();
        
        // Show results
        setTimeout(() => {
            showResults(result);
        }, 500);

    } catch (error) {
        console.error('Error:', error);
        showError(error.message);
    }
}

function showResults(result) {
    processingSection.style.display = 'none';
    resultsSection.style.display = 'block';

    // Show original media
    originalMedia.innerHTML = '';
    if (result.fileType === 'image') {
        const img = document.createElement('img');
        img.src = originalFileUrl;
        img.alt = 'Original';
        originalMedia.appendChild(img);
    } else {
        const video = document.createElement('video');
        video.src = originalFileUrl;
        video.controls = true;
        video.autoplay = false;
        video.style.width = '100%';
        video.style.maxHeight = '600px';
        video.style.borderRadius = '8px';
        video.preload = 'metadata';
        originalMedia.appendChild(video);
    }

    // Show processed media
    processedMedia.innerHTML = '';
    const outputUrl = `${result.outputUrl}?t=${Date.now()}`;
    
    if (result.fileType === 'image') {
        const img = document.createElement('img');
        img.src = outputUrl;
        img.alt = 'Processed';
        processedMedia.appendChild(img);
    } else {
        const video = document.createElement('video');
        video.src = outputUrl;
        video.controls = true;
        video.autoplay = false;
        video.loop = false;
        video.style.width = '100%';
        video.style.maxHeight = '600px';
        video.style.borderRadius = '8px';
        video.preload = 'metadata';
        video.controlsList = 'nodownload'; // Remove download from controls
        
        // Add playback rate controls
        video.addEventListener('loadedmetadata', () => {
            console.log('✅ Processed video ready to play');
            console.log(`📹 Duration: ${Math.round(video.duration)}s`);
        });
        
        video.addEventListener('error', (e) => {
            console.error('❌ Video playback error:', e);
            const errorDetails = video.error ? `Code: ${video.error.code}, Message: ${video.error.message}` : 'Unknown error';
            console.error('🐞 Video error details:', errorDetails);
            console.error('📼 Video source:', video.src);
            processedMedia.innerHTML = `
                <div style="padding: 20px; background: rgba(239, 68, 68, 0.1); border-radius: 8px; text-align: center;">
                    <p style="color: #ef4444; font-weight: bold; margin-bottom: 10px;">⚠️ Video playback not supported in browser</p>
                    <p style="color: #666; margin-bottom: 15px;">The video codec may not be compatible with your browser.</p>
                    <a href="${outputUrl}" class="btn btn-primary" download style="display: inline-block;">⬇️ Download Video to View</a>
                </div>
            `;
        });
        
        processedMedia.appendChild(video);
    }

    // Set download link
    downloadBtn.href = outputUrl;
    downloadBtn.download = result.outputFile;
}

function showError(message) {
    processingSection.style.display = 'none';
    errorSection.style.display = 'block';
    errorMessage.textContent = message;
}

function resetUpload() {
    // Clear file
    selectedFile = null;
    fileInput.value = '';
    
    if (originalFileUrl) {
        URL.revokeObjectURL(originalFileUrl);
        originalFileUrl = null;
    }

    // Reset UI
    uploadBox.style.display = 'block';
    filePreview.style.display = 'none';
    processingSection.style.display = 'none';
    resultsSection.style.display = 'none';
    errorSection.style.display = 'none';

    // Clear preview
    previewMedia.innerHTML = '';
    originalMedia.innerHTML = '';
    processedMedia.innerHTML = '';
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

// Initialize
console.log('🚀 Pet vs Human Detection System initialized!');

// Tab Switching
const tabBtns = document.querySelectorAll('.tab-btn');
const tabContents = document.querySelectorAll('.tab-content');

tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const tabName = btn.getAttribute('data-tab');
        
        console.log(`🔄 Switching to ${tabName} tab`);
        
        // Remove active class from all tabs and hide them
        tabBtns.forEach(b => b.classList.remove('active'));
        tabContents.forEach(c => {
            c.classList.remove('active');
            c.style.display = 'none';
        });
        
        // Add active class to clicked tab and show it
        btn.classList.add('active');
        const activeTab = document.getElementById(`${tabName}-tab`);
        if (activeTab) {
            activeTab.classList.add('active');
            activeTab.style.display = 'block';
            console.log(`✅ ${tabName} tab is now visible`);
        }
    });
});

