# RAF-CDN Directory Listing Website

A modern, responsive web interface for browsing and managing CDN directories.

## Features

- **Clean Interface**: Professional design with "Welcome to RAF-CDN" branding
- **Directory Management**: Easy-to-use interface for adding, editing, and deleting directories
- **Search Functionality**: Real-time search to quickly find directories
- **Responsive Design**: Works on desktop and mobile devices
- **Local Storage**: Remembers your directory configuration between sessions
- **Icon Matching**: Automatically assigns appropriate icons based on directory names

## Getting Started

### Option 1: Simple File Server (Development)
1. Open `index.html` directly in your web browser
2. All functionality will work except for actual directory navigation

### Option 2: Local Development Server
1. Run the included Python server:
   ```bash
   python3 server.py
   ```
2. Open your browser to `http://localhost:8000`

### Option 3: Cloudflare Pages Deployment (Recommended)
1. **Connect your repository**:
   - Go to [Cloudflare Pages](https://pages.cloudflare.com/)
   - Click "Create a project"
   - Connect your GitHub repository

2. **Configure build settings**:
   - **Build command**: Leave empty (static site)
   - **Build output directory**: `/` (root directory)
   - **Root directory**: `/` (or leave empty)

3. **Environment variables** (optional):
   - No environment variables needed for basic setup

4. **Deploy**:
   - Click "Save and Deploy"
   - Your site will be available at `https://your-project.pages.dev`

### Option 4: Custom Domain on Cloudflare Pages
1. After deploying to Cloudflare Pages
2. Go to your project's "Custom domains" tab
3. Add your custom domain
4. Update the `wrangler.toml` file with your domain name

### Option 5: Traditional Web Server Deployment
1. Upload all files to your web server
2. Ensure your server supports directory browsing or has proper index files
3. Access the site through your domain

## Directory Structure

```
CDN/
├── index.html          # Main website page
├── style.css           # Styling and responsive design
├── script.js           # JavaScript functionality
├── server.py           # Local development server
├── package.json        # Project configuration
├── wrangler.toml       # Cloudflare Pages configuration
├── _headers            # Cloudflare Pages headers
├── _redirects          # Cloudflare Pages redirects
├── .gitignore          # Git ignore file
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

### Adding Directories
1. Enter a directory name in the "New directory name" field
2. Click "Add Directory"
3. The directory will be added with an appropriate icon

### Searching Directories
- Type in the search box to filter directories in real-time
- Click "Clear" to reset the search

### Managing Directories
- **Edit**: Click the "Edit" button to rename a directory
- **Delete**: Click the "Delete" button to remove a directory
- **Open**: Click on a directory card to access it (shows navigation info)

### Automatic Icon Assignment
The system automatically assigns icons based on directory names:
- 🖥️ for "backend", "api" related directories
- 🎥 for "video", "movie" related directories
- 🖼️ for "image", "photo" related directories
- 🎵 for "music", "audio" related directories
- 📄 for "doc", "text" related directories
- 💻 for "code", "src" related directories
- 📁 for all other directories

## Customization

### Adding New Directory Types
Edit the `addDirectory()` function in `script.js` to add new icon mappings:

```javascript
if (nameLower.includes('your-keyword')) icon = '🆕';
```

### Changing Styles
Modify `style.css` to customize colors, fonts, and layout. The design uses CSS Grid and Flexbox for responsive layouts.

### Default Directories
Edit the `directories` array in `script.js` to change the default directories that appear on first load.

## Cloudflare Pages Features

### Automatic HTTPS
- All deployments include automatic HTTPS certificates
- HTTP requests are automatically redirected to HTTPS

### Global CDN
- Your site is automatically distributed across Cloudflare's global network
- Fast loading times worldwide

### Custom Headers
- Security headers are automatically applied via `_headers` file
- Cache control headers optimize performance

### URL Redirects
- Directory paths are properly handled via `_redirects` file
- Fallback routing ensures the SPA works correctly

### Performance Optimization
- Static assets are cached for optimal performance
- Gzip compression is automatically applied
- HTTP/2 and HTTP/3 support

## Browser Compatibility

- Chrome/Chromium 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## License

This project is licensed under the GNU General Public License v3.0 - see the LICENSE file for details.