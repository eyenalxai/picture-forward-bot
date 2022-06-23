from aiogram.types import PhotoSize

# Find the largest photo in a list of photos by file size with max() function
from config.app import MAX_OBJECTS
from model.saved import Saved


def find_largest_photo(photos: list[PhotoSize]) -> PhotoSize:
    return max(photos, key=lambda x: x.file_size)


# Check that saved object is already in database by file id using filter() and exists().
# If it is, return True, otherwise return False
async def is_already_saved(file_id: str) -> bool:
    return await Saved.objects.filter(file_id=file_id).exists()


# Save file id to database, if object count is larger than 1000, delete the oldest object
async def save_file_id(file_id: str) -> None:
    await Saved(file_id=file_id).save()
    if await Saved.objects.count() > MAX_OBJECTS:
        oldest_object = await Saved.objects.order_by('id').first()
        await oldest_object.delete()
