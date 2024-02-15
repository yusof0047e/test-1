#وارد_کردن_کتابخانه_های_مربوطه
from tkinter import *
from tkinter import ttk
from messagebox import *
from tkinter import messagebox
from sqlalchemy import create_engine, Column,String,Integer,Text
from sqlalchemy.orm import sessionmaker, declarative_base

#دیتا_بیس
engine = create_engine("sqlite:///quencyz.db",echo=True)
base = declarative_base()
sessions = sessionmaker(bind=engine)
session = sessions()

#ساخت_کاربر
class humman(base):
    __tablename__ = "humman2"
    id = Column(Integer,primary_key=True)
    name = Column(String)
    family = Column(String)
    age = Column(Integer)
    def __init__(self, name = "", family = "", age = 0):
        self.name = name
        self.family = family
        self.age = age
#دیتا_بیس
base.metadata.create_all(engine)

#ساخت_و_تعریف_اپ
class app(Frame):
    def __init__(self,master=None):
        super().__init__(master)
        self.master=master
        self.createWiget()
    def createWiget(self):
        self.namevar=StringVar()
        self.familyvar=StringVar()
        self.agevar=StringVar()
        self.txtName=Entry(self.master,textvariable=self.namevar)
        self.txtName.place(x=100,y=50)
        self.txtfamily=Entry(self.master,textvariable=self.familyvar)
        self.txtfamily.place(x=100,y=90)
        self.txtage=Entry(self.master,textvariable=self.agevar)
        self.txtage.place(x=100,y=130)

        self.btnRegister=Button(self.master,text="Register")
        self.btnRegister.bind("<Button-1>",self.onclickRegister)
        self.btnRegister.place(x=100,y=180)
        columns=("c1","c2","c3","c4")
        self.table=ttk.Treeview(self.master,columns=columns,show="headings")
        for i in range(4):
            self.table.column(columns[i],width=60)
        self.table.heading(columns[0],text="id")
        self.table.heading(columns[1],text="name")
        self.table.heading(columns[2],text="family")
        self.table.heading(columns[3],text="age")
        self.table.bind("<Button-1>",self.getSelection)
        self.table.place(x=400,y=50)

        self.btnsearch=Button(self.master,text="search")
        self.btnsearch.bind("<Button-1>", self.onclickSearch)
        self.btnsearch.place(x=400, y=10)
        self.txtsearch = Entry(self.master)
        self.txtsearch.place(x=600, y=10)

        self.btndelete = Button(self.master, text="delete")
        self.btndelete.bind("<Button-1>", self.onclickDelete)
        self.btndelete.place(x=100, y=220)

        self.btnUpdtae = Button(self.master, text="updtae")
        self.btnUpdtae.bind("<Button-1>", self.onclickUpdtae)
        self.btnUpdtae.place(x=100, y=290)

    def onclickRegister(self, e):
            humman1 = humman(name=self.txtName.get(), family=self.txtfamily.get(), age=int(self.txtage.get()))
            self.Register(humman1)
            self.loadAndClear()

    def Register(self, human):
            session.add(human)
            session.commit()

    def insertTable(self, humman):
            self.table.insert('', "end", values=[humman.id, humman.name, humman.family, humman.age])

    def loadAndClear(self):
            self.clearTable()
            alldata = session.query(humman).all()
            for itme in alldata:
                self.insertTable(itme)

    def clearTable(self):
            for item in self.table.get_children():
                s = item
                self.table.delete(s)

    def onclickSearch(self, e):
            if self.txtsearch.get() == "":
                self.loadAndClear()
            else:
                result = self.search(self.txtsearch.get())
                self.clearTable()
                for item in result:
                    self.insertTable(item)

    def search(self, value):
            resultList = []
            alldata = session.query(humman).all()
            for item in alldata:
                if item.name == value or item.family == value or str(item.age) == value:
                    resultList.append(item)
            return resultList

    def getElementByID(self, id):
            return session.query(humman).filter(humman.id == id).first()

    def onclickDelete(self, e):
            select = self.table.selection()
            if select != ():
                id = self.table.item(select)["values"][0]
                data = self.getElementByID(id)
                session.delete(data)
                session.commit()
                self.table.delete(select)

    def getSelection(self, e):
            select = self.table.selection()
            if select != ():
                id = self.table.item(select)["values"][0]
                data = self.getElementByID(id)
                self.namevar.set(data.name)
                self.familyvar.set(data.family)
                self.agevar.set(data.age)

    def onclickUpdtae(self, e):
            select = self.table.selection()
            if select != ():
                id = self.table.item(select)["values"][0]

                humman1 = humman(name=self.txtName.get(), family=self.txtfamily.get(), age=int(self.txtage.get()))
                self.update1(id, humman1)
                self.loadAndClear()

    def update1(self, id, human):
            data = session.query(human).filter(human.id == id).first()
            data.name = human.name
            data.family = human.family
            data.age = human.age
            session.commit()

#ساخت_پنجره
if __name__=="__main__":
    form = Tk()
    form.geometry("%dx%d+%d+%d"%(500,400,200,200 ))
    form.title("ShahedBBS")

    app1 = app(form)


    form.mainloop()
