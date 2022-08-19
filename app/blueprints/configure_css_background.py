from flask import Blueprint, render_template, request, send_file, send_from_directory

bp = Blueprint('configure_css', __name__, url_prefix='/configure')

@bp.route('/', methods=['GET', 'POST'])
def configure():
    
    args = request.args

    file_path = args['file']

    print('FILE PATH:', file_path)

    return render_template('file_upload/optimise_for_web_background.html', file_path=file_path)
