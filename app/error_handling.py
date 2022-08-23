from flask import redirect, flash, url_for

def request_entity_is_too_large(e):
    print('Reached this point')
    from .config import file_limit_megabytes
    flash(f'Please only upload files under {file_limit_megabytes} MBs.')
    return redirect(url_for('upload.single_file'))

def page_not_found(e):
    flash('The page you requested does not exist.')
    return redirect(url_for('index'))
