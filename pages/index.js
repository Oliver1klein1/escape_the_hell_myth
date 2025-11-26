import { useEffect } from 'react';
import Head from 'next/head';
import fs from 'fs';
import path from 'path';

export default function Home({ htmlContent, headContent }) {
  useEffect(() => {
    // Inject head content (styles, links, etc.)
    if (headContent) {
      const parser = new DOMParser();
      const headDoc = parser.parseFromString(`<head>${headContent}</head>`, 'text/html');
      const headElements = headDoc.head.children;
      
      Array.from(headElements).forEach((element) => {
        // Skip title as Next.js Head handles it
        if (element.tagName.toLowerCase() !== 'title') {
          const newElement = document.createElement(element.tagName.toLowerCase());
          Array.from(element.attributes).forEach((attr) => {
            newElement.setAttribute(attr.name, attr.value);
          });
          if (element.innerHTML) {
            newElement.innerHTML = element.innerHTML;
          }
          document.head.appendChild(newElement);
        }
      });
    }
    
    // Execute any scripts in the body content
    const container = document.getElementById('html-content');
    if (container && htmlContent) {
      const scripts = container.querySelectorAll('script');
      scripts.forEach((oldScript) => {
        const newScript = document.createElement('script');
        Array.from(oldScript.attributes).forEach((attr) => {
          newScript.setAttribute(attr.name, attr.value);
        });
        newScript.appendChild(document.createTextNode(oldScript.innerHTML));
        oldScript.parentNode.replaceChild(newScript, oldScript);
      });
    }
  }, [htmlContent, headContent]);

  // Extract title from head content
  const titleMatch = headContent?.match(/<title>(.*?)<\/title>/i);
  const title = titleMatch ? titleMatch[1] : 'Escape The Hell Myth';

  return (
    <>
      <Head>
        <title>{title}</title>
        <meta charSet="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      </Head>
      <div id="html-content" dangerouslySetInnerHTML={{ __html: htmlContent }} />
    </>
  );
}

export async function getServerSideProps() {
  try {
    const filePath = path.join(process.cwd(), 'index.html');
    const htmlContent = fs.readFileSync(filePath, 'utf8');
    
    // Extract body content
    const bodyMatch = htmlContent.match(/<body[^>]*>([\s\S]*?)<\/body>/i);
    let bodyContent = bodyMatch ? bodyMatch[1] : htmlContent;
    
    // Fix image paths to use API route for serving from root directory
    // Convert relative image paths like "cover.jpg" to "/api/static/cover.jpg"
    bodyContent = bodyContent.replace(/src="([^"]+\.(jpg|jpeg|png|gif|svg))"/gi, (match, imgPath) => {
      // If it's already an absolute path or URL, keep it
      if (imgPath.startsWith('/') || imgPath.startsWith('http')) {
        return match;
      }
      // Otherwise, route through API
      return `src="/api/static/${imgPath}"`;
    });
    
    // Extract head content (styles, links, etc.)
    const headMatch = htmlContent.match(/<head[^>]*>([\s\S]*?)<\/head>/i);
    const headContent = headMatch ? headMatch[1] : '';
    
    return {
      props: {
        htmlContent: bodyContent,
        headContent: headContent,
      },
    };
  } catch (error) {
    console.error('Error reading index.html:', error);
    return {
      props: {
        htmlContent: '<h1>Error loading page</h1>',
        headContent: '',
      },
    };
  }
}

