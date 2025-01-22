
# Create your views here.
from django.shortcuts import render
from user.auth import admin_only
@admin_only
def leader(request):
    return render(request, 'leaderpage/index.html')
