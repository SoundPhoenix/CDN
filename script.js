// Default directories configuration
let directories = [
    { name: 'RAF-Backend', icon: '🖥️', url: '/RAF-Backend/' },
    { name: 'Assets', icon: '📁', url: '/Assets/' },
    { name: 'Videos', icon: '🎥', url: '/Videos/' }
];

// Load directories from localStorage if available
function loadDirectories() {
    const saved = localStorage.getItem('cdn-directories');
    if (saved) {
        directories = JSON.parse(saved);
    }
}

// Save directories to localStorage
function saveDirectories() {
    localStorage.setItem('cdn-directories', JSON.stringify(directories));
}

// Render directories
function renderDirectories(dirsToRender = directories) {
    const grid = document.getElementById('directoryGrid');
    
    if (dirsToRender.length === 0) {
        grid.innerHTML = '<div class="no-results">No directories found matching your search.</div>';
        return;
    }
    
    grid.innerHTML = dirsToRender.map(dir => `
        <div class="directory-item" onclick="openDirectory('${dir.url}')">
            <div class="directory-icon">${dir.icon}</div>
            <div class="directory-name">${dir.name}</div>
            <div class="directory-actions" onclick="event.stopPropagation()">
                <button class="edit-btn" onclick="editDirectory('${dir.name}')">Edit</button>
                <button class="delete-btn" onclick="deleteDirectory('${dir.name}')">Delete</button>
            </div>
        </div>
    `).join('');
}

// Open directory
function openDirectory(url) {
    // In a real CDN, this would navigate to the directory
    // For now, we'll show an alert
    alert(`Opening directory: ${url}\n\nIn a real CDN setup, this would navigate to the directory contents.`);
}

// Search functionality
function setupSearch() {
    const searchInput = document.getElementById('searchInput');
    searchInput.addEventListener('input', (e) => {
        const searchTerm = e.target.value.toLowerCase();
        const filtered = directories.filter(dir => 
            dir.name.toLowerCase().includes(searchTerm)
        );
        renderDirectories(filtered);
    });
}

// Clear search
function clearSearch() {
    document.getElementById('searchInput').value = '';
    renderDirectories(directories);
}

// Add new directory
function addDirectory() {
    const nameInput = document.getElementById('newDirName');
    const name = nameInput.value.trim();
    
    if (!name) {
        alert('Please enter a directory name.');
        return;
    }
    
    if (directories.some(dir => dir.name === name)) {
        alert('A directory with this name already exists.');
        return;
    }
    
    // Get icon based on directory name (simple logic)
    let icon = '📁'; // default
    const nameLower = name.toLowerCase();
    if (nameLower.includes('video') || nameLower.includes('movie')) icon = '🎥';
    else if (nameLower.includes('image') || nameLower.includes('photo')) icon = '🖼️';
    else if (nameLower.includes('music') || nameLower.includes('audio')) icon = '🎵';
    else if (nameLower.includes('backend') || nameLower.includes('api')) icon = '🖥️';
    else if (nameLower.includes('doc') || nameLower.includes('text')) icon = '📄';
    else if (nameLower.includes('code') || nameLower.includes('src')) icon = '💻';
    
    const newDir = {
        name: name,
        icon: icon,
        url: `/${name}/`
    };
    
    directories.push(newDir);
    saveDirectories();
    renderDirectories();
    nameInput.value = '';
    
    alert(`Directory "${name}" added successfully!`);
}

// Edit directory
function editDirectory(name) {
    const dir = directories.find(d => d.name === name);
    if (!dir) return;
    
    const newName = prompt('Enter new directory name:', dir.name);
    if (!newName || newName.trim() === '') return;
    
    const trimmedName = newName.trim();
    if (directories.some(d => d.name === trimmedName && d.name !== name)) {
        alert('A directory with this name already exists.');
        return;
    }
    
    dir.name = trimmedName;
    dir.url = `/${trimmedName}/`;
    
    saveDirectories();
    renderDirectories();
    
    alert(`Directory renamed to "${trimmedName}" successfully!`);
}

// Delete directory
function deleteDirectory(name) {
    if (!confirm(`Are you sure you want to delete the "${name}" directory?`)) {
        return;
    }
    
    directories = directories.filter(dir => dir.name !== name);
    saveDirectories();
    renderDirectories();
    
    alert(`Directory "${name}" deleted successfully!`);
}

// Handle Enter key for adding directories
function setupKeyboardShortcuts() {
    document.getElementById('newDirName').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            addDirectory();
        }
    });
    
    document.getElementById('searchInput').addEventListener('keypress', (e) => {
        if (e.key === 'Escape') {
            clearSearch();
        }
    });
}

// Initialize the application
function init() {
    loadDirectories();
    renderDirectories();
    setupSearch();
    setupKeyboardShortcuts();
    
    console.log('RAF-CDN Directory Listing initialized successfully!');
}

// Run initialization when DOM is loaded
document.addEventListener('DOMContentLoaded', init);