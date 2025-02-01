import os
import time
from PIL import Image
from tqdm import tqdm

# Supported image extensions
SUPPORTED_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.bmp', '.gif'}

def process_images(input_folder, output_folder):
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Get all files in the input folder
    all_files = os.listdir(input_folder)
    
    # Filter out only supported image files
    image_files = [f for f in all_files if os.path.splitext(f)[1].lower() in SUPPORTED_EXTENSIONS]

    # Exclude files with "-PROCESSING-" or "-DONE-" in their names
    image_files = [f for f in image_files if '-PROCESSING-' not in f and '-DONE-' not in f]

    # Process each image file with a progress bar
    for filename in tqdm(image_files, desc="Processing Images", unit="image"):
        original_path = os.path.join(input_folder, filename)
        name, ext = os.path.splitext(filename)
        timestamp = int(time.time())
        
        # Rename the file to indicate processing has started
        processing_filename = f"{name}-PROCESSING-{timestamp}{ext}"
        processing_path = os.path.join(input_folder, processing_filename)
        os.rename(original_path, processing_path)

        try:
            # Open the image using Pillow
            with Image.open(processing_path) as img:
                # Calculate new dimensions while preserving aspect ratio
                width, height = img.size
                new_width = 1200
                new_height = int((new_width / width) * height)

                # Resize the image using LANCZOS filter
                resized_img = img.resize((new_width, new_height), Image.LANCZOS)

                # Save the resized image to the output folder with a timestamp
                output_filename = f"{name}-{timestamp}{ext}"  # Include timestamp in output filename
                output_path = os.path.join(output_folder, output_filename)
                resized_img.save(output_path, quality=95)

            # Rename the processing file to indicate completion
            done_filename = f"{name}-DONE-{timestamp}{ext}"
            done_path = os.path.join(input_folder, done_filename)
            os.rename(processing_path, done_path)

        except Exception as e:
            # If an error occurs, revert the filename back to its original name
            os.rename(processing_path, original_path)
            print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    # Specify the input and output folders
    input_folder = r"D:\Picture\playGround\01"   # update to your source folder
    output_folder = r"D:\Picture\playGround\02"  # update to your destination folder

    # Call the function to process images
    process_images(input_folder, output_folder)