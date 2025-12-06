
import os

# Define the directory to search
target_dir = r"D:\PROGRAMMING\drcil\content\ar\blog"

def fix_svg(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check if the file contains the target string
        if 'x="440"' in content:
            # Replace x="440" with x="360" to move text to the left column (right-aligned to 360)
            # This aligns with the end of the second info box (220 + 140 = 360)
            new_content = content.replace('x="440"', 'x="360"')
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Fixed: {file_path}")
            return True
        else:
            print(f"Skipped (No match): {file_path}")
            return False
            
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    count = 0
    for root, dirs, files in os.walk(target_dir):
        for file in files:
            if file == "featured.svg":
                full_path = os.path.join(root, file)
                if fix_svg(full_path):
                    count += 1
    
    print(f"\nTotal files fixed: {count}")

if __name__ == "__main__":
    main()
