#!/usr/bin/env python3
"""
Comprehensive EPUB Creator for Gumroad and Amazon KDP
Creates both Gumroad and KDP-compliant EPUB files with all metadata and styling preserved.
"""

import os
import json
import shutil
import zipfile
import subprocess
import re
import uuid
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup

# Configuration
METADATA_FILE = 'book_metadata.json'
EPUBCCHECK_PATH = 'epubcheck-5.2.0/epubcheck.jar'

# Files to process in correct order
FILES_TO_PROCESS = [
    "copyright.html",
    "dedication.html",
    "toc.html",
    "introduction.html",
    "part1.html",
    "chapter1.html", "chapter2.html",
    "part2.html",
    "chapter3.html",
    "part3.html",
    "chapter4.html", "chapter5.html",
    "part4.html",
    "chapter6.html", "chapter7.html", "chapter8.html",
    "conclusion.html",
    "other-books.html",
    "appendix.html",
    "bibliography.html",
    "acknowledgments.html"
]

CORRECT_SPINE_ORDER = [
    "cover",
    "copyright",
    "dedication",
    "toc",
    "introduction",
    "part1",
    "chapter1",
    "chapter2",
    "part2",
    "chapter3",
    "part3",
    "chapter4",
    "chapter5",
    "part4",
    "chapter6",
    "chapter7",
    "chapter8",
    "conclusion",
    "other-books",
    "appendix",
    "bibliography",
    "acknowledgments"
]

def load_metadata():
    """Load book metadata from JSON file."""
    if not os.path.exists(METADATA_FILE):
        print(f"❌ No metadata file found: {METADATA_FILE}")
        return None
    
    with open(METADATA_FILE, 'r', encoding='utf-8') as f:
        metadata = json.load(f)
    
    return metadata

def ensure_directory_structure(base_dir):
    """Create EPUB directory structure."""
    dirs = [
        f'{base_dir}/META-INF',
        f'{base_dir}/OEBPS/Text',
        f'{base_dir}/OEBPS/Images',  # Use capital I to match XHTML references
        f'{base_dir}/OEBPS/Styles'
    ]
    
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)
    
    # Create mimetype file
    mimetype_path = f'{base_dir}/mimetype'
    if not os.path.exists(mimetype_path):
        with open(mimetype_path, 'w', encoding='utf-8') as f:
            f.write('application/epub+zip')
    
    # Create container.xml
    container_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
    <rootfiles>
        <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
    </rootfiles>
</container>'''
    
    container_path = f'{base_dir}/META-INF/container.xml'
    with open(container_path, 'w', encoding='utf-8') as f:
        f.write(container_xml)

def convert_html_to_xhtml(html_file_path, output_dir, kdp_mode=False):
    """Convert HTML to XHTML with style preservation."""
    
    # Read the HTML file
    with open(html_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parse with BeautifulSoup
    soup = BeautifulSoup(content, 'html.parser')
    
    # Extract the title
    title_tag = soup.find('title')
    title = title_tag.get_text() if title_tag else "Chapter"
    
    # Extract the body content
    body = soup.find('body')
    if not body:
        return None
    
    # Clean up the content for EPUB while preserving styling
    # Remove navigation elements but keep everything else
    for nav in body.find_all(['div'], class_=['navigation']):
        nav.decompose()
    
    # Remove navigation buttons container
    for nav_buttons in body.find_all(['div'], class_=['navigation-buttons']):
        nav_buttons.decompose()
    
    # Also remove any standalone navigation links
    for nav_link in body.find_all(['a'], class_=['nav-link']):
        nav_link.decompose()
    
    # Remove navigation button links
    for nav_button in body.find_all(['a'], class_=['nav-button']):
        nav_button.decompose()
    
    # Remove page numbers from TOC (EPUBs are reflowable)
    html_filename = os.path.basename(html_file_path)
    if html_filename == 'toc.html':
        page_number_spans = body.find_all('span')
        for span in page_number_spans:
            span_text = span.get_text().strip()
            if span_text.isdigit():
                span.decompose()
    
    # Update image src paths to EPUB format
    for img in body.find_all('img'):
        src = img.get('src', '')
        # Update to proper EPUB image path (use lowercase 'images' for consistency)
        if src and not src.startswith('../Images/'):
            img['src'] = f"../Images/{os.path.basename(src)}"
    
    # Update internal HTML links to XHTML links
    for link in body.find_all('a', href=True):
        href = link.get('href', '')
        # Only convert internal links (not external URLs starting with http/https)
        if href.endswith('.html') and not href.startswith('http'):
            # Convert .html to .xhtml for internal links
            link['href'] = href.replace('.html', '.xhtml')
    
    # Extract any inline styles from the original HTML
    style_content = ""
    style_tag = soup.find('style')
    if style_tag:
        # Get the style content and ensure it has type attribute
        style_text = style_tag.string or ""
        if style_text:
            style_content = f'<style type="text/css">{style_text}</style>'
    
    # Determine body class
    body_classes = []
    existing_class = body.get('class', [])
    if isinstance(existing_class, str):
        body_classes = [existing_class]
    elif isinstance(existing_class, list):
        body_classes = existing_class
    
    if kdp_mode:
        if 'kdp-mode' not in body_classes:
            body_classes.append('kdp-mode')
    
    # Build body class attribute
    body_class_attr = f' class="{" ".join(body_classes)}"' if body_classes else ''
    
    # Extract body content (without the body tag itself to avoid duplicates)
    # Remove HTML comments first to prevent them from being rendered as text
    from bs4 import Comment
    for comment in body.find_all(string=lambda text: isinstance(text, Comment)):
        comment.extract()
    
    # Also remove any text nodes that are just HTML comment strings
    for string in body.find_all(string=True):
        if isinstance(string, str) and string.strip().startswith('<!--') and string.strip().endswith('-->'):
            string.extract()
    
    # Extract body content - only actual HTML elements, not comments
    body_contents_list = []
    for child in body.children:
        if hasattr(child, 'name'):  # It's an element
            body_contents_list.append(str(child))
        elif isinstance(child, str):
            # Only include non-whitespace text that's not a comment
            stripped = child.strip()
            if stripped and not (stripped.startswith('<!--') or stripped == 'Introduction' or stripped == 'Dedication'):
                body_contents_list.append(child)
    
    body_contents = ''.join(body_contents_list)
    
    # Final cleanup: remove any remaining HTML comments or standalone section labels
    body_contents = re.sub(r'<!--.*?-->', '', body_contents, flags=re.DOTALL)
    body_contents = re.sub(r'^\s*(Introduction|Dedication|Chapter|Part)\s*\n', '', body_contents, flags=re.MULTILINE)
    
    # Create XHTML structure with preserved styling (simpler approach)
    xhtml_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <title>{title}</title>
    <link rel="stylesheet" type="text/css" href="../Styles/style.css"/>
    {style_content}
</head>
<body{body_class_attr}>
{body_contents}
</body>
</html>'''
    
    # Clean up the XHTML - but PRESERVE classes and styles
    # Fix common entities first
    xhtml_content = xhtml_content.replace('&nbsp;', '&#160;')  # Fix non-breaking space
    
    # Escape all unescaped ampersands (CRITICAL for XHTML validity)
    # In XHTML, ALL ampersands must be escaped as &amp; unless part of a valid entity
    # Use regex to find & that's not already part of a valid entity
    
    # First, convert &nbsp; and other common entities to numeric form to avoid confusion
    # Then escape all standalone & characters
    
    # Pattern: Find & that's NOT followed by a valid entity pattern
    # Valid entity patterns: &amp; &lt; &gt; &quot; &apos; &#123; &#x1F; &name;
    def escape_ampersands(text):
        # Protect existing valid entities by replacing them with placeholders
        entity_map = {}
        entity_counter = 0
        
        # Find all valid entity references
        def replace_entity(match):
            nonlocal entity_counter
            entity = match.group(0)
            placeholder = f'___ENTITY_{entity_counter}___'
            entity_map[placeholder] = entity
            entity_counter += 1
            return placeholder
        
        # Match valid entities: &name; or &#number; or &#xhex;
        text = re.sub(r'&(?:[a-zA-Z][a-zA-Z0-9]*|#\d+|#x[0-9a-fA-F]+);', replace_entity, text)
        
        # Now escape all remaining & characters
        text = text.replace('&', '&amp;')
        
        # Restore protected entities
        for placeholder, entity in entity_map.items():
            text = text.replace(placeholder, entity)
        
        return text
    
    xhtml_content = escape_ampersands(xhtml_content)
    
    # Convert all internal HTML links to XHTML links in the final output
    # Use regex to find and replace all .html links with .xhtml
    def replace_html_links(match):
        full_match = match.group(0)
        href = match.group(1)
        # Only convert internal links (not external URLs)
        if href.endswith('.html') and not href.startswith('http'):
            new_href = href.replace('.html', '.xhtml')
            return f'href="{new_href}"'
        return full_match
    
    # Replace all href="filename.html" with href="filename.xhtml"
    xhtml_content = re.sub(r'href="([^"]+\.html)"', replace_html_links, xhtml_content)
    
    # Get the filename for output
    filename = os.path.basename(html_file_path).replace('.html', '.xhtml')
    output_path = os.path.join(output_dir, filename)
    
    # Write the XHTML file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(xhtml_content)
    
    return filename

def copy_images(source_dir, dest_dir):
    """Copy all images to EPUB Images directory."""
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.svg']
    copied_count = 0
    
    for file in os.listdir(source_dir):
        if any(file.lower().endswith(ext) for ext in image_extensions):
            src_path = os.path.join(source_dir, file)
            dest_path = os.path.join(dest_dir, file)
            shutil.copy2(src_path, dest_path)
            copied_count += 1
    
    return copied_count

def create_content_opf(metadata, base_dir, kdp_mode=False, book_uuid=None):
    """Create content.opf file with complete metadata."""
    
    # Generate unique identifiers - use proper UUID format
    if not book_uuid:
        book_uuid = str(uuid.uuid4())
    book_id = book_uuid
    
    # Get all XHTML files from Text directory
    text_dir = Path(f'{base_dir}/OEBPS/Text')
    xhtml_files = list(text_dir.glob('*.xhtml'))
    
    # Get cover.xhtml from OEBPS root (if exists)
    cover_xhtml = Path(f'{base_dir}/OEBPS/cover.xhtml')
    
    # Get all image files (use capital I to match XHTML references)
    images_dir = Path(f'{base_dir}/OEBPS/Images')
    if not images_dir.exists():
        # Try lowercase as fallback
        images_dir = Path(f'{base_dir}/OEBPS/images')
    image_files = list(images_dir.glob('*')) if images_dir.exists() else []
    
    # Create manifest items
    manifest_items = []
    spine_items = []
    
    # Add cover.xhtml to manifest (if it exists)
    if cover_xhtml.exists():
        manifest_items.append(f'    <item id="cover" href="{cover_xhtml.name}" media-type="application/xhtml+xml"/>')
    
    # Add XHTML files to manifest
    for xhtml_file in sorted(xhtml_files):
        file_id = xhtml_file.stem
        manifest_items.append(f'    <item id="{file_id}" href="Text/{xhtml_file.name}" media-type="application/xhtml+xml"/>')
    
    # Add spine items in correct order
    for item_id in CORRECT_SPINE_ORDER:
        spine_items.append(f'    <itemref idref="{item_id}"/>')
    
    # Add images to manifest
    used_ids = set()
    used_ids.add('cover')
    used_ids.add('cover-image')
    
    # Get cover filename from metadata
    cover_filename = os.path.basename(metadata.get('cover_image', ''))
    
    for image_file in image_files:
        # Skip cover.jpg as it's already added as 'cover-image'
        if image_file.name == cover_filename:
            continue
        
        # Create unique ID
        base_id = image_file.stem.replace('-', '_').replace(' ', '_')
        file_id = base_id
        
        # Handle duplicate IDs
        counter = 1
        while file_id in used_ids:
            file_id = f"{base_id}_{counter}"
            counter += 1
        
        used_ids.add(file_id)
        
        if image_file.suffix.lower() in ['.jpg', '.jpeg']:
            media_type = 'image/jpeg'
        elif image_file.suffix.lower() == '.png':
            media_type = 'image/png'
        else:
            media_type = 'image/png'
        
        manifest_items.append(f'    <item id="{file_id}" href="Images/{image_file.name}" media-type="{media_type}"/>')
    
    # Add CSS file
    manifest_items.append('    <item id="css" href="Styles/style.css" media-type="text/css"/>')
    
    # Add NCX file
    manifest_items.append('    <item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>')
    
    # Get subtitle for title
    title_text = metadata.get('title', 'Untitled')
    if metadata.get('subtitle'):
        title_text = f"{title_text}: {metadata.get('subtitle')}"
    
    # Create content.opf
    content_opf = f'''<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="book-id" version="2.0">
    <metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf">
        <dc:identifier id="book-id" opf:scheme="UUID">{book_id}</dc:identifier>
        <dc:title>{title_text}</dc:title>
        <dc:creator opf:file-as="{metadata.get('author', 'Unknown')}" opf:role="aut">{metadata.get('author', 'Unknown')}</dc:creator>
        <dc:publisher>{metadata.get('publisher', 'Unknown Publisher')}</dc:publisher>
        <dc:date opf:event="publication">{metadata.get('publication_date', '2025')}</dc:date>
        <dc:language>{metadata.get('language', 'en')}</dc:language>
        <dc:subject>{metadata.get('tags', '')}</dc:subject>
        <dc:description>{metadata.get('description', '')}</dc:description>
        <meta name="cover" content="cover-image"/>
        <meta name="generator" content="EPUB Creator"/>
    </metadata>
    
    <manifest>
        <item id="cover-image" href="Images/{cover_filename}" media-type="image/jpeg"/>
{chr(10).join(manifest_items)}
    </manifest>
    
    <spine toc="ncx">
{chr(10).join(spine_items)}
    </spine>
    
    <guide>
        <reference type="cover" title="Cover" href="cover.xhtml"/>
        <reference type="toc" title="Table of Contents" href="Text/toc.xhtml"/>
    </guide>
</package>'''
    
    return content_opf

def copy_styles_file(base_dir, kdp_mode=False):
    """Copy styles.css file if it exists, and add KDP-specific styles."""
    styles_source = 'epub/OEBPS/styles.css'
    styles_dest = f'{base_dir}/OEBPS/Styles/style.css'
    
    if os.path.exists(styles_source):
        shutil.copy2(styles_source, styles_dest)
    else:
        # Create a basic styles file
        basic_styles = '''/* EPUB Styles */
body {
    font-family: Georgia, serif;
    line-height: 1.6;
    margin: 1em;
    color: #333;
    background-color: #fff;
}
'''
        with open(styles_dest, 'w', encoding='utf-8') as f:
            f.write(basic_styles)
    
    # Add KDP-specific styles if needed
    if kdp_mode:
        with open(styles_dest, 'r', encoding='utf-8') as f:
            existing_styles = f.read()
        
        # Check if KDP styles already exist
        if '.kdp-mode' not in existing_styles:
            kdp_styles = '''

/* Hide navigation in KDP mode */
.kdp-mode .navigation,
.kdp-mode .nav-link,
.kdp-mode .navigation-buttons {
    display: none !important;
}
'''
            with open(styles_dest, 'a', encoding='utf-8') as f:
                f.write(kdp_styles)

def create_toc_ncx(metadata, base_dir, book_uuid=None):
    """Create toc.ncx file."""
    title = metadata.get('title', 'Untitled')
    
    if not book_uuid:
        book_uuid = str(uuid.uuid4())
    
    toc_ncx = f'''<?xml version="1.0" encoding="UTF-8"?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
    <head>
        <meta name="dtb:uid" content="{book_uuid}"/>
        <meta name="dtb:depth" content="1"/>
        <meta name="dtb:totalPageCount" content="0"/>
        <meta name="dtb:maxPageNumber" content="0"/>
    </head>
    <docTitle>
        <text>{title}</text>
    </docTitle>
    <navMap>
        <navPoint id="navpoint-1" playOrder="1">
            <navLabel>
                <text>Table of Contents</text>
            </navLabel>
            <content src="Text/toc.xhtml"/>
        </navPoint>
    </navMap>
</ncx>'''
    
    with open(f'{base_dir}/OEBPS/toc.ncx', 'w', encoding='utf-8') as f:
        f.write(toc_ncx)

def create_cover_page(metadata, base_dir):
    """Create cover.xhtml page."""
    cover_filename = os.path.basename(metadata.get('cover_image', ''))
    title = metadata.get('title', 'Untitled')
    
    cover_xhtml = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <title>Cover</title>
    <link rel="stylesheet" type="text/css" href="Styles/style.css"/>
    <style type="text/css">
        body {{
            margin: 0;
            padding: 0;
            text-align: center;
            background-color: black;
        }}
        .cover {{
            margin: 0;
            padding: 0;
            width: 100%;
            height: 100vh;
            display: block;
        }}
        .cover img {{
            width: 100%;
            height: 100%;
            object-fit: contain;
            display: block;
            margin: 0 auto;
        }}
    </style>
</head>
<body>
    <div class="cover">
        <img src="Images/{cover_filename}" alt="{title} Cover"/>
    </div>
</body>
</html>'''
    
    with open(f'{base_dir}/OEBPS/cover.xhtml', 'w', encoding='utf-8') as f:
        f.write(cover_xhtml)

def create_epub_file(base_dir, output_filename):
    """Create EPUB file with proper mimetype ordering."""
    
    # Remove existing EPUB if it exists
    if os.path.exists(output_filename):
        os.remove(output_filename)
    
    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as epub:
        # CRITICAL: Add mimetype first (Amazon KDP requirement)
        epub.write(f'{base_dir}/mimetype', 'mimetype', compress_type=zipfile.ZIP_STORED)
        
        # Add META-INF files
        epub.write(f'{base_dir}/META-INF/container.xml', 'META-INF/container.xml')
        
        # Add OEBPS files
        for root, dirs, files in os.walk(f'{base_dir}/OEBPS'):
            for file in files:
                file_path = os.path.join(root, file)
                arc_path = os.path.relpath(file_path, base_dir)
                epub.write(file_path, arc_path)
    
    # Verify mimetype is first
    with zipfile.ZipFile(output_filename, 'r') as epub:
        file_list = epub.namelist()
        if file_list[0] == 'mimetype':
            print(f"  ✅ Mimetype file is first (EPUB/Amazon KDP compliant)")
        else:
            print(f"  ❌ Warning: Mimetype is not first. First file: {file_list[0]}")
    
    file_size = os.path.getsize(output_filename) / (1024 * 1024)
    print(f"  📦 EPUB created: {output_filename} ({file_size:.2f} MB)")

def run_epubcheck(epub_file):
    """Run epubcheck on the EPUB file."""
    if not os.path.exists(EPUBCCHECK_PATH):
        print(f"  ⚠️  EPUBCheck not found at {EPUBCCHECK_PATH}. Skipping validation.")
        return True
    
    print(f"  🔍 Running EPUBCheck on {epub_file}...")
    
    try:
        result = subprocess.run(
            ['java', '-jar', EPUBCCHECK_PATH, epub_file],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            print(f"  ✅ EPUBCheck passed! No errors found.")
            return True
        else:
            print(f"  ❌ EPUBCheck found issues:")
            print(result.stdout)
            if result.stderr:
                print(result.stderr)
            return False
    except subprocess.TimeoutExpired:
        print(f"  ⚠️  EPUBCheck timed out")
        return False
    except Exception as e:
        print(f"  ⚠️  Error running EPUBCheck: {e}")
        return False

def create_epub_version(metadata, version_name, kdp_mode=False):
    """Create a single EPUB version (Gumroad or KDP)."""
    
    print(f"\n{'='*60}")
    print(f"Creating {version_name} EPUB ({'KDP mode' if kdp_mode else 'Standard mode'})...")
    print(f"{'='*60}\n")
    
    base_dir = f'epub_{version_name.lower()}'
    
    # Ensure directory structure
    ensure_directory_structure(base_dir)
    
    # Copy styles file
    copy_styles_file(base_dir, kdp_mode=kdp_mode)
    
    # Convert HTML files to XHTML
    print("🔄 Converting HTML files to XHTML...")
    text_dir = f'{base_dir}/OEBPS/Text'
    for html_file in FILES_TO_PROCESS:
        if os.path.exists(html_file):
            print(f"  Converting {html_file}...")
            convert_html_to_xhtml(html_file, text_dir, kdp_mode=kdp_mode)
        else:
            print(f"  ⚠️  Warning: {html_file} not found")
    
    # Copy images
    print("\n🖼️  Copying images...")
    images_dir = f'{base_dir}/OEBPS/Images'
    copied_count = copy_images('.', images_dir)
    print(f"  ✅ Copied {copied_count} images")
    
    # Copy cover image specifically
    cover_path = metadata.get('cover_image', '')
    if cover_path:
        # Handle both absolute and relative paths
        if os.path.isabs(cover_path):
            # Absolute path
            if os.path.exists(cover_path):
                cover_filename = os.path.basename(cover_path)
                shutil.copy2(cover_path, f'{images_dir}/{cover_filename}')
                print(f"  ✅ Copied cover image: {cover_filename}")
            else:
                print(f"  ⚠️  Warning: Cover image not found at {cover_path}")
        else:
            # Relative path
            if os.path.exists(cover_path):
                cover_filename = os.path.basename(cover_path)
                shutil.copy2(cover_path, f'{images_dir}/{cover_filename}')
                print(f"  ✅ Copied cover image: {cover_filename}")
            else:
                print(f"  ⚠️  Warning: Cover image not found at {cover_path}")
    
    # Create cover page
    create_cover_page(metadata, base_dir)
    
    # Generate UUID for this EPUB (shared between OPF and NCX)
    book_uuid = str(uuid.uuid4())
    
    # Create content.opf
    print("\n📄 Creating content.opf...")
    content_opf = create_content_opf(metadata, base_dir, kdp_mode=kdp_mode, book_uuid=book_uuid)
    with open(f'{base_dir}/OEBPS/content.opf', 'w', encoding='utf-8') as f:
        f.write(content_opf)
    
    # Create toc.ncx (using same UUID)
    create_toc_ncx(metadata, base_dir, book_uuid=book_uuid)
    
    # Create EPUB file
    print(f"\n📦 Creating EPUB file...")
    title_safe = metadata.get('title', 'Book').replace(' ', '_')
    output_filename = f"{title_safe}_{version_name}.epub"
    create_epub_file(base_dir, output_filename)
    
    # Run epubcheck
    print(f"\n✅ {version_name} EPUB creation complete!")
    epubcheck_passed = run_epubcheck(output_filename)
    
    return output_filename, epubcheck_passed

def main():
    """Main function to create both EPUB versions."""
    print("=" * 60)
    print("ESCAPE THE HELL MYTH - Complete EPUB Creator")
    print("=" * 60)
    print()
    
    # Load metadata
    metadata = load_metadata()
    if not metadata:
        print("❌ Failed to load metadata. Exiting.")
        return False
    
    print(f"📚 Title: {metadata.get('title', 'Unknown')}")
    print(f"✍️  Author: {metadata.get('author', 'Unknown')}")
    print(f"📅 Year: {metadata.get('publication_date', 'Unknown')}")
    print()
    
    # Create Gumroad EPUB (Standard)
    gumroad_file, gumroad_check = create_epub_version(metadata, "Gumroad", kdp_mode=False)
    
    # Create KDP EPUB
    kdp_file, kdp_check = create_epub_version(metadata, "KDP", kdp_mode=True)
    
    # Summary
    print("\n" + "=" * 60)
    print("EPUB CREATION COMPLETE!")
    print("=" * 60)
    print(f"\nCreated files:")
    print(f"  📄 {gumroad_file} (for Gumroad)")
    print(f"  📄 {kdp_file} (for Amazon KDP)")
    
    print(f"\nEPUBCheck results:")
    print(f"  {'✅' if gumroad_check else '❌'} {gumroad_file}: {'Passed' if gumroad_check else 'Failed'}")
    print(f"  {'✅' if kdp_check else '❌'} {kdp_file}: {'Passed' if kdp_check else 'Failed'}")
    
    print("\nNext steps:")
    print("  1. Test EPUBs in Kindle Previewer")
    print("  2. Upload to respective platforms")
    print("  3. Verify all metadata displays correctly")
    
    return gumroad_check and kdp_check

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)

