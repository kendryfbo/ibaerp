from django.shortcuts import render, HttpResponse

def index(request):

    return HttpResponse("Test View")

def templatetest(request):

    context = {'title': 'base test'}
    #return render(request,"base/base.html",context)
    return render(request,'ibaquotes/base/base.html')