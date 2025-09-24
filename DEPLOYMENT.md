# RAF-CDN Server Deployment Guide

This guide explains how to deploy RAF-CDN behind your own server instead of using Cloudflare Pages.

## Quick Start

1. **Download/Clone the repository** to your server
2. **Run the server**:
   ```bash
   python3 server.py
   ```
3. **Access your CDN** at `http://your-server-ip:8000`

## Server Configuration

### Command Line Options

```bash
python3 server.py [OPTIONS]

Options:
  --host HOST      Host to bind to (default: 0.0.0.0)
  --port PORT      Port to bind to (default: 8000) 
  --debug          Enable debug mode
  --create-config  Create sample configuration file
  --help           Show help message
```

### Configuration File

Create a `server.config.json` file for persistent settings:

```bash
python3 server.py --create-config
cp server.config.json.sample server.config.json
```

Edit `server.config.json`:
```json
{
  "host": "0.0.0.0",
  "port": 8000,
  "debug": false,
  "title": "My RAF-CDN Server"
}
```

## Deployment Options

### Option 1: Direct Python Server (Recommended for small deployments)

```bash
# Run on default settings (0.0.0.0:8000)
python3 server.py

# Custom host and port
python3 server.py --host 192.168.1.100 --port 8080

# Debug mode for troubleshooting
python3 server.py --debug
```

### Option 2: Behind Reverse Proxy (Recommended for production)

#### Nginx Configuration

Add to your nginx config:

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Run RAF-CDN on localhost:
```bash
python3 server.py --host 127.0.0.1 --port 8000
```

#### Apache Configuration

Add to your Apache virtual host:

```apache
<VirtualHost *:80>
    ServerName your-domain.com
    
    ProxyPreserveHost On
    ProxyPass / http://127.0.0.1:8000/
    ProxyPassReverse / http://127.0.0.1:8000/
</VirtualHost>
```

### Option 3: Systemd Service (Linux)

Create `/etc/systemd/system/raf-cdn.service`:

```ini
[Unit]
Description=RAF-CDN Server
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/your/cdn
ExecStart=/usr/bin/python3 server.py --host 127.0.0.1 --port 8000
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable raf-cdn
sudo systemctl start raf-cdn
sudo systemctl status raf-cdn
```

## Security Considerations

### For Internet-Facing Deployments

1. **Use a reverse proxy** (nginx/apache) instead of direct Python server
2. **Enable HTTPS** with SSL certificates (Let's Encrypt recommended)
3. **Configure firewall** to only allow necessary ports
4. **Regular updates** - keep Python and dependencies updated
5. **Consider authentication** if serving sensitive content

### Host Binding

- `0.0.0.0` - Accepts connections from any IP (default for easy setup)
- `127.0.0.1` - Localhost only (recommended with reverse proxy)
- `192.168.1.x` - Specific network interface

## Directory Structure

The server expects this file structure:
```
CDN/
├── server.py           # Enhanced server script
├── index.html          # Main CDN interface
├── style.css           # Styling
├── script.js           # Frontend functionality
├── server.config.json  # Optional configuration
├── RAF-Backend/        # Example directory
│   └── index.html      # Directory listing
├── Assets/             # Example directory
│   └── index.html      # Directory listing
└── Videos/             # Example directory
    └── index.html      # Directory listing
```

## Features

✅ **External Network Access** - Configurable host binding  
✅ **Custom Ports** - Run on any available port  
✅ **Security Headers** - Built-in security headers  
✅ **Directory Navigation** - Full directory browsing  
✅ **Configuration File** - Persistent settings  
✅ **Debug Mode** - Troubleshooting information  
✅ **Reverse Proxy Ready** - Works behind nginx/apache  

## Troubleshooting

### Port Already in Use
```bash
# Check what's using the port
sudo netstat -tlnp | grep :8000

# Use a different port
python3 server.py --port 8080
```

### Permission Denied
```bash
# Use a port > 1024 or run with sudo
python3 server.py --port 8080

# Or for ports < 1024:
sudo python3 server.py --port 80
```

### Can't Access from Other Machines
- Check firewall settings
- Ensure host is set to `0.0.0.0`
- Verify network connectivity

### Debug Mode
```bash
python3 server.py --debug
```

This will show:
- Working directory
- Available directories
- Detailed error messages

## Migration from Cloudflare Pages

If you were previously using Cloudflare Pages:

1. **Files are now in root directory** instead of `/Public/`
2. **No need for `_headers` and `_redirects`** files (handled by server)
3. **Configuration is in `server.config.json`** instead of `wrangler.toml`
4. **Directory navigation works the same way**
5. **All frontend features remain identical**

The enhanced server provides the same functionality as Cloudflare Pages but with more control and customization options.