
import os
import re

# Define the directory to search
target_dir = r"D:\PROGRAMMING\drcil\content\ar\blog"

def fix_svg_content(content, file_path):
    modified = False
    
    # Analyze text position
    # Find x value of the first text tag (Title)
    text_match = re.search(r'<text[^>]+x="(\d+)"', content)
    if not text_match:
        return content, False
        
    text_x = int(text_match.group(1))
    
    # Analyze Image position (Heart group)
    # Look for the group with heart path or just the first major group transform
    # Usually lines 22-23: <g transform="translate(X, Y)">
    # We'll look for translate(X, Y)
    
    # Heuristic:
    # Type B: Text X > 600 (e.g., 740). Image X < 200 (e.g., 120). Boxes X > 400.
    # Type A/C: Text X around 400-550 (e.g., 440, 490). Image X > 400 (e.g., 480, 550). Boxes X < 300.
    
    if text_x > 600:
        print(f"Detected Type B (Full Mirror) in {file_path} (Text X={text_x})")
        
        # 1. Move Text to 360
        content = re.sub(r'x="\d+"', 'x="360"', content)
        
        # 2. Move Image from Left to Right
        # Find translate(120, ...) or similar small number
        # We need to be careful not to mess up other translates.
        # Usually Image is the first group with translate?
        # Let's inspect known Type B image positions: translate(120, 50)
        content = re.sub(r'transform="translate\(\s*120\s*,\s*50\s*\)"', 'transform="translate(480, 50)"', content)
        content = re.sub(r'transform="translate\(\s*120\s*,\s*(\d+)\s*\)"', 'transform="translate(480, \1)"', content) # Generic Y

        # 3. Move Info Boxes from Right to Left
        # Box 1: 610 -> 60
        content = re.sub(r'transform="translate\(\s*610\s*,\s*200\s*\)"', 'transform="translate(60, 200)"', content)
        
        # Box 2: 460 -> 220
        content = re.sub(r'transform="translate\(\s*460\s*,\s*200\s*\)"', 'transform="translate(220, 200)"', content)
        
        modified = True
        
    elif 400 <= text_x <= 550:
        print(f"Detected Type A/C (Text Adjustment) in {file_path} (Text X={text_x})")
        
        # Move all text X to 360
        # Be careful not to change other attributes if they strictly match regex
        content = re.sub(r'x="' + str(text_x) + r'"', 'x="360"', content)
        
        # Also check just in case secondary text has different X (usually same)
        # We can just replace all text X in that range
        
        modified = True
        
    elif text_x == 360:
         # Already fixed
         return content, False
    else:
        print(f"Skipped {file_path}: Text X={text_x} (Unexpected)")
        
    return content, modified

def main():
    count = 0
    skipped = 0
    
    for root, dirs, files in os.walk(target_dir):
        for file in files:
            if file == "featured.svg":
                full_path = os.path.join(root, file)
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    new_content, was_modified = fix_svg_content(content, full_path)
                    
                    if was_modified:
                        with open(full_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        count += 1
                    else:
                         pass
                            
                except Exception as e:
                    print(f"Error processing {file}: {e}")

    print(f"\nTotal files updated this run: {count}")

if __name__ == "__main__":
    main()
