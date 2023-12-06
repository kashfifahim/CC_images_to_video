from os import getenv
from pathlib import Path
import os
import shutil
from image_processing import extract_images_from_zip, natural_sort_key, images_to_video
from pdf_processing import convert_pdf_to_images

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

    # PDF Processing Section
    # PDF Processing Section
    for pdf_file in input_folder.glob('*.pdf'):
        print(f"Processing PDF file: {pdf_file}")
        pdf_output_folder = temp_folder / pdf_file.stem
        pdf_output_folder.mkdir(exist_ok=True)
        convert_pdf_to_images(pdf_file, pdf_output_folder)
        print(f"PDF processed and images saved in {pdf_output_folder}")

        # Zipping the folder with images
        zip_file_path = temp_folder / f"{pdf_file.stem}_Archive.zip"
        shutil.make_archive(zip_file_path.stem, 'zip', pdf_output_folder)
        print(f"Created zip archive at {zip_file_path}")

    # Finding the first zip file in the input folder
    zip_files = list(input_folder.glob('*.zip'))
    if not zip_files:
        print("No zip file found in the input folder")
        raise ValueError("No zip file found in the input folder")
    zip_file_path = zip_files[0]
    print(f"Zip file found: {zip_file_path}")

    # Extracting images from the zip file and finding the folder with images
    images_folder = extract_images_from_zip(zip_file_path, extract_to_folder)
    if not images_folder:
        raise ValueError("No folder containing images was found")

    # Sorting the image paths
    image_paths = sorted([str(file_path) for file_path in Path(images_folder).glob('*.png')], key=natural_sort_key)
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

        try:
            shutil.rmtree(temp_video_file.parent)
            print(f"Deleted temp images folder: {extract_to_folder}")
        except OSError as e:
            print(f"Error deleting folder {extract_to_folder}: {e.strerror}")
    else:
        print(f"Video creation failed or video file is empty: {output_video_file}")

    print("Script ended")