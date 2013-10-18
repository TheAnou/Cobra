from django.db import models

class Cart(models.Model):
  #from apps.admin.models import Currency

  email               = models.EmailField(blank=True, null=True)
  name                = models.CharField(max_length=100, null=True, blank=True)
  address_name        = models.CharField(max_length=100, null=True, blank=True)
  address1            = models.CharField(max_length=100, null=True, blank=True)
  address2            = models.CharField(max_length=100, null=True, blank=True)
  city                = models.CharField(max_length=50,  null=True, blank=True)
  state               = models.CharField(max_length=50,  null=True, blank=True)
  postal_code         = models.CharField(max_length=15,  null=True, blank=True)
  country             = models.CharField(max_length=50,  null=True, blank=True)

  promotions          = models.ManyToManyField('Promotion')

  wepay_checkout_id   = models.BigIntegerField(null=True, blank=True)
  anou_checkout_id    = models.CharField(max_length=15, null=True, blank=True)
  checked_out         = models.BooleanField(default=False)#does not need to be a date

  #total_charge        = models.DecimalField(max_digits=8, decimal_places=2,
  #                                          null=True, blank=True)
  #total_discount      = models.DecimalField(max_digits=8, decimal_places=2,
  #                                          null=True, blank=True)
  #total_paid          = models.DecimalField(max_digits=8, decimal_places=2,
  #                                          null=True, blank=True)
  #total_refunded      = models.DecimalField(max_digits=8, decimal_places=2,
  #                                          null=True, blank=True)
  #currency            = models.ForeignKey(Currency, null=True, blank=True)

  receipt             = models.TextField(blank=True, null=True)
  notes               = models.TextField(blank=True, null=True)

  #update history
  created_at          = models.DateTimeField(auto_now_add = True)
  updated_at          = models.DateTimeField(auto_now = True)

  @property
  def checkout_id(self):
    if self.wepay_checkout_id:
      return self.wepay_checkout_id
    elif self.anou_checkout_id:
      return self.anou_checkout_id
    else:
      return False

class Item(models.Model):
  from apps.seller.models import Product
  cart                = models.ForeignKey('Cart')
  product             = models.ForeignKey(Product)
  #quantity           = models.PositiveIntegerField(default=1)

  @property
  def order(self):
    return self.product.order_set.get(cart=self.cart)

  @property
  def price(self):
    return self.product.display_price

  @property
  def photos(self):
    from apps.seller.models import Photo
    return Photo.objects.filter(product_id=self.product.id)

  @property
  def photo(self):
    photos = self.photos
    try: return photos[0]
    except: return None

  def __unicode__(self):
    #return u'%d units of %s' % (self.quantity, self.product.name)
    return unicode(self.product.name)

class Promotion(models.Model):
  name                = models.CharField(max_length=50,  null=True, blank=True)
  #description         = models.CharField(max_length=200, null=True, blank=True)
  #code                = models.CharField(max_length=50,  null=True, blank=True)
  #automatic           = models.BooleanField(default=False) #auto apply to cart

  #valid_on            = models.DateTimeField(null=True, blank=True)
  #expires_on          = models.DateTimeField(null=True, blank=True)

  def __unicode__(self):
    return unicode(self.name)

class Order(models.Model):
  from apps.seller.models import Product, ShippingOption

  cart                = models.ForeignKey('Cart')

  #charges breakdown in local currency (eg. dirhams in Morocco)
  products_charge     = models.DecimalField(max_digits=8, decimal_places=2)
  anou_charge         = models.DecimalField(max_digits=8, decimal_places=2)
  shipping_charge     = models.DecimalField(max_digits=8, decimal_places=2)
  total_charge        = models.DecimalField(max_digits=8, decimal_places=2)

  shipping_option     = models.ForeignKey(ShippingOption, null=True, blank=True)
  #reported weight and cost after shipped
  shipping_weight     = models.FloatField(blank=True, null=True)
  shipping_cost       = models.DecimalField(blank=True, null=True,
                                            max_digits=8, decimal_places=2)
  tracking_number     = models.CharField(max_length=50, null=True, blank=True)

  seller_paid_amount  = models.DecimalField(blank=True, null=True,
                                            max_digits=8, decimal_places=2)

  #order items
  products            = models.ManyToManyField(Product)

  #Status
  seller_notified_at  = models.DateTimeField(null=True, blank=True)
  seller_confirmed_at = models.DateTimeField(null=True, blank=True)
  shipped_at          = models.DateTimeField(null=True, blank=True)
  received_at         = models.DateTimeField(null=True, blank=True)
  reviewed_at         = models.DateTimeField(null=True, blank=True)
  seller_paid_at      = models.DateTimeField(null=True, blank=True)
  returned_at         = models.DateTimeField(null=True, blank=True)

  #update history
  created_at          = models.DateTimeField(auto_now_add = True)
  updated_at          = models.DateTimeField(auto_now = True)

  #derivative attributes
  @property
  def seller(self): return self.products.all()[0].seller

  @property
  def is_seller_notified(self): return True if self.seller_notified_at else False
  @property
  def is_seller_confirmed(self): return True if self.seller_confirmed_at else False
  @property
  def is_shipped(self): return True if self.shipped_at else False
  @property
  def is_received(self): return True if self.received_at else False
  @property
  def is_reviewed(self): return True if self.reviewed_at else False
  @property
  def is_seller_paid(self): return True if self.seller_paid_at else False

  @property
  def tracking_url(self):
    if self.tracking_number:
      return "https://tools.usps.com/go/TrackConfirmAction_input?qtc_tLabels1=" + self.tracking_number
    else: return False

class Rating(models.Model):
  from apps.seller.models import Product
  from apps.admin.models import RatingSubject

  session_key         = models.CharField(max_length=32)
  product             = models.ForeignKey(Product)
  subject             = models.ForeignKey(RatingSubject)
  value               = models.SmallIntegerField()
  created_at          = models.DateTimeField(auto_now_add = True)

  def __unicode__(self):
    return unicode(self.value)
