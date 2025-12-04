#!/usr/bin/env python3
"""
FAQ Migration Script
Migrates FAQ shortcodes from markdown content to front matter YAML format.

Usage:
    python scripts/migrate_faq.py [--dry-run] [--file PATH]
    
Options:
    --dry-run   Preview changes without modifying files
    --file PATH Process only a specific file
"""

import re
import os
import sys
import argparse
import shutil
from pathlib import Path
from datetime import datetime

# Regex pattern to match FAQ shortcodes
FAQ_PATTERN = re.compile(
    r'\{\{<\s*faq\s+question="([^"]+)"\s*>\}\}\s*(.*?)\s*\{\{<\s*/faq\s*>\}\}',
    re.DOTALL
)

# Pattern to find the end of front matter
FRONTMATTER_END_PATTERN = re.compile(r'^---\s*$', re.MULTILINE)


def extract_faqs(content: str) -> list[dict]:
    """Extract FAQ question-answer pairs from content."""
    faqs = []
    for match in FAQ_PATTERN.finditer(content):
        question = match.group(1).strip()
        answer = match.group(2).strip()
        # Clean up answer - remove extra whitespace
        answer = ' '.join(answer.split())
        faqs.append({'question': question, 'answer': answer})
    return faqs


def escape_yaml_string(s: str) -> str:
    """Escape special characters for YAML string."""
    # Replace double quotes with escaped quotes
    s = s.replace('"', '\\"')
    return s


def generate_faq_yaml(faqs: list[dict]) -> str:
    """Generate YAML block for FAQ data."""
    if not faqs:
        return ""
    
    lines = ["faq:"]
    for faq in faqs:
        q = escape_yaml_string(faq['question'])
        a = escape_yaml_string(faq['answer'])
        lines.append(f'    - question: "{q}"')
        lines.append(f'      answer: "{a}"')
    return '\n'.join(lines)


def remove_faq_shortcodes(content: str) -> str:
    """Remove all FAQ shortcodes and replace with faq-list shortcode."""
    # Find the section containing FAQs
    lines = content.split('\n')
    new_lines = []
    in_faq_section = False
    faq_section_replaced = False
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Check if this line starts a FAQ shortcode
        if '{{< faq question=' in line or '{{<faq question=' in line:
            if not faq_section_replaced:
                # Add the faq-list shortcode only once
                new_lines.append('{{< faq-list >}}')
                new_lines.append('')
                faq_section_replaced = True
            
            # Skip until we find the closing tag
            while i < len(lines) and '{{< /faq >}}' not in lines[i] and '{{</faq>}}' not in lines[i]:
                i += 1
            i += 1  # Skip the closing tag line
            
            # Skip any empty lines after the FAQ
            while i < len(lines) and lines[i].strip() == '':
                i += 1
        else:
            new_lines.append(line)
            i += 1
    
    return '\n'.join(new_lines)


def add_faq_to_frontmatter(content: str, faq_yaml: str) -> str:
    """Add FAQ YAML to the front matter."""
    if not faq_yaml:
        return content
    
    # Find the second --- that closes the front matter
    matches = list(FRONTMATTER_END_PATTERN.finditer(content))
    if len(matches) < 2:
        print("Warning: Could not find front matter boundaries")
        return content
    
    # Insert FAQ YAML before the closing ---
    end_pos = matches[1].start()
    return content[:end_pos] + faq_yaml + '\n' + content[end_pos:]


def process_file(filepath: Path, dry_run: bool = False) -> tuple[bool, int]:
    """
    Process a single markdown file.
    Returns (success, num_faqs_migrated)
    """
    try:
        content = filepath.read_text(encoding='utf-8')
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return False, 0
    
    # Extract FAQs
    faqs = extract_faqs(content)
    if not faqs:
        return True, 0  # No FAQs to migrate
    
    print(f"\n[FILE] {filepath}")
    print(f"   Found {len(faqs)} FAQ(s)")
    
    # Generate YAML
    faq_yaml = generate_faq_yaml(faqs)
    
    # Add to front matter
    new_content = add_faq_to_frontmatter(content, faq_yaml)
    
    # Remove old shortcodes
    new_content = remove_faq_shortcodes(new_content)
    
    if dry_run:
        print(f"   [DRY RUN] Would migrate {len(faqs)} FAQs")
        for faq in faqs[:2]:  # Show first 2 questions
            print(f"      - {faq['question'][:50]}...")
        if len(faqs) > 2:
            print(f"      ... and {len(faqs) - 2} more")
    else:
        # Create backup
        backup_path = filepath.with_suffix('.md.bak')
        shutil.copy2(filepath, backup_path)
        
        # Write new content
        filepath.write_text(new_content, encoding='utf-8')
        print(f"   [OK] Migrated {len(faqs)} FAQs (backup: {backup_path.name})")
    
    return True, len(faqs)


def main():
    parser = argparse.ArgumentParser(description='Migrate FAQ shortcodes to front matter')
    parser.add_argument('--dry-run', action='store_true', help='Preview changes without modifying')
    parser.add_argument('--file', type=str, help='Process only a specific file')
    parser.add_argument('--no-backup', action='store_true', help='Skip creating backup files')
    args = parser.parse_args()
    
    # Determine root directory
    script_dir = Path(__file__).parent
    root_dir = script_dir.parent
    
    print("=" * 60)
    print("FAQ Migration Script")
    print("=" * 60)

    if args.dry_run:
        print("[DRY RUN MODE] No files will be modified\n")
    
    # Collect files to process
    if args.file:
        files = [Path(args.file)]
    else:
        # Process all content directories
        content_dirs = [
            root_dir / 'content' / 'tr' / 'blog',
            root_dir / 'content' / 'en' / 'blog',
            root_dir / 'content' / 'tr' / 'hizmetler',
            root_dir / 'content' / 'en' / 'services',
        ]
        
        files = []
        for dir_path in content_dirs:
            if dir_path.exists():
                files.extend(dir_path.rglob('*.md'))
    
    # Process files
    total_files = 0
    total_faqs = 0
    errors = 0
    
    for filepath in sorted(files):
        success, num_faqs = process_file(filepath, args.dry_run)
        if success and num_faqs > 0:
            total_files += 1
            total_faqs += num_faqs
        elif not success:
            errors += 1
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Files processed: {total_files}")
    print(f"FAQs migrated: {total_faqs}")
    if errors:
        print(f"Errors: {errors}")
    
    if args.dry_run:
        print("\n[TIP] Run without --dry-run to apply changes")


if __name__ == '__main__':
    main()

