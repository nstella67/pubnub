from flask import jsonify
import uuid, re, json, datetime
import base64
import string
import random
import os
import hashlib
from datetime import datetime
from collections import OrderedDict
import requests


def func_naver_geocodeAPI(_address:str) :

    # NAVER 키
    NAVER_KEY_ID = "bn8zl3k3sp"
    NAVER_KEY = "4D1b6TzHBjEf8u1xOLwh4st0WvIpxEVHwXqIPNmy"

    URL = "https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?query=" + _address
    header = {
        "content-type": "application/json",
        "X-NCP-APIGW-API-KEY-ID": NAVER_KEY_ID,
        "X-NCP-APIGW-API-KEY": NAVER_KEY,
    }

    # urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # 주소를 던지고 값을 받아온다.
    response = requests.get(URL, headers=header, verify=False, timeout=2)
    return response.text

def func_xy(_address:str):
    res_json = json.loads(func_naver_geocodeAPI(_address))      # 네이버에 넣고 리턴 받은 값을 json으로 저장
    print(res_json)
    if res_json['meta']['totalCount'] > 0:
        xy = (float(res_json['addresses'][0]['x']), float(res_json['addresses'][0]['y']))   #위 경도 값 (127.102893,38.03921) 을 리턴한다.
        return xy
    else :
        return 0

# 부가세 계산모듈 (전체 금액을 넣으면 공급가,부가세가 나옴)
def vat (_total) :
    supply_price = int(round(_total / 1.1, 0))
    vat = _total - supply_price
    return supply_price, vat

def respond(_code: int, _msg: str, _json_data: dict):       # 세번째 인자는 json 형식으로 받아야 한다.
    try:
        rtn_body = {}
        result_info = {}

        rtn_body["result_info"] = result_info
        result_info['code'] = _code
        result_info['msg'] = _msg

        rtn_body['result_data'] = _json_data
        # logger.debug(rtn_body)      # 내보내는 return에 대해 항상 로그를 남긴다.

        return rtn_body

    except Exception as e:
        rtn_body = {"result_info": {"code":2000, "msg":"Respond Error"}, "result_data": ""}
        # logger.debug(rtn_body)
        # logger.debug(str(e))
        return rtn_body, 210

def func_encode(target: str):
    try:
        if(target is None):
            return ''
        else:
            return target.encode('ISO-8859-1').decode('utf-8')
    except Exception as e:
        return target


def is_valid_phone(phone):
    try:
        if len(phone) == 10 or len(phone) == 11:
            return bool(re.match(r'01{1}[016789]{1}[0-9]{7,8}$', phone))
        else:
            return False
    except Exception as e:
        #print(e)
        return False


def is_valid_email(email):
    try:
        return bool(re.match(r'^[0-9a-zA-Z._\-,]+@[0-9a-zA-Z._\-,]+$', email))
    except Exception as e:
        #print(e)
        return False


def is_valid_time(date):
    try:
        now = datetime.datetime.now()
        date_to_compare = datetime.datetime.strptime(date, "%y%m%d%H%M%S%f")
        date_diff = now - date_to_compare
        if date_diff.seconds < 180:
            return True
        else:
            return False
    except Exception as e:
        #print(e)
        return False

def stringToBase64(key):
    return base64.b64encode(key.encode('utf-8'))


# 2021-09-27추가 4를 넣으면 4자리 난수가 발생된다.
def random_digit(length):  # length = 몇자리?
    string_pool = string.digits  # "0123456789"
    result = ""  # 결과 값문자이다.

    for i in range(length):  # 랜덤한 하나의 숫자를 뽑아서, 문자열 결합을 한다.
        result += random.choice(string_pool)

    return result

################################################################
# FILE_NAME : common_util
# FUNCTION_ID : getEdiDate
# DESCRIPTION : 요청시간 생성 함수 -> YYYYMMDDHHMISS
################################################################
def getEdiDate():
    YYYYmmddHHMMSS = datetime.today().strftime("%Y%m%d%H%M%S")
    return str(YYYYmmddHHMMSS)

################################################################
# FILE_NAME : common_util
# FUNCTION_ID : getSignData
# DESCRIPTION : 데이터 암호화
################################################################
def getSignData(str):
    encoded_str = str.encode()
    EncryptData = hashlib.sha256(encoded_str).hexdigest()
    return EncryptData

################################################################
# FILE_NAME : common_util
# FUNCTION_ID : getMobileNumber
# DESCRIPTION : 핸드폰번호속 숫자만 추출
################################################################
def getMobileNumber(str):
    re_str = str.replace('-', '')
    return re_str

# # DB에서 토큰을 가져온다. 하루에 한번 저장한다.
# def get_token():
#     try:
#         db_class = mysql_dbconn.Database()
#         # DB에서 최근걸 Select 한다.
#         sql = f"SELECT *" \
#               f" FROM AUTH_TOKEN" \
#               f" WHERE IDX = 1;"
#
#         row = db_class.executeOne(sql)      # 데이터가 있으면 {   }로 들어온다. excuteOne 이기 때문이다. #데이터가 없으면 tupe로 반환한다.
#         print("row:", row)
#
#         if row == None:                   # 0 이면 데이터가 없는 것이다.
#             db_class.close()
#             return jsonify(respond(1020, "토큰 데이터가 존재하지 않습니다","")), 200
#
#         db_class.close()
#         return row['TOKEN']
#
#     except Exception as e:
#         db_class.close()
#         return jsonify(respond(1010, str(e), "")), 210    # status=210으로 하고

################################################################
# FILE_NAME : common_util
# FUNCTION_ID : getOrderStatusName
# DESCRIPTION : Order Status Name 추출
################################################################
def getOrderStatusName(code):

    if code == '00':
        name = '저장'
    elif code == '10':
        name = '대기'
    elif code == '20':
        name = '접수완료'
    elif code == '30':
        name = '배차완료'
    elif code == '40':
        name = '운행'
    elif code == '45':
        name = '픽업'
    elif code == '50':
        name = '완료'
    elif code == '60':
        name = '취소'
    elif code == '99':
        name = '예약'

    return name

################################################################
# FILE_NAME : common_util
# FUNCTION_ID : getPayGbnName
# DESCRIPTION : 결제 방법 이름 추출
################################################################
def getPayGbnName(code):

    if code == '1':
        name = '현금선불'
    elif code == '2':
        name = '현금착불'
    elif code == '3':
        name = '신용카드'
    else:
        name = ''

    return name

# list와 키를 넣으면 해당 키를 기준으로 dict를 추출해온다.
def build_dict(seq, key):
    return dict((d[key], dict(d, index=index)) for (index, d) in enumerate(seq))
    # 결과값 : {'dog': {'access_id': 'dog', 'channel': '#chdog2', 'index': 3}, 'cat': {'access_id': 'cat', 'channel': '#chcat', 'index': 1}, 'rabbit': {'access_id': 'rabbit', 'channel': '#chrabbit', 'index': 2}}
