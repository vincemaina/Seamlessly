from flask import Blueprint, render_template, request, redirect, url_for

bp = Blueprint('upload', __name__, url_prefix='/upload')

user_file_directory = './user_files/'

output_file_types = {
    # 'Web-Optimised Background Image': 'webp',
    # 'Web-Optimised Background Animation': 'webp',
    'WebP': 'webp',
    'Mp4': 'mp4',
    'WebM': 'webm',
    # 'Gif': 'gif',
    # 'APng': 'APng',
    # 'Jpeg': 'jpg',
    # 'Png': 'png'
}

@bp.route('/', methods=['GET', 'POST'])
def single_file():

    if request.method == 'POST':

        # File was submitted

        for uploaded_file in request.files.getlist('uploaded_file'):
        
            if uploaded_file.filename != '':

                prefix = 'upload_'

                from datetime import datetime
                upload_time = datetime.utcnow().strftime("%m%d%Y_%H%M%S")

                import os
                file_path = os.path.join(user_file_directory, prefix + upload_time)

                os.makedirs(file_path, exist_ok=True)

                uploaded_file.save(file_path + '/' + uploaded_file.filename)

        output_format = output_file_types[request.form['file_format']]


        # Conditional statements are to prevent the programming from crashing if no crop_width or crop_height is provided.

        if request.form['crop_width']:
            crop_width = int(request.form['crop_width'])
        else:
            crop_width = None
        
        if request.form['crop_height']:
            crop_height = int(request.form['crop_height'])
        else:
            crop_height = None


        print(output_format, crop_width, crop_height)
        
        return redirect(url_for('process.single_file', upload_folder=prefix+upload_time, file_name=uploaded_file.filename, output_format=output_format, crop_width=crop_width, crop_height=crop_height))

    return render_template('file_upload/file_upload.html', output_file_types=output_file_types)
