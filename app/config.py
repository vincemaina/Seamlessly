# File limit in MBs
file_limit_megabytes = 25

# Accepted input file formats, here is a list of the filetypes we can identify: https://pypi.org/project/filetype/
INPUT_FILE_TYPES = {
    'jpg': 'image/jpeg',
    'jpeg': 'image/jpeg',
    'png': 'image/png',
    'gif': 'image/gif',
}

# Accepted file types for the files this program generates
OUTPUT_FILE_TYPES = {
    'Image': 'webp',
    'Animation': 'webp',
}

# Path to file upload location
UPLOAD_FOLDER = 'app/static/user_files'

# Path to the files output by ffmpeg
OUTPUT_FOLDER = 'app/static/generated_media'
