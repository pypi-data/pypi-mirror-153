import PIL
from PIL import Image


def get_image(image_path: str) -> PIL:
    try:
        image = Image.open(open(image_path, 'rb'))
    except FileNotFoundError as e:
        raise e
    return image
