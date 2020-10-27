import json
from django.core import serializers
from pprint import pprint
from django.shortcuts import render, HttpResponse
from ibaquotes.models.quotes import QuotesAgreement
from ibaquotes.models.client import Client
from ibaquotes.models.product import Product

def quote_list(request):

    return render(request,'ibaquotes/quote/list.html',context)

def quote_create(request):

    clients = serializers.serialize('json',Client.objects.all())
    products = serializers.serialize('json',Product.objects.all())
    quotesAgreements = serializers.serialize('json',QuotesAgreement.objects.all())

    context = {
        'clients': clients,
        'products': products,
        'quotesAgreements': quotesAgreements,
    }
    return render(request,'ibaquotes/quote/create.html',context)

def quote_store(request):

    if request.method == 'POST':

        groups = json.loads(request.POST.get('items'))
        #pprint(groups)
        for group in groups:

            pprint(group)
        #print(items)
        return HttpResponse('type(items)')
        #return HttpResponse(request.POST.get('Offer'))