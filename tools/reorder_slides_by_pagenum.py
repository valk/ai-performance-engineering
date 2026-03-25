import os
import re
import subprocess
import tempfile
import sys
from PIL import Image

def get_slide_number(image_path):
    """
    Extract the slide number from the bottom right corner of the image using OCR.
    """
    try:
        img = Image.open(image_path)
        w, h = img.size
        
        # Generous bottom-right crop to ensure we catch most varied slide numbers
        crop_w, crop_h = int(w * 0.25), int(h * 0.2)
        crop_left = w - crop_w
        crop_top = h - crop_h
        crop = img.crop((crop_left, crop_top, w, h))
        
        with tempfile.NamedTemporaryFile(suffix='.png', delete=True) as tmp:
            # 2x upscale is often optimal for Tesseract
            crop = crop.resize((crop.width * 2, crop.height * 2), Image.Resampling.LANCZOS)
            crop.save(tmp.name)
            
            # Use TSV output to get positional data
            cmd = ['tesseract', tmp.name, 'stdout', '--psm', '6', 'tsv']
            output = subprocess.check_output(cmd, stderr=subprocess.DEVNULL).decode('utf-8').strip()
            
            lines = [line.split('\t') for line in output.split('\n')]
            if len(lines) < 2: return None
            
            header = lines[0]
            try:
                text_idx = header.index('text')
                left_idx = header.index('left')
                top_idx = header.index('top')
            except ValueError: return None
            
            candidates = []
            for line in lines[1:]:
                if len(line) <= text_idx: continue
                text = line[text_idx].strip()
                if not text: continue
                
                # Extract all numbers from the found text element
                numbers = re.findall(r'\d+', text)
                if not numbers: continue
                
                # Weigh by how close to the bottom right they are
                left = int(line[left_idx])
                top = int(line[top_idx])
                score = (left / (crop_w * 2)) + (top / (crop_h * 2))
                
                # We prioritize numbers that look like page numbers (usually 1-3 digits)
                for num in numbers:
                    if 1 <= int(num) <= 999:
                        candidates.append((score, num))
            
            if candidates:
                # Pick the one with the best (highest) score for bottom-right position
                candidates.sort(key=lambda x: x[0], reverse=True)
                return candidates[0][1]
                    
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
    return None

def main(directory):
    if not os.path.exists(directory):
        print(f"Error: Directory '{directory}' not found.")
        return

    files = [f for f in os.listdir(directory) if f.lower().endswith('.jpg') or f.lower().endswith('.jpeg')]
    files.sort()

    renames = []
    print(f"Scanning {len(files)} files in '{directory}'...")
    
    for f in files:
        full_path = os.path.join(directory, f)
        num = get_slide_number(full_path)
        
        if num:
            new_name = f"slide_{num}.jpg"
            if f == new_name:
                continue
            renames.append((f, new_name))
            print(f"Detected: {f} -> {new_name}")
        else:
            print(f"No slide number found for: {f}")

    if not renames:
        print("No files to rename.")
        return

    print(f"\nCollected {len(renames)} renames.")
    confirm = input("Proceed? (y/n/i for interaction): ")
    if confirm.lower() == 'n':
        return

    interactive = confirm.lower() == 'i'
    
    temp_dir = os.path.join(directory, "temp_renaming")
    os.makedirs(temp_dir, exist_ok=True)

    for old_name, new_name in renames:
        if interactive:
            resp = input(f"Rename {old_name} to {new_name}? (y/n/skip): ").lower()
            if resp != 'y': continue
            
        try:
            os.rename(os.path.join(directory, old_name), os.path.join(temp_dir, new_name))
        except Exception as e:
            print(f"Error renaming {old_name}: {e}")

    for new_name in os.listdir(temp_dir):
        try:
            os.rename(os.path.join(temp_dir, new_name), os.path.join(directory, new_name))
        except Exception as e:
            print(f"Error moving back {new_name}: {e}")

    os.rmdir(temp_dir)
    print("Completed.")

if __name__ == "__main__":
    target_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    main(target_dir)
