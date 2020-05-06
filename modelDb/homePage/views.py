from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def homePage(request):
    userId = request.session.get('_auth_user_id')
    print(userId)
    print(request.user.is_superuser)
    return render(request,'homePage.html')
