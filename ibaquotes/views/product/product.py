from django.shortcuts import render, HttpResponse

def import_product(request):

    context = {'title': 'base test'}

    return render(request,'ibaquotes/product/import.html')