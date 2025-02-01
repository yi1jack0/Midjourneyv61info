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
        
        if '-PROCESSING-' in filename or '-DONE-' in filename:
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

        try:
            with Image.open(processing_path) as img:
                width = 1200
                original_width, original_height = img.size
                if original_width != width:
                    ratio = width / original_width
                    new_height = int(original_height * ratio)
                    img = img.resize((width, new_height), Image.LANCZOS)
                
                # Create output filename with timestamp
                output_filename = processing_filename.replace("-PROCESSING-", "-")
                output_path = os.path.join(output_folder, output_filename)
                img.save(output_path, quality=95, optimize=True)
        except Exception as e:
            print(f"\nError processing {filename}: {str(e)}")
            continue
        finally:
            # Create DONE filename
            done_filename = processing_filename.replace("-PROCESSING-", "-DONE-")
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