import pymysql
from config import Config, Lake

# DB config 정보
db_type = Config['db_type']
username = Config['username']
password = Config['password']
host = Config['host']
port = Config['port']
database1 = Lake['database1']
database2 = Lake['database2']
database3 = Lake['database3']

# symbol 뽑기
def Symbols():
    # DB 연결 (symbol list는 stock DB에 있음)
    conn = pymysql.connect(host=host, user=username, password=password, database=database2, port=int(port))
    try:
        with conn.cursor() as curs:  # 커서 생성
            sql = 'SELECT symbol from symbol_list'
            curs.execute(sql)
            result = curs.fetchall()
    finally:
        conn.close()  # 연결 닫기

    # 튜플 내의 값만 추출하여 1차원 리스트로 변환
    result_list = [row[0] for row in result]

    return result_list

