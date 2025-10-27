#!/usr/bin/env python3
"""
Fix print CSS to allow lists in callouts to break across pages
"""

import os
import re

def fix_print_css_for_lists(file_path):
    """Update print CSS to allow lists to break across pages"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if print CSS exists
        if '@media print' not in content:
            print(f"  ⏭️  {file_path} doesn't have print CSS")
            return False
        
        changes_made = False
        
        # Fix ul, ol to allow breaking
        old_list_rule = r'ul, ol \{\s*page-break-inside: avoid;\s*\}'
        new_list_rule = '''ul, ol {
                page-break-inside: auto;
            }'''
        
        if re.search(old_list_rule, content):
            content = re.sub(old_list_rule, new_list_rule, content)
            changes_made = True
        
        # Fix li elements to allow breaking (except when in bible quotes)
        old_li_rule = r'p, li \{\s*page-break-inside: avoid;\s*orphans:\s*3;\s*widows:\s*3;\s*margin-bottom:\s*0\.5rem;\s*\}'
        new_li_rule = '''p {
                page-break-inside: avoid;
                orphans: 3;
                widows: 3;
                margin-bottom: 0.5rem;
            }
            
            /* Allow list items to break but keep paragraphs intact */
            li {
                orphans: 2;
                widows: 2;
            }'''
        
        if re.search(old_li_rule, content):
            content = re.sub(old_li_rule, new_li_rule, content)
            changes_made = True
        
        # Add specific rule for callout titles to reduce margins
        if changes_made or '.callout-title' not in content:
            # Add rule for callout titles
            callout_title_rule = '''.callout-title {
                margin-bottom: 0.5rem !important;
                page-break-after: avoid;
            }'''
            
            # Insert after the h2 rule
            if re.search('h2 \{[^}]*margin-bottom:\s*0\.5rem;[^}]*\}', content):
                # Insert after h2 rule
                pattern = '(h2 \{[^}]+\})'
                replacement = r'\1\n            ' + callout_title_rule
                if callout_title_rule not in content:
                    content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        
        if changes_made:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"  ✅ Fixed list page breaks in {file_path}")
            return True
        else:
            print(f"  ⏭️  {file_path} already has correct list CSS")
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
    
    print("🖨️  Fixing list page breaks in print CSS...")
    print("=" * 50)
    
    success_count = 0
    skip_count = 0
    error_count = 0
    
    for html_file in html_files:
        if not os.path.exists(html_file):
            print(f"  ⚠️  {html_file} not found")
            error_count += 1
            continue
        
        result = fix_print_css_for_lists(html_file)
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
        print("\n🎉 List page breaks fixed! Lists will now flow across pages naturally.")
    
if __name__ == "__main__":
    main()

