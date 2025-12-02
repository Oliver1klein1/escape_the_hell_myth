#!/usr/bin/env python3
"""Check for image discrepancies between HTML files and EPUB"""
import os
import re
import zipfile
from collections import defaultdict

# Get all images referenced in HTML files
html_files = [f for f in os.listdir('.') if f.endswith('.html') and f not in ['print_test.html']]

html_images = defaultdict(list)
for html_file in html_files:
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    # Find all img src attributes
    matches = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', content)
    for match in matches:
        # Get just the filename
        filename = os.path.basename(match)
        html_images[html_file].append(filename)

# Get all images in EPUB
with zipfile.ZipFile('Escape_The_Hell_Myth_KDP.epub', 'r') as z:
    epub_images = set()
    for f in z.filelist:
        if '/images/' in f.filename.lower():
            epub_images.add(os.path.basename(f.filename))

# Check source folder images
source_images = set()
for f in os.listdir('.'):
    if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
        source_images.add(f)
# Also check otherbooks folder
if os.path.exists('otherbooks'):
    for f in os.listdir('otherbooks'):
        if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
            source_images.add(f)

print("=" * 60)
print("IMAGE VERIFICATION REPORT")
print("=" * 60)

print(f"\nTotal images in EPUB: {len(epub_images)}")
print(f"Total images in source folders: {len(source_images)}")

# Check each HTML file
missing_in_epub = []
missing_in_source = []

print("\n" + "=" * 60)
print("PER-FILE IMAGE CHECK")
print("=" * 60)

for html_file in sorted(html_files):
    images = html_images.get(html_file, [])
    if images:
        print(f"\n{html_file}: {len(images)} images")
        for img in images:
            in_epub = img in epub_images
            in_source = img in source_images
            status = "✓" if in_epub else "✗ NOT IN EPUB"
            if not in_source:
                status += " (NOT IN SOURCE)"
                missing_in_source.append((html_file, img))
            if not in_epub:
                missing_in_epub.append((html_file, img))
            print(f"  {status} {img}")

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)

if missing_in_epub:
    print(f"\n❌ MISSING FROM EPUB ({len(missing_in_epub)} images):")
    for html_file, img in missing_in_epub:
        print(f"  - {img} (referenced in {html_file})")
else:
    print("\n✅ All referenced images are in the EPUB!")

if missing_in_source:
    print(f"\n⚠️ MISSING FROM SOURCE ({len(missing_in_source)} images):")
    for html_file, img in missing_in_source:
        print(f"  - {img} (referenced in {html_file})")

