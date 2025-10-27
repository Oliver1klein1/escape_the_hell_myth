#!/usr/bin/env python3
"""
Update existing print CSS to allow callouts to break across pages
"""

import os
import re

def update_print_css_in_file(file_path):
    """Update print CSS in a single HTML file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if print CSS exists
        if '@media print' not in content:
            print(f"  ⏭️  {file_path} doesn't have print CSS")
            return False
        
        # Pattern to find the problematic rule
        old_pattern = r'\.highlight,\s*\.callout,\s*\.book-section,\s*\.series-section\s*\{[^}]*page-break-inside:\s*avoid;[^}]*\}'
        
        new_replacement = '''.highlight,
            .callout {
                page-break-inside: auto;
                margin: 1rem 0;
            }
            
            /* Keep these sections together when possible */
            .book-section,
            .series-section {
                page-break-inside: avoid;
                margin: 1rem 0;
            }'''
        
        # Try to replace
        if re.search(old_pattern, content):
            content = re.sub(old_pattern, new_replacement, content, flags=re.DOTALL)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"  ✅ Updated print CSS in {file_path}")
            return True
        else:
            # Try a simpler approach - replace the specific line
            if '.callout {' in content and 'page-break-inside: avoid;' in content:
                # Replace just the callout rule
                content = content.replace(
                    '.highlight,\n            .callout,\n            .book-section,\n            .series-section {\n                page-break-inside: avoid;',
                    '.highlight,\n            .callout {\n                page-break-inside: auto;'
                )
                
                # If we need to split the rules
                if 'page-break-inside: auto;' in content:
                    content = content.replace(
                        '.book-section,\n            .series-section {\n                page-break-inside: avoid;',
                        '/* Keep these sections together when possible */\n            .book-section,\n            .series-section {\n                page-break-inside: avoid;'
                    )
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"  ✅ Updated print CSS in {file_path}")
                return True
            else:
                print(f"  ⏭️  {file_path} already has correct print CSS or doesn't match pattern")
                return False
        
    except Exception as e:
        print(f"  ❌ Error processing {file_path}: {e}")
        return False

def main():
    # List of HTML files to process
    html_files = [
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
    
    print("🖨️  Updating print CSS to allow callouts to break...")
    print("=" * 50)
    
    success_count = 0
    skip_count = 0
    error_count = 0
    
    for html_file in html_files:
        if not os.path.exists(html_file):
            print(f"  ⚠️  {html_file} not found")
            error_count += 1
            continue
        
        result = update_print_css_in_file(html_file)
        if result:
            success_count += 1
        else:
            skip_count += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Summary:")
    print(f"  ✅ Successfully updated: {success_count}")
    print(f"  ⏭️  Skipped: {skip_count}")
    print(f"  ❌ Errors: {error_count}")
    
    if success_count > 0:
        print("\n🎉 Print CSS updated! Callouts will now flow across pages naturally.")
    
if __name__ == "__main__":
    main()

