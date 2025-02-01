import os
from PIL import Image
from tqdm import tqdm

# Define input and output folders
input_folder = r"D:\Picture\playGround\01"   # update to your source folder
output_folder = r"D:\Picture\playGround\02"  # update to your destination folder

# Supported image extensions
image_extensions = ['.png', '.jpg', '.jpeg', '.bmp', '.gif']

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Get list of files in the input folder
files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]

# Filter out files that are already processed or being processed
files = [
    f for f in files 
    if not f.endswith(".PROCESSING") 
    and not f.endswith(".DONE") 
    and not f.endswith(".PROCESSING.png") 
    and not f.endswith(".DONE.png") 
    and not f.endswith(".PROCESSING.jpg") 
    and not f.endswith(".DONE.jpg") 
    and not f.endswith(".PROCESSING.jpeg") 
    and not f.endswith(".DONE.jpeg") 
    and not f.endswith(".PROCESSING.bmp") 
    and not f.endswith(".DONE.bmp") 
    and not f.endswith(".PROCESSING.gif") 
    and not f.endswith(".DONE.gif")
]

# Process each file with a progress bar
for filename in tqdm(files, desc="Processing Images", unit="image"):
    # Extract file name and extension
    name, ext = os.path.splitext(filename)
    
    # Skip unsupported file types
    if ext.lower() not in image_extensions:
        continue
    
    # Define temporary processing file name
    temp_filename = f"{name}-PROCESSING{ext}"
    temp_filepath = os.path.join(input_folder, temp_filename)
    
    # Rename the original file to indicate processing has started
    original_filepath = os.path.join(input_folder, filename)
    os.rename(original_filepath, temp_filepath)
    
    try:
        # Open the image
        with Image.open(temp_filepath) as img:
            # Calculate new dimensions while preserving aspect ratio
            width_percent = 1200 / float(img.width)
            new_height = int(float(img.height) * width_percent)
            
            # Resize the image using LANCZOS filter
            resized_img = img.resize((1200, new_height), Image.LANCZOS)
            
            # Save the resized image to the output folder
            output_filename = f"{name}{ext}"
            output_filepath = os.path.join(output_folder, output_filename)
            resized_img.save(output_filepath, quality=95)
        
        # Rename the temporary file to indicate processing is complete
        done_filepath = os.path.join(input_folder, f"{name}.DONE{ext}")
        os.rename(temp_filepath, done_filepath)
    
    except Exception as e:
        # If an error occurs, revert the temporary file back to its original name
        os.rename(temp_filepath, original_filepath)
        print(f"Error processing {filename}: {e}")

print("All images processed successfully.")