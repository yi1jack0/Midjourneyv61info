#!/usr/bin/env python3
"""
Script to process all image files in an input folder:
  - Only processes files with extensions: .png, .jpg, .jpeg, .bmp, and .gif.
  - Skips files already “marked” as processing or done (i.e. filenames ending with
    -PROCESSING-{timestamp} or -DONE-{timestamp}).
  - For each image:
      1. Renames the file by appending "-PROCESSING-{timestamp}" before processing.
      2. Resizes the image to a width of 1200 pixels (preserving aspect ratio)
         using Pillow’s high-quality LANCZOS filter.
      3. Saves a copy of the resized image into the output folder with the
         "-PROCESSING-" part removed (i.e. {original name}-{timestamp}.{ext}).
      4. Renames the original file (in the input folder) to have "-DONE-{timestamp}".
  - Displays a progress bar using tqdm.
"""

import os
import re
import datetime
import argparse
from PIL import Image
from tqdm import tqdm

# Allowed image extensions
ALLOWED_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.bmp', '.gif'}

def is_image_file(filename):
    """Return True if the file has an allowed image extension and is not already processed."""
    base, ext = os.path.splitext(filename)
    if ext.lower() not in ALLOWED_EXTENSIONS:
        return False
    # Skip files that already have the -PROCESSING- or -DONE- pattern at the end of the base name.
    if re.search(r"-(PROCESSING|DONE)-\d{14}$", base):
        return False
    return True

def resize_image(input_path, output_path, target_width=1200):
    """
    Opens an image from input_path, resizes it to target_width while preserving the
    aspect ratio, and saves it to output_path using a high-quality LANCZOS filter.
    """
    with Image.open(input_path) as img:
        orig_width, orig_height = img.size
        # Calculate new dimensions
        new_width = target_width
        new_height = int(orig_height * new_width / orig_width)
        # Resize using LANCZOS for high quality
        img_resized = img.resize((new_width, new_height), Image.LANCZOS)
        img_resized.save(output_path)

def process_images(input_folder, output_folder):
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # List all files in the input folder and filter by image files
    all_files = os.listdir(input_folder)
    image_files = [f for f in all_files if os.path.isfile(os.path.join(input_folder, f)) and is_image_file(f)]

    for filename in tqdm(image_files, desc="Processing images"):
        # Full path for the original file
        original_path = os.path.join(input_folder, filename)
        name_without_ext, ext = os.path.splitext(filename)
        # Generate a timestamp string (e.g. 20250201123045)
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

        # Build the new processing filename and full path
        processing_filename = f"{name_without_ext}-PROCESSING-{timestamp}{ext}"
        processing_path = os.path.join(input_folder, processing_filename)
        
        # Rename original file to mark as "processing"
        os.rename(original_path, processing_path)

        try:
            # Build the output filename by removing the "-PROCESSING-" part.
            # The output file will be: {original name}-{timestamp}.{extension}
            output_filename = f"{name_without_ext}-{timestamp}{ext}"
            output_path = os.path.join(output_folder, output_filename)
            
            # Resize the image and save the result in the output folder
            resize_image(processing_path, output_path, target_width=1200)
        except Exception as e:
            print(f"Error processing {processing_path}: {e}")
            continue

        # Rename the processed file to mark it as done.
        done_filename = f"{name_without_ext}-DONE-{timestamp}{ext}"
        done_path = os.path.join(input_folder, done_filename)
        os.rename(processing_path, done_path)

def main():
    parser = argparse.ArgumentParser(
        description="Resize images in a folder to a width of 1200px (preserving aspect ratio)."
    )
    parser.add_argument("input_folder", type=str, help="Path to the input folder containing images.")
    parser.add_argument("output_folder", type=str, help="Path to the output folder for resized images.")
    args = parser.parse_args()

    process_images(args.input_folder, args.output_folder)

if __name__ == "__main__":
    main()
