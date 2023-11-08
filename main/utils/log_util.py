import logging
from logging import Formatter, handlers           # logging에는 Formatter가 있다.

# Logging Level
# DEBUG.txt(10) <--------DEBUG 수준 (아주 정교한 모든 LOG 10~50)
# INFO.txt(20)
# WARNING.txt(30)
# ERROR.txt(40)
# CRITICAL.txt(50)

# logger 만드는 순서
# 1) Handler 만들기
# 2) Handler에 SetFormat
# 3) logger 만들기 (getLogger)
# 4) 핸들러 등록하기
# 5) logger에 setLevel

def make_logger(_name,_filename,_max_bytes,_backup_count):

    # 각 로거는 이름을 다르게 만들어야 분리된다.
    logger = logging.getLogger(_name)

    # 스트림핸들러
    stream_handler = logging.StreamHandler()  # stream handler 는 logging 에서 직접 불러온다.
    formatter = logging.Formatter('stream %(asctime)s %(levelname)s: %(message)s [%(filename)s:%(funcName)s:%(lineno)d]')
    stream_handler.setFormatter(formatter)

    # 로테이팅핸들러
    LOGGING_FORMAT = '%(asctime)s %(levelname)s: %(message)s [%(filename)s:%(lineno)d]'
    rotating_handler = logging.handlers.RotatingFileHandler(filename=_filename, mode='a',
                                                            maxBytes=_max_bytes,
                                                            backupCount=_backup_count, encoding='utf-8')
    rotating_handler.setFormatter(Formatter(LOGGING_FORMAT))

    # Adding Stream Handler, Rotating Handler
    logger.addHandler(stream_handler)
    logger.addHandler(rotating_handler)

    logger.setLevel(logging.DEBUG)

    return logger


logger = make_logger("logger", "debug.log", 1000000, 5)                         # 일반 로그용
logger_order = make_logger("logger_order", "debug_order.log", 1000000, 10)      # ORDER 로그용




