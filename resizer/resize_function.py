from PIL import Image
from .s3_util import upload_file_to_s3, gen_s3_filename
import os, io

def convert_and_save_to_s3(image: Image.Image, file_name: str, aspect_ratio: str) -> str:
    # Convert to specified aspect ratio
    image = convert_to_aspect_ratio(image, aspect_ratio)

    # Create a BytesIO buffer to hold the image
    buffer = io.BytesIO()
    
    # Save the image to the buffer in the appropriate format
    file_extension = os.path.splitext(file_name)[1].lower()
    if file_extension == '.png':
        image.save(buffer, format='PNG')
    elif file_extension in ['.jpg', '.jpeg']:
        image.save(buffer, format='JPEG')
    elif file_extension == '.gif':
        image.save(buffer, format='GIF')
    else:
        raise ValueError("Unsupported file format")

    # Seek to the start of the BytesIO buffer
    buffer.seek(0)

    # Generate a unique file key for S3
    file_key = gen_s3_filename(file_extension, 'test')

    # Upload the buffer to S3
    my_img_url = upload_file_to_s3(buffer, file_key)

    return my_img_url


def convert_to_aspect_ratio(image: Image.Image, aspect_ratio: str) -> Image.Image:
    """
    Converts an image to a specified aspect ratio (like 9:16 or 4:5) without stretching the image.
    It can crop or pad the image as necessary to achieve the target aspect ratio.
    
    :param image: Source image (PIL Image object)
    :param aspect_ratio: Aspect ratio as a string (e.g., "9:16", "4:5")
    :return: Image object with the new aspect ratio
    """
    # Get the original dimensions
    original_width, original_height = image.size
    
    # Parse the aspect ratio
    target_width_ratio, target_height_ratio = map(int, aspect_ratio.split(':'))
    target_aspect_ratio = target_width_ratio / target_height_ratio
    original_aspect_ratio = original_width / original_height

    if original_aspect_ratio > target_aspect_ratio:
        # Crop the width
        new_width = int(target_aspect_ratio * original_height)
        offset = (original_width - new_width) // 2
        image = image.crop((offset, 0, original_width - offset, original_height))
    elif original_aspect_ratio < target_aspect_ratio:
        # Crop the height
        new_height = int(original_width / target_aspect_ratio)
        offset = (original_height - new_height) // 2
        image = image.crop((0, offset, original_width, original_height - offset))

    # Optionally, resize to standard dimensions for the aspect ratio (if needed)
    # E.g., for 9:16 we could use standard sizes like 1080x1920 or 720x1280, etc.
    # image = image.resize((target_width, target_height), Image.ANTIALIAS)
    
    return image

def save_image_in_same_format(image: Image.Image, converted_image: Image.Image, output_name: str):
    """
    Saves the converted image in the same format as the original.
    
    :param image: Original image (PIL Image object)
    :param converted_image: Converted image (PIL Image object)
    :param output_name: The base name for the output file (without extension)
    """
    # Get the format of the original image
    original_format = image.format
    
    # Set file extension based on original format
    if original_format == 'JPEG':
        converted_image.save(f"{output_name}.jpg", format='JPEG')
    elif original_format == 'PNG':
        converted_image.save(f"{output_name}.png", format='PNG')
    elif original_format == 'GIF':
        converted_image.save(f"{output_name}.gif", format='GIF')
    elif original_format == 'BMP':
        converted_image.save(f"{output_name}.bmp", format='BMP')
    elif original_format == 'TIFF':
        converted_image.save(f"{output_name}.tiff", format='TIFF')
    else:
        # Default to PNG if the format is unrecognized
        converted_image.save(f"{output_name}.png", format='PNG')

if __name__ == "__main__":
    image = Image.open("sample.png")
    converted_image_9x16 = convert_to_aspect_ratio(image, "9:16")
    save_image_in_same_format(image, converted_image_9x16, "converted_image_9x16")

    converted_image_4x5 = convert_to_aspect_ratio(image, "4:5")
    save_image_in_same_format(image, converted_image_4x5, "converted_image_4x5")