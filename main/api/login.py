from flask import Blueprint, render_template, request, jsonify, redirect, make_response
# from strgen import StringGenerator
from main.utils.common_util import respond
import main.utils.config as def_config
import main.utils.base64 as base64
import main.utils.jwt as def_jwt
import main.dao.dao_login as def_dao_login
import main.dao.dao_pubnub as def_dao_pubnub
import hashlib
import datetime
from main.utils.log_util import logger   # 이렇게 고정해 놓고 쓰면 된다.
import bcrypt   # need package
login_blueprint = Blueprint('login', __name__, url_prefix='/login')

@login_blueprint.route('/', methods=['POST', 'GET'])
def login():

    req = request.get_json()
    logger.debug("[Entering login]%s", req)

    manager_id = req["manager_id"]      # manager 아이디
    manager_pwd = req["manager_pwd"]

    if not manager_id or not manager_pwd:
        return jsonify(respond(1010, "아이디 혹은 비밀번호를 입력해주세요.", "")), 200

    bytes_password = manager_pwd.encode()
    print(bytes_password)

    try:
        dao_result = def_dao_login.dao_login(manager_id)
        print("dao_result:", dao_result)

        if dao_result == None:  # return 값이 없으면(=즉 None면)
            return jsonify(respond(1010, "일치하는 ID가 없습니다", "")), 200

    except Exception as e:
        logger.debug("[ERROR]%s", str(e))

    saved_pwd = dao_result['MANAGER_PWD']
    bytes_saved_pwd = saved_pwd.encode()
    print(bytes_saved_pwd)
    try:
        #isPwdTrue = bcrypt.checkpw(bytes_password, bytes_saved_pwd)
        isPwdTrue = True        # 개발을 위해 임시로 넣음 <-------나중에 지우자
        print(isPwdTrue)
    except ValueError as e:
        logger.debug("[ERROR]%s", str(e))
        # bcrypt로 해시하지 않고 sha256으로 해시했던 다이제스트로 bcrypt.checkpw()를 하면 invalid salt 오류가 발생함
        return jsonify(respond(1040, "DB오류가 발생했습니다. 관리자에게 문의해주세요.", "")), 200

    if not isPwdTrue:
        return jsonify(respond(1030, "비밀번호가 틀렸습니다. 다시 입력해주세요.", "")), 200

    manager_idx = dao_result['IDX']
    manager_id = dao_result['MANAGER_ID']
    manager_name = dao_result['MANAGER_NAME']
    agency_idx = dao_result['AGENCY_IDX']  # 소속 agenc_idx

    # -----------------------------
    # Token Process
    # -----------------------------

    # 토큰 발행(JWT)
    token_payload = {
        "manager_idx": manager_idx,
        "manager_id": manager_id,
        "manager_name": manager_name,
        "agency_idx": agency_idx    # 소속 agence_idx
    }
    print("token_payload", token_payload)
    access_token = def_jwt.get_jwt_access_token(token_payload)
    refresh_token = def_jwt.get_jwt_refresh_token(token_payload)

    # dynamoDB token 저장
    put_payload = {
        "manager_idx": manager_idx,
        "table_name": def_config.DYNAMODB_TABLE_NAME,
        "region_name": def_config.DYNAMODB_REGION_NAME,
        "aws_access_key_id": def_config.DYNAMODB_ACCESS_KEY_ID,
        "aws_secret_access_key": def_config.DYNAMODB_SECRET_ACCESS_KEY,
        "access_token": access_token,
        "refresh_token": refresh_token,
    }

    dao_result = def_jwt.put_jwt(put_payload)
    print(put_payload)
    if dao_result["result"] == "fail":
        return jsonify(respond(dao_result['result_code'][0], dao_result['result_msg'], "")), dao_result['result_code'][1]

    # -----------------------------
    # PubNub Process
    # -----------------------------
    # 받을 채널을 결정한다. (1.전체 채널, 2. 자기 자신의 채널, 3.추가로 받을 allience agency의 채널 : 추가로 받을 채널에 자신이 속해 있을 경우 자신은 받지 않는 중복을 피한다.)
    subscribe_channels = []

    # 1) 모든 매니저에게 보내는 메시지 수신 채널 등록
    subscribe_channels.append("manager.0")

    # 2) 자기 자신의 메시지 수신 채널 등록
    subscribe_channels.append("manager." + str(manager_idx))

    # 3) SHARE_AGENCY_IDX 메시지 수신 채널 등록
    # [주의] 여기에는 SHARE_AGENCY_IDX값이 없을 경우에 대비하는 구문이 들어가야 한다.나중에 꼭 첨가하기
    dao_result_channel = def_dao_pubnub.dao_get_subscribe_channel(agency_idx)   # 여기서는 2,3,4로 일단 고정한다. DB에서 값을 가져온다.
    print("SHARE_AGENCY_IDX:", dao_result_channel['SHARE_AGENCY_IDX'])
    for item in dao_result_channel['SHARE_AGENCY_IDX'].split(','):
        subscribe_channels.append("agency." + str(item))

    logger.debug("[subscribe_channel]%s", subscribe_channels)

    # 로그인이 완료되면 다음을 정하여 클라이언트에 리턴한다. 클라이언트는 해당 정보를 받아서 객체를 생성하여 pubnub서버에 접속한다.
    pubnub_payload = {
        "subscribe_key": def_config.PUBNUB_SUBSCRIBE_KEY,
        "publish_key": def_config.PUBNUB_PUBLISH_KEY,
        "secret_key": def_config.PUBNUB_SECRET_KEY,
        "user_id": manager_id,  # uuid--> user_id로 써야한다.
        "subscribe_channels": subscribe_channels
    }
    etc_token = def_jwt.get_jwt_access_token(pubnub_payload)        # pubnub에 대한 정보를 etc-token에 담아서 보낸다.

    # -----------------------------
    # Making Return Data
    # -----------------------------
    # response setting
    response = make_response(jsonify(respond(1000, "성공", "")))

    # adding header
    response.headers["Authorization-Access"] = access_token
    response.headers["Authorization-Refresh"] = refresh_token
    response.headers["Authorization-Etc"] = etc_token
    response.headers["Access-Control-Expose-Headers"] = "Authorization-access, Authorization-refresh, Authorization-etc, authorization, authorization-refresh,authorization-etc"  # 브라우저의 자바스크립트에서 헤더 접근 허용

    return response, 200