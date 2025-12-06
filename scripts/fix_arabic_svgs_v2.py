
import os
import re

# Define the directory to search
target_dir = r"D:\PROGRAMMING\drcil\content\ar\blog"

def fix_svg_content(content, file_path):
    modified = False
    
    # Strategy 1: "Type A" - Text at 440 (Center-Right), Image at 480 (Right), Boxes Left.
    # Fix: Move Text to 360 (Left).
    if 'x="440"' in content:
        print(f"Applying Type A fix to {file_path}")
        content = content.replace('x="440"', 'x="360"')
        modified = True
        
    # Strategy 2: "Type B" - Text at 740 (Right), Image at 120 (Left), Boxes Right.
    # Fix: Mirror everything to Standard (Text Left, Image Right).
    # Text: 740 -> 360
    # Image: translate(120, 50) -> translate(480, 50)
    # Box 1: translate(610, 200) -> translate(60, 200)
    # Box 2: translate(460, 200) -> translate(220, 200)
    elif 'x="740"' in content:
        print(f"Applying Type B fix to {file_path}")
        content = content.replace('x="740"', 'x="360"')
        content = content.replace('translate(120, 50)', 'translate(480, 50)')
        
        # Note: box positions might be swapped in reading order. 
        # In Type B (Aortic): Box 1 (Early Detection) is at 610 (Rightmost). Box 2 (Modern Treatment) is at 460.
        # We move Box 1 (610) -> 60 (Leftmost).
        # We move Box 2 (460) -> 220 (Mid-Left).
        content = content.replace('translate(610, 200)', 'translate(60, 200)')
        content = content.replace('translate(460, 200)', 'translate(220, 200)')
        modified = True

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
                        # Check if it was already fixed (has x="360")
                        if 'x="360"' in content:
                             pass # Already fixed
                        else:
                            print(f"Skipped (Unknown Layout): {file}")
                            skipped += 1
                            
                except Exception as e:
                    print(f"Error processing {file}: {e}")

    print(f"\nTotal files updated this run: {count}")
    print(f"Total skipped (unknown layout): {skipped}")

if __name__ == "__main__":
    main()
