from django.shortcuts import render, HttpResponse
from ibaquotes.models.quotes import QuotesAgreement

def create_agreement(request):

    return render(request,'ibaquotes/agreement/create.html')

def store_agreement(request):

    return render(request,'ibaquotes/agreement/create.html')