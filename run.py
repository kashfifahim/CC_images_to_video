import cv2
import os
import os
from os import getenv
from pathlib import Path
import logging
import re

# Set up logging
logging.basicConfig(filename='image_to_video_errors.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')

def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]

def resize_image(image, target_width, target_height):
    """
    Resize an image to fit within the specified dimensions while maintaining the original aspect ratio.
    """
    original_height, original_width = image.shape[:2]
    aspect_ratio = original_width / original_height
    
    if original_width > original_height:
        new_width = target_width
        new_height = int(target_width / aspect_ratio)
    else:
        new_height = target_height
        new_width = int(target_height * aspect_ratio)

    resized_image = cv2.resize(image, (new_width, new_height))
    
    # If the new dimensions are smaller in any direction, pad the resized image with black color
    top_padding = (target_height - new_height) // 2
    bottom_padding = target_height - new_height - top_padding
    left_padding = (target_width - new_width) // 2
    right_padding = target_width - new_width - left_padding

    return cv2.copyMakeBorder(resized_image, top_padding, bottom_padding, left_padding, right_padding, cv2.BORDER_CONSTANT, value=[0, 0, 0])

def images_to_video(image_paths, output_video_file, fps=30, duration=5, target_width=1920, target_height=1080):
    """
    Convert a set of images to a video.
    
    Parameters:
    - image_paths: list of paths to the image files
    - output_video_file: path to the output video file (e.g., 'output.mp4')
    - fps, duration, target_width, target_height as before
    """
    out = cv2.VideoWriter(output_video_file, cv2.VideoWriter_fourcc(*'XVID'), fps, (target_width, target_height))
    
    for img_path in image_paths:
        img = cv2.imread(img_path)
        resized_img = resize_image(img, target_width, target_height)
        
        for _ in range(fps * duration):
            out.write(resized_img)
    
    out.release()

try:
    input_folder_path = Path('input_folder')
    output_video_file = Path('output_folder/output_video.mp4')

    # Ensure output folder exists
    output_video_file.parent.mkdir(parents=True, exist_ok=True)

    # Dynamically generate list of image paths
    # image_paths = [str(file_path) for file_path in input_folder_path.glob('*.png')]

    # Natural Sort Function for image paths
    image_paths = sorted([str(file_path) for file_path in input_folder_path.glob('*.png')], key=natural_sort_key)

    # Check if image paths are empty
    if not image_paths:
        raise ValueError("No images found in the input folder")

    # Call the images_to_video function
    images_to_video(image_paths, str(output_video_file), fps=30, duration=5)

except FileNotFoundError as fnf_error:
    logging.error(f"File not found: {fnf_error}", exc_info=True)
except PermissionError as perm_error:
    logging.error(f"Permission error: {perm_error}", exc_info=True)
except ValueError as val_error:
    logging.error(f"Value error: {val_error}", exc_info=True)
except Exception as e:
    logging.error(f"An unexpected error occurred: {e}", exc_info=True)