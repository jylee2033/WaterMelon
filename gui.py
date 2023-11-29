import tkinter
import tkinter as ttk
from tkinter import *
from tkinter.ttk import *
from tkinter import ttk
from database import MyClass
from mongoDB import MyMongo
import sys
import urllib
import csv
sys.setrecursionlimit(5000)
class Chang(tkinter.Tk):
    def __init__(self, parent) :
        tkinter.Tk.__init__(self, parent)
        self.iconbitmap('C:/Users/Playdata/Downloads/watermelon.ico')
        self.parent = parent
        self.searching()
        self.title('WATERMELON')
        self.geometry('750x1000')
        self.frame()
        self.Mydb = MyClass()
    def searching(self):
        # 기간설정버튼
        period_option = LabelFrame(self, text="검색하실 기간을 설정하세요 ")
        period_option.pack(fill='x', padx=5, pady=5, ipady=5)
        day_format = ["일간", "주간", "월간"]
        day_format = ttk.Combobox(period_option, state="readonly", values=day_format, width=20)
        # combobox 값 return
        def btncmd():
            day = day_format.get()
            MyClass().create_table()
            MyClass().insert_m(day)
            c = MyMongo()
            c.insert_db()
            singer = c.s_count()
            c.singer_visualize(singer)
            like = c.l_count()
            c.like_visualize(like)

        # for i in day_format:
        day_format.current(0)
        day_format.pack(side="left", padx=5, pady=5)
        button_period = tkinter.Button(period_option, bg='lightpink', padx=5, pady=5, width=12, text='기간설정', command = btncmd)
        button_period.pack(side="right", padx=5, pady=5)
        # 워드클라우드
        word_frame = LabelFrame(self, text="Wordcloud")
        word_frame.pack(fill='x', padx=3, pady=3)
        btn_image = tkinter.Button(word_frame, bg='ivory', padx=5, pady=5, text="순위권 내 가수", width=12, command=self.pop_up)
        btn_image.pack(side="right", padx=5, pady=5)
        btn_image2 = tkinter.Button(word_frame, bg='ivory', padx=5, pady=5, text="가수별 좋아요 수", width=12, command=self.pop_up2)
        btn_image2.pack(side="right", padx=5, pady=5)

        # 검색창
        search_option = LabelFrame(self, text="가수 혹은 제목을 입력하세요 ")
        search_option.pack(fill='x',padx=5, pady=5, ipady=5)
        self.entryValue = tkinter.StringVar()
        self.entry = tkinter.Entry(search_option, textvariable=self.entryValue)
        self.entry.pack(fill = 'x', padx = 5, pady =3, ipady =3)
        self.entry.bind('<Return>', self.onPressEnter)
        # 검색버튼
        button_add_item = tkinter.Button(search_option,bg='lightpink',padx=5, pady=5, width = 12, text='검색', command = self.onButtonClick or self.onPressEnter )
        #print(button_add_item,'<')
        button_add_item.pack(side="right",padx=5, pady=5)
        #print(day_format.get())
        #라벨창
        self.labelValue = tkinter.StringVar()
        self.label = tkinter.Label(self, fg='IndianRed1', bg='lightgreen', textvariable=self.labelValue)
        self.label.pack(fill = 'x', padx = 5, pady =3, ipady =3)
        self.entryValue.set(' ')
        self.labelValue.set(' ')
        self.entry.focus_set()
        self.entry.select_range(0, tkinter.END)
        # 검색결과 프레임
        tree_frame = LabelFrame(self , text="검색결과")
        tree_frame.pack(fill='x', padx=3, pady=3)
        self.tree = ttk.Treeview(self)
        tree_add_item = tkinter.Button(tree_frame,bg='ivory', padx=5, pady=5, width = 12, text='조회', command = self.treeview)
        tree_add_item.pack(side="right", padx=5, pady=5)
        tree_add_item = tkinter.Button(tree_frame,bg='ivory', padx=5, pady=5, width=12, text='새로고침', command=self.treedelete)
        tree_add_item.pack(side="right", padx=5, pady=5)
        # 컬럼 수
        self.tree["columns"] = ("one","two","three","four","five","six","seven")
        self.tree.heading("#1", text="순위")
        self.tree.heading("#2", text="제목")
        self.tree.heading("#3", text="가수")
        self.tree.heading("#4", text="앨범")
        self.tree.heading("#5", text="좋아요")
        self.tree.heading("#6", text="뮤비")
        self.tree.heading("#7", text="앨범자켓")
        self.tree.column("#0", width=1)
        self.tree.column("#1", width=50)
        self.tree.column("#2", width=90)
        self.tree.column("#3", width=90)
        self.tree.column("#4", width=100, anchor="w")
        self.tree.column("#5", width=100, anchor="w")
        self.tree.column("#6", width=100, anchor="w")
        self.tree.column("#7", width=100, anchor="w")
        self.tree.pack(expand=True,fill='both')
        #실행
        btn_close = tkinter.Button(self,bg='ivory', padx=5, pady=5, text="닫기", width=12, command=self.quit)
        btn_close.pack(side="right", padx=5, pady=5)
        btc_start = tkinter.Button(self, bg='ivory', padx=5, pady=5, text="csv file 저장", width=12, command=self.save_text)
        btc_start.pack(side="right", padx=5, pady=5)
        btn_start = tkinter.Button(self,bg='ivory', padx=5, pady=5, text="사진저장", width=12, command=self.save_pic)
        #만든이
        btn_start.pack(side="right", padx=5, pady=5)
        btn_credit = tkinter.Button(self,bg='ivory', padx=5, pady=5, text="만든이들", width=12, command=self.credit)
        btn_credit.pack(side="right", padx=5, pady=5)

    def get_opr(self):
        return self.opr
    # 검색시 기능 function
    def onPressEnter(self, event):
        self.labelValue.set(self.entryValue.get() + '를 조회하시겠어요?')
        self.opr = self.entryValue.get()
        self.entryValue.set('')
    # 검색시 기능 function
    def onButtonClick(self):
        self.labelValue.set(self.entryValue.get() + '를 조회하시겠어요?')
        self.opr = self.entryValue.get()
    #검색창 Values
    def treeview(self):
        j = self.Mydb.find_all(self.opr)
        for i in j:
           self.tree.insert('','end',values= i)
    #사진 저장
    def save_pic(self):
        j = self.Mydb.find_all(self.opr)
        lst = []
        for i in range(0,len(j)):
            lst.append(j[i][6])
        for idx, p in enumerate(lst,1):
            # 다운 받을 폴더 경로 입력
            urllib.request.urlretrieve(p, "c:/image/" + str(idx) + ".jpg")
    #csv file 저장
    def save_text(self):
        f = open('WaterMelon.csv', 'w', encoding='utf-8', newline='')
        wr = csv.writer(f)
        j = self.Mydb.find_all(self.opr)
        lst = []
        for i in range(0,len(j)):
            lst.append(j[i])
        for i in lst :
            wr.writerow([i])
        f.close()
    def treedelete(self): # <---treeview 삭제...
        for i in self.tree.get_children():
            self.tree.delete(i)
        self.tree.update()
    # Word cloud 저장
    def singer_word(self):
        img = PhotoImage(file='singer_visualize.gif')  # <----여기에다가 클라우드 들어가는 경로 넣으면 됨!!
        lbl = Label(image=img)
        lbl.image = img
        lbl.pack(padx=1, pady=1,expand=True,fill='x')
    def like_word(self):
        img = PhotoImage(file='like_visualize.gif')  # <----여기에다가 클라우드 들어가는 경로 넣으면 됨!!
        lbl = Label(image=img)
        lbl.image = img
        lbl.pack(padx=1, pady=1,expand=True,fill='x')

    def pop_up(self):
        self.pop_up = Toplevel()
        self.pop_up.title("순위권 내 가수")
        self.f = Frame(self.pop_up, height=500, width=550, cursor="hand2")
        self.f.pack()
        self.photo = PhotoImage(file='singer_visualize.gif')
        self.pop_image = Label(self.f, cursor="hand2", image=self.photo)
        self.pop_image.image = self.photo
        self.pop_image.place(x=23, y=0)
        self.pop_up.mainloop()
        self.reload()

    def pop_up2(self):
        self.pop_up = Toplevel()
        self.pop_up.title("가수별 좋아요 수")
        self.f = Frame(self.pop_up, height=500, width=550, cursor="hand2")
        self.f.pack()
        self.photo = PhotoImage(file='like_visualize.gif')
        self.pop_image = Label(self.f, cursor="hand2", image=self.photo)
        self.pop_image.image = self.photo
        self.pop_image.place(x=23, y=0)
        self.pop_up.mainloop()
        self.reload()

    def credit(self):
        credit = Toplevel(self)
        lb = Label(credit, text="김유진, 박민회, 이정훈, 이주영, 신정훈")
        lb.pack()

if __name__ == '__main__':
    m1 = Chang(None)
    m1.resizable(True,True)
    m1.mainloop()