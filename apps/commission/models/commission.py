from datetime import timedelta
from django.db import models
from django.utils import timezone
from apps.communication.views.sms import sendSMS

from apps.public.models.customer import Customer
from apps.seller.models.image import Image
from apps.seller.models.product import Product

class CommissionQuerySet(models.QuerySet):
  def requested(self):
    return self.filter(progress_updated_at__isnull=True,
                       canceled_at__isnull=True)
  def in_progress(self):
    return self.filter(progress_updated_at__isnull=False,
                       complete_at__isnull=True,
                       canceled_at__isnull=True)
  def completed(self):
    return self.filter(complete_at__lte=timezone.now(),
                       canceled_at__isnull=True)

class Commission(models.Model):
  base_product              = models.ForeignKey(Product, null=True, related_name='commissions')
  requirement_images        = models.ManyToManyField(Image)
  product                   = models.OneToOneField(Product, null=True, related_name='commission')
  customer                  = models.ForeignKey(Customer, null=True, related_name='commissions')
  notes                     = models.TextField(null=True, blank=True)

  # DETAILS
  quantity                  = models.SmallIntegerField(default=1)
  length                    = models.IntegerField(null=True, blank=True)
  width                     = models.IntegerField(null=True, blank=True)
  # height                    = models.IntegerField(null=True, blank=True)
  # weight                    = models.IntegerField(null=True, blank=True)
  estimated_artisan_price   = models.IntegerField(null=True, blank=True)
  estimated_display_price   = models.IntegerField(null=True, blank=True)
  price_adjustment          = models.IntegerField(null=True, blank=True)
  estimated_weight          = models.IntegerField(null=True, blank=True)

  artisan_notified_at       = models.DateTimeField(null=True, blank=True)
  artisan_confirmed_at      = models.DateTimeField(null=True, blank=True)
  estimated_completion_date = models.DateTimeField(null=True, blank=True)

  # MILESTONES
  invoice_sent_at           = models.DateTimeField(null=True, blank=True)
  invoice_paid_at           = models.DateTimeField(null=True, blank=True)
  progress_updated_at       = models.DateTimeField(null=True, blank=True)
  progress                  = models.SmallIntegerField(default=0)
  complete_at               = models.DateTimeField(null=True, blank=True)
  customer_confirmed_at     = models.DateTimeField(null=True, blank=True)
  shipped_at                = models.DateTimeField(null=True, blank=True)
  canceled_at               = models.DateTimeField(null=True, blank=True)

  # UPDATE HISTORY
  created_at                = models.DateTimeField(auto_now_add = True)
  updated_at                = models.DateTimeField(auto_now = True)

  #CUSTOMIZED MANAGER
  objects = CommissionQuerySet.as_manager()

  # MODEL PROPERTIES
  @property
  def seller(self):
    if self.product: return self.product.seller
    elif self.base_product: return self.base_product.seller
    else: return None

  @property
  def is_bulk(self):
    return True if self.quantity > 1 else False

  @property
  def progress_photos(self):
    return self.product.photos.filter(is_progress=True) if self.product else []

  @property
  def artisan_notified(self):
    return True if self.artisan_notified_at and self.artisan_notified_at <= timezone.now() else False
  @artisan_notified.setter
  def artisan_notified(self, value):
    if not value:
      self.artisan_notified_at = None
    else:
      self.artisan_notified_at = timezone.now()

  @property
  def artisan_confirmed(self):
    return True if self.artisan_confirmed_at and self.artisan_confirmed_at <= timezone.now() else False
  @artisan_confirmed.setter
  def artisan_confirmed(self, value):
    if not value:
      self.artisan_confirmed_at = None
    elif not self.artisan_confirmed:
      self.artisan_confirmed_at = timezone.now()

  @property
  def invoice_sent(self):
    return True if self.invoice_sent_at and self.invoice_sent_at <= timezone.now() else False
  @invoice_sent.setter
  def invoice_sent(self, value):
    if not value:
      self.invoice_paid_at = None
    else:
      self.invoice_sent_at = timezone.now()

  @property
  def invoice_paid(self):
    return True if self.invoice_paid_at and self.invoice_paid_at <= timezone.now() else False
  @invoice_paid.setter
  def invoice_paid(self, value):
    if not value:
      self.invoice_paid_at = None
    elif not self.invoice_paid:
      self.invoice_paid_at = timezone.now()

  @property
  def in_progress(self):
    return True if self.progress_updated_at else False
  @in_progress.setter
  def in_progress(self, value):
    if not value:
      self.progress_updated_at = None
    else:
      self.progress_updated_at = timezone.now()

  @property
  def complete(self):
    return True if self.complete_at and self.complete_at <= timezone.now() else False
  @complete.setter
  def complete(self, value):
    if not value:
      self.complete_at = None
    elif not self.complete:
      self.complete_at = timezone.now()

  @property
  def customer_confirmed(self):
    return True if self.customer_confirmed_at else False
  @complete.setter
  def complete(self, value):
    if not value:
      self.customer_confirmed_at = None
    elif not self.complete:
      self.customer_confirmed_at = timezone.now()

  @property
  def shipped(self):
    return True if self.shipped_at and self.shipped_at <= timezone.now() else False
  @shipped.setter
  def shipped(self, value):
    if not value:
      self.shipped_at = None
    elif not self.shipped:
      self.shipped_at = timezone.now()

  @property
  def canceled(self):
    return True if self.canceled_at and self.canceled_at <= timezone.now() else False
  @canceled.setter
  def canceled(self, value):
    if not value:
      self.canceled_at = None
    elif not self.canceled:
      self.canceled_at = timezone.now()

  @property
  def has_progress_photo(self):
    return True if len(self.progress_photos) else False

  @property
  def days_to_complete(self):
    if self.estimated_completion_date:
      return (self.estimated_completion_date - timezone.now() + timedelta(days=1)).days

  @property
  def payment_receipt(self):
    try:
      return self.product.orders.first().checkout.receipt
    except:
      return ""

  @property
  def public_id(self): return "C%d" % self.id

  # MODEL FUNCTIONS
  def createDisplayPriceEstimate(self, save=True):
    if not any([self.base_product, self.product]):
      raise Exception("createDisplayPriceEstimate requires existing instance of base_product or product")

    self.product = self.createProduct(save=save)

    if save and self.product.display_price:
      self.estimated_display_price = self.product.display_price
      self.save()

    return self.product.display_price or None

  def createWeightEstimate(self, save=True):
    self.product = self.createProduct(save=save)
    if save:
      self.estimated_weight = self.product.weight
      self.save()
    return self.product.weight

  def createProduct(self, save=True, seller=None):
    if not any([self.base_product, self.product, seller]):
      raise Exception("createProduct requires either seller or existing base_product instance")

    if not self.base_product:
        self.product = Product(seller=seller) if not self.product else self.product
        self.product.length = self.length
        self.product.width = self.width
        # self.product.height = self.height

    else:
      self.mock_product = Product(seller=self.base_product.seller) if not self.product else self.product
      self.base_product.sortDimensions() #sorts base_product dimensions and all set to positive integers
      base_size = self.base_product.length * self.base_product.width
      self.mock_product.length = self.length or self.base_product.length
      self.mock_product.width = self.width or self.base_product.width
      self.mock_product.height = self.base_product.height

      new_size = self.mock_product.length * self.mock_product.width
      ratio = float(new_size) / base_size

      if not self.mock_product.weight:
        self.mock_product.weight = int(((self.base_product.weight * ratio * 1.05) + 100) * self.quantity)
      if not self.mock_product.price or not self.estimated_artisan_price:
        self.mock_product.price = int(self.base_product.price * ratio * self.quantity)
        self.estimated_artisan_price = self.mock_product.price

    if save:
      self.mock_product.save()
      self.product = self.mock_product
      self.save()
      return self.product
    else:
      return self.mock_product

  def getCustomer(self):
    if not self.customer:
      self.customer = Customer.objects.create()
    return self.customer

  def update(self, var, val):
    val = val.strip() if val else ""
    if var == 'quantity':
      self.quantity = int(val)
    elif var == 'requested-length':
      self.length = int(val)
    elif var == 'requested-width':
      self.width = int(val)
    elif var =='weight':
      self.estimated_weight = int(val)
    elif var == 'days-to-complete':
      self.estimated_completion_date = timezone.now() + timedelta(days=int(val.strip('days')))
    elif var == 'progress':
      self.progress = int(val.strip('%'))
      self.in_progress = bool(self.progress)
    elif var == 'country':
      self.customer = self.getCustomer()
      self.customer.country = val
      self.customer.save()
    elif var == 'invoice-price':
      self.estimated_display_price = int(val)


  def askArtisan(self):
    """C%d\r\n%d\r\n%"""

    message = "C%d\r\n#%d\r\n" % (self.id, self.base_product.id)
    message += "%d" % self.length
    if self.width:
      message += " x %d" % self.width
    message += "\r\n"
    if self.quantity > 1:
      message += "*%d\r\n" % int(self.quantity or 0)
    message += "%d\r\n" % int(self.estimated_artisan_price or 0)
    # print message
    sendSMS(message, self.seller.account.phone)


#SIGNALS AND SIGNAL REGISTRATION
from django.dispatch import receiver
from django.db.models.signals import pre_save

# @receiver(pre_save, sender=Commission)
# def createRelatedObjects(sender, instance, **kwargs):
#   if instance.estimated_display_price and not instance.customer:
#     instance.customer = Customer.objects.create()
