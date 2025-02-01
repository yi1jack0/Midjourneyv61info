# from deepseek r1
import os
import time
import shutil
import tempfile
from PIL import Image
from tqdm import tqdm

SUPPORTED_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.bmp', '.gif'}

def process_images(input_folder, output_folder):
    # Create required directories
    os.makedirs(output_folder, exist_ok=True)
    done_folder = os.path.join(input_folder, 'done')
    failed_folder = os.path.join(input_folder, 'failed')
    os.makedirs(done_folder, exist_ok=True)
    os.makedirs(failed_folder, exist_ok=True)

    # Identify files already being processed or completed
    all_files = os.listdir(input_folder)
    processing_files = set()
    for f in all_files:
        if '-PROCESSING-' in f or '-DONE-' in f:
            base_part = f.split('-PROCESSING-')[0].split('-DONE-')[0]
            original_name = f"{base_part}{os.path.splitext(f)[1]}"
            processing_files.add(original_name)

    # Filter valid files (supported extensions and not in processing)
    valid_files = [
        f for f in all_files
        if os.path.splitext(f)[1].lower() in SUPPORTED_EXTENSIONS
        and f not in processing_files
    ]

    # Process files with progress tracking
    for filename in tqdm(valid_files, desc="Processing Images", unit="image"):
        original_path = os.path.join(input_folder, filename)
        base_name, ext = os.path.splitext(filename)
        timestamp = int(time.time())
        
        # Create processing lock file
        processing_filename = f"{base_name}-PROCESSING-{timestamp}{ext}"
        processing_path = os.path.join(input_folder, processing_filename)
        try:
            open(processing_path, 'w').close()
        except:
            continue  # Skip if lock creation fails

        temp_path = None
        try:
            # Copy original to temp file
            with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as temp_file:
                temp_path = temp_file.name
                with open(original_path, 'rb') as src:
                    temp_file.write(src.read())

            # Process image
            try:
                with Image.open(temp_path) as img:
                    width, height = img.size
                    # Resize only if within specified width range
                    if 1150 <= width <= 1250:
                        new_width = 1200
                        new_height = int((new_width / width) * height)
                        img = img.resize((new_width, new_height), Image.LANCZOS)
                    
                    # Save processed image
                    output_filename = f"{base_name}-DONE-{timestamp}{ext}"
                    output_path = os.path.join(output_folder, output_filename)
                    img.save(output_path, quality=95)
                
                # Move original to done folder
                shutil.move(original_path, os.path.join(done_folder, filename))

            except Exception as e:
                # Create failed marker and move original
                output_filename = f"{base_name}-FAILED-{timestamp}{ext}"
                output_path = os.path.join(output_folder, output_filename)
                open(output_path, 'w').close()
                shutil.move(original_path, os.path.join(failed_folder, filename))
                print(f"Error processing {filename}: {str(e)}")

        finally:
            # Cleanup temporary and lock files
            if temp_path and os.path.exists(temp_path):
                os.remove(temp_path)
            if os.path.exists(processing_path):
                os.remove(processing_path)

if __name__ == "__main__":
    input_folder = r"D:\Picture\playGround\01"
    output_folder = r"D:\Picture\playGround\02"
    process_images(input_folder, output_folder)