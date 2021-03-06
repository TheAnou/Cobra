import json

from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone

from apps.admin.utils.decorator import access_required
from apps.admin.utils.exception_handling import ExceptionHandler
from apps.grading.views.action import ActionMaker
from apps.seller.models.product import Product
from apps.seller.models.shipping_option import ShippingOption


@access_required('admin')
def productLookup(request):
  context = {}
  if request.method == "POST":
    try:
      context['product'] = Product.objects.get(id=request.POST.get('product_id'))
    except Product.DoesNotExist:
      context['problem'] = "No Product with that ID"
    except Exception as e:
      context['problem'] = str(e)
  return render(request, 'products/product_lookup.html', context)

@access_required('admin')
def reviewProducts(request):
  products_to_review = (Product.objects.filter(approved_at=None,
                                               active_at__lte=timezone.now(),
                                               deactive_at=None,
                                               sold_at=None,
                                               in_holding=False)
                        .order_by('updated_at'))

  products_in_holding = (Product.objects.filter(in_holding=True,
                                                active_at__lte=timezone.now(),
                                                deactive_at=None,
                                                sold_at=None)
                        .order_by('updated_at'))

  context = {'products_to_review': products_to_review,
             'products_in_holding': products_in_holding
            }
  return render(request, 'products/review_products.html', context)

@access_required('admin')
def unratedProducts(request):
  from django.db.models import Count
  unrated_products = (Product.objects.filter(in_holding=False,
                                             active_at__lte=timezone.now(),
                                             deactive_at=None,
                                             sold_at=None)
                      .annotate(rating_count=Count('rating'))
                      .filter(rating_count__lt=15)
                      .exclude(rating__session_key=request.session.session_key)[:50])

  return render(request, 'products/unrated_products.html', {'products':unrated_products})

@access_required('admin')
def approveProduct(request): #from AJAX GET request
  from apps.seller.models.product import Product
  try:
    product = Product.objects.get(id=request.GET.get('product_id'))
    action = request.GET.get('action')

    if action == 'approve':
      product.is_approved = True
      product.save()
    elif action == 'hold':
      product.is_on_hold = True
      product.save()
    elif action == 'delete':
      product.delete()
    else:
      raise Exception('invalid action: %s' % action)

  except Exception as e:
    ExceptionHandler(e, "error on approve_product")
    response = {'error': str(e)}
  else:
    response = {'success': "%s %s" % (action, product.id)}

  return HttpResponse(json.dumps(response), content_type='application/json')

@access_required('admin')
def rateProduct(request): #from AJAX GET request
  from apps.public.models.rating import Rating

  rating_subjects_dict = {name: key for key, name in Rating.SUBJECT_OPTIONS}

  try:
    product_id      = request.GET.get('product_id')
    rating_subject  = request.GET.get('subject')
    rating_value    = request.GET.get('value')

    rating = Rating.objects.filter(
              session_key=request.session.session_key,
              subject=rating_subjects_dict[rating_subject],
              product_id=product_id
            ).first()
    if rating:
      rating.value = rating_value
    else:
      rating = Rating(
                  session_key=request.session.session_key,
                  subject=rating_subjects_dict[rating_subject],
                  product_id=product_id,
                  value = rating_value
                )
    rating.save()
    ActionMaker(rating=rating)

  except Exception as e:
    ExceptionHandler(e, "error on rate_product")
    response = {'error': str(e)}
  else:
    response = {'success': "%s rated" % product_id}

  return HttpResponse(json.dumps(response), content_type='application/json')


def priceCalc(request):
  from apps.common.models.currency import Currency
  exchange_rate = Currency.objects.get(code='MAD').exchange_rate_to_USD
  return render(request, 'products/price_calc.html', {'exchange_rate':exchange_rate})

def getShippingCost(request):
  from apps.seller.views.shipping import calculateShippingCost

  if request.method == "GET":
    if request.GET.get('product_id', None):
      try:
        shipping_cost = Product.objects.get(id=request.GET['product_id']).shipping_cost
      except: pass

    elif request.GET.get('weight') and request.GET.get('shipping_option'):
      try:
        shipping_option = ShippingOption.objects.get(name=request.GET['shipping_option'])
        shipping_cost = calculateShippingCost(request.GET['weight'], shipping_option, 'US')
      except: pass

  try:
    response = {'shipping_cost': shipping_cost}
    return HttpResponse(json.dumps(response), content_type='application/json')
  except:
    return HttpResponse(status=400)#bad request

def getProductData(request):
  if request.method == "GET" and request.GET.get('product_id'):
    try:
      product = Product.objects.get(id=request.GET['product_id'])
      response = {'price':            product.price,
                  'weight':           product.weight,
                  'length':           product.length or 1,
                  'width':            product.width or 1,
                  'height':           product.height or 1,
                  'shipping_option':  product.shipping_options.all()[0].name,
                  'shipping_cost':    product.shipping_cost
                  }
      return HttpResponse(json.dumps(response), content_type='application/json')

    except:
      return HttpResponse(status=500)#server error
  else:
    return HttpResponse(status=400)#bad request
