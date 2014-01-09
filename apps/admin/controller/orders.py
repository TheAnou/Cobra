from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.utils import timezone, dateformat
from apps.admin.utils.decorator import access_required
from django.views.decorators.csrf import csrf_exempt
from apps.admin.utils.exception_handling import ExceptionHandler
from django.contrib import messages
from apps.communication.controller.email_class import Email
from apps.communication.controller.sms import sendSMS
from apps.public.models import Order
from settings.settings import CLOUDINARY

@access_required('admin')
def allOrders(request):
  orders = Order.objects.all().order_by('created_at').reverse()[:50]

  context = {'orders': orders}
  return render(request, 'orders/all_orders.html', context)

@access_required('admin')
def order(request, order_id):
  try:
    order = Order.objects.get(id=order_id)
    order.shipping_address = order.cart.shipping_address.replace('\n','<br>')

    return render(request, 'orders/order.html', {'order': order, 'CLOUDINARY':CLOUDINARY})
  except Exception as e:
    print str(e)
    return redirect('admin:all orders')

@access_required('admin')
def updateOrder(request):
  from django.utils import timezone

  if request.method == 'GET':
    order_id = request.GET.get('order_id')
    action = request.GET.get('action')
    order = Order.objects.get(id=order_id)

    if action == "seller paid":
      order.seller_paid_at = timezone.now()

      #SEND EMAIL WITH RECEIPT TO SELLER
      if order.seller.account.email:
        message = "%d: %s" % (order.products.all()[0].id, order.seller_paid_receipt.original)
        email = Email(message=message, subject="$")
        email.assignToOrder(order)
        email.sendTo(order.seller.account.email)

      #SEND SMS TO SELLER
      if order.seller.account.phone:
        message = ("%d\r\n$\r\n%dDh" %
                    (order.products.all()[0].id, int(order.seller_paid_amount)))
        message += "\r\n"
        message += ("Anou transfere %d Dh a votre compte pour les produit: %d" %
                    (order.seller_paid_amount, order.products.all()[0].id))
        sendSMS(message, order.seller.account.phone)

    elif action == "add note": #requires order_id, note
      if request.GET.get('note'):
        timestamp = timezone.now()
        note = timestamp.strftime("%H:%M %d/%m/%y - ") + str(request.GET['note'])
        order.notes = order.notes if order.notes else ""
        order.notes += "\n" + note

    order.save()
    return HttpResponse(status=200)#OK

  else:
    return HttpResponse(status=402)#bad request

@access_required('admin')
@csrf_exempt #find a way to add csrf
def imageFormData(request):
  import json
  from apps.seller.controller.cloudinary_upload import createSignature
  from apps.seller.models import Upload

  if request.method == "POST" and 'order_id' in request.POST:
    try:
      order = Order.objects.get(id=request.POST['order_id'])
      timestamp   = dateformat.format(timezone.now(), u'U')#unix timestamp

      #uniquely name every image e.g. "seller23_order123_receipt_time1380924180"
      image_id  = "seller"+str(order.seller.id)
      image_id += "_order"+str(order.id)
      image_id += "_receipt"
      image_id += "_time"+str(timestamp)
      #tag image with seller_id and asset_ilk
      tags = "seller"+str(order.seller.id)+",order"+str(order.id)+",receipt"

      #save as a pending upload
      Upload(public_id = image_id).save()

      form_data = {
        'public_id':        image_id,
        'tags':             tags,
        'api_key':          CLOUDINARY['api_key'],
        'format':           CLOUDINARY['format'],
        'transformation':   CLOUDINARY['transformation'],
        'timestamp':        timestamp,
        'notification_url': request.build_absolute_uri(reverse('seller:complete upload')),
      }
      form_data['signature'] = createSignature(form_data)

      return HttpResponse(json.dumps(form_data), content_type='application/json')

    except Exception as e:
      ExceptionHandler(e, "in orders.imageFormData")
      return HttpResponse(status=500)#server error

  else:
    return HttpResponse(status=402)#bad request
