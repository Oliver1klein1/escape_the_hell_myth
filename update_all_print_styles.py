#!/usr/bin/env python3
"""
Update all HTML files with comprehensive 6x9 FULL COLOR print styles
"""

import os
import re

# Comprehensive print CSS with FULL COLOR printing (no grayscale/black-white forcing)
PRINT_CSS = """        /* Print-specific styles - FULL COLOR */
        @media print {
            /* ============================================
               1. PAGE SIZE & LAYOUT - 6x9 inches
               ============================================ */
            @page {
                size: 6in 9in;
                margin: 0.75in;
            }
            
            /* ============================================
               2. FULL COLOR PRINTING - PRESERVE ORIGINAL COLORS
               ============================================ */
            /* Minimal universal reset: remove shadows/animations only */
            * {
                box-shadow: none !important;
                text-shadow: none !important;
                animation: none !important;
                transition: none !important;
                -webkit-print-color-adjust: exact !important;
                print-color-adjust: exact !important;
                color-adjust: exact !important;
            }
            
            /* Body setup for 6x9 trade paperback */
            body {
                font-family: 'Merriweather', Georgia, 'Times New Roman', Times, serif;
                margin: 0;
                padding: 0;
                line-height: 1.5;
                font-size: 11pt !important;
                overflow: visible !important;
                max-width: none !important;
                width: 100% !important;
            }
            
            /* Body text at 11pt - standard for 6x9 trade paperback */
            p, li {
                font-size: 11pt !important;
            }
            
            /* Typography */
            h1, h2, h3, h4, h5, h6 {
                page-break-after: avoid;
                page-break-inside: avoid;
            }
            
            h1, .chapter-title {
                font-size: 22pt;
                margin-bottom: 1rem;
            }
            
            h2 {
                font-size: 18pt;
                margin-top: 1.5rem;
                margin-bottom: 0.5rem;
            }
            
            .callout-title {
                margin-bottom: 0.5rem !important;
                page-break-after: avoid;
            }
            
            p {
                font-size: 11pt !important;
                page-break-inside: auto;
                orphans: 2;
                widows: 2;
                margin-bottom: 0.5em;
            }
            
            li {
                orphans: 2;
                widows: 2;
                font-size: 11pt !important;
            }
            
            th, td {
                font-size: 10pt !important;
            }
            
            /* Links - keep text readable but underline for clarity */
            a {
                text-decoration: none !important;
            }
            
            /* ============================================
               3. IMAGES PRINT IN FULL COLOR
               ============================================ */
            /* Images print in their original colors - NO grayscale filter */
            img,
            img.chapter-image,
            img.book-cover,
            img.callout-image,
            img.figure,
            img.cover-img,
            img.logo-image,
            img.logo-image-top {
                filter: none !important;
                -webkit-filter: none !important;
                -moz-filter: none !important;
                max-width: 100% !important;
                height: auto !important;
                page-break-inside: avoid;
                display: block;
                margin: 1rem auto;
            }
            
            /* ============================================
               4. PAGE BREAKS & LAYOUT
               ============================================ */
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
                page-break-inside: auto;
                border-collapse: collapse;
                width: 100%;
            }
            
            tr {
                page-break-inside: avoid;
            }
            
            th, td {
                padding: 0.5rem;
                text-align: left;
            }
            
            /* Content boxes */
            .highlight,
            .callout {
                page-break-inside: auto;
                margin: 1rem 0;
            }
            
            .book-section,
            .series-section {
                page-break-inside: avoid;
                margin: 1rem 0;
            }
            
            .info-box {
                page-break-inside: auto;
            }
            
            .info-box-title {
                margin-bottom: 0.75rem !important;
                page-break-after: avoid;
            }
            
            .callout-quote {
                margin: 1rem 0 !important;
                padding: 1rem !important;
                page-break-inside: avoid;
            }
            
            .bible-quote {
                page-break-inside: avoid;
            }
            
            ul, ol {
                page-break-inside: auto;
            }
            
            /* ============================================
               5. HIDE NAVIGATION & UI CHROME IN PRINT
               ============================================ */
            /* Hide standard navigation elements */
            header,
            footer,
            nav,
            .navbar,
            .nav,
            .nav-bar,
            .site-header,
            .site-footer,
            .navigation,
            .nav-link,
            .navigation-buttons,
            .nav-button,
            .pagination,
            .breadcrumbs,
            .breadcrumb,
            .toc-controls,
            .nav-buttons,
            .btn,
            .button,
            .icon-button,
            .back-to-top,
            .menu {
                display: none !important;
                visibility: hidden !important;
                opacity: 0 !important;
                height: 0 !important;
                width: 0 !important;
                margin: 0 !important;
                padding: 0 !important;
                overflow: hidden !important;
            }
            
            /* Override inline display:inline-block styles with attribute selectors */
            nav[style*="display:inline-block"],
            nav[style*="display: inline-block"],
            .nav-buttons[style*="display:inline-block"],
            .nav-buttons[style*="display: inline-block"],
            .navigation-buttons[style*="display:inline-block"],
            .navigation-buttons[style*="display: inline-block"],
            .nav-button[style*="display:inline-block"],
            .nav-button[style*="display: inline-block"],
            .enter-button[style*="display:inline-block"],
            .enter-button[style*="display: inline-block"],
            .btn[style*="display:inline-block"],
            .btn[style*="display: inline-block"],
            .button[style*="display:inline-block"],
            .button[style*="display: inline-block"],
            a[style*="display:inline-block"][class*="nav"],
            a[style*="display: inline-block"][class*="nav"],
            a[style*="display:inline-block"][class*="button"],
            a[style*="display: inline-block"][class*="button"] {
                display: none !important;
                visibility: hidden !important;
            }
            
            /* Hide any element with navigation-related classes */
            [class*="nav"],
            [class*="menu"],
            [class*="breadcrumb"] {
                display: none !important;
            }
            
            /* Hide button classes (but preserve content/text classes) */
            [class*="button"]:not([class*="content"]):not([class*="text"]) {
                display: none !important;
            }
            
            /* Hide elements that shouldn't print */
            .no-print,
            .screen-only {
                display: none !important;
            }
            
            /* ============================================
               6. CONTAINER LAYOUT FOR PRINT
               ============================================ */
            /* Container must have NO max-width for print - let it fill the page */
            .container,
            .chapter,
            body > div {
                width: 100% !important;
                max-width: none !important;
                margin: 0 !important;
                padding: 0 !important;
                box-sizing: border-box !important;
                overflow: visible !important;
            }
        }"""

def fix_stylesheet_links(file_path):
    """Add media="screen" to Tailwind and FontAwesome links to prevent them from affecting print"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix Tailwind link - add media="screen" if not present
        content = re.sub(
            r'<link href="https://cdn\.jsdelivr\.net/npm/tailwindcss[^"]*" rel="stylesheet"(?! media="screen")>',
            r'<link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet" media="screen">',
            content
        )
        
        # Fix FontAwesome link - add media="screen" if not present
        content = re.sub(
            r'<link rel="stylesheet" href="https://cdn\.jsdelivr\.net/npm/@fortawesome/fontawesome-free[^"]*"(?! media="screen")>',
            r'<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.0.0/css/all.min.css" media="screen">',
            content
        )
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  🔧 Fixed stylesheet links in {file_path}")
            return True
        return False
        
    except Exception as e:
        print(f"  ❌ Error fixing stylesheets in {file_path}: {e}")
        return False

def remove_grayscale_javascript(content):
    """Remove the grayscale-forcing JavaScript from HTML content"""
    # Pattern to match the grayscale JavaScript block
    patterns = [
        # Match the entire script block that forces grayscale
        r'<script>\s*//\s*Force grayscale printing via JavaScript.*?</script>',
        r'<script>\s*function forceGrayscalePrint\(\).*?</script>',
        # Also remove any standalone grayscale event listeners
        r"window\.addEventListener\('beforeprint',\s*forceGrayscalePrint\);",
        r"window\.addEventListener\('print',\s*forceGrayscalePrint\);",
    ]
    
    for pattern in patterns:
        content = re.sub(pattern, '', content, flags=re.DOTALL)
    
    # Clean up any empty script tags that might remain
    content = re.sub(r'<script>\s*</script>', '', content)
    
    # Clean up multiple blank lines
    content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content)
    
    return content

def update_print_css_in_file(file_path):
    """Replace existing @media print block with comprehensive FULL COLOR print styles"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove grayscale JavaScript first
        original_content = content
        content = remove_grayscale_javascript(content)
        if content != original_content:
            print(f"  🗑️  Removed grayscale JavaScript from {file_path}")
        
        # Check if file already has @media print
        if '@media print' not in content:
            print(f"  ⚠️  {file_path} doesn't have @media print - skipping")
            return False
        
        # Find @media print block by tracking braces
        lines = content.split('\n')
        start_idx = None
        end_idx = None
        brace_count = 0
        
        for i, line in enumerate(lines):
            if '@media print' in line and start_idx is None:
                start_idx = i
                brace_count = line.count('{') - line.count('}')
                if brace_count == 0:
                    # Single line @media print { }
                    end_idx = i + 1
                    break
            elif start_idx is not None:
                brace_count += line.count('{') - line.count('}')
                if brace_count == 0:
                    # Found the closing brace
                    end_idx = i + 1
                    break
        
        if start_idx is None or end_idx is None:
            # Fallback: try regex
            match = re.search(r'(@media print\s*\{[^}]*\{[^}]*\}[^}]*\})', content, re.DOTALL)
            if not match:
                # Try simpler pattern
                match = re.search(r'(@media print\s*\{.*?\})', content, re.DOTALL)
            
            if match:
                # Replace using regex
                new_content = content[:match.start()] + PRINT_CSS + '\n' + content[match.end():]
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"  ✅ Updated {file_path} (regex method)")
                return True
            else:
                print(f"  ⚠️  Could not find complete @media print block in {file_path}")
                return False
        
        # Replace the block
        new_lines = lines[:start_idx] + PRINT_CSS.split('\n') + lines[end_idx:]
        new_content = '\n'.join(new_lines)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"  ✅ Updated {file_path}")
        return True
        
    except Exception as e:
        print(f"  ❌ Error processing {file_path}: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    # List of HTML files to process
    html_files = [
        "index.html",
        "copyright.html",
        "dedication.html",
        "introduction.html",
        "toc.html",
        "part1.html", "part2.html", "part3.html", "part4.html",
        "chapter1.html", "chapter2.html", "chapter3.html", "chapter4.html",
        "chapter5.html", "chapter6.html", "chapter7.html", "chapter8.html",
        "conclusion.html",
        "other-books.html",
        "appendix.html",
        "bibliography.html"
    ]
    
    print("🖨️  Updating all HTML files with FULL COLOR 6x9 print styles...")
    print("=" * 70)
    print("🎨  FULL COLOR PRINTING ENABLED")
    print("   - Text, backgrounds, and images will print in original colors")
    print("   - Grayscale/black-white forcing has been REMOVED")
    print("   - Navigation/UI elements will be hidden in print")
    print("=" * 70)
    print()
    
    success_count = 0
    skip_count = 0
    error_count = 0
    
    for html_file in html_files:
        if not os.path.exists(html_file):
            print(f"  ⚠️  {html_file} not found - skipping")
            skip_count += 1
            continue
        
        # First fix stylesheet links to add media="screen"
        fix_stylesheet_links(html_file)
        
        # Then update print CSS
        result = update_print_css_in_file(html_file)
        if result:
            success_count += 1
        else:
            skip_count += 1
    
    print()
    print("=" * 70)
    print(f"📊 Summary:")
    print(f"  ✅ Successfully updated: {success_count}")
    print(f"  ⏭️  Skipped: {skip_count}")
    print(f"  ❌ Errors: {error_count}")
    print()
    print("🎉 FULL COLOR Print CSS updated!")
    print()
    print("📝 What changed:")
    print("   ✓ Removed all color: #000 !important overrides")
    print("   ✓ Removed all background: #fff !important overrides")
    print("   ✓ Removed grayscale filter from images")
    print("   ✓ Removed grayscale-forcing JavaScript")
    print("   ✓ Kept 6x9 page size (6in x 9in with 0.75in margins)")
    print("   ✓ Kept navigation/UI hiding rules")
    print()

if __name__ == "__main__":
    main()
