from aiogram.types import PhotoSize


def get_largest_picture(pictures: list[PhotoSize]) -> PhotoSize:
    return max(pictures, key=lambda photo: photo.width * photo.height)
