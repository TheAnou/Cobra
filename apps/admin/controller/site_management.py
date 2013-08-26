from django.http import HttpResponse
from django.shortcuts import render, redirect
from apps.admin.controller.decorator import access_required
from django.contrib import messages
from django.forms.models import modelformset_factory
from django.utils import simplejson

@access_required('admin')
def country(request):
  from apps.admin.models import Country
  CountryFormSet = modelformset_factory(Country)
  context = {}
  if request.method == 'POST':
    formset = CountryFormSet(request.POST)
    try:
      formset.save()
      messages.success(request, 'Country saved.')
    except Exception as e:
      messages.error(request, e)
  formset = CountryFormSet(queryset=Country.objects.all())
  context['formset'] = formset
  return render(request, 'site_management/formset.html', context)

@access_required('admin')
def currency(request):
  from apps.admin.models import Currency
  CurrencyFormSet = modelformset_factory(Currency)
  context = {}
  if request.method == 'POST':
    formset = CurrencyFormSet(request.POST)
    try:
      formset.save()
      messages.success(request, 'Currency saved.')
    except Exception as e:
      messages.error(request, e)
  formset = CurrencyFormSet(queryset=Currency.objects.all())
  context['formset'] = formset
  return render(request, 'site_management/formset.html', context)

@access_required('admin')
def color(request):
  from apps.admin.models import Color
  ColorFormSet = modelformset_factory(Color)
  context = {}
  if request.method == 'POST':
    formset = ColorFormSet(request.POST)
    try:
      formset.save()
      messages.success(request, 'Color saved.')
    except Exception as e:
      messages.error(request, e)
  formset = ColorFormSet(queryset=Color.objects.all())
  context['formset'] = formset
  return render(request, 'site_management/formset.html', context)

@access_required('admin')
def category(request):
  from apps.admin.models import Category
  CategoryFormSet = modelformset_factory(Category)
  context = {}
  if request.method == 'POST':
    formset = CategoryFormSet(request.POST)
    try:
      formset.save()
      messages.success(request, 'Category saved.')
    except Exception as e:
      messages.error(request, e)
  formset = CategoryFormSet(queryset=Category.objects.all())
  context['formset'] = formset
  return render(request, 'site_management/formset.html', context)

@access_required('admin')
def rating_subject(request):
  from apps.admin.models import RatingSubject
  RatingSubjectFormSet = modelformset_factory(RatingSubject)
  context = {}
  if request.method == 'POST':
    formset = RatingSubjectFormSet(request.POST)
    try:
      formset.save()
      messages.success(request, 'Rating Subject saved.')
    except Exception as e:
      messages.error(request, e)
  formset = RatingSubjectFormSet(queryset=RatingSubject.objects.all())
  context['formset'] = formset
  return render(request, 'site_management/formset.html', context)

@access_required('admin')
def shipping_option(request):
  from apps.seller.models import ShippingOption
  ShippingOptionFormSet = modelformset_factory(ShippingOption)
  context = {}
  if request.method == 'POST':
    formset = ShippingOptionFormSet(request.POST)
    try:
      formset.save()
      messages.success(request, 'Shipping Option saved.')
    except Exception as e:
      messages.error(request, e)
  formset = ShippingOptionFormSet(queryset=ShippingOption.objects.all())
  context['formset'] = formset
  return render(request, 'site_management/formset.html', context)

@access_required('admin')
def image_object(request):
  from apps.seller.models import Image
  ImageFormSet = modelformset_factory(Image)
  context = {}
  if request.method == 'POST':
    formset = ImageFormSet(request.POST)
    try:
      formset.save()
      messages.success(request, 'Image Object saved.')
    except Exception as e:
      messages.error(request, e)
  formset = ImageFormSet(queryset=Image.objects.all())
  context['formset'] = formset
  return render(request, 'site_management/formset.html', context)