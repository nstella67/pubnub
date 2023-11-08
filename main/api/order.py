from flask import Blueprint, request, jsonify, current_app
from main.utils.log_util import logger, logger_order
from main.utils import common_util
from main.utils import config as def_config
import main.utils.jwt as def_jwt
import jwt      # PyJwt
import main.pubnub.pubnub

order_blueprint = Blueprint('order', __name__, url_prefix='/order')

@order_blueprint.route('/insert', methods=['GET','POST'])
def index():
    order_json = request.get_json()

    # 들어오는 주문은 무조건 log를 남긴다.
    logger_order.debug("[order insert]%s", order_json)

    #############################
    # payload를 구성한다.
    #############################

    access_token = request.headers.get('Authorization-Access').replace("Bearer ", "") # JWT(access token)의 정보를 파싱하여 나의 수신 채널을 가져온다.(즉, 자신이 속한 agency_idx에 보내면 allience 된 agency의 매니저는 받아올 수 있다.)
    print("access_token:", access_token)

    from_member_type = "server"         # 보내는 사람 멤버형태 (agency, driver, server, manager, company(플사))
    from_idx = 0                        # 0은 서버를 의미한다.
    to_member_type = "agency"           # 받는 사람 멤버형태
    decoded_token = jwt.decode(access_token, def_config.JWT_SECRET_KEY, algorithms=['HS256'])     # agency_idx를 얻어온다.
    to_idx = decoded_token['agency_idx']
    print("decoded_token:", decoded_token)

    # order data를 구성한다.
    data={}
    data['ORDER_PRICE'] = 25000
    data['ORDER_STATUS'] = 10

    payload = {
        "from_member_type": from_member_type,
        "from_idx": from_idx,
        "to_member_type": to_member_type,
        "to_idx": to_idx,
        "data": data
    }
    print("payload", payload)
    main.pubnub.pubnub.publish_to(payload)

    return "This is /order"



