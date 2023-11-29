import cx_Oracle
from crawling import Crawl

class MyClass:
    def __init__(self):
        self.dsn = cx_Oracle.makedsn("localhost", 1521, 'xe') # 오라클 주소를 기입한다.
        self.db = cx_Oracle.connect('SCOTT', 'TIGER', self.dsn) # 오라클 접속 유저 정보
        self.cur = self.db.cursor()

    def create_table(self):
        self.sql_cmd = "CREATE TABLE MUSICCHART (RANK INT, TITLE VARCHAR2(4000), SINGER VARCHAR2(4000), ALBUM VARCHAR2(4000), " \
                       "LIKES VARCHAR2(4000), MV VARCHAR2(4000), URL VARCHAR2(4000))"
        try:
            self.cur.execute(self.sql_cmd)
        except:
            self.cur.execute("DROP TABLE MUSICCHART")
            self.cur.execute(self.sql_cmd)

    def insert_m(self, para):
        items = Crawl.crawling(para)
        i = 1  # 랭킹

        for item in items:
            query = "INSERT INTO MUSICCHART VALUES (" + str(i) + ",'" + item[0] + "','" + item[1] + "','" + item[2] \
                    + "','" + item[3] + "','" + item[4] + "','" + item[5] + "')"
            self.cur.execute(query)
            i += 1

        self.db.commit()

    def find_all(self,para):
        self.cur.execute("SELECT * FROM MUSICCHART WHERE SINGER = '"+str(para)+"' or TITLE ='"+str(para)+"' ORDER BY RANK ASC")
        result = self.cur.fetchall()
        lst = []
        for row in result:
            for i in str(row).split():
                if para in i:
                    lst.append(row)
        return lst

    def select_all(self):
        self.cur.execute("SELECT * FROM MUSICCHART ORDER BY RANK")
        result = self.cur.fetchall()
        lst = []
        for row in result:
            dictionary = {}
            dictionary['RANK'] = row[0]
            dictionary['TITLE'] = row[1]
            dictionary['SINGER'] = row[2]
            dictionary['ALBUM'] = row[3]
            dictionary['LIKES'] = int(row[4].replace(',',''))
            dictionary['MV'] = row[5]
            dictionary['IMAGE'] = row[6]
            lst.append(dictionary)
        return lst

    def drop_table(self):
        self.cur.execute("DROP TABLE MUSICCHART")
        self.cur.close()

    def delete_table(self):
        self.cur.execute("DELETE MUSICCHART")
        self.cur.close()

if __name__ == '__main__':
    m = MyClass()
    m.select_all()
