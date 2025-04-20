import os
from PIL import Image

def flip_images_in_folder(input_folder, output_folder):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Iterate over each file in the input folder
    for filename in os.listdir(input_folder):
        # Construct full file path
        input_path = os.path.join(input_folder, filename)
        
        # Check if the file is an image
        if os.path.isfile(input_path) and filename.lower().endswith(('png', 'jpg', 'jpeg', 'bmp', 'gif')):
            # Open the image
            with Image.open(input_path) as img:
                # Flip the image along the y-axis
                flipped_img = img.transpose(Image.FLIP_LEFT_RIGHT)
                
                # Save the flipped image to the output folder
                output_path = os.path.join(output_folder, filename)
                flipped_img.save(output_path)
                
                print(f"Flipped image saved as: {output_path}")

# Define input and output folders
input_folder = 'C:/Users/suryabhaas/Downloads/new'
output_folder = 'C:/Users/suryabhaas/Downloads/new/flipped'

# Call the function
flip_images_in_folder(input_folder, output_folder)
