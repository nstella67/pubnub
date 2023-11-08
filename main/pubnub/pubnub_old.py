from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory, PNOperationType
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

pnconfig = PNConfiguration()

pnconfig.subscribe_key = 'sub-c-6bb21ba3-6686-49fc-adc9-8fd00ae6f120'
pnconfig.publish_key = 'pub-c-98390fc2-1fe0-4bac-a497-67025c63d17d'
pnconfig.secret_key = "sec-c-NDk1OTY5YjQtMGVlYi00YTVmLTgxMjAtMjIyMmFkMjExNzcw"
pnconfig.user_id = "bansook@gmail.com"     # uuid는 쓰지 않는다.
pn = PubNub(pnconfig)

def my_publish_callback(envelope, status):
    print("envelope:", envelope)
    # Check whether request successfully completed or not
    if not status.is_error():
        print("퍼블리싱이 잘 되었습니다")
        pass  # Message successfully published to specified channel.
    else:
        print("퍼블리싱에 문제가 있습니다")
        pass  # Handle message publish error. Check 'category' property to find out possible issue
        # because of which request did fail.
        # Request can be resent using: [status retry];


class MySubscribeCallback(SubscribeCallback):
    # 서버로부터 어떤 presense를 받았을 경우 작동한다.본인 것은 알수가 없다.
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
        print("status", status)
        if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
            pass  # This event happens when radio / connectivity is lost

        elif status.category == PNStatusCategory.PNConnectedCategory:
            # Connect event. You can do stuff like publish, and know you'll get it.
            # Or just use the connected event to confirm you are subscribed for
            # UI / internal notifications, etc
            pubnub.publish().channel('hello').message('Hello world!').pn_async(my_publish_callback)

        elif status.category == PNStatusCategory.PNDisconnectedCategory:
            pubnub.publish().channel('hello').message('disconnected!').pn_async(my_publish_callback)

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
        print(message.message)

pn.add_listener(MySubscribeCallback())
pn.subscribe().channels('hello').with_presence().execute()