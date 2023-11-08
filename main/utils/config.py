############################ MOMO QUICK API URL ############################
# TEST
API_BASE_URL = "https://localhost:5000"
API_CLIENT_URL = "https://www.macross.kr"

'''
# REAL
API_BASE_URL = "http://"
API_CLIENT_URL = "http://"
'''
############################ DB INFO ############################

# DEV DB - Alpha
DB_HOST = "192.168.0.159"
DB_USR = "admin"
DB_PASSWORD = "mintquick"
DB_DATABASE = "sd"
DB_PORT = 1502      # 3306이 아니라 1502이다.

'''
# DEV DB
DB_HOST = "qcluster.cluster-c4ijdhnilwqv.us-east-1.rds.amazonaws.com"
DB_USR = "admin"
DB_PASSWORD = "mintquick"
DB_DATABASE = "qdb"
DB_PORT = 3306
'''

'''
# REAL DB
DB_HOST = "quick-cluster-instance-1.cmvd8jvvxhjw.ap-northeast-2.rds.amazonaws.com"
DB_USR = "admin"
DB_PASSWORD = "mintquick"
DB_DATABASE = "qdb"
DB_PORT = 3306
'''


############################ Popbill Info ############################
# KAKAO
POPBILL_KAKAO_LINK_ID = 'LOGIALL'
POPBILL_KAKAO_SECRET_KEY = 'yMPUQX7mXDOkEnbOyErplv4qrheJ3oxupsTthx06gJg='

# SMS
POPBILL_SMS_LINK_ID = 'LOGIALL'
POPBILL_SMS_SECRET_KEY = 'yMPUQX7mXDOkEnbOyErplv4qrheJ3oxupsTthx06gJg='

POPBILL_CORPNUM = '5738600351'
POPBILL_USER_ID = 'sgdr8888'
# POPBILL_SENDER = '16614030' # 모모퀵
POPBILL_SENDER = '16440927' # 모모퀵물류
POPBILL_SENDER_NAME = '모모퀵'

############################## DynamoDB / JWT Info ####################################

# TEST
JWT_SECRET_KEY = "NGPGgy2IplUz3IMbf4f2tLZa5gD1KkdY"                      # JWT 암복호화 비밀키
DYNAMODB_TABLE_NAME = 'sd_login_manager'                                        # test서버 dynamoDB
DYNAMODB_REGION_NAME ='us-east-1'                                        # test서버 dynamoDB region
DYNAMODB_ACCESS_KEY_ID = 'AKIAX2OIAPJO75IVJSE2'                          # test서버 dynamoDB access key
DYNAMODB_SECRET_ACCESS_KEY = 'mQ4hIuHDaFkLTDD3EDvWu76aMLN4UqcEOf1AsStu'  # test서버 dynamoDB secret key

# # REAL
# JWT_SECRET_KEY = "NGPGgy2IplUz3IMbf4f2tLZa5gD1KkdY"                      # JWT 암복호화 비밀키
# DYNAMODB_TABLE_NAME = 'momoQuick'                                        # real서버 dynamoDB
# DYNAMODB_REGION_NAME ='ap-northeast-2'                                   # real서버 dynamoDB region
# DYNAMODB_ACCESS_KEY_ID = 'AKIATKY4QBVIPUH6DX75'                          # real서버 dynamoDB access key
# DYNAMODB_SECRET_ACCESS_KEY = 'xz8ROIRZy0GXMX8QdrV2eQvfp4BzKeg1KaKHOq6h'  # real서버 dynamoDB secret key


############################# hash info ################################
KEY_STRETCHING = 10  # 2의 10승만큼 해시 반복


##############################
# Pubnub Information
##############################
# bansook@gmail.com , Demo Keyset
PUBNUB_SUBSCRIBE_KEY = "sub-c-6bb21ba3-6686-49fc-adc9-8fd00ae6f120"
PUBNUB_PUBLISH_KEY = "pub-c-98390fc2-1fe0-4bac-a497-67025c63d17d"
PUBNUB_SECRET_KEY = "sec-c-NDk1OTY5YjQtMGVlYi00YTVmLTgxMjAtMjIyMmFkMjExNzcw"





