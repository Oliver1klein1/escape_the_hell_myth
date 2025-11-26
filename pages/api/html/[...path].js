import fs from 'fs';
import path from 'path';

export default function handler(req, res) {
  const { path: filePath } = req.query;
  
  // Reconstruct the file path
  const requestedPath = Array.isArray(filePath) ? filePath.join('/') : filePath || 'index';
  const fullPath = path.join(process.cwd(), `${requestedPath}.html`);
  
  // Security check - prevent directory traversal
  const resolvedPath = path.resolve(fullPath);
  const rootPath = path.resolve(process.cwd());
  
  if (!resolvedPath.startsWith(rootPath)) {
    return res.status(403).json({ error: 'Forbidden' });
  }
  
  try {
    if (!fs.existsSync(fullPath)) {
      return res.status(404).json({ error: 'File not found' });
    }
    
    let htmlContent = fs.readFileSync(fullPath, 'utf8');
    
    // Fix image paths to use API route for serving from root directory
    // Convert relative image paths like "cover.jpg" to "/api/static/cover.jpg"
    htmlContent = htmlContent.replace(/src="([^"]+\.(jpg|jpeg|png|gif|svg))"/gi, (match, imgPath) => {
      // If it's already an absolute path or URL, keep it
      if (imgPath.startsWith('/') || imgPath.startsWith('http')) {
        return match;
      }
      // Otherwise, route through API
      return `src="/api/static/${imgPath}"`;
    });
    
    // Set proper content type
    res.setHeader('Content-Type', 'text/html; charset=utf-8');
    res.status(200).send(htmlContent);
  } catch (error) {
    console.error('Error reading HTML file:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
}


