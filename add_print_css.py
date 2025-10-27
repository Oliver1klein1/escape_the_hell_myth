#!/usr/bin/env python3
"""
Add print CSS to all HTML files according to cursor rules
"""

import os
import re

# Print CSS template from .cursorrules_pdf
print_css = """
        /* Print-specific styles */
        @media print {
            /* Page setup */
            @page {
                size: 8.5in 11in;
                margin: 1in;
            }
            
            /* Base styles */
            body {
                font-family: Georgia, 'Times New Roman', Times, serif;
                font-size: 12pt;
                line-height: 1.6;
                color: #000;
                background: #fff;
                margin: 0;
                padding: 0;
            }
            
            /* Hide navigation */
            .navigation,
            .nav-link,
            .navigation-buttons,
            .nav-button,
            nav,
            .navbar,
            .menu,
            .breadcrumb,
            .pagination,
            [class*="nav"],
            [class*="menu"],
            [class*="breadcrumb"] {
                display: none !important;
            }
            
            /* Preserve content styling */
            .bible-quote {
                font-family: 'Palatino Linotype', 'Book Antiqua', Palatino, serif;
                font-style: italic;
                color: #2c5282;
                background: #f0f4f8;
                border-left: 4px solid #4299e1;
                padding: 1.2rem 1.5rem;
                margin: 1.5rem 0;
                border-radius: 0 0.5rem 0.5rem 0;
                page-break-inside: avoid;
            }
            
            /* Allow callouts to break across pages naturally */
            .highlight,
            .callout {
                page-break-inside: auto;
                margin: 1rem 0;
            }
            
            /* Keep these sections together when possible */
            .book-section,
            .series-section {
                page-break-inside: avoid;
                margin: 1rem 0;
            }
            
            /* Typography */
            h1, h2, h3, h4, h5, h6 {
                page-break-after: avoid;
                page-break-inside: avoid;
                color: #2d3748;
            }
            
            h1 {
                font-size: 18pt;
                margin-bottom: 1rem;
            }
            
            h2 {
                font-size: 16pt;
                margin-top: 1.5rem;
                margin-bottom: 0.5rem;
            }
            
            p, li {
                page-break-inside: avoid;
                orphans: 3;
                widows: 3;
                margin-bottom: 0.5rem;
            }
            
            /* Images */
            img {
                max-width: 100% !important;
                height: auto !important;
                page-break-inside: avoid;
                display: block;
                margin: 1rem auto;
            }
            
            /* Page breaks */
            .page-break {
                page-break-before: always;
            }
            
            .no-break {
                page-break-inside: avoid;
            }
            
            .chapter {
                page-break-before: always;
            }
            
            /* Tables */
            table {
                page-break-inside: avoid;
                border-collapse: collapse;
                width: 100%;
            }
            
            th, td {
                border: 1px solid #000;
                padding: 0.5rem;
                text-align: left;
            }
            
            /* Lists */
            ul, ol {
                page-break-inside: avoid;
            }
            
            /* Links */
            a {
                color: #000;
                text-decoration: none;
            }
            
            /* Hide elements that shouldn't print */
            .no-print,
            .screen-only {
                display: none !important;
            }
            
            /* Preserve original container and layout */
            .container {
                padding: 20px;
            }
        }
"""

def add_print_css_to_file(file_path):
    """Add print CSS to a single HTML file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if print CSS already exists
        if '@media print' in content:
            print(f"  ⚠️  {file_path} already has print CSS")
            return False
        
        # Find the </style> tag
        if '</style>' not in content:
            print(f"  ❌ {file_path} doesn't have a style tag")
            return False
        
        # Insert print CSS before </style>
        content = content.replace('    </style>', print_css + '    </style>')
        
        # Write the file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  ✅ Added print CSS to {file_path}")
        return True
        
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
    
    print("🖨️  Adding print CSS to HTML files...")
    print("=" * 50)
    
    success_count = 0
    skip_count = 0
    error_count = 0
    
    for html_file in html_files:
        if not os.path.exists(html_file):
            print(f"  ⚠️  {html_file} not found")
            error_count += 1
            continue
        
        result = add_print_css_to_file(html_file)
        if result:
            success_count += 1
        else:
            skip_count += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Summary:")
    print(f"  ✅ Successfully added print CSS: {success_count}")
    print(f"  ⏭️  Skipped (already has print CSS): {skip_count}")
    print(f"  ❌ Errors: {error_count}")
    
    if success_count > 0:
        print("\n🎉 Print CSS added! You can now use Ctrl+P to print to PDF.")
    
if __name__ == "__main__":
    main()

