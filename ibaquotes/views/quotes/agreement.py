from django.shortcuts import render, HttpResponse
from ibaquotes.models.quotes import QuotesAgreement


def agreement_list(request):

    agreements = QuotesAgreement.objects.all();
    context = {
        'agreements': agreements
    }
    return render(request,'ibaquotes/agreement/list.html',context)

def agreement_create(request):

    return render(request,'ibaquotes/agreement/create.html')

def agreement_store(request):

    return render(request,'ibaquotes/agreement/create.html')