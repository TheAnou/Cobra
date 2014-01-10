from django.conf.urls import patterns, include, url
from apps.admin.controller import dashboard, account, products, orders, communication, site_management

#ACCOUNT PAGES
urlpatterns = patterns('',
  #Todo: I'd like to add the word "secure" into all account and checkout pages
    # just to give the user more peace of mind.

  url(r'^create_admin$', account.createAdmin, name='create admin'),
  url(r'^create_seller$', account.createSeller, name='create seller'),

  url(r'^admin_accounts$', account.adminAccounts, name='admin accounts'),
  url(r'^seller_accounts$', account.sellerAccounts, name='seller accounts'),

  url(r'^edit_account/(?P<account_id>\d+)?$', account.edit, name='edit account'),
  url(r'^reset_password/(?P<account_id>\d+)?$', account.resetPassword, name='reset password'),

  url(r'^login_cheat$', account.loginCheat, name='login cheat'),
)

#DASHBOARD PAGES
urlpatterns += patterns('',
  url(r'^dashboard$', dashboard.dashboard, name='dashboard'),

  #SELLER ACCOUNTS
  url(r'^ajax/approve_seller$', account.approveSeller, name='approve seller'),

  #PRODUCTS
  url(r'^review_products$', products.reviewProducts, name='review products'),
  url(r'^unrated_products$', products.unratedProducts, name='unrated products'),
  url(r'^ajax/approve_product$', products.approveProduct, name='approve product'),
  url(r'^ajax/rate_product$', products.rateProduct, name='rate product'),
  url(r'^product_lookup$', products.productLookup, name='product lookup'),
  url(r'^price_calc$', products.priceCalc, name='price calc'),

  #ORDERS
  url(r'^orders/(?P<year>\d+)?/(?P<week>\d+)?$', orders.orders, name='orders range'),
  url(r'^orders$', orders.orders, name='orders'),
  url(r'^order/(?P<order_id>\d+)$', orders.order, name='order'),
  url(r'^ajax/update_order$', orders.updateOrder, name='update order'),
  url(r'^ajax/order_image_data$', orders.imageFormData, name='image form data'),

  #COMMUNICATION
  url(r'^send_sms$', communication.sendSMS, name='send sms'),
  url(r'^sms$', communication.allSMS, name='all sms'),
  url(r'^email$', communication.allEmail, name='all email'),

  #EXTRAS
  url(r'^stats$', dashboard.stats, name='stats'),
  url(r'^research$', dashboard.research, name='research'),

  #SETTINGS
  url(r'^management/country$', site_management.country, name='country'),
  url(r'^management/currency$', site_management.currency, name='currency'),
  url(r'^management/color$', site_management.color, name='color'),
  url(r'^management/category$', site_management.category, name='category'),
  url(r'^management/rating_subject$', site_management.ratingSubject, name='rating subject'),
  url(r'^management/shipping_option$', site_management.shippingOption, name='shipping option'),
  url(r'^management/image_object$', site_management.imageObject, name='image object'),
)

#MANUAL CACHE REBUILDs
urlpatterns += patterns('',
  url(r'^re_homepg$', site_management.rebuildHomePage, name='rebuild homepage'),
  url(r'^re_productpg/(?P<product_id>\d+)$', site_management.rebuildProductPage, name='rebuild productpage'),
  url(r'^re_storepg/(?P<seller_id>\d+)$', site_management.rebuildStorePage, name='rebuild storepage'),
  url(r'^re_prod_ranks$', site_management.rebuildProductRankings, name='rebuild product rankings'),
)
