from flask import Blueprint, render_template, request, redirect, url_for

bp = Blueprint('upload', __name__, '/upload')

user_file_directory = './user_files/'

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
        
        return redirect(url_for('index'))

    output_file_types = {
        'Mp4': '.mp4',
        'WebP': '.webp',
        'Gif': '.gif',
        'APng': '.APng',
        'Jpeg': '.jpg',
        'Png': '.png'
    }

    return render_template('file_upload/file_upload.html', output_file_types=output_file_types)
