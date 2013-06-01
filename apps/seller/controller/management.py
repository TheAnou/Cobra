from django.http import HttpResponse
from django.utils import simplejson
from django.shortcuts import render, redirect
from apps.admin.controller.decorator import access_required
from django.views.decorators.csrf import csrf_exempt

@access_required('seller')
def home(request, context={}):
  from apps.seller.models import Seller

  try:
    seller = Seller.objects.get(id=request.session['seller_id'])
    products = seller.product_set.all()
    context['seller'] = seller
    context['products'] = products
  except Exception as e:
    context = {'exception': e}

  return render(request, 'management/home.html', context)

@access_required('seller')
def orders(request):
  from apps.seller.models import Seller

  context = {}
  try:
    seller = Seller.objects.get(id=request.session['seller_id'])
    products = seller.product_set.all()
    context['seller'] = seller

  except Exception as e:
    context = {'exception': e}

  return render(request, 'management/orders.html', context)

@access_required('seller')
def catalog(request):
  from apps.seller.models import Seller

  context = {}
  try:
    seller = Seller.objects.get(id=request.session['seller_id'])
    products = seller.product_set.all()
    context['seller'] = seller

  except Exception as e:
    context = {'exception': e}

  return render(request, 'management/catalog.html', context)

@access_required('seller')
def test(request):
  from apps.seller.controller.forms import PhotoForm2
  from apps.seller.models import Product

  context = {
    'photo_form': PhotoForm2(),
    'product':    Product.objects.get(id=1)
  }
  if request.method == 'GET':
    context['data'] = request.GET

  return render(request, 'management/test.html', context)

@access_required('seller')
@csrf_exempt
def photoFormData(request):
  from settings.settings import CLOUDINARY
  if request.method == "POST":
    product_id  = request.POST['product']
    rank        = request.POST['rank']
    seller_id   = request.session['seller_id']
    timestamp   = getUnixTimestamp()

    #uniquely name every photo e.g. "seller23_product1024_rank1"
    photo_id  = "seller"+str(seller_id)
    photo_id += "_product"+str(product_id)
    photo_id += "_rank"+str(rank)
    photo_id += "_time"+str(timestamp)
    #tag photo with product_id and seller_id
    tags = "product"+str(product_id)+",seller"+str(seller_id)

    form_data = {
      'public_id':      photo_id,
      'tags':           tags,
      'api_key':        CLOUDINARY['api_key'],
      'format':         CLOUDINARY['format'],
      'transformation': CLOUDINARY['transformation'],
      'timestamp':      timestamp,
    }
    form_data['signature'] = getSignature(form_data)
  return HttpResponse(simplejson.dumps(form_data), mimetype='application/json')


def signForm(photo_form, tags=""):
  photo_form.fields['tags'].initial = tags
  photo_form.fields['timestamp'].initial = getUnixTimestamp()
  photo_form.fields['signature'].initial = getSignatureHash(photo_form)
  return photo_form

def getUnixTimestamp():
  from django.utils.dateformat import format
  from datetime import datetime
  return format(datetime.now(), u'U')

def getSignatureHash(photo_form):
  from settings.settings import CLOUDINARY
  import hashlib
  cloudinary_string  = 'format=' + photo_form.fields['format'].initial
  cloudinary_string += '&tags=' + photo_form.fields['tags'].initial
  cloudinary_string += '&timestamp=' + photo_form.fields['timestamp'].initial
  cloudinary_string += '&transformation=' + photo_form.fields['transformation'].initial
  cloudinary_string += CLOUDINARY['api_secret']

  h = hashlib.new('sha1')
  h.update(cloudinary_string)
  return h.hexdigest()

def getSignature(data):
  from settings.settings import CLOUDINARY
  import hashlib
  cloudinary_string  = 'format='          + data['format']
  cloudinary_string += '&public_id='      + data['public_id']
  cloudinary_string += '&tags='           + data['tags']
  cloudinary_string += '&timestamp='      + data['timestamp']
  cloudinary_string += '&transformation=' + data['transformation']
  cloudinary_string += CLOUDINARY['api_secret']

  h = hashlib.new('sha1')
  h.update(cloudinary_string)
  return h.hexdigest()