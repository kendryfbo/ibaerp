import os
import json
import posixpath
from pprint import pprint
from django.conf import settings
from django.core import serializers
from django.http import JsonResponse
from django.db import transaction
from django.db.models import Count, Max, Sum
from django.db.models.functions import Coalesce
from django.contrib.staticfiles import finders
from django.shortcuts import render, HttpResponse, redirect
from ibaquotes.models.quotes import QuotesAgreement,PaymentCondition,ShippingTerm, Currency, Quote, QuoteDetail, QuoteStatus
from ibaquotes.models.client import Client
from ibaquotes.models.product import Product
from ibaquotes.models.config import ConfigData
from django.template.loader import get_template
from xhtml2pdf import pisa

def quote_list(request):

    quotes = Quote.objects.order_by('-created_at').all();
    context = {
        'quotes': quotes,
    }
    
    return render(request,'ibaquotes/quote/list.html',context)

def quote_create(request):

    clients = serializers.serialize('json',Client.objects.all())
    products = Product.objects.select_related('status').all()
    products = serializers.serialize('json',products)

    quotesAgreements = serializers.serialize('json',QuotesAgreement.objects.all())
    paymentConditions = serializers.serialize('json',PaymentCondition.objects.all())
    shippingTerms = serializers.serialize('json',ShippingTerm.objects.all())
    currencies = serializers.serialize('json',Currency.objects.all())
    configData = serializers.serialize('json',[ConfigData.objects.first()]) # added [] to turn it into a list
    offerNumber = ConfigData.objects.values_list('offer_number', flat=True).first();
    
    if (Quote.objects.exists()):
        
        lastQuoteNumber = Quote.objects.values_list('number', flat=True).latest('created_at') + 1

    else: 
        lastQuoteNumber = offerNumber + 1

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

        paymentCondition = PaymentCondition.objects.get(pk=request.POST.get('paymentCondition'))
        shippingTerm = ShippingTerm.objects.get(pk=request.POST.get('shippingTerm'))
        client = Client.objects.get(pk=request.POST.get('client')) 

        quote = Quote(
            client = client,
            client_name = client.company,
            number = request.POST.get('number'),
            offer = request.POST.get('offer'),
            date = request.POST.get('date'),
            executive = request.POST.get('executive'),
            address = request.POST.get('address'),
            phone = request.POST.get('phone'),
            request = request.POST.get('request'),
            project_name = request.POST.get('project_name'),
            description = request.POST.get('description'),
            email = request.POST.get('email'),
            subtotal = 0,
            taxes = 0,
            total = 0,
            weight = 0,
            exp_date = request.POST.get('expDate'),
            payment_condition = paymentCondition,
            payment_condition_name = paymentCondition.name,
            payment_condition_days = paymentCondition.days,
            shipping_term = shippingTerm,
            shipping_term_name = shippingTerm.name,
            currency_id = request.POST.get('currency'),
            status_id = 1,)

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
                    product_remarks = product['remarks'],
                    quantity = product['quantity'],
                    weight = product['fields']['weight'],
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

def quote_show(request,id):

    quote = Quote.objects.prefetch_related('quotedetail_set').get(pk=id)
    #groups = QuoteDetail.objects.filter(quote_id=id).order_by('group_num').distinct('group_num')
    groups = QuoteDetail.objects.filter(quote_id=id).order_by('group_num').values('group_num','group_name','group_tax').annotate(group_subtotal=Sum('subtotal'))
    quoteDetails = QuoteDetail.objects.filter(quote_id=id).order_by('item_num')
    quoteStatus = QuoteStatus.objects.all()

    context = {
        'quote': quote,
        'quoteDetails': quoteDetails,
        'groups': groups,
        'quoteStatus': quoteStatus
    }  
    #return HttpResponse(serializers.serialize('json',quoteDetails));
    return render(request,'ibaquotes/quote/show.html',context)

def quote_status_update(request,id):

    quote = Quote.objects.get(pk=id)
    quote.status_id = request.POST.get('quote_status')
    quote.save()

    return redirect('quote-show', id=id)

def quote_edit(request,id):

    quote = serializers.serialize('json',[Quote.objects.prefetch_related('quotedetail_set').get(pk=id)])
    groups = serializers.serialize('json',QuoteDetail.objects.filter(quote_id=id).order_by('group_num').distinct('group_num'))
    quoteDetails = serializers.serialize('json',QuoteDetail.objects.filter(quote_id=id).order_by('item_num'))
    clients = serializers.serialize('json',Client.objects.all())
    products = serializers.serialize('json',Product.objects.prefetch_related('status').all())
    quotesAgreements = serializers.serialize('json',QuotesAgreement.objects.all())
    paymentConditions = serializers.serialize('json',PaymentCondition.objects.all())
    shippingTerms = serializers.serialize('json',ShippingTerm.objects.all())
    currencies = serializers.serialize('json',Currency.objects.all())
    
    context = {
        'quoteId': id,
        'quote': quote,
        'quoteDetails': quoteDetails,
        'groups': groups,
        'clients': clients,
        'products': products,
        'quotesAgreements': quotesAgreements,
        'paymentConditions': paymentConditions,
        'shippingTerms': shippingTerms,
        'currencies': currencies
    }  
    #return HttpResponse(serializers.serialize('json',quoteDetails));
    return render(request,'ibaquotes/quote/edit.html',context)

@transaction.atomic
def quote_update(request,id):
    
    if request.method == 'POST':

        paymentCondition = PaymentCondition.objects.get(pk=request.POST.get('paymentCondition'))
        shippingTerm = ShippingTerm.objects.get(pk=request.POST.get('shippingTerm'))
        client = Client.objects.get(pk=request.POST.get('client')) 
        quote = Quote.objects.get(pk=id)

        quote.client_id = client
        quote.client_name = client.company
        quote.number = request.POST.get('number')
        quote.offer = request.POST.get('offer')
        quote.date = request.POST.get('date')
        quote.executive = request.POST.get('executive')
        quote.address = request.POST.get('address')
        quote.phone = request.POST.get('phone')
        quote.request = request.POST.get('request')
        quote.project_name = request.POST.get('project_name')
        quote.description = request.POST.get('description')
        quote.email = request.POST.get('email')
        quote.subtotal = 0
        quote.taxes = 0
        quote.total = 0
        quote.weight = 0
        quote.exp_date = request.POST.get('expDate')
        quote.payment_condition = paymentCondition
        quote.payment_condition_name = paymentCondition.name
        quote.payment_condition_days = paymentCondition.days
        quote.shipping_term = shippingTerm
        quote.shipping_term_name = shippingTerm.name
        quote.currency_id = request.POST.get('currency')
        quote.status_id = 1

        quote.save()

        subtotal = 0
        taxes = 0
        weight = 0
        
        # Delete Existing records of Quote Details
        quoteDetails = QuoteDetail.objects.filter(quote_id=id).delete()

        groups = request.POST.getlist('items')

        for group in groups:
            
            localGroup = json.loads(group)

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
                    product_remarks = product['remarks'],
                    quantity = product['quantity'],
                    weight = product['fields']['weight'],
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

def quote_copy(request,id):

    quote = serializers.serialize('json',[Quote.objects.prefetch_related('quotedetail_set').get(pk=id)])
    groups = serializers.serialize('json',QuoteDetail.objects.filter(quote_id=id).order_by('group_num').distinct('group_num'))
    quoteDetails = serializers.serialize('json',QuoteDetail.objects.filter(quote_id=id).order_by('item_num'))
    clients = serializers.serialize('json',Client.objects.all())
    products = serializers.serialize('json',Product.objects.prefetch_related('status').all())
    quotesAgreements = serializers.serialize('json',QuotesAgreement.objects.all())
    paymentConditions = serializers.serialize('json',PaymentCondition.objects.all())
    shippingTerms = serializers.serialize('json',ShippingTerm.objects.all())
    currencies = serializers.serialize('json',Currency.objects.all())
    
    context = {
        'quoteId': id,
        'quote': quote,
        'quoteDetails': quoteDetails,
        'groups': groups,
        'clients': clients,
        'products': products,
        'quotesAgreements': quotesAgreements,
        'paymentConditions': paymentConditions,
        'shippingTerms': shippingTerms,
        'currencies': currencies
    }  
    #return HttpResponse(serializers.serialize('json',quoteDetails));
    return render(request,'ibaquotes/quote/copy.html',context)

@transaction.atomic
def quote_copy_save(request,id):
    
    if request.method == 'POST':

        # Update Original Quote Copy
        quoteOrig = Quote.objects.get(pk=id)
        copy = quoteOrig.copy + 1
        quoteOrig.copy = copy
        quoteOrig.save() 

        paymentCondition = PaymentCondition.objects.get(pk=request.POST.get('paymentCondition'))
        shippingTerm = ShippingTerm.objects.get(pk=request.POST.get('shippingTerm'))
        client = Client.objects.get(pk=request.POST.get('client')) 

        quote = Quote(
            client = client,
            client_name = client.company,
            number = request.POST.get('number'),
            offer = request.POST.get('offer'),
            date = request.POST.get('date'),
            executive = request.POST.get('executive'),
            address = request.POST.get('address'),
            phone = request.POST.get('phone'),
            request = request.POST.get('request'),
            project_name = request.POST.get('project_name'),
            description = request.POST.get('description'),
            email = request.POST.get('email'),
            subtotal = 0,
            taxes = 0,
            total = 0,
            weight = 0,
            exp_date = request.POST.get('expDate'),
            payment_condition = paymentCondition,
            payment_condition_name = paymentCondition.name,
            payment_condition_days = paymentCondition.days,
            shipping_term = shippingTerm,
            shipping_term_name = shippingTerm.name,
            currency_id = request.POST.get('currency'),
            status_id = 1,)

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
                    product_remarks = product['remarks'],
                    quantity = product['quantity'],
                    weight = product['fields']['weight'],
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
        #return HttpResponse(json.dumps(request.POST.get('items'),indent=4))
        #return HttpResponse(json.dumps(groups, indent=4))
        #return HttpResponse(json.dumps(quoteInfo, indent=4))

def quote_delete(request,id):

    return HttpResponse('Delete quote')

def quote_pdf(request,id):

    quote = Quote.objects.prefetch_related('quotedetail_set').select_related ('client').get(pk=id)
    quoteDetails = QuoteDetail.objects.filter(quote_id=17)
    #groups = QuoteDetail.objects.filter(quote_id=id).order_by('group_num').distinct('group_num')
    groups = QuoteDetail.objects.filter(quote_id=id).order_by('group_num').values('group_num','group_name','group_tax').annotate(group_subtotal=Sum('subtotal'))
    quoteDetails = QuoteDetail.objects.filter(quote_id=id).order_by('item_num').annotate(total_weight=Sum('weight', field='weight*quantity'))
    configData = ConfigData.objects.first()
    template_path = 'ibaquotes/pdf/quotepdf.html'

    context = {
        'myvar': 'this is your template context',
        'quote': quote,
        'quoteDetails': quoteDetails,
        'groups': groups,
        'configData': configData,
    }
    
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    # use short variable names
    sUrl = settings.STATIC_URL      # Typically /static/
    sRoot = settings.STATIC_ROOT    # Typically /home/userX/project_static/
    mUrl = settings.MEDIA_URL       # Typically /static/media/
    mRoot = settings.MEDIA_ROOT     # Typically /home/userX/project_static/media/

    # convert URIs to absolute system paths
    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.repFlace(sUrl, ""))
    else:
        return uri  # handle absolute uri (ie: http://some.tld/foo.png)

    # make sure that file exists
    if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
    return path