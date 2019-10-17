import tkinter as tk
from tkinter import ttk
from pymysql import *
from windowui import *

listbook = []

# 查找图书
def search_button():
    try:
        global listbook
        dellist(tree)
        conn = connect(host='localhost', port=3306, user='root', password='password', database='pythonsql')
        cursor = conn.cursor()
        val = searchEntry.get()
        cursor.execute('select * from library where bookname like %s;' % val)
        result = cursor.fetchall()
        for i in range(len(result)):
            listbook = result[i]
            tree.insert('', 'end', value=listbook)
    except Exception as e:
        pass
    finally:
        cursor.close()
        conn.close()


# 显示所有图书
def allbook_button():
    global listbook
    dellist(tree)
    conn = connect(host='localhost', port=3306, user='root', password='password', database='pythonsql')
    cursor = conn.cursor()
    cursor.execute('select * from library')
    result = cursor.fetchall()
    for i in range(len(result)):
        listbook = result[i]
        tree.insert('', 'end', value=listbook)
    cursor.close()
    conn.close()


def lendbook_button():
    pass


def returnbook_button():
    pass


# 删除图书
def removebook_button():
    val_lb = lb.get('0', 'end')
    for i in range(len(val_lb)):
        val_bn = val_lb[i][0]
        val_an = val_lb[i][1]
        conn = connect(host='localhost', port=3306, user='root', password='password', database='pythonsql')
        cursor = conn.cursor()
        cursor.execute('delete from library where bookname="%s" and place="%s";' % (val_bn, val_an))
        conn.commit()
        cursor.close()
        conn.close()
        lb.delete('0', 'end')
        tk.messagebox.showinfo(title='Hi', message='图书删除成功！')
        

# 编辑图书
def editbook_button():
    editbook()


# 点击treeview事件
def treeviewClick(event):
    for item in tree.selection():
        item_text = tree.item(item, 'values')
        lb.insert('end', item_text[1:5:3])
    

# 清除treeview
def dellist(tree):
    x = tree.get_children()
    for item in x:
        tree.delete(item)


# 用户登录
def loginuser():
    usr()

window1 = tk.Tk()
window1.title('图书管理系统')
window1.geometry('900x627')
window1.resizable(0, 0)

menubar = tk.Menu(window1)

filemenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='管理员', menu=filemenu)
filemenu.add_command(label='登录', command=loginuser)
filemenu.add_command(label='注销')

editmenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='编辑', menu=editmenu)
editmenu.add_command(label='编辑读者')
editmenu.add_command(label='编辑图书', command=editbook_button)

notemenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='日志', menu=notemenu)
notemenu.add_command(label='查看借还记录')
notemenu.add_command(label='查看学生信息')


tree = ttk.Treeview(window1, columns=['0', '1', '2', '3', '4', '5', '6'], show='headings', height=30)
tree.column('0', width=50, anchor='center')
tree.column('1', width=150, anchor='center')
tree.column('2', width=100, anchor='center')
tree.column('3', width=150, anchor='center')
tree.column('4', width=100, anchor='center')
tree.column('5', width=75, anchor='center')
tree.column('6', width=75, anchor='center')
tree.heading('0', text='ID')
tree.heading('1', text='书籍名')
tree.heading('2', text='作者')
tree.heading('3', text='出版社')
tree.heading('4', text='编号')
tree.heading('5', text='馆藏复本')
tree.heading('6', text='可借复本')

tree.bind('<Double-1>', treeviewClick)

var1 = tk.StringVar()
var1.set('管理员未登录')
var2 = tk.StringVar()
userLabel = tk.Label(window1, textvariable=var1, width=20, height=5)

searchEntry = tk.Entry(window1)

searchButton = tk.Button(window1, text='搜索图书',
                         width=6, height=1, command=search_button)

allbookButton = tk.Button(window1, text='所有图书',
                         width=6, height=1, command=allbook_button)

lendbookButton = tk.Button(window1, text='借出图书',
                         width=6, height=1, command=lendbook_button)

returnbookButton = tk.Button(window1, text='归还图书',
                         width=6, height=1, command=returnbook_button)

removebookButton = tk.Button(window1, text='删除图书',
                         width=6, height=1, command=removebook_button)

lb = tk.Listbox(window1, listvariable=var2, width=28)

userLabel.place(x=22, y=0, anchor='nw')
searchEntry.place(x=0, y=125, anchor='nw')
searchButton.place(x=145, y=120, anchor='nw')
allbookButton.place(x=145, y=150, anchor='nw')
lendbookButton.place(x=40, y=230, anchor='nw')
returnbookButton.place(x=110, y=230, anchor='nw')
lb.place(x=0, y=260, anchor='nw')
removebookButton.place(x=75, y=460, anchor='nw')

tree.place(x=200, y=0, anchor='nw')

window1.config(menu=menubar)
window1.mainloop()
