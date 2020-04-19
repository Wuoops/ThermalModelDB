from django.shortcuts import render,redirect
from dao.daoUtils import *

class LoginView():
    usernamme = 'Wuuops'
    def login(request):

        if request.method == 'POST':
            u = request.POST.get('username')
            p = request.POST.get('pwd')
            LoginView.username = LoginView.check(u,p)

            if LoginView.username == 0:
                return render(request,'login.html',{'msg':'用户名或密码错误'})
            else:
                return redirect('/model/')

        else:
            print(request.GET)
            return render(request,'login.html')

    def index(request):
        pass
    #检查账号密码，返回用户名
    def check(username,pwd):
        sql = 'SELECT * FROM d_users AS S WHERE S.user_name = "%s"  '
        result = searchDataP(sql,username)
        if (result.__len__() == 1 ):
            return result[0][3]
        else:
            print('账号或密码错误')
            print(result)
            return 0
