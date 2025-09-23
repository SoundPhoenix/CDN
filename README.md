# RAF-CDN Static Website

A modern, responsive directory listing website designed for Cloudflare Pages deployment.

## 🚀 Quick Deploy to Cloudflare Pages

1. **Fork or clone this repository**
2. **Connect to Cloudflare Pages**:
   - Go to [Cloudflare Pages](https://pages.cloudflare.com/)
   - Click "Create a project" → "Connect to Git"
   - Select this repository
3. **Configure build settings**:
   - Framework preset: `None` (Static site)
   - Build command: *(leave empty)*
   - Build output directory: `/` (root directory)
   - Root directory: `/` (or leave empty)
4. **Deploy**: Click "Save and Deploy"

## 📁 Directory Structure

```
CDN/
├── index.html          # Main website page
├── style.css           # Styling and responsive design
├── script.js           # JavaScript functionality
├── _headers            # Cloudflare Pages headers
├── _redirects          # Cloudflare Pages redirects
├── wrangler.toml       # Cloudflare configuration
├── Assets/             # Assets directory with index.html
├── RAF-Backend/        # Backend directory with index.html
├── Videos/             # Videos directory with index.html
└── Public/             # Original files (reference)
```

## ✨ Features

- **Clean Interface**: Professional design with RAF-CDN branding
- **Directory Management**: Add, edit, and delete directories
- **Search Functionality**: Real-time directory search
- **Responsive Design**: Works on desktop and mobile
- **Local Storage**: Remembers directory configuration
- **Icon Matching**: Automatic icons based on directory names

## 🔧 Local Development

```bash
# Simple Python server
python3 -m http.server 8000

# Or use the included server
python3 server.py
```

Open `http://localhost:8000` in your browser.

## 📚 Documentation

- [Detailed Setup Guide](Public/README.md)
- [Cloudflare Deployment Guide](CLOUDFLARE_DEPLOYMENT.md)

## 🛠️ Troubleshooting

**"No loader configured for .html files" Error**: 
This has been fixed by moving core files to the root directory where Cloudflare Pages expects them.

## 📄 License

GPL-3.0 License - see [LICENSE](Public/LICENSE) for details.