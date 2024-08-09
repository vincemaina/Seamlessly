from flask import Blueprint, request, redirect, url_for, flash

from app.config import UPLOAD_FOLDER

bp = Blueprint('process', __name__, url_prefix='/process')

@bp.route('', methods=['GET', 'POST'])
def single_file():

    args = request.args

    root_directory = UPLOAD_FOLDER
    file_directory = args['upload_folder']
    file_name = args['file_name']
    output_format = args['output_format']

    import os
    file_path = os.path.join(root_directory, file_directory, file_name)

    print('FILE PATH:', file_path)

    from image_generator import generate

    output_path, success = generate(file_path, output_format)

    if success:

        output_path = output_path.replace('app/static/', '')

        return redirect(url_for('configure_css.configure', file=output_path))
    
    else:

        message = 'File generation was unsuccessful. Please check the file you submitted is an accepted file type.'
        flash(message)
        
        return redirect(url_for('upload.single_file'))
