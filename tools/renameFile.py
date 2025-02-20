import os
from datetime import datetime

def rename_png_files(folder_path):
    # Get today's date in ddmmyyyy format
    today_date = datetime.now().strftime("%d%m%Y")
    
    # List all files in the folder
    files = os.listdir(folder_path)
    
    # Filter only .png files
    png_files = [f for f in files if f.lower().endswith('.png')]
    
    # Sort the files to ensure consistent ordering
    png_files.sort()
    
    # Initialize the counter
    counter = 1
    
    for png_file in png_files:
        # Extract the first 10 characters from the original file name (without extension)
        original_name = os.path.splitext(png_file)[0]
        name_prefix = original_name[:10]
        
        # Format the counter with leading zeros (e.g., 001, 002, ...)
        counter_str = f"{counter:03d}"
        
        # Create the new file name
        new_file_name = f"{name_prefix}_{counter_str}_{today_date}.png"
        
        # Get full paths for the old and new file names
        old_file_path = os.path.join(folder_path, png_file)
        new_file_path = os.path.join(folder_path, new_file_name)
        
        # Rename the file
        os.rename(old_file_path, new_file_path)
        
        print(f"Renamed '{png_file}' to '{new_file_name}'")
        
        # Increment the counter
        counter += 1

# Example usage
folder_path = r"D:\Picture\playGround\0018"  # Replace this with the path to your folder
rename_png_files(folder_path)