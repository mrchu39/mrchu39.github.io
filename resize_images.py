import os, shutil
from PIL import Image

# Disable the decompression bomb safety limit for massive images
Image.MAX_IMAGE_PIXELS = None

def batch_resize_longest_edge(input_folder, output_folder, max_dimension=2000, quality=85):
    # Create the output folder if it doesn't exist
    shutil.rmtree(output_folder, ignore_errors=True)
    os.makedirs(output_folder, exist_ok=True)

    # Loop through all files in the input folder
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(input_folder, filename)
            
            try:
                with Image.open(img_path) as img:
                    current_width, current_height = img.size
                    
                    # Find the longest edge
                    longest_edge = max(current_width, current_height)
                    
                    # Only resize if the image is actually larger than our target
                    if longest_edge > max_dimension:
                        # Calculate the ratio to shrink by
                        ratio = max_dimension / float(longest_edge)
                        
                        new_width = int(current_width * ratio)
                        new_height = int(current_height * ratio)
                        
                        resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    else:
                        # If it's already small enough, just process it as is
                        resized_img = img
                        new_width, new_height = current_width, current_height

                    # Save the optimized image to the output folder
                    output_path = os.path.join(output_folder, filename)
                    
                    if filename.lower().endswith('.png'):
                         resized_img.save(output_path, optimize=True)
                    else:
                         # Convert to RGB to prevent errors with some JPEGs
                         if resized_img.mode in ("RGBA", "P"):
                             resized_img = resized_img.convert("RGB")
                         resized_img.save(output_path, 'JPEG', quality=quality, optimize=True)
                         
                print(f"Processed {filename}: Original {current_width}x{current_height} -> New {new_width}x{new_height}")
                
            except Exception as e:
                print(f"Error processing {filename}: {e}")

# --- Run the Script ---
# Change these paths to point to your actual folders
input_directory = '/mnt/c/Users/mrchu/Downloads/cmb_pics'
output_directory = '/mnt/c/Users/mrchu/Downloads/cmb_pics_small'

batch_resize_longest_edge(input_directory, output_directory, max_dimension=2000)