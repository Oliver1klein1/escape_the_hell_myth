#!/usr/bin/env python3
"""
Add print CSS to reduce callout-quote margins
"""

import os

def add_callout_quote_rules(file_path):
    """Add or update callout-quote print CSS to reduce margins"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if print CSS exists
        if '@media print' not in content:
            print(f"  ⏭️  {file_path} doesn't have print CSS")
            return False
        
        changes_made = False
        
        # Check if callout-quote rule already exists
        if '/* Reduce margins on callout-quotes to prevent large gaps */' in content:
            print(f"  ⏭️  {file_path} already has callout-quote CSS")
            return False
        
        # Insert the rule before the Lists section or Links section
        callout_quote_rule = '''            /* Reduce margins on callout-quotes to prevent large gaps */
            .callout-quote {
                margin: 1rem 0 !important;
                padding: 1rem !important;
            }
            
'''
        
        # Try to insert before Lists section
        if '/* Lists */' in content:
            content = content.replace('/* Lists */', callout_quote_rule + '/* Lists */')
            changes_made = True
        elif '/* Links */' in content:
            content = content.replace('/* Links */', callout_quote_rule + '/* Links */')
            changes_made = True
        
        if changes_made:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"  ✅ Fixed callout-quote margins in {file_path}")
            return True
        else:
            print(f"  ⚠️  {file_path} couldn't be updated (no insertion point)")
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
    
    print("🖨️  Fixing callout-quote margins in print CSS...")
    print("=" * 50)
    
    success_count = 0
    skip_count = 0
    error_count = 0
    
    for html_file in html_files:
        if not os.path.exists(html_file):
            print(f"  ⚠️  {html_file} not found")
            error_count += 1
            continue
        
        result = add_callout_quote_rules(html_file)
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
        print("\n🎉 Callout-quote margins fixed! No more large gaps when printing.")
    
if __name__ == "__main__":
    main()

