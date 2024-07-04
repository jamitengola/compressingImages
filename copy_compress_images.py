import os
import io
from PIL import Image

def compress_and_copy_image(source_path, destination_folder, max_image_size):
    image = Image.open(source_path)
    if image.mode in ('RGBA', 'LA'):
        background = Image.new('RGB', image.size, (255, 255, 255))
        background.paste(image, (0, 0), image)
        image = background.convert('RGB')
    elif image.mode != 'RGB':
        image = image.convert('RGB')
    
    quality = 90
    file_name = os.path.basename(source_path)
    # Ensure the file extension is .jpg
    file_name = os.path.splitext(file_name)[0] + '.jpg'
    destination_path = os.path.join(destination_folder, file_name)

    while quality > 0:
        buffer = io.BytesIO()
        image.save(buffer, format='JPEG', quality=quality)
        if buffer.tell() <= max_image_size:
            with open(destination_path, 'wb') as f:
                f.write(buffer.getbuffer())
            break
        quality -= 10

def main():
    root_folder_path = 'origin'
    backup_folder_path = 'destination'
    max_image_size = 512 * 1024  # 1 MB

    for foldername, subfolders, filenames in os.walk(root_folder_path):
        for filename in filenames:
            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif')):
                image_file = os.path.join(foldername, filename)
                relative_path = os.path.relpath(foldername, root_folder_path)
                backup_folder = os.path.join(backup_folder_path, relative_path)
                os.makedirs(backup_folder, exist_ok=True)
                compress_and_copy_image(image_file, backup_folder, max_image_size)

if __name__ == "__main__":
    main()
