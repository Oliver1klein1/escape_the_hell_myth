# New Book Project Setup Guide

## Overview
This guide provides a complete setup template for creating a new book project with EPUB and PDF capabilities, following the proven workflow from the "Escape The Hell Myth" project.

## Initial Project Statement

The aim of this project is to create a book with the following metadata:

**[INSERT NEW BOOK METADATA HERE - see Metadata Template section below]**

- For publication to Amazon as an **ebook** (create an EPUB file that converts cleanly in Kindle Previewer to KDP format)
- For publication to Amazon as **paperback** and **hardcover** (print to PDF using the cursor rules in the root directory)
- Book dimensions: **6 x 9 inches** for paperback and hardcover
- Print specifications: **Black and white on white paper**

---

## Files to Copy to New Project Root

### 1. Cursor Rules (Copy all to new project root)
- **`.cursorrules`** - Main EPUB conversion and creation rules
- **`.cursorrules_pdf`** - PDF printing rules and guidelines  
- **`.cursorrules_writing`** - Writing style and tone guidelines

### 2. Python Scripts (Copy all to new project root, then update metadata)
- **`create_epub_enhanced.py`** - Converts HTML to XHTML with style preservation
- **`create_final_epub.py`** - Creates final EPUB file
- **`create_kdp_epub.py`** - Creates Amazon KDP-compliant EPUB
- **`verify_epub_conversion.py`** - Verifies HTML to XHTML conversion integrity
- **`check_metadata.py`** - Checks and validates book metadata
- **`server.js`** - Node.js local server for viewing HTML files (optional)
- **`package.json`** - Node.js dependencies (for server.js, optional)

### 3. Configuration Files (Copy all, update with new metadata)
- **`book_metadata.json`** - **UPDATE THIS WITH NEW BOOK METADATA** (see template below)

### 4. Documentation Files (Copy all for reference)
- **`EPUB_SETUP_GUIDE.md`** - EPUB creation workflows and standards
- **`KINDLE_COMPATIBILITY_GUIDE.md`** - Kindle-specific compatibility fixes
- **`PDF_SETUP_GUIDE.md`** - PDF printing guidelines and best practices
- **`PROJECT_SETUP_GUIDE.md`** - Project structure and organization

---

## Essential Workflow

### 1. Update Metadata Files

#### Update `book_metadata.json`:
```json
{
  "title": "[NEW BOOK TITLE]",
  "subtitle": "[BOOK SUBTITLE IF ANY]",
  "author": "[AUTHOR NAME]",
  "publisher": "[PUBLISHER NAME]",
  "publication_date": "2025",
  "cover_image": "[PATH TO COVER IMAGE]",
  "tags": "[comma,separated,keywords]",
  "description": "[BOOK DESCRIPTION]",
  "language": "en",
  "isbn": "[ISBN IF AVAILABLE]"
}
```

#### Update Python Scripts (Search and replace book-specific references):
In `create_epub_enhanced.py`, `create_final_epub.py`, and `create_kdp_epub.py`:
- Search for old book title references
- Search for old cover image filename
- Update `files_to_process` or `files_to_check` lists if book structure differs
- Update `correct_order` in `fix_spine_order()` functions if needed

### 2. Cursor Rules Reference

#### When Printing from HTML to PDF:
Follow the rules in: **`.cursorrules_pdf`**

**Key print specifications:**
- Page size: `8.5in 11in` (default) or customize for your needs
- Body font: `14pt`
- H1 headings: `22pt`
- H2 headings: `18pt`
- All text prints in black (`#000`)
- Paragraphs can break naturally across pages
- Callouts, tables, lists can break when needed

#### When Creating EPUB Files:
Follow the rules in: **`.cursorrules`**

**Key EPUB requirements:**
- Use enhanced conversion script: `python create_epub_enhanced.py`
- Verify conversion: `python verify_epub_conversion.py`
- Create final EPUB: `python create_final_epub.py`
- Create KDP EPUB: `python create_kdp_epub.py`

#### When Writing or Editing Text:
Follow the rules in: **`.cursorrules_writing`**

**Key writing principles:**
- Conversational, engaging, colorful style
- Avoid clichéd phrases ("here's the kicker", etc.)
- Strategic use of **bold**, *italics*, ALL CAPS
- Never use em-dashes — use ellipses (…), colons (:), or commas (,)
- Preserve all original concepts and ideas
- Add contemporary analogies when beneficial

### 3. Standard EPUB Workflow

```bash
# 1. Check metadata completeness
python check_metadata.py

# 2. Convert HTML to XHTML with style preservation
python create_epub_enhanced.py

# 3. Verify conversion integrity
python verify_epub_conversion.py

# 4. Create final EPUB (only if verification passes)
python create_final_epub.py

# 5. Create Amazon KDP-compliant EPUB
python create_kdp_epub.py
```

### 4. Required HTML File Structure

Your HTML files should follow this naming convention:
- `cover.html` - Cover page
- `copyright.html` - Copyright page  
- `introduction.html` - Book introduction
- `toc.html` - Table of contents
- `chapter1.html`, `chapter2.html`, etc. - Chapters
- `part1.html`, `part2.html`, etc. - Part dividers (if used)
- `conclusion.html` - Book conclusion
- `other-books.html` - Other books by author
- `appendix.html` - Appendices
- `bibliography.html` - Bibliography

### 5. HTML File Requirements

Each HTML file must include:
- Proper print CSS (`@media print` section)
- Navigation elements for web viewing
- Proper semantic HTML structure
- Alt text for all images
- CSS classes for styling (bible-quote, callout, etc.)

### 6. Image Directory Structure

Create an `images/` or `Images/` directory containing all book images. Ensure:
- All images are properly named and referenced in HTML
- Image paths in HTML match actual file locations
- Cover image is named `cover.jpg` (or update in metadata)

---

## Metadata Template

Copy this template and fill in your new book's information:

```json
{
  "title": "Your Book Title Here",
  "subtitle": "Your Book Subtitle Here",
  "author": "Your Name",
  "publisher": "Your Publisher Name",
  "publication_date": "2025",
  "cover_image": "C:\\full\\path\\to\\cover.jpg",
  "tags": "keyword1, keyword2, keyword3, keyword4, keyword5",
  "description": "A compelling book description that captures the essence and value proposition of your book. This will be used for marketing and discovery on Amazon.",
  "language": "en",
  "isbn": "978-XXXXXXXXX"
}
```

---

## Important Cursor Rule References

### For PDF Printing:
Refer to: **`.cursorrules_pdf`** in root directory

**Main rules:**
1. Never rely on browser defaults - always define explicit print styles
2. Hide all navigation elements when printing
3. Preserve all styling and formatting
4. Optimize page breaks
5. Ensure fonts and colors render correctly
6. Body: 14pt, H1: 22pt, H2: 18pt
7. All text must print in black (#000)

### For EPUB Creation:
Refer to: **`.cursorrules`** in root directory

**Main rules:**
1. Always use enhanced conversion script
2. Always verify before finalizing
3. Mimetype file MUST be first in EPUB archive
4. Fix spine order to prevent alphabetical sorting
5. Handle duplicate IDs for images
6. Create proper TOC structure
7. Include complete metadata in content.opf

### For Writing/Editing:
Refer to: **`.cursorrules_writing`** in root directory

**Main rules:**
1. Write conversationally and engagingly
2. Avoid common clichés
3. Use strategic emphasis (bold, italics, ALL CAPS)
4. Preserve all original concepts
5. Never use em-dashes
6. Add contemporary analogies when helpful
7. Tap into reader psychology and emotion

---

## Python Scripts to Reference

These scripts handle the automated workflows:

### 1. `create_epub_enhanced.py`
- Converts HTML files to XHTML format
- Preserves all CSS classes and inline styles
- Copies images to EPUB structure
- Handles file renaming and path conversion

**What to update:**
- `files_to_process` list with your book's reading order
- Book title references in comments

### 2. `verify_epub_conversion.py`
- Compares HTML and XHTML files
- Verifies CSS class preservation
- Checks image counts match
- Ensures content integrity

**What to update:**
- `files_to_check` list with your book's file names

### 3. `create_final_epub.py`
- Creates final EPUB file
- Manages EPUB structure and metadata
- Ensures mimetype is first
- Fixes spine order

**What to update:**
- Output filename
- `correct_order` list in `fix_spine_order()` function

### 4. `create_kdp_epub.py`
- Creates Amazon KDP-compliant EPUB
- Handles all KDP requirements
- Generates metadata from book_metadata.json
- Manages image IDs to prevent conflicts

**What to update:**
- `correct_order` list in `fix_spine_order()` function
- Output filename

### 5. `check_metadata.py`
- Validates metadata completeness
- Checks for required fields
- Verifies cover image exists

**No updates needed** - works with book_metadata.json

---

## Guidelines Documents to Follow

### 1. EPUB_SETUP_GUIDE.md
Contains:
- EPUB conversion workflow
- Required scripts and their purposes
- File structure requirements
- Quality assurance checklists
- Troubleshooting guides

### 2. KINDLE_COMPATIBILITY_GUIDE.md
Contains:
- Amazon KDP compliance requirements
- Kindle Previewer compatibility fixes
- Common issues and solutions
- CSS limitations for Kindle

### 3. PDF_SETUP_GUIDE.md
Contains:
- Print CSS template
- Font size specifications
- Page break controls
- Typography standards
- PDF generation methods

### 4. PROJECT_SETUP_GUIDE.md
Contains:
- Project structure organization
- File naming conventions
- Directory layouts
- Best practices

---

## Project Setup Checklist

When starting a new book project:

### Phase 1: File Setup
- [ ] Copy all cursor rules files to new project root
- [ ] Copy all Python scripts to new project root
- [ ] Copy all documentation/guide files to new project root
- [ ] Copy `book_metadata.json` and update with new book metadata
- [ ] Create HTML files for your book content
- [ ] Set up images directory with all book images
- [ ] Copy cover image and ensure path is correct in metadata

### Phase 2: Script Configuration
- [ ] Update `files_to_process` in create_epub_enhanced.py
- [ ] Update `files_to_check` in verify_epub_conversion.py
- [ ] Update `correct_order` in create_final_epub.py
- [ ] Update `correct_order` in create_kdp_epub.py
- [ ] Update output filenames in create_final_epub.py
- [ ] Review all scripts for old book references

### Phase 3: HTML File Preparation
- [ ] Add print CSS to all HTML files
- [ ] Ensure all images are properly referenced
- [ ] Verify navigation works correctly
- [ ] Check Bible quotes use correct CSS class
- [ ] Ensure all callouts are properly styled
- [ ] Add alt text to all images

### Phase 4: EPUB Generation
- [ ] Run metadata check: `python check_metadata.py`
- [ ] Convert HTML to XHTML: `python create_epub_enhanced.py`
- [ ] Verify conversion: `python verify_epub_conversion.py`
- [ ] Create final EPUB: `python create_final_epub.py`
- [ ] Create KDP EPUB: `python create_kdp_epub.py`

### Phase 5: Quality Assurance
- [ ] Test EPUB in Kindle Previewer
- [ ] Verify spine order (book opens to correct page)
- [ ] Check cover image displays correctly
- [ ] Verify all images display properly
- [ ] Check navigation links work
- [ ] Test in Calibre for validation
- [ ] Print preview HTML files for PDF preparation

### Phase 6: PDF Preparation
- [ ] Open each HTML file and use Ctrl+P to preview
- [ ] Verify all text prints in black
- [ ] Check font sizes are readable (14pt body)
- [ ] Verify page breaks are appropriate
- [ ] Test print to PDF
- [ ] Verify images print correctly

---

## What Gets Updated with New Book Metadata?

### Files Requiring Metadata Updates:
1. **`book_metadata.json`** - Complete replacement with new book info
2. **Python scripts** - Update book title references, cover image filename
3. **`files_to_process` lists** - Update if book structure differs
4. **`correct_order` in spine functions** - Update if order differs

### Files That Work As-Is:
1. **Cursor rules** - Work universally
2. **Documentation guides** - Reference materials
3. **Verification scripts** - Automated to check files
4. **Server files** - Node.js server for local viewing

---

## Directory Structure Reference

```
new-book-project/
├── .cursorrules                 # EPUB rules
├── .cursorrules_pdf            # PDF rules
├── .cursorrules_writing        # Writing style rules
├── book_metadata.json          # UPDATE THIS
├── create_epub_enhanced.py    # UPDATE THIS
├── create_final_epub.py        # UPDATE THIS
├── create_kdp_epub.py          # UPDATE THIS
├── verify_epub_conversion.py   # UPDATE THIS
├── check_metadata.py           # No changes needed
├── server.js                   # No changes needed
├── package.json                # No changes needed
├── EPUB_SETUP_GUIDE.md         # Reference
├── KINDLE_COMPATIBILITY_GUIDE.md # Reference
├── PDF_SETUP_GUIDE.md          # Reference
├── PROJECT_SETUP_GUIDE.md      # Reference
├── cover.jpg                   # Your cover image
├── cover.html                  # Your HTML files
├── introduction.html
├── chapter1.html
├── chapter2.html
├── ... (all other HTML files)
├── images/                     # Your images directory
│   └── (all book images)
└── epub/                       # Generated by scripts
    └── (generated EPUB structure)
```

---

## Quick Start Commands

Once you've set up your new project:

```bash
# 1. Check that all metadata is complete
python check_metadata.py

# 2. Convert HTML to XHTML
python create_epub_enhanced.py

# 3. Verify conversion quality
python verify_epub_conversion.py

# 4. Create final EPUB files
python create_final_epub.py
python create_kdp_epub.py

# 5. Test in Kindle Previewer (manual step)

# 6. View HTML locally (optional)
node server.js
# Then visit http://localhost:3000

# 7. Print to PDF (in browser)
# Open HTML file, press Ctrl+P, save as PDF
```

---

## Common Issues and Solutions

### Issue: EPUB opens to wrong page
**Solution:** Update `correct_order` list in both create_final_epub.py and create_kdp_epub.py

### Issue: Text not printing in black
**Solution:** Check `.cursorrules_pdf` - ensure all quote classes have `color: #000 !important`

### Issue: Cover image not displaying
**Solution:** Verify cover image path in book_metadata.json and ensure file exists in images/ directory

### Issue: "Item or process id already used"
**Solution:** Scripts automatically handle unique IDs, but check for duplicate image names

### Issue: Table of Contents in wrong position
**Solution:** Ensure "toc" appears before "introduction" in `correct_order` list

---

## Summary

**Files to copy to new project:**
- All cursor rules files (3 files)
- All Python scripts (5-7 files)
- All documentation guides (4 files)
- book_metadata.json (update this)
- server.js and package.json (optional)

**Files requiring metadata updates:**
- book_metadata.json
- create_epub_enhanced.py
- create_final_epub.py
- create_kdp_epub.py
- verify_epub_conversion.py

**What you'll create:**
- HTML files for each chapter/section
- Images directory with all book images
- Cover image file

This setup gives you a complete, proven workflow for creating professional EPUB and PDF files for Amazon publication.




