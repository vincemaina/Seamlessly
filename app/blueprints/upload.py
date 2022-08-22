from flask import Blueprint, render_template, request, redirect, url_for, flash

bp = Blueprint('upload', __name__, url_prefix='/upload')

from .. import file_limit_megabytes
file_limit_bytes = file_limit_megabytes * 1024 * 1024 # Converting into bytes

user_file_directory = './user_files/'

from .. config import output_file_types

def check_file_size(file):

    file.seek(0, 2)
    file_size = file.tell()
    file.seek(0, 0)

    print('FILE SIZE:', file_size)

    print('FILE LIMIT:', file_limit_bytes, 'bytes')

    if int(file_size) > int(file_limit_bytes):

        return False
    
    else: return True


@bp.route('/', methods=['GET', 'POST'])
def single_file():

    if request.method == 'POST':

        # File was submitted

        uploaded_file_list = request.files.getlist('uploaded_file')

        # Added this block to prevent multiple file uploads. Can remove in future if needed, although note that the frontend script that checks file sizes is only configured to check the first one.
        if len(uploaded_file_list) > 1:
            flash('Please only upload one file.')
            return redirect(url_for('upload.single_file'))

        for uploaded_file in uploaded_file_list:
        
            if uploaded_file.filename != '':

                if check_file_size(uploaded_file):

                    # File size was accepted

                    prefix = 'upload_'

                    from datetime import datetime
                    upload_time = datetime.utcnow().strftime("%m%d%Y_%H%M%S")

                    import os
                    file_path = os.path.join(user_file_directory, prefix + upload_time)

                    os.makedirs(file_path, exist_ok=True)

                    from werkzeug.utils import secure_filename
                    uploaded_file.save(file_path + '/' + secure_filename(uploaded_file.filename))


                else:

                    # File was too large

                    from werkzeug.exceptions import RequestEntityTooLarge
                    raise RequestEntityTooLarge(f'Please upload a file under {file_limit_megabytes} MBs.')


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

    return render_template('file_upload/file_upload.html', output_file_types=output_file_types, file_limit_bytes=file_limit_bytes)
