def limit_dimensions(width, height):

    '''Scales down the image to MAX_DIMENSION if either width or height exceed MAX_DIMENSION.'''

    MAX_DIMENSION = 2000

    if width > MAX_DIMENSION:

        scaler = MAX_DIMENSION/width
        width = MAX_DIMENSION
        height *= scaler

    if height > MAX_DIMENSION:

        scaler = MAX_DIMENSION/height
        height = MAX_DIMENSION
        width *= scaler
    
    return width, height


def ensure_even_dimensions(width, height):

    '''Ensures both width and height are even'''

    if height % 2 == 1:
        print('Height is odd.')
        height -= 1
    else:
        print('Height is even')

    if width % 2 == 1:
        print('Width is odd.')
        width -= 1
    else:
        print('Width is even.')

    return width, height


def crop_video(source, crop_width, crop_height, crop_position_x, crop_position_y, fps):

    cropped_video = source.filter('crop', w=crop_width, h=crop_height, x=crop_position_x, y=crop_position_y)
    # .filter('fps', fps=fps, round='up')

    width = crop_width
    height = crop_height
    
    return cropped_video, width, height


def get_file_name(file_path):

    '''Generates output file name without the extensions'''
    
    from pathlib import Path

    file_path = Path(file_path)
    file_name = Path(file_path.parts[-1])

    file_extensions = "".join(file_name.suffixes)
    
    file_name = str(file_name).replace(file_extensions,'')

    return file_name


def generate(file_path, output_format, crop_width='iw', crop_height='ih', crop_position_x='(in_w-out_w)/2', crop_position_y='(in_h-out_h)/2', fps=25):

    import ffmpeg

    input_file = ffmpeg.input(file_path)


    # Getting the dimensions of the file the user has submitted

    try:
        from . get_video_properties import get_video_properties
    except ImportError:
        from get_video_properties import get_video_properties

    video_properties = get_video_properties(file_path)

    width = int(video_properties['width'])
    height = int(video_properties['height'])


    # Placing a limit of the dimensions of this image
    width, height = limit_dimensions(width, height)

    # Crop file
    # input_file, width, height = crop_video(input_file, crop_width, crop_height, crop_position_x, crop_position_y, fps)

    # Defining dimensions of the tile
    tile_width = width * 2
    tile_height = height * 2


    # stream, width, height = crop_video(stream)


    # This allows us to create four overlays from the same input
    split = input_file.split()


    # Applying transformation to the input file and creating the seamless output media
    canvas = split[0].filter('scale', w=tile_width, h=tile_height, flags='lanczos') # canvas
    canvas = canvas.overlay(split[1].filter('scale', w=width, h=height), x=0, y=0) # top left
    canvas = canvas.overlay(split[2].hflip().filter('scale', w=width, h=height), x=width, y=0) # top right
    canvas = canvas.overlay(split[3].hflip().vflip().filter('scale', w=width, h=height), x=width, y=height) # bottom right
    canvas = canvas.overlay(split[4].vflip().filter('scale', w=width, h=height), x=0, y=height) # bottom left


    # Getting file name without extensions
    file_name = get_file_name(file_path)


    # File creation time
    from datetime import datetime
    creation_time = datetime.utcnow().strftime("%m%d%Y_%H%M%S")


    # Directory for generated files

    generated_file_directory = 'app/static/generated_media'
    prefix = 'download_'

    import os
    file_path = os.path.join(generated_file_directory, prefix + creation_time)

    os.makedirs(file_path, exist_ok=True)

    # Defines output file name/path.
    output_location = f'{file_path}/seamlessly_{file_name}_{creation_time}.{output_format}'
    canvas = canvas.output(output_location)
    
    # Executes all of the above
    canvas.run()

    # Uploading file to S3
    from aws_s3.upload_files import upload_file


    generated_file_directory = 'generated_media'
    prefix = 'download_'

    file_path = os.path.join(generated_file_directory, prefix + creation_time)

    object_path = f'{file_path}/seamlessly_{file_name}_{creation_time}.{output_format}'

    if upload_file(file_path=output_location, object_path=object_path):
        print('Successfully uploaded generated media to S3 bucket.')
    else:
        print('Failed to upload generated media to S3 bucket.')
    

    # Removing user uploaded files

    from pathlib import Path
    import shutil

    dirpath = Path('user_files')
    if dirpath.exists() and dirpath.is_dir():
        shutil.rmtree(dirpath)
        print('Removed directory.')


    # Removing generated files

    dirpath = Path('app/static/generated_media')
    if dirpath.exists() and dirpath.is_dir():
        shutil.rmtree(dirpath)
        print('Removed directory.')


    # from pygifsicle import gifsicle
    # gifsicle(
    #     sources=['out.gif'], # or a single_file.gif
    #     destination="out_comp_1.gif", # or just omit it and will use the first source provided.
    #     optimize=True, # Whetever to add the optimize flag of not
    #     colors=15, # Number of colors t use
    #     options=["--verbose"] # Options to use.
    # )


    #     # .output('out.mp4')
    #     # .run()

    return output_location


if __name__ == '__main__':

    generate('user_files/upload_08192022_105858/y-so-serious.png', 'png')