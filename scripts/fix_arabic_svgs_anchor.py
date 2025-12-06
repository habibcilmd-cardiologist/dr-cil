
import os
import re

# Define the directory to search
target_dir = r"D:\PROGRAMMING\drcil\content\ar\blog"

def fix_svg_anchor(content, file_path):
    modified = False
    
    # We want to change text-anchor="end" to text-anchor="start" ONLY for the main title/desc text
    # The main text was moved to x="360" in the previous step.
    # So we look for <text ... x="360" ... text-anchor="end" ...>
    
    # Regex to find text tag with x="360" and text-anchor="end"
    # Note: Attributes order can vary.
    
    # Find all text tags
    def replace_anchor(match):
        tag = match.group(0)
        if 'x="360"' in tag and 'text-anchor="end"' in tag:
            print(f"Fixing anchor in {file_path}")
            # Change anchor to start (for RTL this aligns right edge to X)
            new_tag = tag.replace('text-anchor="end"', 'text-anchor="start"')
            # Also move x slightly to 340 to provide padding from the center line? 
            # 360 is the theoretical max, but 350 is safer.
            new_tag = new_tag.replace('x="360"', 'x="350"')
            return new_tag
        return tag

    new_content = re.sub(r'<text[^>]+>', replace_anchor, content)
    
    if new_content != content:
        modified = True
        
    return new_content, modified

def main():
    count = 0
    
    for root, dirs, files in os.walk(target_dir):
        for file in files:
            if file == "featured.svg":
                full_path = os.path.join(root, file)
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    new_content, was_modified = fix_svg_anchor(content, full_path)
                    
                    if was_modified:
                        with open(full_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        count += 1
                            
                except Exception as e:
                    print(f"Error processing {file}: {e}")

    print(f"\nTotal files updated this run: {count}")

if __name__ == "__main__":
    main()
