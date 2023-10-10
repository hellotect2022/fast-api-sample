
import pymysql

class Database:
    def __init__(self):
        self.conn = pymysql.connect(host='localhost', user='dhhan', password='0000', db='fastapi', charset='utf8')

    def selectLastCreateTime(self) -> str:
        cur = self.conn.cursor()
        #sql = "insert into user values(%s, %s, %s, %s, 'Y')"
        sql = '''
        SELECT createTime 
        FROM fastapi.user 
        WHERE useYn = 'Y'
        ORDER BY createTime desc 
        LIMIT 1;
        '''
        cur.execute(sql)
        result = cur.fetchone()
        self.conn.commit()
        self.conn.close()
        if result is None:
            return result
        return result[0]
    
