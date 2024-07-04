# Image Compression and Conversion Script

This repository contains a Python script to automate the compression and conversion of images to JPEG format. This script was created to meet the requirements of a Human Resources (HR) system that needed images of all employees to be under 512 KB in size and in JPEG format.

## Features

- **Automated Image Processing**: Automatically compress and convert images to JPEG format.
- **Quality Adjustment**: Adjusts image quality to ensure the file size is below 512 KB.
- **Directory Navigation**: Recursively processes images in a specified root folder and saves them in a backup folder, maintaining the original directory structure.

## Prerequisites

- Python 3.x
- Pillow library

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your-username/image-compression-script.git
   cd image-compression-script
   ```

2. **Install Dependencies**

   Use pip to install the required libraries:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Configure Paths**

   Modify the `root_folder_path` and `backup_folder_path` variables in the script to point to your source and backup directories.

   ```python
   root_folder_path = '/path/to/source/folder'
   backup_folder_path = '/path/to/backup/folder'
   ```

2. **Run the Script**

   Execute the script from the command line:

   ```bash
   python compress_images.py
   ```

## Script Overview

### Importing Libraries

The script begins by importing necessary libraries for file handling and image processing.

```python
import os
import io
from PIL import Image
```

### Compression and Conversion Function

The `compress_and_copy_image` function handles the opening, conversion, and compression of each image.

```python
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
```

### Main Function

The `main` function traverses the directory tree and applies the compression function to each image file.

```python
def main():
    root_folder_path = '/path/to/source/folder'
    backup_folder_path = '/path/to/backup/folder'
    max_image_size = 512 * 1024  # 512 KB

    for foldername, subfolders, filenames in os.walk(root_folder_path):
        for filename in filenames:
            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif')):
                image_file = os.path.join(foldername, filename)
                relative_path = os.path.relpath(foldername, root_folder_path)
                backup_folder = os.path.join(backup_folder_path, relative_path)
                os.makedirs(backup_folder, exist_ok=True)
                compress_and_copy_image(image_file, backup_folder, max_image_size)
```

### Script Execution

Ensure the script runs when executed directly.

```python
if __name__ == "__main__":
    main()
```

## Contributing

Feel free to submit issues or pull requests if you have suggestions for improvements or encounter any bugs.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

This script was created to automate the process of image compression and conversion for a company's HR system, demonstrating the power of Python in solving real-world problems efficiently.

---

Feel free to use this script as a starting point for your own image processing needs. Happy coding!
