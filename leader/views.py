
# Create your views here.
from django.shortcuts import render

def leader(request):
    return render(request, 'leaderpage/index.html')
