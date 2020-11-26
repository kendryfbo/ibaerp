from django.db import IntegrityError
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, HttpResponse, redirect
from ibaquotes.models.product import Product, ProductStatus
from ibaquotes.forms import CreateProductForm

def product_list(request):

    products = Product.objects.all().values('pk','pdid','name','status','weight','date','harmonizedcode')
    context = {
        'products': products
    }
    return render(request,'ibaquotes/product/list.html',context)


def product_create(request):

    productStatus = ProductStatus.objects.all()
    context = {
        'productStatus': productStatus}

    return render(request,'ibaquotes/product/create.html',context)


def product_store(request):

    if request.method == 'POST':

        try:   
            
            imagePath = request.FILES.get('imagepath', False)
            if imagePath != False:
                fs = FileSystemStorage()
                filename = fs.save(imagePath.name, imagePath)

            product = Product(
            pdid = request.POST.get('pdid'), 
            name = request.POST.get('name'),
            descr1 = request.POST.get('descr1'), 
            descr2 = request.POST.get('descr2'),  
            detail = request.POST.get('detail'), 
            remarks = request.POST.get('remarks'), 
            status_id = request.POST.get('status'), 
            price= request.POST.get('price'), 
            date = request.POST.get('date'), 
            handlager = request.POST.get('handlager') if request.POST.get('handlager') else None,
            lang_id = request.POST.get('lang_id') if request.POST.get('lang_id') else None, 
            weight = request.POST.get('weight'),
            ptype = request.POST.get('ptype'), 
            harmonizedcode =  request.POST.get('harmonizedcode') if request.POST.get('harmonizedcode') else None,
            eccn = request.POST.get('eccn'),  
            lkz = request.POST.get('lkz'),   
            ag = request.POST.get('ag'),  
            imageurl = imagePath, 
            imagepath = request.POST.get('imagepath'),)

            product.save()

        except IntegrityError as e:
            return HttpResponse(e)

        return redirect('product-list')

    else:
        return HttpResponse('ERROR REQUEST')


def product_show(request,id):

    product = Product.objects.get(pk=id)

    context = {
        'product': product
    }

    return render(request,'ibaquotes/product/show.html',context)

def product_edit(request, id):

    product = Product.objects.get(pk=id)
    productStatus = ProductStatus.objects.all()
    context = {
        'product': product,
        'productStatus': productStatus,
    }

    return render(request,'ibaquotes/product/edit.html',context)
    
def product_update(request, id):
    
    if request.method == 'POST':

        product = Product.objects.get(pk=id);
        imagePath = request.FILES['imagepath']
        fs = FileSystemStorage()
        filename = fs.save(imagePath.name, imagePath)
    
        product.pdid = request.POST.get('pdid')
        product.name = request.POST.get('name')
        product.descr1 = request.POST.get('descr1') 
        product.descr2 = request.POST.get('descr2')  
        product.detail = request.POST.get('detail') 
        product.remarks = request.POST.get('remarks') 
        product.status_id = request.POST.get('status') 
        product.price= request.POST.get('price')
        product.date = request.POST.get('date') 
        product.handlager = request.POST.get('handlager')
        product.lang_id = request.POST.get('lang_id') 
        product.weight = request.POST.get('weight')
        product.ptype = request.POST.get('ptype') 
        product.harmonizedcode = request.POST.get('harmonizedcode')
        product.eccn = request.POST.get('eccn')
        product.lkz = request.POST.get('lkz') 
        product.ag = request.POST.get('ag') 
        product.imageurl = imagePath
        product.imagepath = request.POST.get('imagepath')

        product.save()

        return redirect('product-list')

    else:
        return HttpResponse('ERROR REQUEST')


def product_delete(request, id):

    product = Product.objects.get(pk=id).delete()

    return redirect('product-list')


def product_import(request):

    context = {'title': 'base test'}

    return render(request,'ibaquotes/product/importFile.html')