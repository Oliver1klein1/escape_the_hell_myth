#!/usr/bin/env python3
"""
Fix print CSS to allow tables and info-boxes to break across pages
"""

import os
import re

def fix_table_css(file_path):
    """Update print CSS to allow tables to break across pages"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if print CSS exists
        if '@media print' not in content:
            print(f"  ⏭️  {file_path} doesn't have print CSS")
            return False
        
        changes_made = False
        
        # Fix table to allow breaking
        if 'table {\n                page-break-inside: avoid;' in content:
            content = content.replace(
                'table {\n                page-break-inside: avoid;',
                'table {\n                page-break-inside: auto;'
            )
            changes_made = True
        
        # Add tr rule if not present
        if 'tr {\n                page-break-inside: avoid;' not in content and changes_made:
            # Insert tr rule after table rule
            pattern = r'(table \{[^\}]+\})'
            replacement = r'''\1
            
            /* Keep table rows together when possible */
            tr {
                page-break-inside: avoid;
            }'''
            content = re.sub(pattern, replacement, content)
        
        # Add info-box rules if not present
        if '.info-box {\n                page-break-inside: auto;' not in content:
            # Insert info-box rules before Lists section
            if '/* Lists */' in content:
                info_box_rules = '''/* Allow info-boxes (like the prophecy table box) to break */
            .info-box {
                page-break-inside: auto;
            }
            
            /* Reduce info-box title margins */
            .info-box-title {
                margin-bottom: 0.75rem !important;
                page-break-after: avoid;
            }
            
            /* Lists */
'''
                content = content.replace('/* Lists */', info_box_rules)
                changes_made = True
        
        if changes_made:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"  ✅ Fixed table page breaks in {file_path}")
            return True
        else:
            print(f"  ⏭️  {file_path} already has correct table CSS")
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
    
    print("🖨️  Fixing table page breaks in print CSS...")
    print("=" * 50)
    
    success_count = 0
    skip_count = 0
    error_count = 0
    
    for html_file in html_files:
        if not os.path.exists(html_file):
            print(f"  ⚠️  {html_file} not found")
            error_count += 1
            continue
        
        result = fix_table_css(html_file)
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
        print("\n🎉 Table page breaks fixed! Tables will now flow across pages naturally.")
    
if __name__ == "__main__":
    main()

