import os
from pathlib import Path
from wand.image import Image
from pdf2image import convert_from_path


def get_images_from_pdf(pdf_file: str):
    images = call_convert(pdf_file)
    wand_images = [Image(filename=image_path) for image_path in images]
    clear_images(images)
    return wand_images


def call_convert(src: str):
    return convert_from_path(src, 300, output_folder=Path(src).parent, fmt='jpg', paths_only=True, thread_count=6)


def clear_images(images: list):
    for image_path in images:
        os.remove(image_path)
