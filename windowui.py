import tkinter as tk
from pymysql import *
import pickle
from tkinter import messagebox


def editbook():

    def appendbook_button():
        try:
            eb = entry_bookname.get()
            ea = entry_author.get()
            ec = entry_company.get()
            ep = entry_place.get()
            es = entry_sumbook.get()
            el = entry_lendbook.get()
            conn = connect(host='localhost', port=3306, user='root', password='password', database='pythonsql', charset='utf8mb4')
            cursor = conn.cursor()
            cursor.execute('insert into library (bookname, author, company, place, sumbook, lendbook) values ("%s", "%s", "%s", "%s", "%s", "%s");' % (eb, ea, ec, ep, es, el))
            conn.commit()
            tk.messagebox.showinfo(title='Hi', message='图书添加成功！')
        except Exception as e:
            pass
        finally:
            entry_bookname.delete('0', 'end')
            entry_author.delete('0', 'end')
            entry_company.delete('0', 'end')
            entry_place.delete('0', 'end')
            entry_sumbook.delete('0', 'end')
            entry_lendbook.delete('0', 'end')
            cursor.close()
            conn.close()


    def revisebook_button():
        try:
            eb = entry_bookname.get()
            ea = entry_author.get()
            ec = entry_company.get()
            ep = entry_place.get()
            es = entry_sumbook.get()
            el = entry_lendbook.get()
            conn = connect(host='localhost', port=3306, user='root', password='password', database='pythonsql')
            cursor = conn.cursor()
            cursor.execute('update library set bookname="%s", author="%s", company="%s", place="%s", sumbook="%s", lendbook="%s" where place="%s";' % (eb, ea, ec, ep, es, el, es))
            conn.commit()
            tk.messagebox.showinfo(title='Hi', message='图书修改成功！')
        except Exception as e:
            pass
        finally:
            entry_bookname.delete('0', 'end')
            entry_author.delete('0', 'end')
            entry_company.delete('0', 'end')
            entry_place.delete('0', 'end')
            entry_sumbook.delete('0', 'end')
            entry_lendbook.delete('0', 'end')
            cursor.close()
            conn.close()
    
    editwindow = tk.Toplevel()
    editwindow.title('编辑图书')
    editwindow.geometry('450x300+800+300')
    editwindow.resizable(0, 0)

    var = tk.StringVar()
    tk.Label(editwindow, text='书名').place(x=50, y=20)
    tk.Label(editwindow, text='作者').place(x=50, y=60)
    tk.Label(editwindow, text='出版社').place(x=50, y=100)
    tk.Label(editwindow, text='编号').place(x=50, y=140)
    tk.Label(editwindow, text='图书数量').place(x=50, y=180)
    tk.Label(editwindow, text='可借数量').place(x=50, y=220)

    val_eb = tk.StringVar()
    val_ea = tk.StringVar()
    val_ec = tk.StringVar()
    val_ep = tk.StringVar()
    val_es = tk.StringVar()
    val_el = tk.StringVar()
    
    entry_bookname = tk.Entry(editwindow, textvariable=val_eb)
    entry_author = tk.Entry(editwindow, textvariable=val_ea)
    entry_company = tk.Entry(editwindow, textvariable=val_ec)
    entry_place = tk.Entry(editwindow, textvariable=val_ep)
    entry_sumbook = tk.Entry(editwindow, textvariable=val_es)
    entry_lendbook = tk.Entry(editwindow, textvariable=val_el)

    entry_bookname.place(x=160, y=20)
    entry_author.place(x=160, y=60)
    entry_company.place(x=160, y=100)
    entry_place.place(x=160, y=140)
    entry_sumbook.place(x=160, y=180)
    entry_lendbook.place(x=160, y=220)

    btn_append = tk.Button(editwindow, text='添加图书', command=appendbook_button)
    btn_remove = tk.Button(editwindow, text='修改图书', command=revisebook_button)
    btn_append.place(x=150, y=260)
    btn_remove.place(x=250, y=260)
    

if __name__ == '__main__':
    editbook()
    usr()
