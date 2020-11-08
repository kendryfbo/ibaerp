import os
import json
from pprint import pprint
from django.conf import settings
from django.core import serializers
from django.http import JsonResponse
from django.db.models import Count, Max
from django.contrib.staticfiles import finders
from django.shortcuts import render, HttpResponse, redirect
from ibaquotes.models.quotes import QuotesAgreement,PaymentCondition,ShippingTerm, Currency, Quote, QuoteDetail
from ibaquotes.models.client import Client
from ibaquotes.models.product import Product
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

    context = {
        'clients': clients,
        'products': products,
        'quotesAgreements': quotesAgreements,
        'paymentConditions': paymentConditions,
        'shippingTerms': shippingTerms,
        'currencies': currencies,
    }
    return render(request,'ibaquotes/quote/create.html',context)

def quote_store(request):

    if request.method == 'POST':

        quote = Quote(
            client_id = request.POST.get('client'),
            offer = request.POST.get('offer'),
            date = request.POST.get('date'),
            executive = request.POST.get('executive'),
            address = request.POST.get('address'),
            phone = request.POST.get('phone'),
            fax = request.POST.get('fax'),
            request = request.POST.get('request'),
            description = request.POST.get('description'),
            email = request.POST.get('email'),
            exp_date = request.POST.get('expDate'),
            payment_condition_id = request.POST.get('paymentCondition'),
            shipping_term_id = request.POST.get('shippingTerm'),
            currency_id = request.POST.get('currency'))

        quote.save()

        groups = request.POST.getlist('items')
        #pprint(groups)
        for group in groups:
            
            localGroup = json.loads(group)

            #return HttpResponse(json.dumps(localGroup, indent=2))
            for product in localGroup['products']:

                quoteDetails = QuoteDetail(
                    quote = quote,
                    group_num = localGroup['id'], 
                    group_name = localGroup['name'],
                    item_num = product['id'],
                    product_id = product['pk'],
                    product_name = product['fields']['name'],
                    quantity = product['quantity'],
                    price = product['price'],
                )

                quoteDetails.save()

        return redirect('quote-list')
        return HttpResponse(json.dumps(request.POST.get('items'),indent=4))
        return HttpResponse(json.dumps(groups, indent=4))
        return HttpResponse(json.dumps(quoteInfo, indent=4))

def quote_show(request,id):

    quote = Quote.objects.prefetch_related('quotedetail_set').get(pk=id)
    numberOfGroups = QuoteDetail.objects.filter(quote_id=id).aggregate(Max('group_num')).values()
    quoteDetails = QuoteDetail.objects.filter(quote_id=id)

    context = {
        'quote': quote,
        'quoteDetails': quoteDetails,
        'numberOfGroups': numberOfGroups
    }  
    #return HttpResponse(json.dumps(context.values()));
    return render(request,'ibaquotes/quote/show.html',context)

def quote_pdf(request):

    template_path = 'ibaquotes/pdf/quotepdf.html'
    context = {'myvar': 'this is your template context'}
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