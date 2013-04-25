from django import template
register = template.Library()

@register.inclusion_tag('inventory/photo_upload.html')
def photo_upload_tag(photo_form, product, rank=None, photo=None):
  if photo is not None:
    rank = photo.rank
    photo_url = photo.thumb
  else:
    photo_url = None

  photo_form.fields['rank'].initial = rank
  photo_form.fields['product'].initial = product.id

  return {'photo_form':photo_form, 'photo_url':photo_url}

@register.inclusion_tag('inventory/product_asset_choosers/asset_chooser.html')
def asset_chooser_tag(request, ilk):
  from seller.models import Asset
  try:
    seller_id = request.session['seller_id']
    assets = Asset.objects.filter(seller_id=seller_id, ilk=ilk)

  except Exception as e:
    assets = None

  return {'assets':assets, 'ilk':ilk}

@register.inclusion_tag('inventory/product_asset_choosers/shipping_option_chooser.html')
def shipping_option_chooser_tag(request):
  from seller.models import Seller, ShippingOption
  try:
    country = Seller.objects.get(id=request.session['seller_id']).country
    shipping_options = ShippingOption.objects.filter(country=country)

  except Exception as e:
    shipping_options = None

  return {'shipping_options':shipping_options}

@register.inclusion_tag('inventory/product_asset_choosers/color_chooser.html')
def color_chooser_tag():
  from admin.models import Color
  try:
    colors = Color.objects.all()
  except Exception as e:
    colors = None
  return {'colors':colors}