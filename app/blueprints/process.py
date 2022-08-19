from flask import Blueprint, render_template, request, send_file, redirect, url_for

bp = Blueprint('process', __name__, url_prefix='/process')

@bp.route('', methods=['GET', 'POST'])
def single_file():

    args = request.args

    root_directory = 'user_files'
    file_directory = args['upload_folder']
    file_name = args['file_name']
    output_format = args['output_format']

    import os
    file_path = os.path.join(root_directory, file_directory, file_name)

    print('FILE PATH:', file_path)

    from image_generator import generate

    output_path = generate(file_path, output_format)

    output_path = output_path.replace('app/static/', '')

    return redirect(url_for('configure_css.configure', file=output_path))