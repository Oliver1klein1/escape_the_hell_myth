#!/usr/bin/env python3
"""
Enhanced EPUB Conversion Script for Escape The Hell Myth
Converts HTML files to EPUB-compatible XHTML format while preserving ALL styling
"""

import os
import re
from bs4 import BeautifulSoup
import shutil
import json

def convert_html_to_xhtml_enhanced(html_file_path, output_dir):
    """Convert a single HTML file to EPUB-compatible XHTML while preserving all styling"""
    
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
    
    # Also remove any standalone navigation links
    for nav_link in body.find_all(['a'], class_=['nav-link']):
        nav_link.decompose()
    
    # Update image src paths to EPUB format
    for img in body.find_all('img'):
        src = img.get('src', '')
        if src.startswith('.') or not src.startswith('../'):
            # Update to proper EPUB image path
            img['src'] = f"../Images/{os.path.basename(src)}"
    
    # Extract any inline styles from the original HTML
    style_content = ""
    style_tag = soup.find('style')
    if style_tag:
        style_content = str(style_tag)
    
    # Create XHTML structure with preserved styling
    xhtml_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <title>{title}</title>
    <link rel="stylesheet" type="text/css" href="../Styles/style.css"/>
    {style_content}
</head>
<body>
{str(body)}
</body>
</html>'''
    
    # Clean up the XHTML - but PRESERVE classes and styles
    xhtml_content = xhtml_content.replace('&nbsp;', '&#160;')  # Fix entities
    xhtml_content = xhtml_content.replace('&amp;', '&amp;')  # Ensure proper entity encoding
    
    # Get the filename for output
    filename = os.path.basename(html_file_path).replace('.html', '.xhtml')
    output_path = os.path.join(output_dir, filename)
    
    # Write the XHTML file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(xhtml_content)
    
    return filename

def verify_html_xhtml_match(html_file, xhtml_file):
    """Verify that XHTML file matches HTML file content"""
    print(f"Verifying {html_file} vs {xhtml_file}...")
    
    # Read both files
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    with open(xhtml_file, 'r', encoding='utf-8') as f:
        xhtml_content = f.read()
    
    # Parse both files
    html_soup = BeautifulSoup(html_content, 'html.parser')
    xhtml_soup = BeautifulSoup(xhtml_content, 'html.parser')
    
    # Extract body content
    html_body = html_soup.find('body')
    xhtml_body = xhtml_soup.find('body')
    
    if not html_body or not xhtml_body:
        print(f"  ❌ Missing body content")
        return False
    
    # Check for key elements and classes
    issues = []
    
    # Check for bible-quote classes
    html_quotes = html_body.find_all('div', class_='bible-quote')
    xhtml_quotes = xhtml_body.find_all('div', class_='bible-quote')
    
    if len(html_quotes) != len(xhtml_quotes):
        issues.append(f"Bible quote count mismatch: HTML has {len(html_quotes)}, XHTML has {len(xhtml_quotes)}")
    
    # Check for other important classes
    important_classes = ['bible-quote', 'highlight', 'callout', 'emphasis']
    for class_name in important_classes:
        html_elements = html_body.find_all(class_=class_name)
        xhtml_elements = xhtml_body.find_all(class_=class_name)
        
        if len(html_elements) != len(xhtml_elements):
            issues.append(f"{class_name} class count mismatch: HTML has {len(html_elements)}, XHTML has {len(xhtml_elements)}")
    
    # Check for inline styles
    html_styled = html_body.find_all(attrs={'style': True})
    xhtml_styled = xhtml_body.find_all(attrs={'style': True})
    
    if len(html_styled) != len(xhtml_styled):
        issues.append(f"Inline style count mismatch: HTML has {len(html_styled)}, XHTML has {len(xhtml_styled)}")
    
    # Check for images
    html_images = html_body.find_all('img')
    xhtml_images = xhtml_body.find_all('img')
    
    if len(html_images) != len(xhtml_images):
        issues.append(f"Image count mismatch: HTML has {len(html_images)}, XHTML has {len(xhtml_images)}")
    
    if issues:
        print(f"  ❌ Issues found:")
        for issue in issues:
            print(f"    - {issue}")
        return False
    else:
        print(f"  ✅ Content matches")
        return True

def main():
    # Define paths
    epub_dir = "epub"
    oebps_dir = os.path.join(epub_dir, "OEBPS")
    text_dir = os.path.join(oebps_dir, "Text")
    images_dir = os.path.join(oebps_dir, "Images")
    
    # Files to process (in order)
    files_to_process = [
        "copyright.html",
        "introduction.html",
        "toc.html",
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
        "bibliography.html"
    ]
    
    print("🔄 Converting HTML files to XHTML with preserved styling...")
    
    # Convert HTML files to XHTML
    converted_files = []
    for html_file in files_to_process:
        if os.path.exists(html_file):
            print(f"Converting {html_file}...")
            xhtml_filename = convert_html_to_xhtml_enhanced(html_file, text_dir)
            if xhtml_filename:
                converted_files.append((html_file, xhtml_filename))
        else:
            print(f"Warning: {html_file} not found")
    
    # Copy images to EPUB Images directory
    print("\n🖼️ Copying images...")
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.svg']
    for file in os.listdir('.'):
        if any(file.lower().endswith(ext) for ext in image_extensions):
            print(f"Copying image {file}...")
            shutil.copy2(file, images_dir)
    
    # Verify conversions
    print("\n🔍 Verifying conversions...")
    verification_results = []
    for html_file, xhtml_filename in converted_files:
        xhtml_path = os.path.join(text_dir, xhtml_filename)
        if os.path.exists(xhtml_path):
            result = verify_html_xhtml_match(html_file, xhtml_path)
            verification_results.append((html_file, result))
        else:
            print(f"  ❌ XHTML file not found: {xhtml_filename}")
            verification_results.append((html_file, False))
    
    # Summary
    print("\n📊 Conversion Summary:")
    successful_conversions = sum(1 for _, result in verification_results if result)
    total_conversions = len(verification_results)
    
    print(f"✅ Successful conversions: {successful_conversions}/{total_conversions}")
    
    if successful_conversions < total_conversions:
        print("\n❌ Files with issues:")
        for html_file, result in verification_results:
            if not result:
                print(f"  - {html_file}")
    
    print("\n✨ Enhanced conversion complete!")
    return successful_conversions == total_conversions

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n⚠️ Some files had conversion issues. Please review the output above.")
        exit(1)
