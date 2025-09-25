// Admin Panel JavaScript
class AdminPanel {
    constructor() {
        this.sessionId = localStorage.getItem('session_id');
        this.username = localStorage.getItem('username');
        this.init();
    }
    
    async init() {
        // Check authentication
        if (!this.sessionId || localStorage.getItem('user_role') !== 'admin') {
            window.location.href = '/login.html';
            return;
        }
        
        // Set current user
        document.getElementById('currentUser').textContent = this.username;
        
        // Setup event listeners
        this.setupEventListeners();
        
        // Load initial data
        await this.refreshData();
    }
    
    setupEventListeners() {
        // Video upload
        const videoUpload = document.getElementById('videoUpload');
        const uploadArea = document.getElementById('videoUploadArea');
        
        videoUpload.addEventListener('change', (e) => this.handleVideoUpload(e.target.files));
        
        // Drag and drop
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('dragover');
        });
        
        uploadArea.addEventListener('dragleave', () => {
            uploadArea.classList.remove('dragover');
        });
        
        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
            this.handleVideoUpload(e.dataTransfer.files);
        });
        
        uploadArea.addEventListener('click', () => {
            videoUpload.click();
        });
        
        // Create user form
        document.getElementById('createUserForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.createUser();
        });
    }
    
    async refreshData() {
        this.showMessage('Refreshing data...', 'info');
        
        try {
            await Promise.all([
                this.loadActivityLog(),
                this.loadUsers(),
                this.loadVideos()
            ]);
            
            this.showMessage('Data refreshed successfully!', 'success');
        } catch (error) {
            console.error('Error refreshing data:', error);
            this.showMessage('Failed to refresh data', 'error');
        }
    }
    
    async loadActivityLog() {
        try {
            const response = await fetch('/api/activity-log', {
                headers: { 'Authorization': `Bearer ${this.sessionId}` }
            });
            
            if (response.ok) {
                const logs = await response.json();
                this.displayActivityLog(logs);
            }
        } catch (error) {
            console.error('Error loading activity log:', error);
        }
    }
    
    displayActivityLog(logs) {
        const container = document.getElementById('activityLogList');
        
        if (logs.length === 0) {
            container.innerHTML = '<div class="log-entry">No activity logs found</div>';
            return;
        }
        
        container.innerHTML = logs.map(log => `
            <div class="log-entry">
                <div>
                    <div class="log-action">${log.username} - ${log.action}</div>
                    <div class="log-details">${log.details}</div>
                </div>
                <div class="log-time">${new Date(log.timestamp).toLocaleString()}</div>
            </div>
        `).join('');
    }
    
    async loadUsers() {
        try {
            const response = await fetch('/api/users', {
                headers: { 'Authorization': `Bearer ${this.sessionId}` }
            });
            
            if (response.ok) {
                const users = await response.json();
                this.displayUsers(users);
            }
        } catch (error) {
            console.error('Error loading users:', error);
        }
    }
    
    displayUsers(users) {
        const container = document.getElementById('usersList');
        
        if (users.length === 0) {
            container.innerHTML = '<div class="user-item">No users found</div>';
            return;
        }
        
        container.innerHTML = users.map(user => `
            <div class="user-item">
                <div>
                    <strong>${user.username}</strong>
                    <div style="font-size: 0.9em; color: #718096;">
                        Created: ${new Date(user.created_at).toLocaleDateString()}
                    </div>
                </div>
                <div class="user-role role-${user.role}">${user.role}</div>
            </div>
        `).join('');
    }
    
    async loadVideos() {
        try {
            const response = await fetch('/api/videos', {
                headers: { 'Authorization': `Bearer ${this.sessionId}` }
            });
            
            if (response.ok) {
                const videos = await response.json();
                this.displayVideos(videos);
            }
        } catch (error) {
            console.error('Error loading videos:', error);
        }
    }
    
    displayVideos(videos) {
        const container = document.getElementById('videoList');
        
        if (videos.length === 0) {
            container.innerHTML = '<div style="text-align: center; color: #718096; padding: 40px;">No videos uploaded yet</div>';
            return;
        }
        
        container.innerHTML = videos.map(video => `
            <div class="video-item">
                <div class="video-info">
                    <div class="video-name">${video.name}</div>
                    <div class="video-size">${video.size ? this.formatFileSize(video.size) : 'Unknown size'}</div>
                    <div style="font-size: 0.8em; color: #718096; margin-top: 5px;">
                        Uploaded: ${new Date(video.uploaded_at).toLocaleDateString()}
                    </div>
                    ${video.uploaded_by ? `<div style="font-size: 0.8em; color: #718096;">By: ${video.uploaded_by}</div>` : ''}
                </div>
            </div>
        `).join('');
    }
    
    async handleVideoUpload(files) {
        if (files.length === 0) return;
        
        this.showMessage('Uploading videos...', 'info');
        
        for (const file of files) {
            if (!file.type.startsWith('video/')) {
                this.showMessage(`${file.name} is not a video file`, 'error');
                continue;
            }
            
            if (file.size > 500 * 1024 * 1024) { // 500MB limit
                this.showMessage(`${file.name} is too large (max 500MB)`, 'error');
                continue;
            }
            
            await this.uploadSingleVideo(file);
        }
        
        // Refresh video list after uploads
        await this.loadVideos();
    }
    
    async uploadSingleVideo(file) {
        const formData = new FormData();
        formData.append('video', file);
        
        try {
            const response = await fetch('/api/upload-video', {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${this.sessionId}` },
                body: formData
            });
            
            if (response.ok) {
                this.showMessage(`${file.name} uploaded successfully!`, 'success');
            } else {
                const error = await response.text();
                this.showMessage(`Failed to upload ${file.name}: ${error}`, 'error');
            }
        } catch (error) {
            console.error('Upload error:', error);
            this.showMessage(`Failed to upload ${file.name}`, 'error');
        }
    }
    
    async createUser() {
        const username = document.getElementById('newUsername').value.trim();
        const password = document.getElementById('newPassword').value;
        const role = document.getElementById('newUserRole').value;
        
        if (!username || !password) {
            this.showMessage('Please fill all fields', 'error');
            return;
        }
        
        try {
            const response = await fetch('/api/create-user', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${this.sessionId}`
                },
                body: JSON.stringify({ username, password, role })
            });
            
            if (response.ok) {
                this.showMessage(`User ${username} created successfully!`, 'success');
                document.getElementById('createUserForm').reset();
                await this.loadUsers();
            } else {
                const error = await response.text();
                this.showMessage(`Failed to create user: ${error}`, 'error');
            }
        } catch (error) {
            console.error('Error creating user:', error);
            this.showMessage('Failed to create user', 'error');
        }
    }
    
    showMessage(text, type) {
        const messageEl = document.getElementById('message');
        messageEl.textContent = text;
        messageEl.className = `message ${type}`;
        messageEl.style.display = 'block';
        
        setTimeout(() => {
            messageEl.style.display = 'none';
        }, 5000);
    }
    
    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
    
    scrollToSection(sectionId) {
        document.getElementById(sectionId).scrollIntoView({ behavior: 'smooth' });
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

function refreshData() {
    window.adminPanel.refreshData();
}

function scrollToSection(sectionId) {
    window.adminPanel.scrollToSection(sectionId);
}

// Initialize admin panel
window.addEventListener('load', () => {
    window.adminPanel = new AdminPanel();
});