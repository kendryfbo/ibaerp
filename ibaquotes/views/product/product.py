from django.shortcuts import render, HttpResponse
from ibaquotes.forms import CreateProductForm
from ibaquotes.models.product import Product

def product_list(request):

    products = Product.objects.all();
    context = {
        'products': products
    }
    return render(request,'ibaquotes/product/list.html',context)
def create_product(request):

    form = CreateProductForm()
    context = {'form': form}

    return render(request,'ibaquotes/product/create.html',context)


def store_product(request):

    if request.method == 'POST':

        return HttpResponse(request.POST.get("name"))

    else:
        return HttpResponse('ERROR REQUEST')

def import_product(request):

    context = {'title': 'base test'}

    return render(request,'ibaquotes/product/importFile.html')