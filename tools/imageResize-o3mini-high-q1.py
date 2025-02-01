## from o3-mini-high
import os
import argparse
import time
import shutil
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
        if any(tag in filename for tag in ["-PROCESSING-", "-DONE-", "-FAILED-"]):
            continue
        valid_files.append(filename)

    for filename in tqdm(valid_files, desc="Processing images"):
        original_path = os.path.join(input_folder, filename)
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        base, ext = os.path.splitext(filename)
        
        # Create a temporary copy of the original file.
        tmp_path = os.path.join(input_folder, filename + ".tmp")
        try:
            shutil.copy2(original_path, tmp_path)
        except Exception as e:
            print(f"Error copying file {filename} to tmp: {e}")
            continue
        
        # Rename the tmp file to include the PROCESSING tag.
        processing_filename = f"{base}-PROCESSING-{timestamp}{ext}"
        processing_path = os.path.join(input_folder, processing_filename)
        try:
            os.rename(tmp_path, processing_path)
        except Exception as e:
            print(f"Error renaming tmp file for {filename}: {e}")
            continue

        resize_success = False
        try:
            with Image.open(processing_path) as img:
                width = 1200
                original_width, original_height = img.size
                if original_width != width:
                    ratio = width / original_width
                    new_height = int(original_height * ratio)
                    resized_img = img.resize((width, new_height), Image.LANCZOS)
                else:
                    resized_img = img.copy()
            # At this point, the Image object is closed; save the resized image.
            resized_img.save(processing_path, quality=95, optimize=True)
            resize_success = True
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            resize_success = False

        # Set tag and subfolder name based on the resize result.
        if resize_success:
            new_tag = "DONE"
            subfolder = "done"
        else:
            new_tag = "FAILED"
            subfolder = "failed"
        new_filename = f"{base}-{new_tag}-{timestamp}{ext}"
        new_processing_path = os.path.join(output_folder, new_filename)
        try:
            os.rename(processing_path, new_processing_path)
        except Exception as e:
            print(f"Error moving processed file {filename} to output: {e}")
            continue

        # Create the destination subfolder inside the input folder and move the original file.
        dest_folder = os.path.join(input_folder, subfolder)
        os.makedirs(dest_folder, exist_ok=True)
        dest_original_path = os.path.join(dest_folder, filename)
        try:
            os.rename(original_path, dest_original_path)
        except Exception as e:
            print(f"Error moving original file {filename} to {subfolder} folder: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Resize images to 1200px width while preserving aspect ratio.')
    parser.add_argument('input_folder', help='Path to the input folder containing images')
    parser.add_argument('output_folder', help='Path to the output folder for resized images')
    args = parser.parse_args()

    if not os.path.exists(args.input_folder):
        print(f"Error: Input folder '{args.input_folder}' does not exist.")
        exit(1)

    process_images(args.input_folder, args.output_folder)
