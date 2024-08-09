from flask import Blueprint, render_template, request, redirect, url_for, flash
from .. config import OUTPUT_FILE_TYPES, INPUT_FILE_TYPES, UPLOAD_FOLDER
from .. import file_limit_megabytes

bp = Blueprint('upload', __name__, url_prefix='/upload')

file_limit_bytes = file_limit_megabytes * 1024 * 1024 # Converting into bytes

user_file_directory = UPLOAD_FOLDER

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


                    # Formats filename to improve security
                    from werkzeug.utils import secure_filename
                    file_name = secure_filename(uploaded_file.filename)


                    # Setting file_name if there isn't one. This doesn't add an extension. Ideally it should add the same extension that was submitted.
                    if not file_name:
                        file_name = upload_time

                    upload_path = file_path + '/' + file_name
                    uploaded_file.save(upload_path)


                    def remove_the_new_file():

                        # Removes the file that was just added.
                        try:
                            os.remove(upload_path)
                        except Exception as e:
                            print(e)
                        
                        # Removes the subfolder for that file.
                        from pathlib import Path
                        folder_path = '/'.join(Path(upload_path).parts[:-1])
                        try:
                            os.rmdir(folder_path)
                        except OSError:
                            print('Cannot remove, folder is not empty.')


                    # VERIFYING FILE TYPE

                    import filetype
                    kind = filetype.guess(upload_path)

                    if kind is None:

                        message = 'We do not recognise that file type.'

                        print(message)
                        flash(message)

                        remove_the_new_file()

                        return redirect(url_for('upload.single_file'))
                                            
                    else:

                        print(f'File extension: {kind.extension}')
                        print(f'File MIME type: {kind.mime}')
                        
                        if kind.extension in dict.keys(INPUT_FILE_TYPES):

                            print('FILE IS VALID')

                        else:

                            message = 'We do not currently support that file type.'

                            print(message)
                            flash(message)

                            remove_the_new_file()
                            
                            return redirect(url_for('upload.single_file'))


                else:

                    # File was too large

                    from werkzeug.exceptions import RequestEntityTooLarge
                    raise RequestEntityTooLarge(f'Please upload a file under {file_limit_megabytes} MBs.')


        output_format = OUTPUT_FILE_TYPES[request.form['file_format']]


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
        
        return redirect(url_for('process.single_file', upload_folder=prefix+upload_time, file_name=file_name, output_format=output_format, crop_width=crop_width, crop_height=crop_height))


    
    # CREATING accept tag for our input:file element

    accepted_file_types = []

    for mime in dict.values(INPUT_FILE_TYPES):
        accepted_file_types.append(mime)

    accepted_file_types = ','.join(accepted_file_types)

    print('ACCEPTED:', accepted_file_types)
    
    return render_template('file_upload/file_upload.html', output_file_types=OUTPUT_FILE_TYPES, file_limit_bytes=file_limit_bytes, accepted_file_types=accepted_file_types)
