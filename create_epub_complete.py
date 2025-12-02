#!/usr/bin/env python3
"""
Complete EPUB Creator for Gumroad and Amazon KDP
Creates two EPUB files with proper metadata, styling preservation, and Amazon KDP compliance.
"""

import json
import os
import shutil
import zipfile
import re
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup
import html
import urllib.parse

# Configuration
HTML_FILES_ORDER = [
    "index.html",      # Cover
    "copyright.html",
    "dedication.html",
    "toc.html",
    "introduction.html",
    "part1.html",
    "chapter1.html",
    "chapter2.html",
    "part2.html",
    "chapter3.html",
    "part3.html",
    "chapter4.html",
    "chapter5.html",
    "part4.html",
    "chapter6.html",
    "chapter7.html",
    "chapter8.html",
    "conclusion.html",
    "other-books.html",
    "appendix.html",
    "bibliography.html"
]

# Spine order (without file extensions, mapped to IDs)
SPINE_ORDER = [
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
    "bibliography"
]

def load_metadata():
    """Load book metadata from JSON file."""
    if not os.path.exists('book_metadata.json'):
        print(" No metadata file found.")
        return None
    
    with open('book_metadata.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def create_directory_structure():
    """Create the EPUB directory structure."""
    dirs = [
        'epub_build/META-INF',
        'epub_build/OEBPS/Text',
        'epub_build/OEBPS/Styles',
        'epub_build/OEBPS/images'
    ]
    
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)
    
    print(" Directory structure created")

def create_mimetype():
    """Create the mimetype file."""
    with open('epub_build/mimetype', 'w', encoding='utf-8', newline='\n') as f:
        f.write('application/epub+zip')
    print(" Mimetype file created")

def create_container_xml():
    """Create the container.xml file."""
    container_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
    <rootfiles>
        <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
    </rootfiles>
</container>'''
    
    with open('epub_build/META-INF/container.xml', 'w', encoding='utf-8') as f:
        f.write(container_xml)
    print(" Container.xml created")

def get_comprehensive_css():
    """Return comprehensive CSS that preserves all styling."""
    return '''/* EPUB Styles for Escape The Hell Myth - Complete Styling */

/* ============================================
   BASE STYLES
   ============================================ */
body {
    font-family: Georgia, "Times New Roman", serif;
    line-height: 1.6;
    margin: 1em;
    padding: 0;
    color: #2d3748;
    background-color: #fff;
}

/* KDP Mode - Hide navigation */
body.kdp-mode .navigation-buttons,
body.kdp-mode .nav-button,
body.kdp-mode .enter-button {
    display: none !important;
}

/* KDP Mode - Copyright page images at 55% */
body.kdp-mode .logo-image,
body.kdp-mode .logo-image-top {
    width: 55% !important;
    max-width: 55% !important;
    margin: 1.5em auto;
}

/* ============================================
   TYPOGRAPHY
   ============================================ */
h1 {
    font-size: 1.8em;
    text-align: center;
    margin-bottom: 1em;
    margin-top: 0.5em;
    color: #2a4365;
    page-break-before: always;
    page-break-after: avoid;
}

h1:first-child {
    page-break-before: avoid;
}

h2 {
    font-size: 1.4em;
    margin-top: 1.5em;
    margin-bottom: 0.75em;
    color: #2a4365;
    border-bottom: 2px solid #7f9cf5;
    padding-bottom: 0.3em;
    page-break-after: avoid;
}

h3 {
    font-size: 1.25em;
    margin-top: 1.3em;
    margin-bottom: 0.6em;
    color: #2a4365;
    page-break-after: avoid;
}

h4 {
    font-size: 1.1em;
    margin-top: 1.1em;
    margin-bottom: 0.5em;
    color: #2a4365;
    page-break-after: avoid;
}

p {
    margin-bottom: 1em;
    text-align: justify;
    orphans: 2;
    widows: 2;
}

/* ============================================
   DROP CAP
   ============================================ */
.drop-cap::first-letter,
.drop-cap:first-letter {
    float: left;
    font-size: 3.5em;
    line-height: 0.8;
    padding-right: 0.1em;
    padding-top: 0.1em;
    color: #7f9cf5;
    font-weight: bold;
}

/* ============================================
   COVER PAGE
   ============================================ */
.cover {
    text-align: center;
    page-break-after: always;
}

.cover img {
    max-width: 100%;
    height: auto;
    margin: 1em auto;
}

.book-cover {
    max-width: 100%;
    height: auto;
    margin: 1em auto;
    display: block;
}

.title-container {
    text-align: center;
    padding: 1em;
}

.book-title {
    font-size: 1.8em;
    color: #2a4365;
    margin-bottom: 0.5em;
    text-align: center;
}

.book-subtitle {
    font-size: 1.2em;
    color: #c53030;
    font-style: italic;
    margin-bottom: 1em;
    text-align: center;
}

.author-name {
    font-size: 1.1em;
    color: #2a4365;
    text-align: center;
}

/* ============================================
   CHAPTER STYLES
   ============================================ */
.chapter {
    page-break-before: always;
    padding: 1em 0;
}

.chapter:first-child {
    page-break-before: avoid;
}

.chapter-title {
    text-align: center;
    font-size: 1.8em;
    margin-bottom: 1.5em;
    color: #2a4365;
    page-break-after: avoid;
}

.chapter-quote {
    font-style: italic;
    text-align: center;
    font-size: 1.1em;
    margin-bottom: 2em;
    color: #7f9cf5;
}

.chapter-image {
    max-width: 90%;
    height: auto;
    display: block;
    margin: 1.5em auto;
    page-break-inside: avoid;
}

/* ============================================
   CALLOUTS AND QUOTES
   ============================================ */
.callout {
    background-color: #ebf4ff;
    border-left: 4px solid #7f9cf5;
    padding: 1em 1.2em;
    margin: 1.5em 0;
    border-radius: 0.3em;
    page-break-inside: avoid;
}

.callout-title {
    font-weight: bold;
    margin-bottom: 0.5em;
    font-size: 1.1em;
    color: #2a4365;
    page-break-after: avoid;
}

.callout-quote {
    background-color: #fff8e1;
    border-left: 4px solid #f6ad55;
    padding: 1em 1.2em;
    margin: 1.5em 0;
    font-style: italic;
    border-radius: 0.3em;
    page-break-inside: avoid;
}

.quote {
    font-style: italic;
    margin: 1.5em 0;
    padding: 1em;
    border-left: 4px solid #7f9cf5;
    background-color: #f7fafc;
    page-break-inside: avoid;
}

/* ============================================
   BIBLE VERSES AND REFERENCES
   ============================================ */
.bible-quote {
    background-color: #f7fafc;
    border-left: 3px solid #7f9cf5;
    padding: 1em;
    margin: 1.5em 0;
    font-style: italic;
    page-break-inside: avoid;
}

.bible-reference {
    font-style: italic;
    color: #2a4365;
    font-weight: bold;
    text-align: right;
    display: block;
    margin-top: 0.5em;
}

.bible-verse {
    font-style: italic;
    margin: 1em 0;
    padding: 1em;
    background-color: #f7fafc;
    border-left: 3px solid #7f9cf5;
    page-break-inside: avoid;
}

.verse-reference {
    font-weight: bold;
    color: #2a4365;
    text-align: right;
    margin-top: 0.5em;
}

/* ============================================
   INFO BOXES AND CARDS
   ============================================ */
.info-box {
    background-color: #fff;
    border: 1px solid #e2e8f0;
    border-radius: 0.5em;
    padding: 1.2em;
    margin: 1.5em 0;
    page-break-inside: avoid;
}

.info-box-title {
    font-weight: bold;
    margin-bottom: 0.75em;
    font-size: 1.1em;
    color: #2a4365;
    text-align: center;
    page-break-after: avoid;
}

.card {
    background-color: #f7fafc;
    border: 1px solid #7f9cf5;
    border-radius: 0.5em;
    padding: 1.2em;
    margin: 1em 0;
    page-break-inside: avoid;
}

.card-title {
    font-weight: bold;
    color: #2a4365;
    margin-bottom: 0.5em;
    font-size: 1.1em;
}

.card-content {
    margin: 0;
}

.card-grid {
    margin: 1em 0;
}

.info-grid {
    margin: 1.5em 0;
}

/* ============================================
   TABLES
   ============================================ */
table {
    width: 100%;
    border-collapse: collapse;
    margin: 1.5em 0;
    page-break-inside: auto;
}

th, td {
    border: 1px solid #e2e8f0;
    padding: 0.6em;
    text-align: left;
    vertical-align: top;
}

th {
    background-color: #2a4365;
    color: white;
    font-weight: bold;
}

tr {
    page-break-inside: avoid;
}

.comparison-table {
    width: 100%;
    margin: 1.5em 0;
    border-collapse: collapse;
    background: white;
    border-radius: 0.5em;
    overflow: hidden;
}

.comparison-table th {
    background: #2a4365;
    color: white;
    padding: 0.8em;
}

.comparison-table td {
    padding: 0.8em;
    border: 1px solid #e2e8f0;
}

/* ============================================
   LISTS
   ============================================ */
ul, ol {
    margin: 1em 0;
    padding-left: 2em;
}

li {
    margin-bottom: 0.5em;
    orphans: 2;
    widows: 2;
}

.bullet-points {
    list-style-type: disc;
    margin: 1em 0;
    padding-left: 2em;
}

.bullet-points li {
    margin-bottom: 0.5em;
}

.bullet-points li::marker {
    color: #7f9cf5;
}

/* ============================================
   PART PAGES
   ============================================ */
.part {
    page-break-before: always;
    text-align: center;
    padding: 2em 1em;
}

.part-container {
    text-align: center;
    padding: 2em 1em;
    page-break-before: always;
}

.part-title {
    font-size: 2em;
    color: #2a4365;
    margin-bottom: 0.5em;
    text-align: center;
}

.part-subtitle {
    font-style: italic;
    color: #7f9cf5;
    font-size: 1.2em;
    text-align: center;
}

/* ============================================
   DEDICATION PAGE
   ============================================ */
.dedication {
    text-align: center;
    padding: 2em 1em;
    page-break-after: always;
}

.dedication-image {
    width: 100%;
    max-width: 100%;
    height: auto;
    margin: 1em auto;
    display: block;
}

.dedication-text {
    font-style: italic;
    color: #2a4365;
    font-size: 1.1em;
    margin: 1em 0;
}

/* ============================================
   TABLE OF CONTENTS
   ============================================ */
.table-of-contents {
    padding: 1em;
}

.toc-title {
    text-align: center;
    font-size: 1.6em;
    margin-bottom: 1.5em;
    color: #2a4365;
}

.toc-item {
    margin-bottom: 0.5em;
    text-align: center;
}

.toc-item a {
    color: #2a4365;
    text-decoration: none;
}

.part-section {
    margin: 1.5em 0;
    padding: 0.5em;
}

/* ============================================
   BOOK SECTIONS (Other Books page)
   ============================================ */
.book-section {
    margin: 1.5em 0;
    padding: 1em 0;
    page-break-inside: avoid;
}

.book-section .book-cover {
    width: 40%;
    max-width: 40%;
    margin: 0 auto 1em auto;
}

.book-section .book-cover img {
    width: 100%;
    height: auto;
    display: block;
}

.book-content {
    margin: 1em 0;
}

.book-description {
    margin: 0.5em 0;
}

.series-section {
    background-color: #f7fafc;
    padding: 1.5em;
    margin: 1.5em 0;
    border: 1px solid #7f9cf5;
    border-radius: 0.5em;
    page-break-inside: avoid;
}

.series-header {
    text-align: center;
    margin-bottom: 1em;
}

.series-title {
    font-size: 1.3em;
    color: #2a4365;
    margin-bottom: 0.3em;
}

.series-tagline {
    font-size: 1em;
    color: #7f9cf5;
    font-style: italic;
}

.series-author {
    font-size: 0.9em;
    color: #666;
}

.series-description {
    text-align: left;
}

/* ============================================
   BIBLIOGRAPHY AND APPENDIX
   ============================================ */
.bibliography-entry {
    margin-bottom: 0.8em;
    text-indent: -1.5em;
    padding-left: 1.5em;
}

.term {
    margin-bottom: 1.5em;
}

.term-name {
    font-weight: bold;
    color: #2a4365;
    font-size: 1.1em;
    margin-bottom: 0.3em;
    border-bottom: 1px dotted #7f9cf5;
    padding-bottom: 0.2em;
}

.term-definition {
    margin-left: 0;
}

/* ============================================
   STEPS AND PROCESSES
   ============================================ */
.step {
    padding: 1.2em;
    margin: 1em 0;
    background-color: #f7fafc;
    border-left: 3px solid #7f9cf5;
    page-break-inside: avoid;
}

.step-number {
    font-weight: bold;
    color: #2a4365;
    font-size: 1.2em;
}

/* ============================================
   IMAGES
   ============================================ */
img {
    max-width: 100%;
    height: auto;
    display: block;
    margin: 1em auto;
}

.logo-image,
.logo-image-top {
    max-width: 50%;
    margin: 1em auto;
}

/* ============================================
   EMPHASIS AND HIGHLIGHTS
   ============================================ */
strong {
    color: #2a4365;
}

em {
    color: #4a5568;
}

.highlight {
    background-color: #ebf4ff;
    padding: 0.1em 0.3em;
    border-radius: 0.2em;
}

/* ============================================
   NAVIGATION (Hidden in KDP mode)
   ============================================ */
.navigation-buttons {
    text-align: center;
    margin: 2em 0;
    padding: 1em 0;
    border-top: 1px solid #7f9cf5;
}

.nav-button {
    display: inline-block;
    margin: 0.3em;
    padding: 0.5em 1em;
    background-color: #2a4365;
    color: white;
    text-decoration: none;
    border-radius: 0.3em;
}

.enter-button {
    display: inline-block;
    padding: 0.5em 1em;
    background-color: #2a4365;
    color: white;
    text-decoration: none;
    border-radius: 0.3em;
}

/* ============================================
   AUTHOR NOTE
   ============================================ */
.author-note {
    font-style: italic;
    text-align: center;
    margin-top: 2em;
    padding-top: 1em;
    border-top: 1px solid #7f9cf5;
}

/* ============================================
   COPYRIGHT PAGE
   ============================================ */
.copyright-page {
    text-align: center;
    padding: 2em 1em;
}

.copyright-text {
    font-size: 0.9em;
    color: #4a5568;
    margin: 0.5em 0;
}

/* ============================================
   LINKS
   ============================================ */
a {
    color: #2a4365;
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}

/* ============================================
   SECTION HEADERS
   ============================================ */
.section-header {
    margin-bottom: 1em;
    page-break-after: avoid;
}

.chapter-title-section {
    page-break-inside: avoid;
    page-break-after: avoid;
}

.chapter-title-card {
    padding: 1em;
    margin-bottom: 1em;
}

/* ============================================
   PAGE BREAK CONTROLS
   ============================================ */
.page-break {
    page-break-before: always;
}

.no-break {
    page-break-inside: avoid;
}

section {
    page-break-before: avoid;
}
'''

def create_css_file():
    """Create the comprehensive CSS file."""
    css_content = get_comprehensive_css()
    
    with open('epub_build/OEBPS/Styles/style.css', 'w', encoding='utf-8') as f:
        f.write(css_content)
    print(" Comprehensive CSS file created")

def sanitize_filename(filename):
    """Sanitize filename by replacing spaces and special characters."""
    # Replace spaces with hyphens
    sanitized = filename.replace(' ', '-')
    # Replace parentheses
    sanitized = sanitized.replace('(', '').replace(')', '')
    return sanitized

def convert_html_to_xhtml(html_file, is_kdp=False, is_cover=False):
    """Convert HTML file to valid XHTML, preserving all classes and styles."""
    
    if not os.path.exists(html_file):
        print(f" File not found: {html_file}")
        return None
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parse with BeautifulSoup
    soup = BeautifulSoup(content, 'html.parser')
    
    # Get the title
    title_tag = soup.find('title')
    title = title_tag.string if title_tag else 'Untitled'
    
    # Extract body content
    body = soup.find('body')
    if not body:
        body = soup
    
    # Remove navigation elements for EPUB
    for nav in body.find_all(['nav', 'header', 'footer']):
        nav.decompose()
    
    # Remove elements with navigation classes
    for elem in body.find_all(class_=['navigation-buttons', 'nav-button', 'enter-button']):
        elem.decompose()
    
    # Remove external stylesheet links
    for link in soup.find_all('link', rel='stylesheet'):
        link.decompose()
    
    # Remove script tags
    for script in soup.find_all('script'):
        script.decompose()
    
    # Remove style tags (we'll use our own CSS)
    for style in soup.find_all('style'):
        style.decompose()
    
    # Fix image paths
    for img in body.find_all('img'):
        src = img.get('src', '')
        if src:
            # Get just the filename (handle subdirectory paths)
            filename = os.path.basename(src)
            # Sanitize filename
            filename = sanitize_filename(filename)
            # Set correct path based on whether this is cover or text file
            if is_cover:
                img['src'] = f'images/{filename}'
            else:
                img['src'] = f'../images/{filename}'
            # Ensure alt attribute exists
            if not img.get('alt'):
                img['alt'] = filename.replace('.jpg', '').replace('.png', '').replace('-', ' ').replace('_', ' ')
    
    # Fix internal links
    for a in body.find_all('a'):
        href = a.get('href', '')
        if href and href.endswith('.html'):
            # Convert .html to .xhtml
            new_href = href.replace('.html', '.xhtml')
            # Handle special cases
            if new_href == 'index.xhtml':
                if is_cover:
                    new_href = 'cover.xhtml'
                else:
                    new_href = '../cover.xhtml'
            a['href'] = new_href
    
    # Get body content as string
    body_content = ''.join(str(child) for child in body.children)
    
    # Determine body class
    body_class = 'kdp-mode' if is_kdp else ''
    body_class_attr = f' class="{body_class}"' if body_class else ''
    
    # Determine CSS path based on file location
    css_path = 'Styles/style.css' if is_cover else '../Styles/style.css'
    
    # Create valid XHTML document with EPUB 3 DOCTYPE
    xhtml = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="en">
<head>
    <meta charset="UTF-8"/>
    <title>{html.escape(title)}</title>
    <link rel="stylesheet" type="text/css" href="{css_path}"/>
</head>
<body{body_class_attr}>
{body_content}
</body>
</html>'''
    
    return xhtml

def convert_all_html_files(is_kdp=False):
    """Convert all HTML files to XHTML."""
    print(f"\n Converting HTML files to XHTML {'(KDP mode)' if is_kdp else '(Standard mode)'}...")
    
    converted_files = []
    
    for html_file in HTML_FILES_ORDER:
        if not os.path.exists(html_file):
            print(f"   Skipping (not found): {html_file}")
            continue
        
        # Determine if this is the cover file
        is_cover = (html_file == 'index.html')
        
        xhtml_content = convert_html_to_xhtml(html_file, is_kdp, is_cover)
        
        if xhtml_content:
            # Determine output filename
            if html_file == 'index.html':
                output_file = 'epub_build/OEBPS/cover.xhtml'
            else:
                output_name = html_file.replace('.html', '.xhtml')
                output_file = f'epub_build/OEBPS/Text/{output_name}'
            
            # Write the XHTML file
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(xhtml_content)
            
            converted_files.append(html_file)
            print(f"   Converted: {html_file}")
    
    return converted_files

def copy_images():
    """Copy all images to the EPUB structure, including from subdirectories."""
    print("\n Copying images...")
    
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.svg']
    copied_count = 0
    copied_files = set()
    
    # Copy from root directory
    for file in os.listdir('.'):
        if any(file.lower().endswith(ext) for ext in image_extensions):
            src = file
            # Sanitize filename
            dst_filename = sanitize_filename(file)
            dst = f'epub_build/OEBPS/images/{dst_filename}'
            if dst_filename not in copied_files:
                shutil.copy2(src, dst)
                copied_files.add(dst_filename)
                copied_count += 1
    
    # Copy from otherbooks directory if it exists
    if os.path.exists('otherbooks'):
        for file in os.listdir('otherbooks'):
            if any(file.lower().endswith(ext) for ext in image_extensions):
                src = f'otherbooks/{file}'
                # Sanitize filename
                dst_filename = sanitize_filename(file)
                dst = f'epub_build/OEBPS/images/{dst_filename}'
                if dst_filename not in copied_files:
                    shutil.copy2(src, dst)
                    copied_files.add(dst_filename)
                    copied_count += 1
    
    print(f"   Copied {copied_count} images")
    return copied_count

def get_book_id():
    """Get a consistent book ID for the entire build."""
    if not hasattr(get_book_id, 'cached_id'):
        get_book_id.cached_id = f"urn:uuid:escape-hell-myth-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    return get_book_id.cached_id

def reset_book_id():
    """Reset the book ID for a new build."""
    if hasattr(get_book_id, 'cached_id'):
        delattr(get_book_id, 'cached_id')

def create_content_opf(metadata, is_kdp=False):
    """Create the content.opf file with complete metadata."""
    
    book_id = get_book_id()
    
    # Get all XHTML files
    text_dir = Path('epub_build/OEBPS/Text')
    xhtml_files = list(text_dir.glob('*.xhtml')) if text_dir.exists() else []
    
    # Get all images
    images_dir = Path('epub_build/OEBPS/images')
    image_files = list(images_dir.glob('*')) if images_dir.exists() else []
    
    # Build manifest items
    manifest_items = []
    
    # Add cover.xhtml
    if os.path.exists('epub_build/OEBPS/cover.xhtml'):
        manifest_items.append('        <item id="cover" href="cover.xhtml" media-type="application/xhtml+xml"/>')
    
    # Add all XHTML files from Text directory
    for xhtml_file in sorted(xhtml_files):
        file_id = xhtml_file.stem
        # Handle hyphenated filenames for IDs - make XML-safe
        safe_id = re.sub(r'[^a-zA-Z0-9_]', '_', file_id)
        manifest_items.append(f'        <item id="{safe_id}" href="Text/{xhtml_file.name}" media-type="application/xhtml+xml"/>')
    
    # Add images
    used_ids = {'cover', 'cover_image', 'ncx', 'nav', 'css'}
    cover_filename = sanitize_filename(os.path.basename(metadata.get('cover_image', 'cover.jpg')))
    
    for img_file in sorted(image_files):
        # Determine media type
        ext = img_file.suffix.lower()
        if ext in ['.jpg', '.jpeg']:
            media_type = 'image/jpeg'
        elif ext == '.png':
            media_type = 'image/png'
        elif ext == '.gif':
            media_type = 'image/gif'
        elif ext == '.svg':
            media_type = 'image/svg+xml'
        else:
            continue
        
        # Create unique XML-safe ID
        base_id = re.sub(r'[^a-zA-Z0-9_]', '_', img_file.stem)
        file_id = base_id
        counter = 1
        while file_id in used_ids:
            file_id = f"{base_id}_{counter}"
            counter += 1
        used_ids.add(file_id)
        
        # Mark cover image
        if img_file.name == cover_filename:
            manifest_items.append(f'        <item id="cover_image" href="images/{img_file.name}" media-type="{media_type}" properties="cover-image"/>')
        else:
            manifest_items.append(f'        <item id="{file_id}" href="images/{img_file.name}" media-type="{media_type}"/>')
    
    # Build spine items in correct order
    spine_items = []
    for item_id in SPINE_ORDER:
        safe_id = re.sub(r'[^a-zA-Z0-9_]', '_', item_id)
        # Check if the file exists
        if item_id == 'cover' and os.path.exists('epub_build/OEBPS/cover.xhtml'):
            spine_items.append(f'        <itemref idref="cover"/>')
        elif os.path.exists(f'epub_build/OEBPS/Text/{item_id}.xhtml'):
            spine_items.append(f'        <itemref idref="{safe_id}"/>')
    
    # Escape description for XML
    description = html.escape(metadata.get('description', ''))
    
    content_opf = f'''<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="book-id" version="3.0">
    <metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf">
        <dc:identifier id="book-id">{book_id}</dc:identifier>
        <dc:title>{html.escape(metadata.get('title', 'Untitled'))}</dc:title>
        <dc:creator id="author">{html.escape(metadata.get('author', 'Unknown'))}</dc:creator>
        <meta refines="#author" property="role" scheme="marc:relators">aut</meta>
        <meta refines="#author" property="file-as">{html.escape(metadata.get('author', 'Unknown'))}</meta>
        <dc:publisher>{html.escape(metadata.get('publisher', 'Unknown Publisher'))}</dc:publisher>
        <dc:date>{metadata.get('publication_date', '2025')}</dc:date>
        <dc:language>{metadata.get('language', 'en')}</dc:language>
        <dc:subject>{html.escape(metadata.get('tags', ''))}</dc:subject>
        <dc:description>{description}</dc:description>
        <meta property="dcterms:modified">{datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')}</meta>
        <meta name="cover" content="cover_image"/>
    </metadata>
    
    <manifest>
        <item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>
        <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>
        <item id="css" href="Styles/style.css" media-type="text/css"/>
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
    
    with open('epub_build/OEBPS/content.opf', 'w', encoding='utf-8') as f:
        f.write(content_opf)
    
    print(f" content.opf created {'(KDP version)' if is_kdp else '(Standard version)'}")

def create_toc_ncx(metadata):
    """Create the toc.ncx file for EPUB 2 compatibility."""
    
    book_id = get_book_id()
    
    nav_points = []
    play_order = 1
    
    # Define navigation structure
    nav_structure = [
        ('cover', 'Cover', 'cover.xhtml'),
        ('copyright', 'Copyright', 'Text/copyright.xhtml'),
        ('dedication', 'Dedication', 'Text/dedication.xhtml'),
        ('toc', 'Table of Contents', 'Text/toc.xhtml'),
        ('introduction', 'Introduction', 'Text/introduction.xhtml'),
        ('part1', 'Part 1: Unmasking the Myth', 'Text/part1.xhtml'),
        ('chapter1', 'Chapter 1: The Invention of Eternal Fire', 'Text/chapter1.xhtml'),
        ('chapter2', 'Chapter 2: Jesus vs. the Punishing God', 'Text/chapter2.xhtml'),
        ('part2', 'Part 2: How Fear Slipped Back In', 'Text/part2.xhtml'),
        ('chapter3', 'Chapter 3: Paul and the Return of Fear', 'Text/chapter3.xhtml'),
        ('part3', 'Part 3: Clearing Up The "Hell" Texts', 'Text/part3.xhtml'),
        ('chapter4', 'Chapter 4: The Verses Everyone Can\'t Unsee', 'Text/chapter4.xhtml'),
        ('chapter5', 'Chapter 5: The Day the World Ended', 'Text/chapter5.xhtml'),
        ('part4', 'Part 4: The Gospel Of Love', 'Text/part4.xhtml'),
        ('chapter6', 'Chapter 6: The Father Who Never Stops Loving', 'Text/chapter6.xhtml'),
        ('chapter7', 'Chapter 7: Escaping the Fear Cycle', 'Text/chapter7.xhtml'),
        ('chapter8', 'Chapter 8: The Wounds We Inherit', 'Text/chapter8.xhtml'),
        ('conclusion', 'Conclusion: Love Wins. Always.', 'Text/conclusion.xhtml'),
        ('other-books', 'Books By Ansilo Boff', 'Text/other-books.xhtml'),
        ('appendix', 'Appendix: Glossary of Key Terms', 'Text/appendix.xhtml'),
        ('bibliography', 'Bibliography', 'Text/bibliography.xhtml'),
    ]
    
    for nav_id, title, src in nav_structure:
        # Check if file exists
        full_path = f'epub_build/OEBPS/{src}'
        if os.path.exists(full_path):
            nav_points.append(f'''    <navPoint id="{nav_id}" playOrder="{play_order}">
      <navLabel><text>{html.escape(title)}</text></navLabel>
      <content src="{src}"/>
    </navPoint>''')
            play_order += 1
    
    toc_ncx = f'''<?xml version="1.0" encoding="UTF-8"?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
  <head>
    <meta name="dtb:uid" content="{book_id}"/>
    <meta name="dtb:depth" content="1"/>
    <meta name="dtb:totalPageCount" content="0"/>
    <meta name="dtb:maxPageNumber" content="0"/>
  </head>
  <docTitle>
    <text>{html.escape(metadata.get('title', 'Untitled'))}</text>
  </docTitle>
  <docAuthor>
    <text>{html.escape(metadata.get('author', 'Unknown'))}</text>
  </docAuthor>
  <navMap>
{chr(10).join(nav_points)}
  </navMap>
</ncx>'''
    
    with open('epub_build/OEBPS/toc.ncx', 'w', encoding='utf-8') as f:
        f.write(toc_ncx)
    
    print(" toc.ncx created")

def create_nav_xhtml(metadata):
    """Create the nav.xhtml file for EPUB 3."""
    
    nav_items = []
    
    nav_structure = [
        ('Cover', 'cover.xhtml'),
        ('Copyright', 'Text/copyright.xhtml'),
        ('Dedication', 'Text/dedication.xhtml'),
        ('Table of Contents', 'Text/toc.xhtml'),
        ('Introduction', 'Text/introduction.xhtml'),
        ('Part 1: Unmasking the Myth', 'Text/part1.xhtml'),
        ('Chapter 1: The Invention of Eternal Fire', 'Text/chapter1.xhtml'),
        ('Chapter 2: Jesus vs. the Punishing God', 'Text/chapter2.xhtml'),
        ('Part 2: How Fear Slipped Back In', 'Text/part2.xhtml'),
        ('Chapter 3: Paul and the Return of Fear', 'Text/chapter3.xhtml'),
        ('Part 3: Clearing Up The "Hell" Texts', 'Text/part3.xhtml'),
        ('Chapter 4: The Verses Everyone Can\'t Unsee', 'Text/chapter4.xhtml'),
        ('Chapter 5: The Day the World Ended', 'Text/chapter5.xhtml'),
        ('Part 4: The Gospel Of Love', 'Text/part4.xhtml'),
        ('Chapter 6: The Father Who Never Stops Loving', 'Text/chapter6.xhtml'),
        ('Chapter 7: Escaping the Fear Cycle', 'Text/chapter7.xhtml'),
        ('Chapter 8: The Wounds We Inherit', 'Text/chapter8.xhtml'),
        ('Conclusion: Love Wins. Always.', 'Text/conclusion.xhtml'),
        ('Books By Ansilo Boff', 'Text/other-books.xhtml'),
        ('Appendix', 'Text/appendix.xhtml'),
        ('Bibliography', 'Text/bibliography.xhtml'),
    ]
    
    for title, src in nav_structure:
        full_path = f'epub_build/OEBPS/{src}'
        if os.path.exists(full_path):
            nav_items.append(f'                <li><a href="{src}">{html.escape(title)}</a></li>')
    
    nav_xhtml = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="en">
<head>
    <meta charset="UTF-8"/>
    <title>Navigation</title>
    <link rel="stylesheet" type="text/css" href="Styles/style.css"/>
</head>
<body>
    <nav epub:type="toc" id="toc">
        <h1>Table of Contents</h1>
        <ol>
{chr(10).join(nav_items)}
        </ol>
    </nav>
</body>
</html>'''
    
    with open('epub_build/OEBPS/nav.xhtml', 'w', encoding='utf-8') as f:
        f.write(nav_xhtml)
    
    print(" nav.xhtml created")

def create_epub_file(output_name, metadata):
    """Create the final EPUB file with proper mimetype ordering."""
    
    print(f"\n Creating EPUB: {output_name}")
    
    # Remove existing file
    if os.path.exists(output_name):
        os.remove(output_name)
    
    with zipfile.ZipFile(output_name, 'w', zipfile.ZIP_DEFLATED) as epub:
        # CRITICAL: Add mimetype first, uncompressed
        epub.write('epub_build/mimetype', 'mimetype', compress_type=zipfile.ZIP_STORED)
        
        # Add META-INF
        for root, dirs, files in os.walk('epub_build/META-INF'):
            for file in files:
                file_path = os.path.join(root, file)
                arc_path = os.path.relpath(file_path, 'epub_build')
                epub.write(file_path, arc_path)
        
        # Add OEBPS
        for root, dirs, files in os.walk('epub_build/OEBPS'):
            for file in files:
                file_path = os.path.join(root, file)
                arc_path = os.path.relpath(file_path, 'epub_build')
                epub.write(file_path, arc_path)
    
    # Verify mimetype is first
    with zipfile.ZipFile(output_name, 'r') as epub:
        file_list = epub.namelist()
        if file_list[0] == 'mimetype':
            print(f"   Mimetype is first (EPUB/Amazon KDP compliant)")
        else:
            print(f"   Warning: Mimetype is not first! First file: {file_list[0]}")
    
    # Get file size
    file_size = os.path.getsize(output_name) / (1024 * 1024)
    print(f"   EPUB created: {output_name} ({file_size:.2f} MB)")
    
    return output_name

def cleanup():
    """Clean up build directory."""
    if os.path.exists('epub_build'):
        shutil.rmtree('epub_build')

def run_epubcheck(epub_file):
    """Run EPUBCheck on the created file."""
    print(f"\n Running EPUBCheck on {epub_file}...")
    
    # Check if epubcheck is available
    epubcheck_jar = 'epubcheck-5.2.0/epubcheck.jar'
    
    if not os.path.exists(epubcheck_jar):
        print("   EPUBCheck not found. Skipping validation.")
        print(f"  To validate, ensure {epubcheck_jar} exists.")
        return
    
    import subprocess
    try:
        result = subprocess.run(
            ['java', '-jar', epubcheck_jar, epub_file],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if result.returncode == 0:
            print("   EPUBCheck passed! No errors found.")
        else:
            print("   EPUBCheck found issues:")
            # Show only error lines
            for line in result.stdout.split('\n'):
                if 'ERROR' in line or 'FATAL' in line:
                    print(f"    {line}")
            for line in result.stderr.split('\n'):
                if 'ERROR' in line or 'FATAL' in line:
                    print(f"    {line}")
                    
    except FileNotFoundError:
        print("   Java not found. Please install Java to run EPUBCheck.")
    except subprocess.TimeoutExpired:
        print("   EPUBCheck timed out.")
    except Exception as e:
        print(f"   Error running EPUBCheck: {e}")

def create_gumroad_epub(metadata):
    """Create standard EPUB for Gumroad."""
    print("\n" + "=" * 60)
    print(" Creating Gumroad EPUB (Standard)")
    print("=" * 60)
    
    # Reset book ID for new build
    reset_book_id()
    
    # Clean and create structure
    cleanup()
    create_directory_structure()
    create_mimetype()
    create_container_xml()
    create_css_file()
    
    # Convert HTML files (standard mode)
    convert_all_html_files(is_kdp=False)
    
    # Copy images
    copy_images()
    
    # Create navigation files
    create_content_opf(metadata, is_kdp=False)
    create_toc_ncx(metadata)
    create_nav_xhtml(metadata)
    
    # Create EPUB
    epub_file = create_epub_file('Escape_The_Hell_Myth_Gumroad.epub', metadata)
    
    return epub_file

def create_amazon_kdp_epub(metadata):
    """Create Amazon KDP-compliant EPUB."""
    print("\n" + "=" * 60)
    print(" Creating Amazon KDP EPUB")
    print("=" * 60)
    
    # Reset book ID for new build
    reset_book_id()
    
    # Clean and create structure
    cleanup()
    create_directory_structure()
    create_mimetype()
    create_container_xml()
    create_css_file()
    
    # Convert HTML files (KDP mode - adds class="kdp-mode" to body)
    convert_all_html_files(is_kdp=True)
    
    # Copy images
    copy_images()
    
    # Create navigation files
    create_content_opf(metadata, is_kdp=True)
    create_toc_ncx(metadata)
    create_nav_xhtml(metadata)
    
    # Create EPUB
    epub_file = create_epub_file('Escape_The_Hell_Myth_KDP.epub', metadata)
    
    return epub_file

def main():
    """Main function to create both EPUBs."""
    print("=" * 60)
    print("ESCAPE THE HELL MYTH - Complete EPUB Creator")
    print("=" * 60)
    
    # Load metadata
    metadata = load_metadata()
    if not metadata:
        print(" Failed to load metadata. Exiting.")
        return False
    
    print(f"\n Title: {metadata.get('title')}")
    print(f" Author: {metadata.get('author')}")
    print(f" Year: {metadata.get('publication_date')}")
    
    try:
        # Create Gumroad EPUB
        gumroad_epub = create_gumroad_epub(metadata)
        
        # Create Amazon KDP EPUB
        kdp_epub = create_amazon_kdp_epub(metadata)
        
        # Clean up build directory
        cleanup()
        
        # Run EPUBCheck on both files
        run_epubcheck(gumroad_epub)
        run_epubcheck(kdp_epub)
        
        print("\n" + "=" * 60)
        print(" EPUB CREATION COMPLETE!")
        print("=" * 60)
        print(f"\n Created files:")
        print(f"    {gumroad_epub} (for Gumroad)")
        print(f"    {kdp_epub} (for Amazon KDP)")
        print("\n Next steps:")
        print("   1. Test EPUBs in Kindle Previewer")
        print("   2. Upload to respective platforms")
        print("   3. Verify all metadata displays correctly")
        
        return True
        
    except Exception as e:
        print(f"\n Error creating EPUBs: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    main()
