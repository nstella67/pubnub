from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory, PNOperationType
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from main.utils.common_util import respond
from main.utils.log_util import logger

'''
---------------------------------------------
테스팅 : 사용자로 부터 계속 입력(input) 위한 루틴이다.
---------------------------------------------
'''
from threading import Thread
def send():
    while True:
        input_data = input("what is your message?")
        pn.pubnub.publish().channel("hello").message({'from': pn.pubnub.uuid, 'content': input_data}).pn_async(pn.my_publish_callback)
th = Thread(target = send)
th.start()





'''
pubnub의 메시지 구조는 다음과 같다.
{
  "channel": "agency.2",
  "actualChannel": null,
  "subscribedChannel": "agency.2",
  "timetoken": "16715260383325853",
  "publisher": "bansook@gmail.com",
  "message": {
    "result_info": {
      "code": 1000,
      "msg": "정상"
    },
    "result_data": "HI!!!!!"
  }
}
'''

pnconfig = PNConfiguration()
pnconfig.subscribe_key = 'sub-c-6bb21ba3-6686-49fc-adc9-8fd00ae6f120'   # DemoKey
pnconfig.publish_key = 'pub-c-98390fc2-1fe0-4bac-a497-67025c63d17d00000'     # DemoKey
pnconfig.secret_key = "sec-c-NDk1OTY5YjQtMGVlYi00YTVmLTgxMjAtMjIyMmFkMjExNzcw"
pnconfig.user_id = "bansook@gmail.com"     # uuid는 쓰지 않는다. publisher로 표기됨
pn = PubNub(pnconfig)

def my_publish_callback(envelope, status):
    print("envelope:", envelope)
    # Check whether request successfully completed or not
    if not status.is_error():
        print("퍼블리싱이 잘 되었습니다")
    else:
        print("퍼블리싱에 문제가 있습니다")

class MySubscribeCallback(SubscribeCallback):
    # 서버로부터 어떤 presence를 받았을 경우 작동한다. 본인 것은 알수가 없다.
    def presence(self, pubnub, presence):
        # Can be join, leave, state-change, timeout, or interval
        print("Presence event: %s" % presence.event)

        # The channel to which the message was published
        print("Presence channel: %s" % presence.channel)

        # Number of users subscribed to the channel
        print("Presence occupancy: %s" % presence.occupancy)

        # User state
        print("Presence state: %s" % presence.state)

        # Channel group or wildcard subscription match, if any
        print("Presence subscription: %s" % presence.subscription)

        # UUID to which this event is related
        print("Presence UUID: %s" % presence.uuid)

        # Publish timetoken
        print("Presence timestamp: %s" % presence.timestamp)

        # Current timetoken
        print("Presence timetoken: %s" % presence.timetoken)

        # List of users that have joined the channel (if event is 'interval')
        joined = presence.join

        # List of users that have left the channel (if event is 'interval')
        left = presence.leave

        # List of users that have timed-out off the channel (if event is 'interval')
        timed_out = presence.timeout

    # 내 자신에게 이벤트가 일어 났을 때를 의미한다.
    def status(self, pubnub, status):
        print(pubnub)
        print("status:", status)
        if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
            pass  # This event happens when radio / connectivity is lost

        elif status.category == PNStatusCategory.PNConnectedCategory:
            # Connect event. You can do stuff like publish, and know you'll get it.
            # Or just use the connected event to confirm you are subscribed for
            # UI / internal notifications, etc
            print("connected!!")
            pubnub.publish().channel('drive').message('Hello world!').pn_async(my_publish_callback)

        elif status.category == PNStatusCategory.PNDisconnectedCategory:
            pubnub.publish().channel('drive').message('disconnected!').pn_async(my_publish_callback)

        elif status.category == PNStatusCategory.PNReconnectedCategory:
            pass
            # Happens as part of our regular operation. This event happens when
            # radio / connectivity is lost, then regained.
        elif status.category == PNStatusCategory.PNDecryptionErrorCategory:
            pass
            # Handle message decryption error. Probably client configured to
            # encrypt messages and on live data feed it received plain text.

    def message(self, pubnub, message):
        # Handle new message stored in message.message
        print("Message channel: %s" % message.channel)
        print("Message subscription: %s" % message.subscription)
        print("Message timetoken: %s" % message.timetoken)
        print("Message payload: %s" % message.message)
        print("Message publisher: %s" % message.publisher)
        print("Subscribed Message: %s" % message.message)


# ---------------------------------------------------
# Method for Using
# ---------------------------------------------------


def my_callback_function(_envelope, _status):   # callback은 두개 인자를 써준다.

    # Check whether request successfully completed or not
    if not _status.is_error():
        logger.debug("[envelope] %s [status] %s" % (_envelope, "Well Published"))
    else:
        logger.debug("[envelope] %s [status] %s because of code %s" % (_envelope, "Wrong Published", str(_status.category)))  # 결과: [envelope] None [status] Wrong Published because of code 11 [pubnub.py:my_callback_function:151]

# payload에 맞추어 publish한다.(전체에게 메시지를 보낼 수도 있다)
def publish_to(_payload: dict):

    logger.debug("[publish_to 진입]: %s", _payload)

    try :
        from_member_type = _payload["from_member_type"]     # 보내는 사람 멤버형태 (agency,driver, server(프로그램에 의한 자동 idx=0) ,manager,company플사)
        from_idx = _payload["from_idx"]                     # 0은 서버를 의미한다.
        to_member_type = _payload["to_member_type"]         # 받는 사람 멤버형태
        to_idx = _payload["to_idx"]                         # 0은 전체를 의미한다.
        data = _payload["data"]

        # 보낼 채널 결정
        if int(to_idx) == 0:    # 0 이면 해당 type 전체에 메시지를 보낸다.
            send_channel = to_member_type + ".0"
        else:
            send_channel = to_member_type + "." + str(to_idx)   # 특정인에게만 메시지를 보낸다.

        # 보낼 내용 결정
        rtn_body = {}
        rtn_body['from_member_type'] = from_member_type
        rtn_body['from_idx'] = from_idx
        rtn_body['data'] = data

        # 메시지 보내기
        pn\
            .publish()\
            .channel(send_channel)\
            .message(respond(1000, "정상", rtn_body))\
            .pn_async(my_callback_function)     # callback은 인자가 없는 형태로 써준다.

    except Exception as e:
        logger.debug(e)  # 항상 로그를 남긴다.
