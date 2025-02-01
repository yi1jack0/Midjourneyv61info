import os
from PIL import Image
from tqdm import tqdm

# Define input and output directories and desired new width.
input_folder = r"D:\Picture\playGround\01"   # update to your source folder
output_folder = r"D:\Picture\playGround\02"  # update to your destination folder
new_width = 1200

os.makedirs(output_folder, exist_ok=True)

# Filter valid image files, skipping those that are already being processed or done.
valid_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.gif')
files = [f for f in os.listdir(input_folder)
         if f.lower().endswith(valid_extensions)
         and "-processing." not in f.lower()
         and ".done." not in f.lower()]

for file in tqdm(files, desc="Processing images"):
    original_path = os.path.join(input_folder, file)
    base, ext = os.path.splitext(file)
    
    # Rename the file to mark it as processing.
    processing_name = f"{base}-PROCESSING{ext}"
    processing_path = os.path.join(input_folder, processing_name)
    os.rename(original_path, processing_path)
    
    try:
        with Image.open(processing_path) as img:
            width, height = img.size
            new_height = int(new_width * height / width)
            resized_img = img.resize((new_width, new_height), Image.LANCZOS)
            # Save a copy to the output folder with the original file name.
            output_path = os.path.join(output_folder, file)
            resized_img.save(output_path)
    except Exception as e:
        print(f"Error processing {processing_path}: {e}")
        continue
    
    # Rename the processing file to mark it as done.
    done_name = f"{base}.DONE{ext}"
    done_path = os.path.join(input_folder, done_name)
    os.rename(processing_path, done_path)
