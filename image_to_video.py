import cv2
import os
import os
from os import getenv
from pathlib import Path

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

# Adapted for CrossCompute - example usage with a list of image paths
image_paths = [str(Path('input_folder') / f'image{i}.png') for i in range(1, num_images+1)]  # num_images is the number of images you have
output_video_file = str(Path('output_folder') / 'output_video.mp4')

images_to_video(image_paths, output_video_file, fps=30, duration=5)