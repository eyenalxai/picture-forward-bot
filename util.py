from aiogram.types import PhotoSize


# Find the largest photo in a list of photos by file size with max() function
def find_largest_photo(photos: list[PhotoSize]) -> PhotoSize:
    return max(photos, key=lambda x: x.file_size)
