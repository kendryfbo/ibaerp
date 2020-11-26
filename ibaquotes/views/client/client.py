from django.shortcuts import render, HttpResponse, redirect
from ibaquotes.forms import CreateProductForm, CreateClientForm
from ibaquotes.models.client import Client

def client_list(request):

    clients = Client.objects.all().order_by('company');
    context = {
        'clients': clients
    }
    return render(request,'ibaquotes/client/list.html',context)


def client_create(request):

    clientForm = CreateClientForm()
    context = {'clientForm': clientForm}

    return render(request,'ibaquotes/client/create.html',context)


def client_store(request):

    if request.method == 'POST':

        # Django is not getting the proper next id so get it manually. "This because the clients where uploaded from database"
        id = Client.objects.latest('id').id + 1

        client = Client(
            id = id,
            username = request.POST.get('username'),
            cfname = request.POST.get('cfname'),
            clname = request.POST.get('clname'),
            usergroup = request.POST.get('usergroup'),
            cemail = request.POST.get('cemail'),
            company = request.POST.get('company'),
            newsletter = request.POST.get('newsletter'),
            address = request.POST.get('address'),
            zipcode = request.POST.get('zipcode'),
            city = request.POST.get('city'),
            country = request.POST.get('country'),
            domain = request.POST.get('domain'),
            phone = request.POST.get('phone'),
        )

        client.save()

        context = {
            'client': client,
        }

        return render(request,'ibaquotes/client/show.html',context)

    else:
        return HttpResponse('ERROR REQUEST')

def client_edit(request,id):

    client = Client.objects.get(pk=id);

    context = {
        'client': client,
    }

    return render(request,'ibaquotes/client/edit.html',context)

def client_update(request,id):

    if request.method == 'POST':

        client = Client.objects.get(pk=id);

        client.username = request.POST.get('username')
        client.cfname = request.POST.get('cfname')
        client.clname = request.POST.get('clname')
        client.usergroup = request.POST.get('usergroup')
        client.cemail = request.POST.get('cemail')
        client.company = request.POST.get('company')
        client.newsletter = request.POST.get('newsletter')
        client.address = request.POST.get('address')
        client.zipcode = request.POST.get('zipcode')
        client.city = request.POST.get('city')
        client.country = request.POST.get('country')
        client.domain = request.POST.get('domain')
        client.phone = request.POST.get('phone')

        client.save()
        
        context = {
            'client': client,
        }

        return render(request,'ibaquotes/client/show.html',context)

    else:
        
        return HttpResponse('ERROR REQUEST')


def client_show(request,id):

    client = Client.objects.get(pk=id);

    context = {
        'client': client,
    }

    return render(request,'ibaquotes/client/show.html',context)

def client_delete(request,id):

    client = Client.objects.get(pk=id).delete();

    context = {
        'client': client,
    }

    return redirect('client-list')