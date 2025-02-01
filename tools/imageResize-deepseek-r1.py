import os
from PIL import Image
from tqdm import tqdm

def process_images(input_folder, output_folder, target_width=1200):
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Collect valid files to process
    allowed_extensions = {'.png', '.jpg', '.jpeg', '.bmp', '.gif'}
    valid_files = []
    
    for filename in os.listdir(input_folder):
        filepath = os.path.join(input_folder, filename)
        if os.path.isfile(filepath):
            name_part, ext_part = os.path.splitext(filename)
            ext_lower = ext_part.lower()
            if ext_lower in allowed_extensions:
                if not (name_part.endswith('-PROCESSING') or name_part.endswith('.DONE')):
                    valid_files.append(filename)
    
    # Process files with progress bar
    for filename in tqdm(valid_files, desc='Processing images'):
        original_path = os.path.join(input_folder, filename)
        name, ext = os.path.splitext(filename)
        processing_filename = f"{name}-PROCESSING{ext}"
        processing_path = os.path.join(input_folder, processing_filename)
        
        try:
            # Rename to processing file
            os.rename(original_path, processing_path)
        except FileNotFoundError:
            continue  # File was moved by another process
        
        processed = False
        
        try:
            with Image.open(processing_path) as img:
                # Calculate new dimensions
                width = target_width
                ratio = width / img.width
                height = int(img.height * ratio)
                
                # Resize and save
                resized_img = img.resize((width, height), Image.LANCZOS)
                output_filename = f"{name}{ext}"
                output_path = os.path.join(output_folder, output_filename)
                
                # Handle transparency for JPEG format
                if ext.lower() in ('.jpg', '.jpeg') and resized_img.mode in ('RGBA', 'LA'):
                    resized_img = resized_img.convert('RGB')
                
                resized_img.save(output_path, optimize=True, quality=85)
            
            processed = True
        except Exception as e:
            print(f"Error processing {processing_path}: {str(e)}")
        finally:
            if processed:
                # Rename to done
                processing_name = os.path.splitext(processing_filename)[0]
                original_name = processing_name.split('-PROCESSING')[0]
                done_filename = f"{original_name}.DONE{ext}"
                done_path = os.path.join(input_folder, done_filename)
                try:
                    os.rename(processing_path, done_path)
                except Exception as e:
                    print(f"Failed to rename to DONE: {str(e)}")
            else:
                # Revert to original filename on failure
                try:
                    os.rename(processing_path, original_path)
                except Exception as e:
                    print(f"Failed to revert filename: {str(e)}")

if __name__ == "__main__":
    input_folder = r"D:\Picture\playGround\01"   # update to your source folder
    output_folder = r"D:\Picture\playGround\02"  # update to your destination folder
    process_images(input_folder, output_folder)