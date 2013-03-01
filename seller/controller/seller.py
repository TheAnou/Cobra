from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from admin.controller import decorator

@decorator.requires_seller_or_admin
def home(request):
  return render(request, 'seller/home.html')

@decorator.requires_seller_or_admin
def edit(request):
  if request.method == 'POST':
    try: # it must be a post to work
      name      = request.POST['name']
      email     = request.POST['email']
      phone     = request.POST['phone']
      bio       = request.POST['bio']
      country   = request.POST['country']
      currency  = request.POST['currency']

      seller = Seller.objects.get(pk=request.session['seller_pk'])

    except Exception as e:
      context = {'exception': e}

  #collect all seller info and assets for template

  return render(request, 'seller/edit.html', context)

@decorator.requires_seller_or_admin
def asset(request): # use api.jquery.com/jQuery.post/
  from seller.models import Asset, Category
  try: # it must be a post to work
    ilk =          request.POST['asset_ilk']
    rank =   request.POST['asset_rank']
    name =         request.POST['asset_name']
    description =  request.POST['asset_description']

    asset = Asset.objects.get_or_create(
      ilk = ilk,
      rank = rank
    )

    asset.name = name
    asset.description = description

    if ilk == "product" and 'category' in request.POST:
      category_string = request.POST['category']
      #category string is a string of space separated category names
      category_object_list = []
      for category_name in category_string.split():
        #split() created a list of strings, one for each category name
        category_object = Category.object.get(name=category_name)
        category_object_list.append(category_object)

      asset.category.add(*category_object_list)

    asset.save()
    context = {'sucess': "asset saved"}

  except Exception as e:
    context = {'exception': e}

  if 'sucess' in context:
    return HttpResponse("success") #ajax response
