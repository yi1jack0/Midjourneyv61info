# from qwen 2.5 max
import os
import time
from PIL import Image
from tqdm import tqdm

# Supported image extensions
SUPPORTED_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.bmp', '.gif'}

def process_images(input_folder, output_folder):
    # Create necessary folders
    os.makedirs(output_folder, exist_ok=True)
    done_folder = os.path.join(input_folder, 'done')
    failed_folder = os.path.join(input_folder, 'failed')
    os.makedirs(done_folder, exist_ok=True)
    os.makedirs(failed_folder, exist_ok=True)
    
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
        
        # Create a temporary lock file
        lock_filename = f"{name}-PROCESSING-{timestamp}{ext}"
        lock_path = os.path.join(input_folder, lock_filename)
        
        try:
            # Create lock file
            open(lock_path, 'w').close()
            
            # Open the image using Pillow
            with Image.open(original_path) as img:
                width, height = img.size
                
                # Only resize if width is outside the range 1150-1250
                if not (1150 <= width <= 1250):
                    new_width = 1200
                    new_height = int((new_width / width) * height)
                    
                    # Resize the image using LANCZOS filter
                    resized_img = img.resize((new_width, new_height), Image.LANCZOS)
                    
                    # Save the resized image to the output folder with a timestamp
                    output_filename = f"{name}-DONE-{timestamp}{ext}"  # Include timestamp in output filename
                    output_path = os.path.join(output_folder, output_filename)
                    resized_img.save(output_path, quality=95)
                
                # Move the original file to the done folder
                done_path = os.path.join(done_folder, filename)
                
                # Retry logic to handle file access issues
                retries = 3
                for _ in range(retries):
                    try:
                        os.rename(original_path, done_path)
                        break  # Exit retry loop if successful
                    except PermissionError:
                        time.sleep(0.1)  # Wait briefly before retrying
            
        except Exception as e:
            # If an error occurs, move the file to the failed folder
            failed_path = os.path.join(failed_folder, filename)
            
            # Retry logic to handle file access issues
            retries = 3
            for _ in range(retries):
                try:
                    os.rename(original_path, failed_path)
                    break  # Exit retry loop if successful
                except PermissionError:
                    time.sleep(0.1)  # Wait briefly before retrying
            
            print(f"Error processing {filename}: {e}")
        
        finally:
            # Remove the lock file
            if os.path.exists(lock_path):
                os.remove(lock_path)

if __name__ == "__main__":
    # Specify the input and output folders
    input_folder = r"D:\Picture\playGround\01"   # update to your source folder
    output_folder = r"D:\Picture\playGround\02"  # update to your destination folder
    
    # Call the function to process images
    process_images(input_folder, output_folder)