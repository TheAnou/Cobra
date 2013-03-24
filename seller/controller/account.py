from django.http import HttpResponse, Http404
from django.utils import simplejson
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404
from admin.controller.decorator import access_required

@access_required('seller')
def home(request, context={}):
  return render(request, 'account/home.html')

def create(account_id):
  try:
    from seller.models import Seller
    account = Seller(account_id=account_id)
    account.save()
    return True
  except Exception as e:
    context = {'exception': e}
    return False

@access_required('seller')
def edit(request):
  from seller.models import Seller
  from seller.controller.forms import *
  from django.forms.formsets import formset_factory
  from seller.controller.aws_forms import S3UploadForm
  from anou import settings
  from datetime import datetime

  if request.method == 'POST':

    seller_form = SellerEditForm(request.POST)
    try: # it must be a post to work
      if seller_form.is_valid():
        seller_data = seller_form.cleaned_data
        seller = Seller.objects.get(id=request.session['seller_id'])
        seller.update(data)
        seller.save()
        return HttpResponseRedirect('account/home/')

    except Exception as e:
      context = {'exception': e}

  else: #not POST
    seller_form   = SellerEditForm()
    if 'admin_id' not in request.session:
      seller_form.fields['country'].widget.attrs['disabled'] = True
      seller_form.fields['currency'].widget.attrs['disabled'] = True

    asset_form = AssetForm()

    prefix_key = 'images/seller_' + str(request.session['seller_id'])
    if settings.DEBUG: prefix_key = 'test/'+prefix_key
    image_form = S3UploadForm(settings.AWS_ACCESS_KEY_ID,
                              settings.AWS_SECRET_ACCESS_KEY,
                              settings.AWS_STORAGE_BUCKET_NAME,
                              prefix_key,
                              success_action_redirect = reverse('seller:save image'))
    key_date = datetime.now().strftime('%Y-%m-%d-%H-%M')

  context = {
              'seller_form': seller_form,
              'asset_form': asset_form,
              'image_form': image_form,
              'key_date': key_date,
              'asset_ilks': ['artisan','product','tool','material']
            }
  return render(request, 'account/edit.html', context)

@access_required('seller')
def asset(request): # use api.jquery.com/jQuery.post/
  from seller.models import Asset
  from admin.models import Category
  from seller.controller.forms import AssetProductForm
  from django.forms.formsets import formset_factory

  try: # it must be an ajax post to work
    form = AssetForm(request.POST, request.FILES)
    if formset.is_valid():
      #asset = Asset.objects.get_or_create(**form.cleaned_data)
      #use image url to lookup image and assign it
      #asset.save()
      context = {'sucess': True}
    else:
      context = {'problem': "invalid form data"}

  except Exception as e:
    context = {'exception': e}

  return HttpResponse(context) #ajax response

@access_required('seller')
def saveImage(request): #ajax requests only
  from seller.models import Image, Asset, Seller
  from seller.controller.aws_forms import S3UploadForm
  from anou import settings
  from django.core.validators import URLValidator
  from django.core.exceptions import ValidationError
  validate = URLValidator(verify_exists=True)
  url_root = "http://s3.amazonaws.com/anou/"

  try:

    url = url_root + request.GET[u'url']
    ilk = str(request.GET[u'ilk'])

    validate(url)#will throw a ValidationError exception error if invalid

    image = Image(url=url)
    image.save()

    #save Image and create or update Asset
    if 'asset' in request.GET:
      asset = Asset.get(id=request.GET[u'asset'])
      asset.image = image
      asset.save()
    else:
      seller = Seller.objects.get(id=request.session['seller_id'])
      asset = Asset(seller=seller, ilk=ilk, image=image)
      asset.save()

    #pull image from url (on S3)
    #create thumb and pinky using easy-thumbnail app
    #save thumb and pinky on S3
    #return thumbnail url

    response = {'asset':asset.id, 'url':url}

  except ValidationError:
    response = {'problem': "url does not exist yet"}

  except Exception as e:
    response = {'exception': str(e)}

  return HttpResponse(simplejson.dumps(response), mimetype='application/json')
