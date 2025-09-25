# User Authentication and Activity System
import json
import hashlib
import secrets
import datetime
from typing import Dict, List, Optional

class UserManager:
    def __init__(self, users_file='users.json', logs_file='activity_logs.json'):
        self.users_file = users_file
        self.logs_file = logs_file
        self.sessions = {}  # session_id -> user_info
        self.users = self.load_users()
        self.activity_logs = self.load_logs()
        
    def load_users(self) -> Dict:
        """Load users from file or create default admin user"""
        try:
            with open(self.users_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Create default admin user with password 'admin123'
            default_users = {
                'admin': {
                    'password_hash': self.hash_password('admin123'),
                    'role': 'admin',
                    'created_at': datetime.datetime.now().isoformat()
                }
            }
            self.save_users(default_users)
            return default_users
    
    def save_users(self, users: Dict):
        """Save users to file"""
        with open(self.users_file, 'w') as f:
            json.dump(users, f, indent=2)
    
    def load_logs(self) -> List:
        """Load activity logs from file"""
        try:
            with open(self.logs_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
    
    def save_logs(self):
        """Save activity logs to file"""
        with open(self.logs_file, 'w') as f:
            json.dump(self.activity_logs, f, indent=2)
    
    def hash_password(self, password: str) -> str:
        """Hash password with salt"""
        salt = secrets.token_hex(16)
        hash_obj = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
        return f"{salt}:{hash_obj.hex()}"
    
    def verify_password(self, password: str, password_hash: str) -> bool:
        """Verify password against hash"""
        try:
            salt, hash_hex = password_hash.split(':')
            hash_obj = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
            return hash_obj.hex() == hash_hex
        except ValueError:
            return False
    
    def authenticate(self, username: str, password: str) -> Optional[str]:
        """Authenticate user and return session ID"""
        if username in self.users:
            user = self.users[username]
            if self.verify_password(password, user['password_hash']):
                session_id = secrets.token_hex(32)
                self.sessions[session_id] = {
                    'username': username,
                    'role': user['role'],
                    'login_time': datetime.datetime.now().isoformat()
                }
                self.log_activity(username, 'login', f'User logged in')
                return session_id
        return None
    
    def get_user_from_session(self, session_id: str) -> Optional[Dict]:
        """Get user info from session ID"""
        return self.sessions.get(session_id)
    
    def logout(self, session_id: str) -> bool:
        """Logout user and remove session"""
        if session_id in self.sessions:
            user_info = self.sessions[session_id]
            self.log_activity(user_info['username'], 'logout', 'User logged out')
            del self.sessions[session_id]
            return True
        return False
    
    def register_user(self, username: str, password: str, role: str = 'user') -> bool:
        """Register new user"""
        if username in self.users:
            return False
        
        self.users[username] = {
            'password_hash': self.hash_password(password),
            'role': role,
            'created_at': datetime.datetime.now().isoformat()
        }
        self.save_users(self.users)
        self.log_activity('admin', 'user_created', f'New user created: {username} with role: {role}')
        return True
    
    def log_activity(self, username: str, action: str, details: str):
        """Log user activity"""
        log_entry = {
            'timestamp': datetime.datetime.now().isoformat(),
            'username': username,
            'action': action,
            'details': details
        }
        self.activity_logs.append(log_entry)
        # Keep only last 1000 logs to prevent file from growing too large
        if len(self.activity_logs) > 1000:
            self.activity_logs = self.activity_logs[-1000:]
        self.save_logs()
    
    def get_activity_logs(self, limit: int = 50) -> List:
        """Get recent activity logs"""
        return self.activity_logs[-limit:][::-1]  # Return most recent first