import tkinter as tk
from tkinter import ttk
from pymysql import *
from windowui import *
import pickle
import xlrd
from tkinter import messagebox
import time


listbook = []
power = False


# 判断管理员是否登录
def log(func):
    global power

    def wrapper(*args, **kw):
        if power is False:
            tk.messagebox.showerror(title='Error', message='你还未登录,没有管理员权限')
        else:
            return func(*args, **kw)
    return wrapper


# 用户登录
def usr():

    def usr_login():  # 登录功能
        global power
        usr_name = var_usr_name.get()  # .get()获得在Entry输入的username和password
        usr_pwd = var_usr_pwd.get()  # 将username和password分别赋值给usr_n和usr_p

        try:  # 错误处理
            with open('usrs_info.pickle', 'rb') as usr_file:  # 将usrs_info.pickle(存放用户信息的资料夹)装载到usr_file里
                usrs_info = pickle.load(usr_file)  # .load():加载usr_file文件存到变量usrs_info里
        except FileNotFoundError:  # FileNotFoundError:如果还没有创建文件
            with open('usrs_info.pickle', 'wb') as usr_file:  # 创建usrs_info.pickle并装载到usr_file里
                usrs_info = {'admin': 'admin'}
                pickle.dump(usrs_info, usr_file)  # 把字典usrs_info的内容剪切到usr_file

        if usr_name in usrs_info:  # 如果在输入框输入的username在资料夹usrs_info字典里
            if usr_pwd == usrs_info[usr_name]:  # 如果在输入框输入的password对应usrs_info字典里usr_name的索引
                tk.messagebox.showinfo(title='Welcome', message='管理员' + usr_name + '登录成功')  # 登录成功
                power = True
                var1.set('管理员' + usr_name + '已登录')
                userwindow.destroy()
            else:  # 如果不对应
                tk.messagebox.showerror(message='密码错误，请重新输入密码。')
        else:  # 如果在资料夹usrs_info字典里没有对应的usr_name
            is_sign_up = tk.messagebox.askyesno(title='Welcome',  # 用弹出窗口问你是否注册
                                                message='用户不存在，是否注册')
            if is_sign_up is True:
                usr_sign_up()
            else:
                pass

    @log
    def usr_sign_up():

        def sign_to_Mofan_Python():  # 注册功能
            np = new_pwd.get()  # get()到在Toplevel窗口中Entry里输入的值
            npf = new_pwd_confirm.get()
            nn = new_name.get()
            with open('usrs_info.pickle', 'rb') as usr_file:  # 以只读的形式打开usrs_info.pickle
                exist_usr_info = pickle.load(usr_file)
                if np != npf:  # 如果判断np和npf不相同
                    tk.messagebox.showerror(title='Error',
                                            message='两次密码输入不一致')
                elif nn in exist_usr_info:  # 如果用户已被注册
                    tk.messagebox.showerror(title='Error', message='该用户已被注册')
                else:
                    exist_usr_info[nn] = np  # 把nn和np存到字典exist_usr_info中
                    with open('usrs_info.pickle', 'wb') as usr_file:  # 把字典exist_usr_info里的键值对写入usrs_info.pickle
                        pickle.dump(exist_usr_info, usr_file)
                    tk.messagebox.showinfo('Welcome', '添加管理员成功!')  # 提示注册成功
                    window_sign_up.destroy()  # .destroy()：摧毁(关闭)注册窗口

        window_sign_up = tk.Toplevel(userwindow)  # .Toplevel()：窗口上的窗口，不需要再window.mainloop()
        window_sign_up.geometry('350x200')
        window_sign_up.title('注册窗口')

        new_name = tk.StringVar()
        new_name.set('')
        tk.Label(window_sign_up, text='用户名:').place(x=10, y=10)
        entry_new_name = tk.Entry(window_sign_up, textvariable=new_name)
        entry_new_name.place(x=150, y=10)

        new_pwd = tk.StringVar()
        tk.Label(window_sign_up, text='密码:').place(x=10, y=50)
        entry_new_pwd = tk.Entry(window_sign_up, textvariable=new_pwd, show='*')
        entry_new_pwd.place(x=150, y=50)

        new_pwd_confirm = tk.StringVar()
        tk.Label(window_sign_up, text='确认密码:').place(x=10, y=90)
        entry_new_pwd_confirm = tk.Entry(window_sign_up, textvariable=new_pwd_confirm, show='*')
        entry_new_pwd_confirm.place(x=150, y=90)

        btn_confirm_sign_up = tk.Button(window_sign_up,
                                        text='添加管理员',
                                        command=sign_to_Mofan_Python)
        btn_confirm_sign_up.place(x=150, y=130)

    userwindow = tk.Toplevel()
    userwindow.title('管理员登录')
    userwindow.geometry('450x300+450+300')
    userwindow.resizable(0, 0)

    tk.Label(userwindow, text='请管理员登录\n吉林大学珠海学院\n图书馆分馆', font=('Arial', 20)).place(x=110, y=40)
    tk.Label(userwindow, text='用户名:').place(x=100, y=150)
    tk.Label(userwindow, text='密码:').place(x=100, y=190)

    var_usr_name = tk.StringVar()
    # var_usr_name.set('exampel@python.com')  # 给username的Entry一个初始值
    entry_usr_name = tk.Entry(userwindow, textvariable=var_usr_name)
    entry_usr_name.place(x=160, y=150)

    var_usr_pwd = tk.StringVar()
    entry_usr_pwd = tk.Entry(userwindow, textvariable=var_usr_pwd, show='*')
    entry_usr_pwd.place(x=160, y=190)

    btn_login = tk.Button(userwindow, text='管理员登录', command=usr_login)
    btn_login.place(x=140, y=230)
    btn_sign_up = tk.Button(userwindow, text='添加管理员', command=usr_sign_up)
    btn_sign_up.place(x=240, y=230)


# 查找图书
def search_button():
    try:
        global listbook
        dellist(tree)
        val = searchEntry.get()
        conn = connect(host='localhost', port=3306, user='root', password='password', database='library')
        cursor = conn.cursor()
        cursor.execute("select * from book where book_name like '%%%s%%';" % val)
        result = cursor.fetchall()
        if len(result) == 0:
            tk.messagebox.showinfo(title='Hi', message='图书馆暂无此书')
        else:
            for i in range(len(result)):
                listbook = result[i][1:]
                tree.insert('', 'end', value=listbook)
        cursor.close()
        conn.close()
    except Exception as e:
        pass
    finally:
        pass


# 显示分类图书
def allbook_button():
    try:
        global listbook
        dellist(tree)
        val = searchEntry.get()
        conn = connect(host='localhost', port=3306, user='root', password='password', database='library')
        cursor = conn.cursor()
        cursor.execute("select * from book where book_id like '%s%%';" % val)
        result = cursor.fetchall()
        for i in range(len(result)):
            listbook = result[i][1:]
            tree.insert('', 'end', value=listbook)
        cursor.close()
        conn.close()
    except Exception as e:
        pass
    finally:
        pass


# 借出图书
@log
def lendbook_button():
    try:
        sql1 = 'begin;'
        sql2 = 'insert into borrow (s_id, s_name, b_id, b_name, borrow_date, return_date) values ("%s", "%s", "%s", "%s", curdate(), date_add(curdate(), interval 1 month));'
        sql3 = 'update students set returnbook = returnbook + 1 where stu_id = "%s" and returnbook < 10;'
        sql4 = 'update book set lendbook = lendbook - 1 where book_id = "%s" and lendbook > 0;'
        sql5 = 'commit;'
        s_id = stu_idEntry.get()
        s_name = stu_nameEntry.get()
        val_lb = lb.get('0', 'end')
        for i in range(len(val_lb)):
            b_id = val_lb[i][0]
            b_name = val_lb[i][1]
            conn = connect(host='localhost', port=3306, user='root', password='password', database='library')
            cursor = conn.cursor()
            cursor.execute('select returnbook from students where stu_id="%s";' % s_id)
            result_rb = cursor.fetchall()
            cursor.execute('select lendbook from book where book_id="%s";' % b_id)
            result_lb = cursor.fetchall()
            if int(result_rb[0][0]) > 9:
                tk.messagebox.showwarning(title='Hi', message=('该学生<%s>借书已达到上限！' % s_name))
            elif int(result_lb[0][0]) < 1:
                tk.messagebox.showwarning(title='Hi', message=('该图书《%s》已借完！' % b_name))
            else:
                cursor.execute(sql1)
                cursor.execute(sql2 % (s_id, s_name, b_id, b_name))
                cursor.execute(sql3 % s_id)
                cursor.execute(sql4 % b_id)
                cursor.execute(sql5)
                conn.commit()
                lb.delete('0', 'end')
                tk.messagebox.showinfo(title='Hi', message=('图书《%s》已成功借给学生<%s>！' % (b_name, s_name)))
            cursor.close()
            conn.close()

            myFile = open('log.txt', 'a')
            myFile.write('[%s],图书《%s》已成功借给学生<%s>！\n' % (time.asctime(), b_name, s_name))
            myFile.close()
    except IntegrityError as e:
        sign_up_stu = tk.messagebox.askyesno(title='Hi', message='该学生还未录取系统，是否添加')
        if sign_up_stu is True:
            editreader()
        else:
            pass
    except IndexError as e:
        sign_up_stu = tk.messagebox.askyesno(title='Hi', message='该学生还未录取系统，是否添加')
        if sign_up_stu is True:
            editreader()
        else:
            pass
    finally:
        search_button()


# 归还图书(需改进)
@log
def returnbook_button():
    try:
        sql1 = 'begin;'
        sql2 = 'delete from borrow where s_id = "%s" and b_id = "%s";'
        sql3 = 'update students set returnbook = returnbook - 1 where stu_id = "%s";'
        sql4 = 'update book set lendbook = lendbook + 1 where book_id = "%s";'
        sql5 = 'commit;'
        s_id = stu_idEntry.get()
        s_name = stu_nameEntry.get()
        val_lb = lb.get('0', 'end')
        for i in range(len(val_lb)):
            b_id = val_lb[i][0]
            b_name = val_lb[i][1]
            conn = connect(host='localhost', port=3306, user='root', password='password', database='library')
            cursor = conn.cursor()
            cursor.execute('select returnbook from students where stu_id="%s";' % s_id)
            result_rb = cursor.fetchall()
            cursor.execute('select lendbook from book where book_id="%s";' % b_id)
            result_lb = cursor.fetchall()
            cursor.execute(sql1)
            cursor.execute(sql2 % (s_id, b_id))
            cursor.execute(sql3 % s_id)
            cursor.execute(sql4 % b_id)
            cursor.execute(sql5)
            conn.commit()
            lb.delete('0', 'end')
        cursor.close()
        conn.close()

        myFile = open('log.txt', 'a')
        myFile.write('[%s],学生<%s>借出的图书《%s》已成功归还！\n' % (time.asctime(), s_name, b_name))
        myFile.close()
        tk.messagebox.showinfo(title='Hi', message='图书已归还')
    except IntegrityError as e:
        pass
    except IndexError as e:
        pass
    finally:
        search_button()


# 删除图书
@log
def removebook_button():
    sign_up_stu = tk.messagebox.askyesno(title='Hi', message='是否删除图书？')
    if sign_up_stu is True:
        val_lb = lb.get('0', 'end')
        for i in range(len(val_lb)):
            b_id = val_lb[i][0]
            b_name = val_lb[i][1]
            conn = connect(host='localhost', port=3306, user='root', password='password', database='library')
            cursor = conn.cursor()
            cursor.execute('delete from book where book_id="%s" and book_name="%s" where (lendbook = sumbook - 1);' % (b_id, b_name))
            conn.commit()
            cursor.close()
            conn.close()
            lb.delete('0', 'end')
        tk.messagebox.showinfo(title='Hi', message='图书删除成功！')
    else:
        pass


# 导入图书
def importbook_button():
    data = xlrd.open_workbook('book.xlsx')
    table = data.sheets()[0]
    nrows = table.nrows
    for i in range(nrows-1):
        li_book = table.row_values(i+1)
        try:
            eb = li_book[1]
            ea = li_book[2]
            ec = li_book[3]
            ep = li_book[4]
            es = li_book[5]
            el = li_book[6]
            conn = connect(host='localhost', port=3306, user='root', password='password', database='library')
            cursor = conn.cursor()
            cursor.execute(
                'insert into book (book_name, book_author, book_comp, book_id, sumbook, lendbook) values ("%s", "%s", "%s", "%s", "%s", "%s");'
                % (eb, ea, ec, ep, es, el))
            conn.commit()
            tk.messagebox.showinfo(title='Hi', message='图书导入成功！')
            search_button()
        except Exception as e:
            pass
        finally:
            cursor.close()
            conn.close()
# 编辑图书
@log
def editbook_button():
    editbook()


# 编辑读者
@log
def editreader_button():
    editreader()


# 点击treeview事件
@log
def treeviewClick(event):
    for item in tree.selection():
        item_text = tree.item(item, 'values')
        lb.insert('end', (item_text[0], item_text[1], item_text[2]))


def dellb():
    lb.delete('0', 'end')


# 清除treeview
def dellist(y):
    x = y.get_children()
    for item in x:
        y.delete(item)


# 用户登录
def loginuser():
    usr()


# 查看学生信息
def viewstudent():
    try:
        global listbook
        stuwindow = tk.Toplevel()
        stuwindow.title('学生借书信息')
        stuwindow.geometry('600x300+450+300')
        stuwindow.resizable(0, 0)
        tree_stu = ttk.Treeview(stuwindow, columns=['1', '2', '3', '4', '5', '6'], show='headings', height=14)
        tree_stu.column('1', width=100, anchor='center')
        tree_stu.column('2', width=100, anchor='center')
        tree_stu.column('3', width=100, anchor='center')
        tree_stu.column('4', width=100, anchor='center')
        tree_stu.column('5', width=100, anchor='center')
        tree_stu.column('6', width=100, anchor='center')
        tree_stu.heading('1', text='学生学号')
        tree_stu.heading('2', text='学生姓名')
        tree_stu.heading('3', text='书籍编号')
        tree_stu.heading('4', text='书籍名称')
        tree_stu.heading('5', text='借书日期')
        tree_stu.heading('6', text='还书期限')

        tree_stu.place(x=0, y=0, anchor='nw')

        dellist(tree_stu)
        s_id = stu_idEntry.get()
        s_name = stu_nameEntry.get()
        conn = connect(host='localhost', port=3306, user='root', password='password', database='library')
        cursor = conn.cursor()
        cursor.execute('select * from borrow where s_id = "%s" and s_name = "%s";' % (s_id, s_name))
        result = cursor.fetchall()
        for i in range(len(result)):
            listbook = result[i][1:]
            tree_stu.insert('', 'end', value=listbook)
        cursor.close()
        conn.close()
    except Exception as e:
        pass
    finally:
        pass


# 查看逾期未还学生
def overtime():
    try:
        global listbook
        stuwindow = tk.Toplevel()
        stuwindow.title('学生借书信息')
        stuwindow.geometry('600x300+450+300')
        stuwindow.resizable(0, 0)
        tree_stu = ttk.Treeview(stuwindow, columns=['1', '2', '3', '4', '5', '6'], show='headings', height=14)
        tree_stu.column('1', width=100, anchor='center')
        tree_stu.column('2', width=100, anchor='center')
        tree_stu.column('3', width=100, anchor='center')
        tree_stu.column('4', width=100, anchor='center')
        tree_stu.column('5', width=100, anchor='center')
        tree_stu.column('6', width=100, anchor='center')
        tree_stu.heading('1', text='学生学号')
        tree_stu.heading('2', text='学生姓名')
        tree_stu.heading('3', text='书籍编号')
        tree_stu.heading('4', text='书籍名称')
        tree_stu.heading('5', text='借书日期')
        tree_stu.heading('6', text='还书期限')

        tree_stu.place(x=0, y=0, anchor='nw')

        dellist(tree_stu)
        conn = connect(host='localhost', port=3306, user='root', password='password', database='library')
        cursor = conn.cursor()
        cursor.execute("select * from borrow where return_date < curdate();")
        result = cursor.fetchall()
        for i in range(len(result)):
            listbook = result[i][1:]
            tree_stu.insert('', 'end', value=listbook)
        cursor.close()
        conn.close()
    except Exception as e:
        pass
    finally:
        pass


# 查看日志
def book_log():
    myFile = open('log.txt', 'r')
    content = myFile.read()
    print(content)
    myFile.close()


@log
def overuser():
    global power
    power = False
    var1.set('管理员未登录')


window1 = tk.Tk()
window1.title('图书管理系统')
window1.geometry('900x627')
window1.resizable(0, 0)

menubar = tk.Menu(window1)

filemenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='管理员', menu=filemenu)
filemenu.add_command(label='登录', command=loginuser)
filemenu.add_command(label='注销', command=overuser)

editmenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='编辑', menu=editmenu)
# editmenu.add_command(label='编辑读者', command=editreader_button)
editmenu.add_command(label='编辑图书', command=editbook_button)

notemenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='日志', menu=notemenu)
notemenu.add_command(label='查看逾期名单', command=overtime)
notemenu.add_command(label='查看日志', command=book_log)


tree = ttk.Treeview(window1, columns=['1', '2', '3', '4', '5', '6'], show='headings', height=30)
tree.column('1', width=125, anchor='center')
tree.column('2', width=175, anchor='center')
tree.column('3', width=100, anchor='center')
tree.column('4', width=150, anchor='center')
tree.column('5', width=75, anchor='center')
tree.column('6', width=75, anchor='center')
tree.heading('1', text='编号')
tree.heading('2', text='书籍名')
tree.heading('3', text='作者')
tree.heading('4', text='出版社')
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

allbookButton = tk.Button(window1, text='搜索分类',
                         width=6, height=1, command=allbook_button)

stu_idEntry = tk.Entry(window1, width=12)
stu_nameEntry = tk.Entry(window1, width=12)

lendbookButton = tk.Button(window1, text='借出图书',
                         width=6, height=1, command=lendbook_button)

returnbookButton = tk.Button(window1, text='归还图书',
                         width=6, height=1, command=returnbook_button)

removebookButton = tk.Button(window1, text='删除图书',
                         width=6, height=1, command=removebook_button)

importbookButton = tk.Button(window1, text='导入图书',
                         width=6, height=1, command=importbook_button)

clearbookButton = tk.Button(window1, text='清空列表',
                         width=6, height=1, command=dellb)

viewstudentButton = tk.Button(window1, text='借书信息',
                         width=6, height=1, command=viewstudent)

lb = tk.Listbox(window1, listvariable=var2, width=28)


tk.Label(window1, text='A 马列主义、毛泽东思想、邓小平理论\nB 哲学、宗教；C 社会科学总论\n'
                       'D 政治、法律；E 军事；F 经济\nG 文化、科学、教育、体育\nH 语言、文字；'
                       'I 文学；J 艺术；K 地理\nN 自然科学总论；O 数理科学与化学\nP 天文学、地球科学'
                       '；Q 生物科学\nR 医药、卫生；农业科学；T 工业技术\nU 交通运输；V 航空、航天\nX 环境科学,安全科学；Z 综合性图书',
         font=('微软雅黑', 8)).place(x=0, y=460, anchor='nw')


userLabel.place(x=22, y=0, anchor='nw')
searchEntry.place(x=0, y=65, anchor='nw')
searchButton.place(x=145, y=60, anchor='nw')
allbookButton.place(x=145, y=90, anchor='nw')
tk.Label(window1, text='学生学号').place(x=0, y=160, anchor='nw')
tk.Label(window1, text='学生姓名').place(x=0, y=195, anchor='nw')
stu_idEntry.place(x=55, y=160, anchor='nw')
stu_nameEntry.place(x=55, y=195, anchor='nw')
lendbookButton.place(x=145, y=145, anchor='nw')
viewstudentButton.place(x=145, y=175, anchor='nw')
returnbookButton.place(x=145, y=200, anchor='nw')
lb.place(x=0, y=230, anchor='nw')
# removebookButton.place(x=40, y=420, anchor='nw')
importbookButton.place(x=40, y=420, anchor='nw')
clearbookButton.place(x=110, y=420, anchor='nw')

tree.place(x=200, y=0, anchor='nw')

window1.config(menu=menubar)
window1.mainloop()
