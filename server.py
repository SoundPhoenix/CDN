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
from urllib.parse import urlparse

class RAFCDNRequestHandler(http.server.SimpleHTTPRequestHandler):
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
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        
        # Cache control headers
        if self.path.endswith(('.css', '.js')):
            self.send_header('Cache-Control', 'public, max-age=31536000, immutable')
        elif self.path.startswith(('/RAF-Backend/', '/Assets/', '/Videos/')):
            self.send_header('Cache-Control', 'public, max-age=3600')
        
        super().end_headers()

    def do_GET(self):
        # Handle directory requests by serving index.html if it exists
        if self.path.endswith('/') and self.path != '/':
            index_path = self.path + 'index.html'
            if os.path.exists('.' + index_path):
                self.path = index_path
        
        # For root path, always serve the main index.html
        if self.path == '/':
            self.path = '/index.html'
            
        return super().do_GET()

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