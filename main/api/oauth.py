from flask import Blueprint, request, jsonify, make_response
from utils.common_util import respond
import utils.config as def_config
import utils.jwt as def_jwt
import jwt
import time
import main.utils.log_util  # 로그는 이렇게 고정해 놓고 쓰면 된다.

oauth_blueprint = Blueprint('oauth', __name__)

# decorator
def check_access_jwt_decorator(func):
    def check_jwt_exp():

        if request.headers.get('momo-non-member') == 'Y' or request.headers.get('momo-non-member') == 'y':
            # 비회원일 경우 : jwt check를 수행하지 않는다.
            pass
        else:
            # 로그인한 회원일 경우
            key = def_config.JWT_SECRET_KEY


            if not "Authorization" in request.headers:
                return jsonify(respond(3040, "access token을 확인할 수 없습니다.", "")), 900
            if request.headers['Authorization'].find('Bearer ') == -1:
                return jsonify(respond(3050, "Authorization의 값이 잘못 세팅되었습니다.", "")), 900
            access_token = (request.headers['Authorization']).split('Bearer ')[1]
            if len(access_token) == 0:
                return jsonify(respond(3070, "Authorization의 값이 없습니다.", "")), 900

            try:
                decoded_token = jwt.decode(access_token, key, algorithms='HS256')
            except jwt.ExpiredSignatureError:
                return jsonify(respond(3000, "access token 만료", "")), 900

            token_exp = decoded_token["exp"]
            now_timestamp = time.time()

            table_name = def_config.DYNAMODB_TABLE_NAME
            region_name = def_config.DYNAMODB_REGION_NAME
            aws_access_key_id = def_config.DYNAMODB_ACCESS_KEY_ID
            aws_secret_access_key = def_config.DYNAMODB_SECRET_ACCESS_KEY
            member_id = str(decoded_token['member_id'])

            # check exp
            if now_timestamp > token_exp:
                return jsonify(respond(3000, "access token 만료", "")), 900

            # check valid
            dynamo_result = def_jwt.get_jwt(member_id, table_name, region_name, aws_access_key_id, aws_secret_access_key)
            if dynamo_result['result'] == "fail":
                return jsonify(respond(dynamo_result['result_code'][0], dynamo_result['result_msg'], "")), dynamo_result['result_code'][1]

            dynamo_access_token = dynamo_result['data']['accessToken']

            if access_token != dynamo_access_token:
                # 비정상적인 접근으로 간주하여 access token, refresh token 폐기
                dynamo_result = def_jwt.delete_jwt(member_id, access_token, table_name, region_name, aws_access_key_id, aws_secret_access_key)
                if dynamo_result['result'] == "fail":
                    return jsonify(respond(dynamo_result['result_code'][0], dynamo_result['result_msg'], "")), dynamo_result['result_code'][1]
                return jsonify(respond(3010, "access token 불일치", "")), 900

        return func()
    return check_jwt_exp


@oauth_blueprint.route('/new_access_token', methods=['POST'])
def get_new_access_token():

    key = def_config.JWT_SECRET_KEY
    table_name = def_config.DYNAMODB_TABLE_NAME
    region_name = def_config.DYNAMODB_REGION_NAME
    aws_access_key_id = def_config.DYNAMODB_ACCESS_KEY_ID
    aws_secret_access_key = def_config.DYNAMODB_SECRET_ACCESS_KEY

    # 헤더에서 auth가 잘 들어오는지 파악하기 위해 로그를 남긴다. 2022-06-06 수정 (by Joon)
    utils.log_util.logger.info("Authorization" + request.headers.get('Authorization'))
    utils.log_util.logger.info("Authorization-refresh" + request.headers.get('Authorization-refresh'))

    access_token = (request.headers.get('Authorization')).split('Bearer ')[1]
    refresh_token = (request.headers.get('Authorization-refresh')).split('Bearer ')[1]

    try:
        # access token은 이미 만료되어 exception 발생하여 refresh token으로 payload 정보 가져온다.
        decoded_token = jwt.decode(refresh_token, key, algorithms='HS256')
    except jwt.ExpiredSignatureError:
        # refresh token 만료시 로그아웃
        return jsonify(respond(3020, "refresh token 만료", "")), 900

    member_id = str(decoded_token['member_id'])
    cust_name = decoded_token['cust_name']
    cust_id = decoded_token['cust_id']
    cust_id_gbn = decoded_token['cust_id_gbn']
    user_id = decoded_token['user_id']

    # check valid 1 : 요청한 access token, refresh token이 동일한지 체크.
    dynamo_result = def_jwt.get_jwt(member_id, table_name, region_name, aws_access_key_id, aws_secret_access_key)

    if dynamo_result["result"] == "fail":
        return jsonify(respond(dynamo_result['result_code'][0], dynamo_result['result_msg'], "")), dynamo_result['result_code'][1]

    dynamo_access_token = dynamo_result['data']['accessToken']
    dynamo_refresh_token = dynamo_result['data']['refreshToken']

    if access_token != dynamo_access_token or refresh_token != dynamo_refresh_token:
        # 비정상적인 접근으로 간주하여 access token, refresh token 폐기
        dynamo_result = def_jwt.delete_jwt(member_id, access_token, table_name, region_name, aws_access_key_id, aws_secret_access_key)
        if dynamo_result["result"] == "fail":
            return jsonify(respond(dynamo_result['result_code'][0], dynamo_result['result_msg'], "")), dynamo_result['result_code'][1]
        return jsonify(respond(3010, "access token 불일치", "")), 900

    # check valid 2 : access token 만료 전 토큰 재발급 요청이 올 경우 refresh token이 탈취되었다고 가정하여 폐기.
    try:
        decoded_token = jwt.decode(access_token, key, algorithms='HS256')

        token_exp = decoded_token["exp"]
        now_timestamp = time.time()
        if now_timestamp < token_exp:
            dynamo_result = def_jwt.delete_jwt(member_id, access_token, table_name, region_name, aws_access_key_id, aws_secret_access_key)
            if dynamo_result["result"] == "fail":
                return jsonify(respond(dynamo_result['result_code'][0], dynamo_result['result_msg'], "")), dynamo_result['result_code'][1]
            return jsonify(respond(3030, "비정상적인 토큰 발급 요청", "")), 900
    except jwt.ExpiredSignatureError:
        # access token 만료.(정상)
        pass

    # create new access token
    new_access_token = def_jwt.get_jwt_access_token(member_id, cust_name, cust_id, cust_id_gbn, user_id)

    # update access token
    dynamo_result = def_jwt.update_jwt(member_id, new_access_token, table_name, region_name, aws_access_key_id, aws_secret_access_key)
    if dynamo_result["result"] == "fail":
        return jsonify(respond(dynamo_result['result_code'][0], dynamo_result['result_msg'], "")), dynamo_result['result_code'][1]

    # response setting
    response = make_response(jsonify(respond(1000, "성공", "")))
    response.headers["Authorization"] = "Bearer " + new_access_token
    response.headers["Authorization-refresh"] = "Bearer " + refresh_token
    response.headers["Access-Control-Expose-Headers"] = "Authorization, Authorization-refresh"  # 브라우저의 자바스크립트에서 헤더 접근 허용

    return response, 200