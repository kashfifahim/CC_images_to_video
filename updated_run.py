from os import getenv
from pathlib import Path
import os
import shutil
from image_processing import extract_images_from_zip, natural_sort_key, images_to_video
from pdf_processing import convert_pdf_to_images


def process_images_to_video(extract_to_folder, output_folder, temp_video_file):
    # Sorting the image paths
    image_paths = sorted([str(file_path) for file_path in Path(extract_to_folder).glob('*.png')], key=natural_sort_key)
    print(f"Sorted image paths: {image_paths}")

    # Setting the path for the output video file
    output_video_file = Path(output_folder / 'output_video.mp4')
    print(f"Output video file will be saved as: {output_video_file}")

    # Creating the video from images
    images_to_video(image_paths, str(temp_video_file), fps=30, duration=5)

    # Verifying the video creation and performing cleanup
    if os.path.exists(temp_video_file) and os.path.getsize(temp_video_file) > 0:
        print(f"Video file created successfully: {temp_video_file}")
        shutil.move(str(temp_video_file), str(output_video_file))
        print(f"Video moved to output folder: {output_video_file}")

        # try:
        #     shutil.rmtree(temp_video_file.parent)
        #     print(f"Deleted temp images folder: {extract_to_folder}")
        # except OSError as e:
        #     print(f"Error deleting folder {extract_to_folder}: {e.strerror}")
    else:
        print(f"Video creation failed or video file is empty: {output_video_file}")
 

if __name__ == '__main__':
    print("Script started")
    # Setting up input and output folders
    input_folder = Path(getenv('CROSSCOMPUTE_INPUT_FOLDER', 'batches/standard/input'))
    output_folder = Path(getenv('CROSSCOMPUTE_OUTPUT_FOLDER', 'batches/standard/output'))
    print(f"Input folder: {input_folder}, Output folder: {output_folder}")
    output_folder.mkdir(parents=True, exist_ok=True)

    # Creating temporary folders for processing
    temp_folder = output_folder / 'temp'
    print(f"Temporary folder: {temp_folder}")
    temp_folder.mkdir(exist_ok=True)
    temp_video_file = temp_folder / 'temp_output_video.mp4'

    extract_to_folder = temp_folder / 'extracted_images'
    extract_to_folder.mkdir(exist_ok=True)

    if (input_folder.glob('*.pdf')):
        for pdf_file in input_folder.glob('*.pdf'):
             print(f"Processing PDF file: {pdf_file}")
             convert_pdf_to_images(pdf_file, extract_to_folder)
             print(f"PDF processed and images saved in {extract_to_folder}")
        
        # After PDF processing and saving images
        process_images_to_video(extract_to_folder, output_folder, temp_video_file)
    else: 
        zip_files = list(input_folder.glob('*.zip'))
        if not zip_files:
            print("No zip file found in the input folder")
            raise ValueError("No zip file found in the input folder")
        zip_file_path = zip_files[0]
        print(f"Zip file found: {zip_file_path}")
        images_folder = extract_images_from_zip(zip_file_path, extract_to_folder)
        if not images_folder:
            raise ValueError("No folder containing images was found")
        # After extracting images from ZIP
        process_images_to_video(extract_to_folder, output_folder, temp_video_file)