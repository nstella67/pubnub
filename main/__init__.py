from flask import Flask, current_app
from main.pubnub.pubnub import pn       # pubnub 객체를 현재 파일에 주입한다.
from flask_cors import CORS, cross_origin


def create_app():
    print("create_app 진입")
    app = Flask(__name__, instance_relative_config=True)

    # -------------------------------
    # CORS Setting
    # -------------------------------
    app.config['JSON_AS_ASCII'] = False
    CORS(app, resources={r'/*': {'origins': '*'}})
    CORS(app)

    # -------------------------------
    # BLUE PRINTS
    # -------------------------------
    from main.api.red import red_blueprint
    app.register_blueprint(red_blueprint)

    from main.api.green import green_blueprint
    app.register_blueprint(green_blueprint)

    from main.api.login import login_blueprint
    app.register_blueprint(login_blueprint)

    from main.api.order import order_blueprint
    app.register_blueprint(order_blueprint)


    # -------------------------------
    # App Context Setting
    # -------------------------------
    with app.app_context():
        print("app.app_context(),current_app.name:", current_app.name)
        # app.pn = pn  # 이렇게 정의하여 쓰면 모든 main 안에 blueprint에서 current_app.pn 형태로 사용 가능하다.

    return app












