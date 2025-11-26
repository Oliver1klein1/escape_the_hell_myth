import fs from 'fs';
import path from 'path';

export default function handler(req, res) {
  const { path: filePath } = req.query;
  
  // Reconstruct the file path
  const requestedPath = Array.isArray(filePath) ? filePath.join('/') : filePath;
  const fullPath = path.join(process.cwd(), requestedPath);
  
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
    
    const fileContent = fs.readFileSync(fullPath);
    const ext = path.extname(fullPath).toLowerCase();
    
    // Set proper content type based on file extension
    const contentTypes = {
      '.jpg': 'image/jpeg',
      '.jpeg': 'image/jpeg',
      '.png': 'image/png',
      '.gif': 'image/gif',
      '.svg': 'image/svg+xml',
      '.css': 'text/css',
      '.js': 'application/javascript',
      '.ico': 'image/x-icon',
    };
    
    res.setHeader('Content-Type', contentTypes[ext] || 'application/octet-stream');
    res.status(200).send(fileContent);
  } catch (error) {
    console.error('Error reading static file:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
}



