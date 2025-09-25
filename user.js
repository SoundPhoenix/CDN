// User Dashboard JavaScript
class UserDashboard {
    constructor() {
        this.sessionId = localStorage.getItem('session_id');
        this.username = localStorage.getItem('username');
        this.uploads = [];
        this.init();
    }
    
    async init() {
        // Check authentication
        if (!this.sessionId || !localStorage.getItem('user_role')) {
            window.location.href = '/login.html';
            return;
        }
        
        // Set current user
        document.getElementById('currentUser').textContent = this.username;
        
        // Setup event listeners
        this.setupEventListeners();
        
        // Load initial data
        await this.loadUploadHistory();
        this.updateStats();
        
        // Show welcome message
        this.showMessage('Welcome to your video upload dashboard!', 'info');
    }
    
    setupEventListeners() {
        const videoUpload = document.getElementById('videoUpload');
        const uploadArea = document.getElementById('uploadArea');
        const uploadBtn = document.getElementById('uploadBtn');
        
        // File input change
        videoUpload.addEventListener('change', (e) => {
            this.handleFileSelect(e.target.files);
        });
        
        // Drag and drop events
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('dragover');
        });
        
        uploadArea.addEventListener('dragleave', (e) => {
            if (!uploadArea.contains(e.relatedTarget)) {
                uploadArea.classList.remove('dragover');
            }
        });
        
        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
            this.handleFileSelect(e.dataTransfer.files);
        });
        
        // Click to upload
        uploadArea.addEventListener('click', (e) => {
            // Don't trigger if clicking the button
            if (e.target !== uploadBtn) {
                videoUpload.click();
            }
        });
    }
    
    async handleFileSelect(files) {
        if (files.length === 0) return;
        
        // Validate files
        const validFiles = [];
        for (const file of files) {
            if (!file.type.startsWith('video/')) {
                this.showMessage(`${file.name} is not a video file`, 'error');
                continue;
            }
            
            if (file.size > 500 * 1024 * 1024) { // 500MB limit
                this.showMessage(`${file.name} is too large (max 500MB)`, 'error');
                continue;
            }
            
            validFiles.push(file);
        }
        
        if (validFiles.length === 0) return;
        
        // Upload files
        for (const file of validFiles) {
            await this.uploadVideo(file);
        }
        
        // Refresh history and stats
        await this.loadUploadHistory();
        this.updateStats();
    }
    
    async uploadVideo(file) {
        const formData = new FormData();
        formData.append('video', file);
        
        // Add upload to tracking list
        const uploadId = Date.now() + Math.random();
        const upload = {
            id: uploadId,
            name: file.name,
            size: file.size,
            status: 'uploading',
            timestamp: new Date().toISOString(),
            progress: 0
        };
        
        this.uploads.unshift(upload);
        this.updateUploadHistory();
        this.showUploadProgress(true);
        
        try {
            const xhr = new XMLHttpRequest();
            
            // Track upload progress
            xhr.upload.addEventListener('progress', (e) => {
                if (e.lengthComputable) {
                    const progress = (e.loaded / e.total) * 100;
                    upload.progress = progress;
                    this.updateUploadProgress(progress);
                    this.updateUploadHistory();
                }
            });
            
            // Handle completion
            xhr.addEventListener('load', () => {
                if (xhr.status === 200) {
                    upload.status = 'completed';
                    this.showMessage(`${file.name} uploaded successfully!`, 'success');
                } else {
                    upload.status = 'failed';
                    this.showMessage(`Failed to upload ${file.name}`, 'error');
                }
                
                this.updateUploadHistory();
                this.updateStats();
                this.showUploadProgress(false);
            });
            
            xhr.addEventListener('error', () => {
                upload.status = 'failed';
                this.showMessage(`Failed to upload ${file.name}`, 'error');
                this.updateUploadHistory();
                this.updateStats();
                this.showUploadProgress(false);
            });
            
            // Send request
            xhr.open('POST', '/api/upload-video');
            xhr.setRequestHeader('Authorization', `Bearer ${this.sessionId}`);
            xhr.send(formData);
            
        } catch (error) {
            console.error('Upload error:', error);
            upload.status = 'failed';
            this.showMessage(`Failed to upload ${file.name}`, 'error');
            this.updateUploadHistory();
            this.updateStats();
            this.showUploadProgress(false);
        }
    }
    
    async loadUploadHistory() {
        try {
            const response = await fetch('/api/my-uploads', {
                headers: { 'Authorization': `Bearer ${this.sessionId}` }
            });
            
            if (response.ok) {
                const serverUploads = await response.json();
                
                // Merge server uploads with local tracking
                const allUploads = [...this.uploads];
                
                for (const serverUpload of serverUploads) {
                    if (!allUploads.find(u => u.name === serverUpload.name && u.timestamp === serverUpload.timestamp)) {
                        allUploads.push({
                            ...serverUpload,
                            status: 'completed',
                            progress: 100
                        });
                    }
                }
                
                // Sort by timestamp (newest first)
                this.uploads = allUploads.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
                this.updateUploadHistory();
            }
        } catch (error) {
            console.error('Error loading upload history:', error);
        }
    }
    
    updateUploadHistory() {
        const container = document.getElementById('uploadHistory');
        
        if (this.uploads.length === 0) {
            container.innerHTML = `
                <div style="text-align: center; padding: 40px; color: #718096;">
                    <div style="font-size: 3rem; margin-bottom: 15px;">📁</div>
                    <div>No uploads yet</div>
                    <div style="font-size: 0.9em; margin-top: 5px;">Start by uploading your first video above!</div>
                </div>
            `;
            return;
        }
        
        container.innerHTML = this.uploads.map(upload => `
            <div class="upload-item">
                <div class="upload-info">
                    <div class="upload-name">🎥 ${upload.name}</div>
                    <div class="upload-details">
                        ${this.formatFileSize(upload.size)} • 
                        ${new Date(upload.timestamp).toLocaleString()}
                        ${upload.status === 'uploading' ? ` • ${Math.round(upload.progress)}% complete` : ''}
                    </div>
                </div>
                <div class="upload-status status-${upload.status}">
                    ${upload.status === 'uploading' ? '⏳ Processing' : 
                      upload.status === 'completed' ? '✅ Completed' : 
                      '❌ Failed'}
                </div>
            </div>
        `).join('');
    }
    
    updateStats() {
        const total = this.uploads.length;
        const completed = this.uploads.filter(u => u.status === 'completed').length;
        const processing = this.uploads.filter(u => u.status === 'uploading').length;
        
        document.getElementById('totalUploads').textContent = total;
        document.getElementById('completedUploads').textContent = completed;
        document.getElementById('processingUploads').textContent = processing;
    }
    
    showUploadProgress(show) {
        const progressEl = document.getElementById('uploadProgress');
        progressEl.style.display = show ? 'block' : 'none';
        
        if (!show) {
            this.updateUploadProgress(0);
        }
    }
    
    updateUploadProgress(progress) {
        document.getElementById('progressFill').style.width = `${progress}%`;
        document.getElementById('progressText').textContent = `Uploading... ${Math.round(progress)}%`;
    }
    
    showMessage(text, type) {
        const messageEl = document.getElementById('message');
        messageEl.textContent = text;
        messageEl.className = `message ${type}`;
        messageEl.style.display = 'block';
        
        // Auto-hide info messages after 3 seconds
        if (type === 'info') {
            setTimeout(() => {
                messageEl.style.display = 'none';
            }, 3000);
        } else {
            setTimeout(() => {
                messageEl.style.display = 'none';
            }, 5000);
        }
    }
    
    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
}

// Global functions
function logout() {
    fetch('/api/logout', {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${localStorage.getItem('session_id')}` }
    }).finally(() => {
        localStorage.clear();
        window.location.href = '/login.html';
    });
}

// Initialize user dashboard
window.addEventListener('load', () => {
    window.userDashboard = new UserDashboard();
});