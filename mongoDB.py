#1.모듈 import
from pymongo import MongoClient
from database import MyClass
import matplotlib.pyplot as plt
from wordcloud import WordCloud

class MyMongo:
    #2.DB에 연결 & 데이터 가져오기
    def conn_db(self):
        client = MongoClient("localhost:27017") #Mongodb연동
        db = client.wm #'wm'라는 db 생성
        collect = db.collect #'collect'라는 컬렉션을 가져오기
        return collect

    #3.db내용 collect에 insert
    def insert_db(self):
        collect = self.conn_db()
        c = MyClass()
        lst = c.select_all()
        collect.drop()
        for i in lst:
            collect.insert_one(i)  #db 내용 'collect'컬렉션에 insert

    # 전체 데이터 조회
    def find_all(self):
        collect = self.conn_db()
        result = collect.find()
        for r in result:
            print(r)

    def s_count(self):
        collect = self.conn_db()
        params = []

        for doc in collect.aggregate([{'$group': {'_id':'$SINGER', 'COUNT': {'$sum':1}}}]):
            params.append((doc['_id'], doc['COUNT']))
            # print((doc['_id'], doc['COUNT']))
        return params

    def l_count(self):
        collect = self.conn_db()
        params = []

        for doc in collect.aggregate([{'$group': {'_id': '$SINGER', 'LIKES': {'$sum': '$LIKES'}}}]):
            params.append((doc['_id'], doc['LIKES']))
            # print((doc['_id'], doc['LIKES']))
        return params

    def singer_visualize(self, lst):
        wc = WordCloud(font_path='c:/Windows/Fonts/malgun.ttf', \
                       background_color="white", \
                       width=500, \
                       height=500, \
                       max_words=50, \
                       max_font_size=100)
        cloud = wc.generate_from_frequencies(dict(lst))
        plt.figure(figsize=(10, 8))
        plt.axis('off')
        plt.imshow(cloud)
        wc.to_file('singer_visualize.gif')

    def like_visualize(self, lst):
        wc = WordCloud(font_path='c:/Windows/Fonts/malgun.ttf', \
                       background_color="white", \
                       width=500, \
                       height=500, \
                       max_words=50, \
                       max_font_size=100)
        cloud = wc.generate_from_frequencies(dict(lst))
        plt.figure(figsize=(10, 8))
        plt.axis('off')
        plt.imshow(cloud)
        wc.to_file('like_visualize.gif')

if __name__ == '__main__':
    c = MyMongo()
    c.insert_db()
    singer = c.s_count()
    c.singer_visualize(singer)
    like = c.l_count()
    c.like_visualize(like)