from flask import request,Blueprint, render_template,current_app
green_blueprint = Blueprint('green', __name__, url_prefix='/green')

@green_blueprint.route('/a', methods=['GET','POST'])
def index():
    print("green진입")
    return "Hello Green!!"

@green_blueprint.route('/test', methods=['GET', 'POST'])
def test():
    return render_template('index.html')

