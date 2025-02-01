import os
import argparse
import time
from PIL import Image
from tqdm import tqdm

ALLOWED_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.bmp', '.gif'}

def process_images(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    if os.path.abspath(input_folder) == os.path.abspath(output_folder):
        print("Error: Input and output folders must be different.")
        return

    valid_files = []
    for filename in os.listdir(input_folder):
        file_path = os.path.join(input_folder, filename)
        if not os.path.isfile(file_path):
            continue
        
        ext = os.path.splitext(filename)[1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            continue
        
        if any(x in filename for x in ['-PROCESSING-', '-DONE-']):
            continue
        
        valid_files.append(filename)

    for filename in tqdm(valid_files, desc="Processing images"):
        original_path = os.path.join(input_folder, filename)
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        base, ext = os.path.splitext(filename)
        
        # Create processing filename
        processing_filename = f"{base}-PROCESSING-{timestamp}{ext}"
        processing_path = os.path.join(input_folder, processing_filename)
        
        try:
            os.rename(original_path, processing_path)
        except FileNotFoundError:
            continue

        output_filename = f"{base}-{timestamp}{ext}"  # Maintain original filename for output
        output_path = os.path.join(output_folder, output_filename)

        try:
            with Image.open(processing_path) as img:
                if img.width != 1200:
                    ratio = 1200 / img.width
                    new_height = int(img.height * ratio)
                    img = img.resize((1200, new_height), Image.LANCZOS)
                
                # Save with original filename to output folder
                img.save(output_path, quality=95, optimize=True)
                
        except Exception as e:
            print(f"\nError processing {filename}: {str(e)}")
            continue
        finally:
            # Rename to DONE even if processing failed
            done_filename = f"{base}-DONE-{timestamp}{ext}"
            done_path = os.path.join(input_folder, done_filename)
            if os.path.exists(processing_path):
                os.rename(processing_path, done_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Resize images to 1200px width while preserving aspect ratio.')
    parser.add_argument('input_folder', help='Path to the input folder containing images')
    parser.add_argument('output_folder', help='Path to the output folder for resized images')
    args = parser.parse_args()

    if not os.path.exists(args.input_folder):
        print(f"Error: Input folder '{args.input_folder}' does not exist.")
        exit(1)

    process_images(args.input_folder, args.output_folder)