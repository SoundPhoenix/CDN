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

### Option 1: Simple File Server
1. Open `index.html` directly in your web browser
2. All functionality will work except for actual directory navigation

### Option 2: Local Development Server
1. Run the included Python server:
   ```bash
   python3 server.py
   ```
2. Open your browser to `http://localhost:8000`

### Option 3: Web Server Deployment
1. Upload all files to your web server
2. Access the site through your domain

## Directory Structure

```
CDN/
├── index.html          # Main website page
├── style.css           # Styling and responsive design
├── script.js           # JavaScript functionality
├── server.py           # Local development server
├── RAF-Backend/        # Backend files directory
├── Assets/             # Assets directory
├── Videos/             # Videos directory
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

## Browser Compatibility

- Chrome/Chromium 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## License

This project is licensed under the GNU General Public License v3.0 - see the LICENSE file for details.