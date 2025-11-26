from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def password_change_done(request):
    return render(request, 'account/password_change_done.html')
