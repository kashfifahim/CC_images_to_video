import os
from pdf2image import convert_from_path

def convert_pdf_to_images(input_pdf, output_folder):
    # Convert PDF pages to images
    images = convert_from_path(input_pdf)

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Save the images to the output folder
    for i, image in enumerate(images):
        image_path = os.path.join(output_folder, f"page_{i+1}.png")
        image.save(image_path, "PNG")

if __name__ == "__main__":
    input_pdf = "input.pdf"  # Replace with your input PDF file
    output_folder = "output_images"  # Replace with your desired output folder

    convert_pdf_to_images(input_pdf, output_folder)
    print(f"Converted PDF to images and saved to {output_folder}")
