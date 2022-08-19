from flask import Blueprint, render_template, current_app, request, redirect, url_for

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/purge_cache', methods=['POST'])
def purge_cache():
    from pathlib import Path
    import shutil

    dirpath = Path('user_files')
    if dirpath.exists() and dirpath.is_dir():
        shutil.rmtree(dirpath)
        print('Removed directory.')
    
    return redirect(url_for('admin.view_user_files'))

@bp.route('/view_user_files', methods=['GET', 'POST'])
def view_user_files():

    if request.method == 'POST':

        if request.form['purge-button']:

            # The user clicked the purge button (or the purge request was trigged by a POST request.)

            purge_cache()

    import os
    from pathlib import Path

    root = 'user_files'
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

if __name__ == '__main__':
    view_user_files()
