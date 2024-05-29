from PIL import Image
import os
import imagehash
from heapq import nlargest
import time

def crop_image(image_path):
    # Open the image file
    with Image.open(image_path) as img:
        width, height = img.size
        # Calculate new dimensions
        new_width, new_height = width // 2, height // 2
        # Crop the image
        cropped_img = img.crop((0, 0, new_width, new_height))
        return cropped_img

def calculate_similarity(cropped_img, directory):
    hash_orig = imagehash.average_hash(cropped_img)
    similarities = {}
    
    # Iterate through all jp2 files in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.jp2'):
            with Image.open(os.path.join(directory, filename)) as img:
                hash_current = imagehash.average_hash(img)
                # Calculate the difference in hashes
                difference = hash_orig - hash_current
                similarities[filename] = difference
    return similarities

def find_nearest_images(similarities, k=5):
    # Find the k images with the smallest difference
    nearest_images = nlargest(k, similarities, key=lambda x: -similarities[x])
    return nearest_images

# Set the directory and image path
directory = 'jpg2'
image_path = 'jpg2/image.jp2'

# Start timing
start_time = time.time()

# Crop the image
cropped_img = crop_image(image_path)

# Calculate similarities
similarities = calculate_similarity(cropped_img, directory)

# Find the nearest 5 images
nearest_images = find_nearest_images(similarities)

# Stop timing
end_time = time.time()

# Print the nearest images
print("Nearest 5 images based on hash similarity:")
for image in nearest_images:
    print(image)

# Print the time taken
print(f"Time taken to find nearest images: {end_time - start_time:.2f} seconds")


# Output

# Nearest 5 images based on hash similarity:
# ids_0046.jp2
# ids_0033.jp2
# ids_0032.jp2
# ids_0074.jp2
# ids_0070.jp2
# Time taken to find nearest images: 17.64 seconds