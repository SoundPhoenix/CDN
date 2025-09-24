# RAF-CDN Directory Listing Website

A modern, responsive web interface for browsing and managing CDN directories. Can be deployed on Cloudflare Pages or any traditional web server.

## Features

- **Clean Interface**: Professional design with "Welcome to RAF-CDN" branding
- **Directory Management**: Easy-to-use interface for adding, editing, and deleting directories
- **Search Functionality**: Real-time search to quickly find directories
- **Responsive Design**: Works on desktop and mobile devices
- **Local Storage**: Remembers your directory configuration between sessions
- **Icon Matching**: Automatically assigns appropriate icons based on directory names
- **Multiple Deployment Options**: Works with Cloudflare Pages, traditional servers, or locally

## Quick Start

### Option 1: Run Your Own Server (Recommended)

**Perfect for running behind your own server infrastructure!**

```bash
# Clone or download this repository
git clone <repository-url>
cd CDN

# Run the server (accessible from external networks)
python3 server.py

# Or with custom settings
python3 server.py --host 0.0.0.0 --port 8080 --debug
```

Your CDN will be available at `http://your-server-ip:8000`

**For production deployment**, see [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions including:
- Running behind nginx/apache reverse proxy
- Setting up systemd service
- SSL/HTTPS configuration
- Security considerations

### Option 2: Local Development

```bash
# Simple local testing
python3 server.py --host 127.0.0.1 --port 8000
```

Open `http://localhost:8000` in your browser.

### Option 3: Cloudflare Pages (Alternative)

1. **Connect your repository**:
   - Go to [Cloudflare Pages](https://pages.cloudflare.com/)
   - Click "Create a project"
   - Connect your GitHub repository

2. **Configure build settings**:
   - **Build command**: Leave empty (static site)
   - **Build output directory**: `/` (root directory)
   - **Root directory**: `/` (or leave empty)

3. **Deploy**:
   - Your site will be available at `https://your-project.pages.dev`

## Directory Structure

```
CDN/
├── index.html          # Main website page
├── style.css           # Styling and responsive design
├── script.js           # JavaScript functionality
├── server.py           # Enhanced server for any deployment
├── server.config.json  # Optional server configuration
├── DEPLOYMENT.md       # Detailed deployment guide
├── Public/             # Legacy Cloudflare Pages files
├── RAF-Backend/        # Backend files directory
│   ├── README.md       # Backend directory info
│   └── index.html      # Backend directory listing
├── Assets/             # Assets directory
│   ├── README.md       # Assets directory info
│   └── index.html      # Assets directory listing
├── Videos/             # Videos directory
│   ├── README.md       # Videos directory info
│   └── index.html      # Videos directory listing
└── README.md           # This file
```

## Usage

1. **Browse Directories**: Click on any directory tile to navigate to its contents
2. **Add Directories**: Use the "Add Directory" section to create new directory entries
3. **Search**: Use the search box to quickly find specific directories
4. **Edit/Delete**: Use the action buttons on each directory tile to modify or remove entries

## Server Configuration

### Command Line Options

```bash
python3 server.py --help

Options:
  --host HOST      Host to bind to (default: 0.0.0.0)
  --port PORT      Port to bind to (default: 8000)
  --debug          Enable debug mode
  --create-config  Create sample configuration file
```

### Configuration File

Create persistent settings:

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

## Deployment Options Comparison

| Method | Best For | Pros | Cons |
|--------|----------|------|------|
| **Own Server** | Full control, custom domains | Complete control, any port/host, behind firewall | Requires server management |
| **Cloudflare Pages** | Easy deployment, global CDN | Automatic HTTPS, global distribution | Less control, Cloudflare dependency |
| **Local Development** | Testing, development | Quick setup, no external dependencies | Not accessible externally |

## Advanced Features

### Server Features

- **External Network Access**: Configurable host binding (0.0.0.0 for external access)
- **Custom Ports**: Run on any available port
- **Security Headers**: Built-in security headers for production use
- **Reverse Proxy Ready**: Works seamlessly behind nginx/apache
- **Debug Mode**: Detailed logging and troubleshooting information
- **Configuration File**: Persistent settings via JSON configuration

### Web Interface Features

- **Real-time Directory Management**: Add, edit, delete directories without server restart
- **Persistent Configuration**: Settings saved in browser localStorage
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Search and Filter**: Quickly find directories in large collections
- **Icon Customization**: Emoji icons for easy visual identification

## Security

For production deployments:

1. **Use HTTPS**: Deploy behind a reverse proxy with SSL certificates
2. **Firewall Configuration**: Only expose necessary ports
3. **Access Control**: Consider adding authentication for sensitive content
4. **Regular Updates**: Keep Python and dependencies updated

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed security considerations.

## Browser Compatibility

- Chrome/Chromium 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## Contributing

1. Fork the repository
2. Create your feature branch
3. Make your changes
4. Test with both server deployment and Cloudflare Pages
5. Submit a pull request

## License

This project is licensed under the GNU General Public License v3.0 - see the LICENSE file for details.

---

## Migration from Cloudflare-Only Setup

If you previously could only use Cloudflare Pages, you can now:

✅ **Run on any server** with the enhanced `server.py`  
✅ **Use custom domains** without Cloudflare dependency  
✅ **Deploy behind corporate firewalls**  
✅ **Use any port/host configuration**  
✅ **Integrate with existing web server infrastructure**  

The web interface remains exactly the same - only the deployment method has been enhanced!