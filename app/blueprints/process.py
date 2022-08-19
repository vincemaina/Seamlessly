from flask import Blueprint, render_template, request

bp = Blueprint('process', __name__, url_prefix='/process')

@bp.route('', methods=['GET', 'POST'])
def single_file():

    args = request.args

    return args