#!/usr/bin/env python3
"""
Fix broken service links in markdown files
- Add language prefix (/en/ or /ar/) to service links
- Redirect to /blog/ if content exists in blog instead of services
"""

import os
import re
from pathlib import Path

def get_available_services_and_blogs(base_dir, lang_code):
    """Get list of available services and blogs for a language"""
    services_dir = Path(base_dir) / 'content' / lang_code / 'services'
    blog_dir = Path(base_dir) / 'content' / lang_code / 'blog'
    
    services = set()
    blogs = set()
    
    if services_dir.exists():
        services = {d.name for d in services_dir.iterdir() if d.is_dir()}
    
    if blog_dir.exists():
        blogs = {d.name for d in blog_dir.iterdir() if d.is_dir()}
    
    return services, blogs

def fix_service_links(content, lang_code, services, blogs):
    """Fix service links by adding language prefix and determining blog vs service"""
    
    # Slug alias mappings for blog posts with different names
    SLUG_ALIASES = {
        'pci': 'percutaneous-coronary-intervention',
        'ptca': 'percutaneous-coronary-intervention',
    }
    
    # Pattern to match [text](/services/slug/) or [text](/services/slug)
    pattern = r'\[([^\]]+)\]\(/services/([^/)]+)/?(\))'
    
    def replace_link(match):
        text = match.group(1)
        slug = match.group(2)
        
        # Check for slug aliases first
        if slug in SLUG_ALIASES:
            slug = SLUG_ALIASES[slug]
        
        # Check if slug exists in services
        if slug in services:
            return f'[{text}](/{lang_code}/services/{slug}/)'
        # Check if slug exists in blog
        elif slug in blogs:
            return f'[{text}](/{lang_code}/blog/{slug}/)'
        # Special case for ambulatory monitoring
        elif slug == 'ambulatory-cardiac-monitoring' and 'ambulatory-blood-pressure-monitoring' in services:
            return f'[{text}](/{lang_code}/services/ambulatory-blood-pressure-monitoring/)'
        else:
            # Keep as is but add language prefix (will be caught in review)
            return f'[{text}](/{lang_code}/services/{slug}/)'
    
    # Replace all service links
    fixed_content = re.sub(pattern, replace_link, content)
    
    return fixed_content

def process_directory(base_dir, lang_code, services, blogs):
    """Process all index.md files in services directory"""
    services_dir = Path(base_dir) / 'content' / lang_code / 'services'
    
    if not services_dir.exists():
        print(f"Directory not found: {services_dir}")
        return 0, 0
    
    fixed_count = 0
    fixed_links = 0
    
    # Find all index.md files
    for index_file in services_dir.rglob('index.md'):
        try:
            with open(index_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Count broken links
            broken_count = len(re.findall(r'\]\(/services/', content))
            
            # Check if file contains /services/ links
            if '/services/' not in content:
                continue
            
            # Fix links
            fixed_content = fix_service_links(content, lang_code, services, blogs)
            
            # Write back if changed
            if fixed_content != content:
                with open(index_file, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)
                print(f"Fixed {broken_count} links in: {index_file.relative_to(base_dir)}")
                fixed_count += 1
                fixed_links += broken_count
        
        except Exception as e:
            print(f"Error processing {index_file}: {e}")
    
    print(f"\n{lang_code.upper()}: Fixed {fixed_links} links in {fixed_count} files")
    return fixed_count, fixed_links

def main():
    base_dir = Path(__file__).parent.parent
    
    print("=" * 60)
    print("Fixing Service Links")
    print("=" * 60)
    
    # Get available services and blogs for each language
    print("\nScanning English content...")
    en_services, en_blogs = get_available_services_and_blogs(base_dir, 'en')
    print(f"Found {len(en_services)} services and {len(en_blogs)} blog posts")
    
    print("\nScanning Arabic content...")
    ar_services, ar_blogs = get_available_services_and_blogs(base_dir, 'ar')
    print(f"Found {len(ar_services)} services and {len(ar_blogs)} blog posts")
    
    print("\nFixing English service links...")
    en_files, en_links = process_directory(base_dir, 'en', en_services, en_blogs)
    
    print("\nFixing Arabic service links...")
    ar_files, ar_links = process_directory(base_dir, 'ar', ar_services, ar_blogs)
    
    print("\n" + "=" * 60)
    print(f"Total: Fixed {en_links + ar_links} links in {en_files + ar_files} files")
    print("=" * 60)

if __name__ == '__main__':
    main()
