#!/usr/bin/env python3
"""
Enhanced HTTP server for RAF-CDN that can run behind any server.
Supports configuration for production deployment.
"""

import http.server
import socketserver
import os
import sys
import argparse
import json
import cgi
import shutil
from urllib.parse import urlparse, parse_qs
from auth import UserManager

class RAFCDNRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.user_manager = UserManager()
        super().__init__(*args, **kwargs)
    
    def end_headers(self):
        # Security headers
        self.send_header('X-Frame-Options', 'DENY')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('X-XSS-Protection', '1; mode=block')
        self.send_header('Referrer-Policy', 'strict-origin-when-cross-origin')
        self.send_header('Content-Security-Policy', 
                        "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; font-src 'self' data:; img-src 'self' data:")
        
        # CORS headers (for development - adjust for production)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        
        # Cache control headers
        if self.path.endswith(('.css', '.js')):
            self.send_header('Cache-Control', 'public, max-age=31536000, immutable')
        elif self.path.startswith(('/RAF-Backend/', '/Assets/', '/Videos/')):
            self.send_header('Cache-Control', 'public, max-age=3600')
        
        super().end_headers()

    def do_OPTIONS(self):
        """Handle preflight requests"""
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        """Handle POST requests for API endpoints"""
        if self.path.startswith('/api/'):
            self.handle_api_request()
        else:
            self.send_error(404, "Not Found")
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path.startswith('/api/'):
            self.handle_api_request()
        else:
            # Handle directory requests by serving index.html if it exists
            if self.path.endswith('/') and self.path != '/':
                index_path = self.path + 'index.html'
                if os.path.exists('.' + index_path):
                    self.path = index_path
            
            # For root path, check if user is authenticated
            if self.path == '/':
                # If user has session, redirect to appropriate dashboard
                auth_header = self.headers.get('Authorization')
                if auth_header and auth_header.startswith('Bearer '):
                    session_id = auth_header.split(' ', 1)[1]
                    user_info = self.user_manager.get_user_from_session(session_id)
                    if user_info:
                        if user_info['role'] == 'admin':
                            self.path = '/admin.html'
                        else:
                            self.path = '/user.html'
                    else:
                        self.path = '/login.html'
                else:
                    self.path = '/login.html'
            
            # Serve index.html for root path if no session
            if self.path == '/':
                self.path = '/login.html'
                
            return super().do_GET()
    
    def handle_api_request(self):
        """Handle API requests"""
        try:
            if self.path == '/api/login' and self.command == 'POST':
                self.handle_login()
            elif self.path == '/api/logout' and self.command == 'POST':
                self.handle_logout()
            elif self.path == '/api/ensure-demo-user' and self.command == 'POST':
                self.handle_ensure_demo_user()
            elif self.path == '/api/activity-log' and self.command == 'GET':
                self.handle_activity_log()
            elif self.path == '/api/users' and self.command == 'GET':
                self.handle_get_users()
            elif self.path == '/api/videos' and self.command == 'GET':
                self.handle_get_videos()
            elif self.path == '/api/my-uploads' and self.command == 'GET':
                self.handle_get_my_uploads()
            elif self.path == '/api/create-user' and self.command == 'POST':
                self.handle_create_user()
            elif self.path == '/api/upload-video' and self.command == 'POST':
                self.handle_upload_video()
            else:
                self.send_error(404, "API endpoint not found")
        except Exception as e:
            print(f"API Error: {e}")
            self.send_json_response({'error': 'Internal server error'}, 500)
    
    def handle_login(self):
        """Handle user login"""
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
            username = data.get('username')
            password = data.get('password')
            
            session_id = self.user_manager.authenticate(username, password)
            
            if session_id:
                user_info = self.user_manager.get_user_from_session(session_id)
                self.send_json_response({
                    'success': True,
                    'session_id': session_id,
                    'username': user_info['username'],
                    'role': user_info['role']
                })
            else:
                self.send_json_response({'error': 'Invalid credentials'}, 401)
                
        except json.JSONDecodeError:
            self.send_json_response({'error': 'Invalid JSON'}, 400)
        except Exception as e:
            print(f"Login error: {e}")
            self.send_json_response({'error': 'Login failed'}, 500)
    
    def handle_logout(self):
        """Handle user logout"""
        session_id = self.get_session_id()
        if session_id:
            self.user_manager.logout(session_id)
        
        self.send_json_response({'success': True})
    
    def handle_ensure_demo_user(self):
        """Ensure demo user exists"""
        # Create demo user if it doesn't exist
        if 'user' not in self.user_manager.users:
            self.user_manager.register_user('user', 'user123', 'user')
        
        self.send_json_response({'success': True})
    
    def handle_activity_log(self):
        """Get activity log (admin only)"""
        if not self.check_admin_auth():
            return
        
        logs = self.user_manager.get_activity_logs()
        self.send_json_response(logs)
    
    def handle_get_users(self):
        """Get users list (admin only)"""
        if not self.check_admin_auth():
            return
        
        users = []
        for username, user_data in self.user_manager.users.items():
            users.append({
                'username': username,
                'role': user_data['role'],
                'created_at': user_data['created_at']
            })
        
        self.send_json_response(users)
    
    def handle_get_videos(self):
        """Get videos list"""
        if not self.check_auth():
            return
        
        videos_dir = 'Videos'
        videos = []
        
        if os.path.exists(videos_dir):
            for filename in os.listdir(videos_dir):
                file_path = os.path.join(videos_dir, filename)
                if os.path.isfile(file_path) and filename.lower().endswith(('.mp4', '.avi', '.mov', '.mkv', '.webm')):
                    stat = os.stat(file_path)
                    videos.append({
                        'name': filename,
                        'size': stat.st_size,
                        'uploaded_at': stat.st_mtime
                    })
        
        self.send_json_response(videos)
    
    def handle_get_my_uploads(self):
        """Get current user's uploads"""
        user_info = self.check_auth()
        if not user_info:
            return
        
        # For now, return all videos - in a real system, you'd track per-user uploads
        videos_dir = 'Videos'
        uploads = []
        
        if os.path.exists(videos_dir):
            for filename in os.listdir(videos_dir):
                file_path = os.path.join(videos_dir, filename)
                if os.path.isfile(file_path) and filename.lower().endswith(('.mp4', '.avi', '.mov', '.mkv', '.webm')):
                    stat = os.stat(file_path)
                    uploads.append({
                        'name': filename,
                        'size': stat.st_size,
                        'timestamp': stat.st_mtime,
                        'status': 'completed'
                    })
        
        self.send_json_response(uploads)
    
    def handle_create_user(self):
        """Create new user (admin only)"""
        if not self.check_admin_auth():
            return
        
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
            username = data.get('username')
            password = data.get('password')
            role = data.get('role', 'user')
            
            if not username or not password:
                self.send_json_response({'error': 'Username and password required'}, 400)
                return
            
            if self.user_manager.register_user(username, password, role):
                self.send_json_response({'success': True})
            else:
                self.send_json_response({'error': 'User already exists'}, 409)
                
        except json.JSONDecodeError:
            self.send_json_response({'error': 'Invalid JSON'}, 400)
    
    def handle_upload_video(self):
        """Handle video upload"""
        user_info = self.check_auth()
        if not user_info:
            return
        
        try:
            # Ensure Videos directory exists
            os.makedirs('Videos', exist_ok=True)
            
            # Parse multipart form data
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST', 'CONTENT_TYPE': self.headers['Content-Type']}
            )
            
            video_field = form['video']
            if video_field.filename:
                # Save the uploaded file
                filename = video_field.filename
                file_path = os.path.join('Videos', filename)
                
                with open(file_path, 'wb') as f:
                    shutil.copyfileobj(video_field.file, f)
                
                # Log the upload
                self.user_manager.log_activity(
                    user_info['username'], 
                    'video_upload', 
                    f'Uploaded video: {filename}'
                )
                
                self.send_json_response({'success': True, 'filename': filename})
            else:
                self.send_json_response({'error': 'No file provided'}, 400)
                
        except Exception as e:
            print(f"Upload error: {e}")
            self.send_json_response({'error': 'Upload failed'}, 500)
    
    def get_session_id(self):
        """Extract session ID from Authorization header"""
        auth_header = self.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            return auth_header.split(' ', 1)[1]
        return None
    
    def check_auth(self):
        """Check if user is authenticated"""
        session_id = self.get_session_id()
        if not session_id:
            self.send_json_response({'error': 'Authentication required'}, 401)
            return None
        
        user_info = self.user_manager.get_user_from_session(session_id)
        if not user_info:
            self.send_json_response({'error': 'Invalid session'}, 401)
            return None
        
        return user_info
    
    def check_admin_auth(self):
        """Check if user is authenticated as admin"""
        user_info = self.check_auth()
        if not user_info:
            return False
        
        if user_info['role'] != 'admin':
            self.send_json_response({'error': 'Admin access required'}, 403)
            return False
        
        return True
    
    def send_json_response(self, data, status=200):
        """Send JSON response"""
        response = json.dumps(data).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(response)))
        self.end_headers()
        self.wfile.write(response)

def load_config():
    """Load configuration from config file if it exists"""
    config_file = 'server.config.json'
    default_config = {
        'host': '0.0.0.0',  # Changed to allow external connections
        'port': 8000,
        'debug': False,
        'title': 'RAF-CDN Server'
    }
    
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
                # Merge with defaults
                for key in default_config:
                    config.setdefault(key, default_config[key])
                return config
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not load config file: {e}")
            print("Using default configuration.")
    
    return default_config

def create_sample_config():
    """Create a sample configuration file"""
    config = {
        "host": "0.0.0.0",
        "port": 8000,
        "debug": False,
        "title": "RAF-CDN Server",
        "_comment": "host 0.0.0.0 allows external connections. Use 127.0.0.1 for localhost only."
    }
    
    with open('server.config.json.sample', 'w') as f:
        json.dump(config, f, indent=2)
    print("Sample configuration created: server.config.json.sample")

def main():
    parser = argparse.ArgumentParser(description='RAF-CDN HTTP Server')
    parser.add_argument('--host', default=None, help='Host to bind to (default: from config or 0.0.0.0)')
    parser.add_argument('--port', type=int, default=None, help='Port to bind to (default: from config or 8000)')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('--create-config', action='store_true', help='Create sample configuration file')
    
    args = parser.parse_args()
    
    if args.create_config:
        create_sample_config()
        return
    
    # Load configuration
    config = load_config()
    
    # Override with command line arguments
    host = args.host or config['host']
    port = args.port or config['port']
    debug = args.debug or config.get('debug', False)
    title = config.get('title', 'RAF-CDN Server')
    
    # Change to the directory containing this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Verify required files exist
    required_files = ['index.html', 'style.css', 'script.js']
    missing_files = [f for f in required_files if not os.path.exists(f)]
    if missing_files:
        print(f"Error: Missing required files: {', '.join(missing_files)}")
        print("Make sure you're running this script from the CDN root directory.")
        sys.exit(1)
    
    try:
        with socketserver.TCPServer((host, port), RAFCDNRequestHandler) as httpd:
            print(f"🚀 {title} running at http://{host}:{port}")
            if host == '0.0.0.0':
                print(f"   Also accessible via http://localhost:{port}")
            print(f"   Debug mode: {'ON' if debug else 'OFF'}")
            print("   Press Ctrl+C to stop the server")
            print()
            
            if debug:
                print("Debug info:")
                print(f"  - Working directory: {os.getcwd()}")
                print(f"  - Available directories: {[d for d in os.listdir('.') if os.path.isdir(d) and not d.startswith('.')]}")
                print()
            
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\n✋ Server stopped by user.")
                
    except OSError as e:
        if e.errno == 98:  # Address already in use
            print(f"❌ Error: Port {port} is already in use.")
            print("   Try a different port with --port <number>")
        elif e.errno == 13:  # Permission denied
            print(f"❌ Error: Permission denied to bind to {host}:{port}")
            print("   Try running with sudo or use a port > 1024")
        else:
            print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()