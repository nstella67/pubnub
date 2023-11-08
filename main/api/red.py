from flask import Blueprint, request,render_template, current_app,jsonify
from ..utils.common_util import respond
from main.pubnub.pubnub import publish_to

red_blueprint = Blueprint('red', __name__, url_prefix='/red')       # url_prefix를 해준다.


# # jwt에 저장해야 할 정보
# # manager_idx,agency_idx,
# # 구독할 채널 list
# #
#
# # 본사여부 본사 =1 , 일반 =0
# # group장 여부 그룹장= 1 , 일반 =0
# # DB 설계할때 group_idx를 만든다.
#
# # 모든 클라이언트에 메시지를 보낸다. 모든 클라이언트에 subscribe (mamanger.0.0)을 등록하여 준다.
# def publish_all(_data: dict):
#     print("publish_all작동")
#     current_app.pn \
#         .publish() \
#         .channel('manager.0.0') \
#         .message(_data) \
#         .pn_async(my_function)
#
#
# # 해당 agency list에 publish한다.
# def publish_agency(_agency_idx_list: list, _data: dict):
#     print("publish_agency작동")
#     for agency in _agency_idx_list:
#         current_app.pn\
#             .publish()\
#             .channel()\
#             .message({'from': current_app.pn.uuid, 'content': "red/send에서 보냅니다."})\
#             .pn_async(my_function)
#
#
# # 해당 list에 publish한다. 1명인 경우도 가능
# def publish_user(_user_list: list):
#     print("publish_user작동")
#
#
#
# @red_blueprint.route('/',methods=['GET','POST'])
# def index():
#     print("/red 진입")
#     return render_template('index.html')
#
# @red_blueprint.route('/test',methods=['GET','POST'])
# def test():
#     print("red/test 진입")
#     return "data"
#
# @red_blueprint.route('/publish', methods=['GET', 'POST'])
# def publish():
#     print("red/publish_to 진입")
#     payload = {
#         "from_member_type": "agency",     # 멤버형태 (agency,driver, server(프로그램에 의한 자동 idx=0) ,manager,company플사)
#         "from_idx": 2,
#         "to_member_type": "agency",
#         "to_idx": 0,
#         "data": "HI!!!!!"
#     }
#     print(payload)
#     publish_to(payload)
#     return "publish_to called"
#
#
# @red_blueprint.route('/send_all', methods=['GET', 'POST'])
# def send_all():
#     data={"from":"server","conetent":"send all에서 보냅니다."}
#     print("red/send_all 진입")
#     publish_all(data)
#     return "publish send_all 됨"
#
# @red_blueprint.route('/send_user', methods=['GET', 'POST'])
# def send_user():
#     print("red/send_user 진입")
#     req = request.get_json()
#     print(req)
#     # 보낼 메시지 만들기
#     rtn_body = {}
#     rtn_body['data'] = req['data']
#     for item in req['user_list']:
#         print(item)
#         current_app.pn\
#             .publish()\
#             .channel("manager." + str(item['user_idx']))\
#             .message(respond(1000, "정상", rtn_body))\
#             .pn_async(my_function)
#     return "publish send_user 됨"
#
# @red_blueprint.route('/insert_order', methods=['GET', 'POST'])
# def insert_order():
#     print("red/insert_order 진입")
#     req = request.get_json()
#     print(req)
#
#     # jwt를 decoding 한다. 구독할 agency_idx를 얻어낸다.
#     agency_idx = 3
#
#     # 보낼 채널을 결정한다.
#     send_channel = "agency." + str(agency_idx)
#     print(send_channel)
#
#     # 보낼 메시지 만들기
#     rtn_body = {}
#     rtn_body['data'] = req['data']
#     print(respond(1000, "정상", rtn_body))
#     # 본인이 속한 agency_idx에 메시지를 publish 한다. 그러면 본인은 물론 alience된 모든 구독자가 받을 수 있다.
#     # message는 json형태로 형식에 맞추어 넣어야 함
#     current_app.pn\
#         .publish()\
#         .channel(send_channel)\
#         .message(respond(1000, "정상", rtn_body))\
#         .pn_async(my_function)
#
#     return "insert order에서 publish 됨"
#
# def my_function(_env, _sta):      # 콜백 함수는 두개의 인자를 가져야 한다.
#     print("callback 함수(my_function)를 호출 했습니다")
#
# @red_blueprint.route('/send',methods=['GET','POST'])
# def send():
#     print("red/send 진입")
#     publish_all()
#     # current_app.pn.publish().channel("hello").message({'from': current_app.pn.uuid, 'content': "red/send에서 보냅니다."}).pn_async(my_function)       # publish된 후 현재 파일에 있는 함수를 호출할 수도 있다.
#     return 'Hello, Red!'
#
# @red_blueprint.route('/group',methods=['GET','POST'])
# def group():
#     print("red/group 진입")
#     current_app.pn.add_channel_to_channel_group() \
#         .channels(["chats.room1", "chats.room2", "alerts.system"]) \
#         .channel_group("cg_user123") \
#         .sync()
#     # current_app.pn.publish().channel("hello").message({'from': current_app.pn.uuid, 'content': "red/send에서 보냅니다."}).pn_async(my_function)       # publish된 후 현재 파일에 있는 함수를 호출할 수도 있다.
#     return 'Group is Setted'