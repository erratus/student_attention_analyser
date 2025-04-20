import os

def rename_images_in_folder(folder_path, start_number):
    # Ensure the folder exists
    if not os.path.exists(folder_path):
        print("Error: The specified folder does not exist.")
        return

    # Filter files for image formats
    valid_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.gif')
    images = [f for f in os.listdir(folder_path) if f.lower().endswith(valid_extensions)]

    if not images:
        print("No images found in the folder.")
        return

    # Sort images to maintain order
    images.sort()

    # Rename images
    for idx, filename in enumerate(images, start=start_number):
        # Get the file extension
        file_ext = os.path.splitext(filename)[1]
        # Construct the new filename
        new_name = f"img{idx:02d}{file_ext}"
        # Full paths
        old_path = os.path.join(folder_path, filename)
        new_path = os.path.join(folder_path, new_name)
        # Rename the file
        os.rename(old_path, new_path)
        print(f"Renamed: {filename} -> {new_name}")

    print("Renaming completed.")

# Folder path and start number
folder_path = 'C:/Users/suryabhaas/Downloads/new/flipped'  # Replace with your folder path
start_number = 244  # Replace with your starting number

rename_images_in_folder(folder_path, start_number)
