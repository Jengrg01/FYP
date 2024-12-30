from django.shortcuts import render

def adminpage(request):
    return render(request, 'adminpage/index.html')
