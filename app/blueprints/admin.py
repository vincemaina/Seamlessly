from flask import Blueprint, render_template, current_app, request, redirect, url_for, send_from_directory, send_file

from app.config import UPLOAD_FOLDER

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/purge_user_files', methods=['POST'])
def purge_user_files():
    from pathlib import Path
    import shutil

    dirpath = Path(UPLOAD_FOLDER)
    if dirpath.exists() and dirpath.is_dir():
        shutil.rmtree(dirpath)
        print('Removed directory.')
    
    return redirect(url_for('admin.view_user_files'))

@bp.route('/view_user_files', methods=['GET', 'POST'])
def view_user_files():

    if request.method == 'POST':

        if request.form['purge-button']:

            # The user clicked the purge button (or the purge request was trigged by a POST request.)

            purge_user_files()

    import os
    from pathlib import Path

    root = UPLOAD_FOLDER
    user_files_directory = {}

    with current_app.app_context():
        for path, subdirs, files in os.walk(root):
            for name in files:
                root_directory, sub_directory, file = Path(path, name).parts
                try:
                    user_files_directory[sub_directory]
                except:
                    user_files_directory[sub_directory] = []
                finally:
                    user_files_directory[sub_directory].append(file)

    sorted_directory = sorted(user_files_directory, reverse=True)

    return render_template('admin/view_user_files.html', user_files=user_files_directory, sorted_directory=sorted_directory)


@bp.route('/purge_generated_media', methods=['POST'])
def purge_generated_media():
    from pathlib import Path
    import shutil

    dirpath = Path('app/static/generated_media')
    if dirpath.exists() and dirpath.is_dir():
        shutil.rmtree(dirpath)
        print('Removed directory.')
    
    return redirect(url_for('admin.view_user_files'))

@bp.route('/view_generated_media', methods=['GET', 'POST'])
def view_generated_media():

    if request.method == 'POST':

        try:
            
            request.form['purge-button']
            purge_generated_media()

        except KeyError:

            from pathlib import Path

            root = 'static/generated_media'

            file_path = Path(root, request.form['file_to_download'])

            return send_file(file_path)

    import os
    from pathlib import Path

    generated_media_directory = {}

    root = 'app/static/generated_media'

    with current_app.app_context():
        for path, subdirs, files in os.walk(root):
            for name in files:
                sub_directory, file = Path(path, name).parts[-2:]
                try:
                    generated_media_directory[sub_directory]
                except:
                    generated_media_directory[sub_directory] = []
                finally:
                    generated_media_directory[sub_directory].append(file)

    sorted_directory = sorted(generated_media_directory, reverse=True)

    return render_template('admin/view_generated_media.html', user_files=generated_media_directory, sorted_directory=sorted_directory)
