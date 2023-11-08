import main.utils.dbconn as mysql_dbconn
from main.utils.log_util import logger

# --------------------------------------------------------
# agency_idx를 가져와서 오더를 쉐어하는 agency_idx를 리턴한다.
# --------------------------------------------------------

def dao_get_subscribe_channel(_agency_idx: int):

    try:
        db_class = mysql_dbconn.Database()

        sql = f"SELECT SHARE_AGENCY_IDX " \
              f"FROM order_share_info " \
              f"WHERE AGENCY_IDX ='{_agency_idx}'" \

        logger.debug(sql)  # 직접 정의하고 써줘야 해당 라인에서 에러를 감지할 수 있다. [dao_login.py:17] <-- 이렇게 라인이 표시됨

        row = db_class.executeOne(sql)  # row로 쓴다.
        db_class.close()

    except Exception as e:

        logger.debug(e)  # 항상 로그를 남긴다.

        if db_class != None and db_class.db.open:
            db_class.rollback()
            db_class.close()
        raise RuntimeError(str(e))  # 함수를 부른 상위 콜에 상위에 지금 나온 에러를 그대로 전달한다.

    return row