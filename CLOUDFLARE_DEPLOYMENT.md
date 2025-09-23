# Cloudflare Pages Deployment Guide

## Quick Setup

1. **Connect Repository**
   - Go to [Cloudflare Pages](https://pages.cloudflare.com/)
   - Click "Create a project" → "Connect to Git"
   - Select this repository

2. **Build Settings** (IMPORTANT - Updated Configuration)
   - Framework preset: `None` (Static site)
   - Build command: *(leave empty)*
   - Build output directory: `/` (root directory)
   - Root directory: `/` (or leave empty)

3. **Deploy**
   - Click "Save and Deploy"
   - Your site will be live at `https://your-project.pages.dev`

## Fix for "No loader configured for .html files" Error

This error was resolved by moving the core website files from the `Public/` subdirectory to the repository root directory. The files now in root include:

- `index.html` - Main website page
- `style.css` - Styling file  
- `script.js` - JavaScript functionality
- `package.json` - Project configuration
- `wrangler.toml` - Cloudflare configuration
- `_headers` - Security and caching headers
- `_redirects` - SPA routing and directory navigation
- `.gitignore` - Git ignore rules

## Directory Structure

```
CDN/
├── index.html          # Main website (moved from Public/)
├── style.css           # Styling (moved from Public/)
├── script.js           # JavaScript (moved from Public/)
├── package.json        # Project config (moved from Public/)
├── wrangler.toml       # Cloudflare config (moved from Public/)
├── _headers            # Headers config (moved from Public/)
├── _redirects          # Redirects config (moved from Public/)
├── .gitignore          # Git ignore (moved from Public/)
├── Public/             # Original files (kept for reference)
├── Assets/             # Assets directory with index.html
├── RAF-Backend/        # Backend directory with index.html
└── Videos/             # Videos directory with index.html
```

## Configuration Files

- `_headers`: Sets security and caching headers for all routes
- `_redirects`: Handles directory navigation and SPA routing
- `wrangler.toml`: Cloudflare Workers/Pages configuration
- `package.json`: Project metadata and dependencies

## Features Enabled

✅ Automatic HTTPS  
✅ Global CDN distribution  
✅ Directory navigation  
✅ Security headers  
✅ Asset caching  
✅ Mobile responsive design  
✅ Static site deployment (no build step required)

## Troubleshooting

### "No loader configured for .html files" Error
- **Cause**: HTML files not in the root directory where Cloudflare expects them
- **Solution**: Core files have been moved to root directory ✅

### Build fails or site doesn't load
- Verify build output directory is set to `/` (root)
- Ensure build command is empty for static sites
- Check that `index.html` exists in repository root

### Subdirectory navigation issues
- `_redirects` file handles directory routing
- Subdirectories have their own `index.html` files
- CSS references use `../style.css` from subdirectories

## Custom Domain (Optional)

After deployment:
1. Go to your project → "Custom domains"
2. Add your domain
3. Update DNS records as instructed
4. SSL certificate will be automatically provisioned

## Environment

This is a pure static site with no build process required. All functionality runs client-side using JavaScript and localStorage for persistence.