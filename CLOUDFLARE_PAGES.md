# Cloudflare Pages Deployment Guide

## Quick Setup

1. **Connect Repository**
   - Go to [Cloudflare Pages](https://pages.cloudflare.com/)
   - Click "Create a project" → "Connect to Git"
   - Select this repository

2. **Build Settings**
   - Framework preset: `None` (Static site)
   - Build command: *(leave empty)*
   - Build output directory: `/` 
   - Root directory: `/`

3. **Deploy**
   - Click "Save and Deploy"
   - Your site will be live at `https://your-project.pages.dev`

## Configuration Files

- `_headers`: Sets security and caching headers
- `_redirects`: Handles SPA routing and directory navigation
- `wrangler.toml`: Optional Cloudflare configuration
- `package.json`: Project metadata

## Features Enabled

✅ Automatic HTTPS  
✅ Global CDN distribution  
✅ Directory navigation  
✅ Security headers  
✅ Asset caching  
✅ Mobile responsive design  

## Custom Domain (Optional)

After deployment:
1. Go to your project → "Custom domains"
2. Add your domain
3. Update DNS records as instructed
4. SSL certificate will be automatically provisioned

## Environment

This is a pure static site with no build process required. All functionality runs client-side using JavaScript and localStorage for persistence.