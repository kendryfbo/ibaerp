import os
import json
from pprint import pprint
from django.conf import settings
from django.core import serializers
from django.http import JsonResponse
from django.db import transaction
from django.db.models import Count, Max
from django.contrib.staticfiles import finders
from django.shortcuts import render, HttpResponse, redirect
from ibaquotes.models.quotes import QuotesAgreement,PaymentCondition,ShippingTerm, Currency, Quote, QuoteDetail
from ibaquotes.models.client import Client
from ibaquotes.models.product import Product
from ibaquotes.models.config import ConfigData
from django.template.loader import get_template
from xhtml2pdf import pisa

def quote_list(request):

    quotes = Quote.objects.all();
    context = {
        'quotes': quotes,
    }
    
    return render(request,'ibaquotes/quote/list.html',context)

def quote_create(request):

    clients = serializers.serialize('json',Client.objects.all())
    products = serializers.serialize('json',Product.objects.all())
    quotesAgreements = serializers.serialize('json',QuotesAgreement.objects.all())
    paymentConditions = serializers.serialize('json',PaymentCondition.objects.all())
    shippingTerms = serializers.serialize('json',ShippingTerm.objects.all())
    currencies = serializers.serialize('json',Currency.objects.all())
    config = ConfigData.objects.first() # added [] to turn it into a list
    configData = serializers.serialize('json',[config]) # added [] to turn it into a list

    lastQuoteNumber = Quote.objects.values_list('number', flat=True).latest('created_at')
    if not (lastQuoteNumber):
        lastQuoteNumber = config.offer_number
    lastQuoteNumber += 1
    
    context = {
        'clients': clients,
        'products': products,
        'quotesAgreements': quotesAgreements,
        'paymentConditions': paymentConditions,
        'shippingTerms': shippingTerms,
        'currencies': currencies,
        'configData': configData,
        'lastQuoteNumber': lastQuoteNumber,
    }
    return render(request,'ibaquotes/quote/create.html',context)

@transaction.atomic
def quote_store(request):

    if request.method == 'POST':

        quote = Quote(
            client_id = request.POST.get('client'),
            number = request.POST.get('number'),
            offer = request.POST.get('offer'),
            date = request.POST.get('date'),
            executive = request.POST.get('executive'),
            address = request.POST.get('address'),
            phone = request.POST.get('phone'),
            request = request.POST.get('request'),
            description = request.POST.get('description'),
            email = request.POST.get('email'),
            subtotal = 0,
            taxes = 0,
            total = 0,
            weight = 0,
            exp_date = request.POST.get('expDate'),
            payment_condition_id = request.POST.get('paymentCondition'),
            shipping_term_id = request.POST.get('shippingTerm'),
            currency_id = request.POST.get('currency'))

        quote.save()

        subtotal = 0
        taxes = 0
        weight = 0

        groups = request.POST.getlist('items')
        #pprint(groups)
        for group in groups:
            
            localGroup = json.loads(group)

            #return HttpResponse(json.dumps(localGroup, indent=2))
            for product in localGroup['products']:

                prodtaxes = (float(localGroup['taxPercentage']) / 100) * (float(product['price']) * float(product['quantity']))
                prodSubtotal = float(product['price']) * float(product['quantity'])
                prodWeight = float(product['fields']['weight']) * float(product['quantity'])
                prodTotal = prodSubtotal + prodtaxes

                quoteDetails = QuoteDetail(
                    quote = quote,
                    group_num = localGroup['id'], 
                    group_name = localGroup['name'],
                    group_tax = localGroup['taxPercentage'],
                    item_num = product['id'],
                    product_id = product['pk'],
                    product_name = product['fields']['name'],
                    product_detail = product['detail'],
                    #product_remarks = product['remarks'],
                    quantity = product['quantity'],
                    price = product['price'],
                    tax = prodtaxes,
                    subtotal = prodSubtotal,
                    total = prodTotal,
                )
                subtotal += prodSubtotal
                taxes += prodtaxes
                weight += prodWeight

                quoteDetails.save()

        quote.subtotal = subtotal
        quote.taxes = taxes
        quote.total = subtotal + taxes
        quote.weight = weight

        quote.save()
        return redirect('quote-list')
        return HttpResponse(json.dumps(request.POST.get('items'),indent=4))
        return HttpResponse(json.dumps(groups, indent=4))
        return HttpResponse(json.dumps(quoteInfo, indent=4))

def quote_show(request,id):

    quote = Quote.objects.prefetch_related('quotedetail_set').get(pk=id)
    numberOfGroups = QuoteDetail.objects.filter(quote_id=id).aggregate(Max('group_num')).values()
    groups = QuoteDetail.objects.filter(quote_id=id).order_by('group_num').distinct('group_num')
    quoteDetails = QuoteDetail.objects.filter(quote_id=id)
    
    context = {
        'quote': quote,
        'quoteDetails': quoteDetails,
        'groups': groups,
        'numberOfGroups': numberOfGroups
    }  
    #return HttpResponse(serializers.serialize('json',quoteDetails));
    return render(request,'ibaquotes/quote/show.html',context)

def quote_pdf(request):

    quoteDetails = QuoteDetail.objects.filter(quote_id=17)
    template_path = 'ibaquotes/pdf/quotepdf.html'
    context = {
        'myvar': 'this is your template context',
        'quoteDetails': quoteDetails
        }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response,link_callback=link_callback)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def link_callback(uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those
        resources
        """
        result = finders.find(uri)
        if result:
                if not isinstance(result, (list, tuple)):
                        result = [result]
                result = list(os.path.realpath(path) for path in result)
                path=result[0]
        else:
                sUrl = settings.STATIC_URL        # Typically /static/
                sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
                mUrl = settings.MEDIA_URL         # Typically /media/
                mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

                if uri.startswith(mUrl):
                        path = os.path.join(mRoot, uri.replace(mUrl, ""))
                elif uri.startswith(sUrl):
                        path = os.path.join(sRoot, uri.replace(sUrl, ""))
                else:
                        return uri

        # make sure that file exists
        if not os.path.isfile(path):
                raise Exception(
                        'media URI must start with %s or %s' % (sUrl, mUrl)
                )
        return path