from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.views.generic import TemplateView,ListView,DetailView
from museumapp.models import *
from museumapp.serializers import *
from rest_framework import generics
from rest_framework.generics import ListAPIView
from django.http import *

from django.db.models import Count, Q
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic

from django.urls import reverse, reverse_lazy
from django import forms
from django.views.generic.edit import FormMixin
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

import json
import os

# from .forms import DataForm, RequirementForm

# from posts.models import Post
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response


from .serializers import ObjectSerializer
from .pagination import StandardResultsSetPagination



from django.views.decorators.csrf import csrf_exempt
import smtplib, ssl
from email.mime.text import MIMEText
from django.db import connection




# Create your views here.

def get_json_file():
	# region = os.path.join(settings.STATIC_ROOT,'aspire/region.json')
	# property_file = os.path.join(settings.STATIC_ROOT,'aspire/property_name.json')

	with open('/mocamuseum/site/public/static/museumapp/object_type.json', 'w') as outfile:
		object_type_list = []
		object_type = Object.objects.exclude(object_type__isnull=True).\
			exclude(object_type__exact='').order_by('object_type').values_list('object_type').distinct()
		for i in list(object_type):
			data = {}
			data['team'] = i[0]
			object_type_list.append(data)
		json.dump(object_type_list, outfile)

	with open('/mocamuseum/site/public/static/museumapp/material.json', 'w') as outfile:
		material_list = []
		material = Object.objects.exclude(material__isnull=True).\
			exclude(material__exact='').order_by('material').values_list('material').distinct()
		for i in list(material):
			data = {}
			data['team'] = i[0]
			material_list.append(data)
		json.dump(material_list, outfile)

	with open('/mocamuseum/site/public/static/museumapp/location.json', 'w') as outfile:
		location_list = []
		location = Object.objects.exclude(location__isnull=True).\
			exclude(location__exact='').order_by('location').values_list('location').distinct()
		for i in list(location):
			data = {}
			data['team'] = i[0]
			location_list.append(data)
		json.dump(location_list, outfile)

	with open('/mocamuseum/site/public/static/museumapp/period.json', 'w') as outfile:
		period_list = []
		time_period = Object.objects.exclude(time_period__isnull=True).\
			exclude(time_period__exact='').order_by('time_period').values_list('time_period').distinct()
		for i in list(time_period):
			data = {}
			data['team'] = i[0]
			period_list.append(data)
		json.dump(period_list, outfile)

	with open('/mocamuseum/site/public/static/museumapp/category.json', 'w') as outfile:
		category_list = []
		category = Featured_Event.objects.exclude(category__isnull=True).\
			exclude(category__exact='').order_by('category').values_list('category').distinct()
		for i in list(category):
			data = {}
			data['team'] = i[0]
			period_list.append(data)
		json.dump(category_list, outfile)
	return 0


class CollectionPage(ListView):
	template_name = "museumapp/collection.html"
	context_object_name = "collection"
	def get_queryset(self):
		return Collection.objects.all()


class ObjectViewPage(ListView):  
	template_name = "museumapp/listofObjects.html"
	context_object_name = "objectslist"
	
	def get_queryset(self):
		return Object.objects.all()


class CollectionObjectDetails(DetailView):
	model = Object
	template_name = "museumapp/colldetails.html"
	context_object_name = "objects"
	def get_query(self, **kwargs):
		demo = self.kwargs['slug']


class Storylist(generics.ListCreateAPIView):
	queryset = Story.objects.all()
	serializer_class = StorySerializer


class StoryDetailREST(generics.RetrieveUpdateDestroyAPIView):
	queryset = Story.objects.all()
	serializer_class = StorySerializer


class Objectlist(generics.RetrieveUpdateDestroyAPIView):
	queryset = Object.objects.all()
	serializer_class = ObjectSerializer

class ProjectListing(ListAPIView):
	# set the pagination and serializer class
	pagination_class = StandardResultsSetPagination
	serializer_class = ObjectSerializer

	def get_queryset(self):
		filterBy = self.request.query_params.get('filterBy', None)
		query = Collection.objects.filter(collection_name = filterBy).values('pk')

		# if query:
		# 	queryList = Property.objects.filter(Q(name__icontains=query)).distinct()
		# else:
		# 	queryList = Property.objects.all()

		queryList = Object.objects.filter( collection_name = query[0]['pk'] )
		
		# filter the queryset based on the filters applied
		object_type = self.request.query_params.get('object_type', None)  
		material = self.request.query_params.get('material', None)
		location = self.request.query_params.get('location', None)
		time_period = self.request.query_params.get('time_period', None)
		#sort_by = self.request.query_params.get('sort_by', None)

		if object_type:
			if object_type == 'collection highlights':
				queryList = queryList.filter(collection_higlights = True)
			else: 
				queryList = queryList.filter(object_type = object_type)
		if material:
			queryList = queryList.filter(material = material)
		if time_period:
			queryList = queryList.filter(time_period = time_period)
		if location:
			queryList = queryList.filter(location = location)
    
		return queryList

def getobj_type(request):
	# get all the regions from the database excluding 
	# null and blank values
	if request.method == "GET" and request.is_ajax():
		object_type = Object.objects.exclude(object_type__isnull=True).\
			exclude(object_type__exact='').order_by('object_type').values_list('object_type').distinct()
		object_type = [i[0] for i in list(object_type)]
		data = {
			"object_type": object_type, 
		}
		return JsonResponse(data, status = 200)

def getmaterial(request):
	if request.method == "GET" and request.is_ajax():
		# get all the status from the database excluding 
		# null and blank values
		material = Object.objects.exclude(material__isnull=True).\
			exclude(material__exact='').order_by('material').values_list('material').distinct()
		material = [i[0] for i in list(material)]
		data = {
			"material": material, 
		}
		return JsonResponse(data, status = 200)

def getdate(request):
	# get the budget from the database excluding null
	# database excluding null and blank values
	if request.method == "GET" and request.is_ajax():
		time_period = Object.objects.exclude(time_period__isnull=True).\
					exclude(time_period__exact='').order_by('time_period').values_list('time_period').distinct()
		time_period = [i[0] for i in list(time_period)]
		data = {
			"time_period": time_period, 
		}
		return JsonResponse(data, status = 200)

def getlocation(request):
	# get the type for given budget from the database 
	# database excluding null and blank values
	if request.method == "GET" and request.is_ajax():
		location = Object.objects.exclude(location__isnull=True).\
				exclude(location__exact='').values_list('location').distinct()
		
		location = [i[0] for i in list(location)]
		data = {
			"location": location, 
		}
		return JsonResponse(data, status = 200)


class aboutMocaView(generic.TemplateView):
	template_name = "museumapp/aboutUsMocaU.html"

class knowledgeMocaView(generic.TemplateView):
	template_name = "museumapp/knowledgeCenterMoca.html"

class planAVisitMocaView(generic.TemplateView):
	template_name = "museumapp/planAVisitMocaU.html"

class indexMocaView(generic.TemplateView):
	data = get_json_file()
	template_name = "museumapp/indexMoca.html"

class guidedToursMocaView(generic.TemplateView):
	template_name = "museumapp/guidedToursMocaU.html"

class connectionsMocaView(generic.TemplateView):
	template_name = "museumapp/connectionsMocaU.html"

class cafeMocaView(generic.TemplateView):
	template_name = "museumapp/cafeMocaU.html"

class learnMocaView(generic.TemplateView):
	template_name = "museumapp/learnMoca.html"

class supportMocaView(generic.TemplateView):
	template_name = "museumapp/supportMocaU.html"

class accessibilityMocaView(generic.TemplateView):
	template_name = "museumapp/accessibilityMoca.html"

class conservationMocaView(generic.TemplateView):
	template_name = "museumapp/conservationMoca.html"

class indexMocaView(generic.TemplateView):
	template_name = "museumapp/indexL.html"

class familiesMocaView(generic.TemplateView):
	template_name = "museumapp/familiesMoca.html"

class communityIniMocaView(generic.TemplateView):
	template_name = "museumapp/communityIniMoca.html"

class restorationMocaView(generic.TemplateView):
	template_name = "museumapp/restorationMoca.html"

class researchMocaView(generic.TemplateView):
	template_name = "museumapp/researchMoca.html"

class libraryArchivesMocaView(generic.TemplateView):
	template_name = "museumapp/libraryArchivesMoca.html"

class digitalrepMocaView(generic.TemplateView):
	template_name = "museumapp/digitalrepMoca.html"

class mocapressMocaView(generic.TemplateView):
	template_name = "museumapp/mocapressMoca.html"

class pressMocaView(generic.TemplateView):
	template_name = "museumapp/pressMoca.html"

class contactUsMocaView(generic.TemplateView):
	template_name = "museumapp/contactUsMoca.html"

class careerMocaView(generic.TemplateView):
	template_name = "museumapp/careerMoca.html"
    
class artCultureMocaView(generic.TemplateView):
	template_name = "museumapp/artCultureMoca.html"

class journalMocaView(generic.TemplateView):
	template_name = "museumapp/journalMoca.html"

class ticketMocaView(generic.TemplateView):
	template_name = "museumapp/ticketMoca.html"

class whatsOnMocaView(generic.TemplateView):
	template_name = "museumapp/whatsOnMoca.html"


class demoMocaView(generic.TemplateView):
	template_name = "museumapp/acessi.html"



#all stories listing
class storiesMocaView(ListView):
	template_name = "museumapp/storiesMoca.html"
	context_object_name = "stories"

	def get_queryset(self):
		#return Story.objects.all()
		return Story.objects.filter(hide= '0')

#single story detail
class storyDetailsMocaView(DetailView):
	model = Story
	template_name = "museumapp/storyDetailsMoca.html"
	context_object_name = "story"
	 
	def get_query(self, **kwargs):
		demo = self.kwargs['slug']

#all collections listing
class collectionsMocaView(ListView):
	template_name = "museumapp/collectionsMoca.html"
	context_object_name = "collections"
	
	def get_queryset(self):
		return Collection.objects.all()



# #all objects listing
# class objectsMocaView(ListView):
# 	template_name = "museumapp/objectsMoca.html"
# 	context_object_name = "objects"

# 	def get_queryset(self):
# 		return Object.objects.all()
	
# 	def get_context_data(self, *args, **kwargs):
# 		# Get the existing context dictionary, then add
# 		# your custom object to it before returning it
# 		ctx = super(objectsMocaView, self).get_context_data(*args, **kwargs)
# 		ctx['filterValue'] = self.kwargs['slug']
# 		return ctx

#single object detail
class objectDetailsMocaView(DetailView):
	model = Object
	template_name = "museumapp/objectDetailsMoca.html"
	context_object_name = "object"

	def get_context_data(self, *args, **kwargs):
		ctx = super(objectDetailsMocaView, self).get_context_data(*args, **kwargs)
		common = self.object.object_type
		object_slug = self.object.slug
		count = Object.objects.filter(object_type = common).exclude(slug = object_slug).count()
		if count > 3:
			count = 3
		ctx['similarItems'] = Object.objects.filter(object_type = common).exclude(slug = object_slug)
		ctx['count'] = count
		return ctx
	
	def get_query(self, **kwargs):
		demo = self.kwargs['slug']









class eventsMocaView(ListView):
	template_name = "museumapp/eventsMoca.html"

	# def get_context_data(self, *args, **kwargs):
		# Get the existing context dictionary, then add
		# your custom object to it before returning it
		# filterType = 'object_type'
		# filterValue = self.kwargs['slug']
		# ctx = super(objectsMocaView, self).get_context_data(*args, **kwargs)
		# if self.request.GET.get('search'):
		# 	queryValue = self.request.GET.get('search')
		# 	if Object.objects.filter(
		# 		Q(object_type__icontains=queryValue)):
		# 		filterType = 'object_type'
		# 		filterValue = queryValue
		# 	elif Object.objects.filter(
		# 		Q(material__icontains=queryValue)):
		# 		filterType = 'material'
		# 		filterValue = queryValue
		# 	elif Object.objects.filter(
		# 		Q(time_period__icontains=queryValue)):
		# 		filterType = 'material'
		# 		filterValue = queryValue
		# 	else :
		# 		filterType = 'location'
		# 		filterValue = queryValue
		# ctx['filterType'] = filterType
		# ctx['filterValue'] = filterValue
		# return ctx

	def get_queryset(self):
		return Featured_Event.objects.all()


class eventListing(ListAPIView):
	# set the pagination and serializer class
	pagination_class = StandardResultsSetPagination
	serializer_class = EventSerializer

	def get_queryset(self):
		# querytype = self.request.query_params.get('object_type', None)
		queryList = Featured_Event.objects.all()
		# if query:
		# 	queryList = Object.objects.filter(Q(object_name__icontains=query)).distinct()
		# 	print(queryList)
		# else:
		# 	queryList = Object.objects.all()
		
		# filter the queryset based on the filters applied
		start_date = self.request.query_params.get('start_date', None)
		end_date = self.request.query_params.get('end_date', None)
		category = self.request.query_params.get('category', None)
		# time_period = self.request.query_params.get('time_period', None)	
		#sort_by = self.request.query_params.get('sort_by', None)

		# if object_type:
		# 	if object_type == 'collection highlights':
		# 		queryList = queryList.filter(collection_higlights = True)
		# 	else: 
		# 		queryList = queryList.filter(object_type = object_type)
		if start_date:
			queryList = queryList.filter(end_date__gte = start_date)
		if end_date:
			queryList = queryList.filter(start_date__lte = end_date)
		if category:
			queryList = queryList.filter(category = category)
		
		return queryList

def getcategory(request):
	# get all the regions from the database excluding 
	# null and blank values
	if request.method == "GET" and request.is_ajax():
		category = Featured_Event.objects.exclude(category__isnull=True).\
			exclude(category__exact='').order_by('category').values_list('category').distinct()
		category = [i[0] for i in list(category)]
		data = {
			"category": category, 
		}
		return JsonResponse(data, status = 200)

class featuredDetailMocaView(DetailView):
	model = Featured_Event
	template_name = "museumapp/featuredDetailMoca.html"
	context_object_name = "featuredDetail"
	 
	def get_query(self, **kwargs):
		demo = self.kwargs['slug']




"""   New Features starts From Here   """
#In The News


def whatsOn_search_data(request):
	if request.method == 'GET':
		all_data = Featured_Event.objects.all().order_by('-id')
		category_filter = Featured_Event.objects.all().values('category').distinct()
		print(category_filter)
		return render(request, 'museumapp/eventMoca1.html', {'all_data': all_data, 'category_filter': category_filter})
	elif request.method == 'POST':
		search_input = request.POST.get('search_data')
		print(search_input)
		if len(search_input) > 0:
			data = Featured_Event.objects.filter(event_name__icontains= search_input).values()
			print(data)
			return JsonResponse(list(data), content_type='application/json', safe=False)
		elif len(search_input) <= 0:
			print("SEARCH DATA IS EMPTY")
			all_data = Featured_Event.objects.all().values()
			print(all_data)
			return JsonResponse(list(all_data), content_type='application/json', safe=False)


# Whats On
def whatsOn_get_category(request):
	input_category_filter = request.POST.get('category_input')
	print(input_category_filter)

	if input_category_filter != 'SELECT CATEGORY':
		category_filter_data = Featured_Event.objects.filter(category= input_category_filter).values().order_by('-id')
	else:
		category_filter_data = Featured_Event.objects.all().values().order_by('-id')
	print(category_filter_data)
	return JsonResponse(list(category_filter_data), content_type='application/json', safe=False)


def whatsOn_get_start_end_date(request):
	start_date = request.POST.get('start_date')
	end_date = request.POST.get('end_date')
	print(start_date)
	print(end_date)
	if (start_date != 'START DATE') & (end_date == 'END DATE'):
		print("THIS IS ONLY FOR YR FILTER")
		data = Featured_Event.objects.filter(Q(start_date__year__gte=start_date)).values().order_by('-id')
		print(data)
		return JsonResponse(list(data), content_type='application/json', safe=False)
	elif (start_date != 'START DATE') & (end_date != 'END DATE'):
		data = Featured_Event.objects.filter(Q(start_date__year__gte=start_date) & Q(end_date__year__lte=end_date)).values().order_by('-id')
		print(data)
		return JsonResponse(list(data), content_type='application/json', safe=False)


def whatsOn_detailed_view(request, slug_text):
	query = Featured_Event.objects.filter(slug= slug_text)
	print(query)
	if query:
		query = query.first()
	else:
		return HttpResponse("<h1>Page Not Found</h1>")
	context = {
		'featuredDetail': query
	}
	return render(request, 'museumapp/featuredDetailMoca.html', context)




def in_the_news_search_data(request):
	if request.method == 'GET':
		all_data = InTheNews.objects.all()
		topic_filter = InTheNews.objects.all().values('topic').distinct()
		return render(request, 'museumapp/in_the_news.html',{'all_data':all_data, 'topic_filter':topic_filter})
	elif request.method == 'POST':
		search_input = request.POST.get('search_data')
		print(search_input)
		if len(search_input) > 0:
			data = InTheNews.objects.filter(Q(author__icontains= search_input) | Q(event_name__icontains= search_input)).values()
			print(data)
			return JsonResponse(list(data), content_type='application/json', safe=False)
		elif len(search_input) <= 0:
			print("SEARCH DATA IS EMPTY")
			all_data = InTheNews.objects.all().values()
			print(all_data)
			return JsonResponse(list(all_data), content_type='application/json', safe=False)



# In The News 
def in_the_news_get_tpoic(request):
	input_topic_filter = request.POST.get('topic_input')
	print(input_topic_filter)

	if input_topic_filter != 'SELECT TOPIC':
		topic_filter_data = InTheNews.objects.filter(topic= input_topic_filter).values()
	else:
		topic_filter_data = InTheNews.objects.all().values()
	print(topic_filter_data)
	return JsonResponse(list(topic_filter_data), content_type='application/json', safe=False)


def in_the_news_get_mn_year(request):
	yr = request.POST.get('year')
	mn = request.POST.get('month')
	print(yr)
	print(mn)
	if (yr != 'BY YEAR') & (mn == 'BY MONTH'):
		print("THIS IS ONLY FOR YR FILTER")
		data = InTheNews.objects.filter(Q(year__year=yr)).values()
		print(data)
		return JsonResponse(list(data), content_type='application/json', safe=False)
	elif (yr != 'BY YEAR') & (mn != 'BY MONTH'):
		data = InTheNews.objects.filter(Q(year__year=yr) & Q(month__month=mn)).values()
		print(data)
		return JsonResponse(list(data), content_type='application/json', safe=False)









def journals_search_data(request):
	if request.method == 'GET':
		all_data = Journals.objects.all()
		topic_filter = Journals.objects.all().values('topic').distinct()
		return render(request, 'museumapp/journals.html',{'all_data':all_data, 'topic_filter':topic_filter})
	elif request.method == 'POST':
		search_input = request.POST.get('search_data')
		print(search_input)
		if len(search_input) > 0:
			data = Journals.objects.filter(Q(author__icontains= search_input) | Q(event_name__icontains= search_input)).values()
			print(data)
			return JsonResponse(list(data), content_type='application/json', safe=False)
		elif len(search_input) <= 0:
			print("SEARCH DATA IS EMPTY")
			all_data = Journals.objects.all().values()
			print(all_data)
			return JsonResponse(list(all_data), content_type='application/json', safe=False)



# Journals
def journals_get_tpoic(request):
	input_topic_filter = request.POST.get('topic_input')
	print(input_topic_filter)
	if input_topic_filter != 'SELECT TOPIC':
		topic_filter_data = Journals.objects.filter(topic= input_topic_filter).values()
	else:
		topic_filter_data = Journals.objects.all().values()
	print(topic_filter_data)
	return JsonResponse(list(topic_filter_data), content_type='application/json', safe=False)




def journals_get_mn_year(request):
	yr = request.POST.get('year')
	mn = request.POST.get('month')
	print(yr)
	print(mn)
	if (yr != 'BY YEAR') & (mn == 'BY MONTH'):
		print("THIS IS ONLY FOR YR FILTER")
		data = Journals.objects.filter(Q(year__year=yr)).values()
		print(data)
		return JsonResponse(list(data), content_type='application/json', safe=False)
	elif (yr != 'BY YEAR') & (mn != 'BY MONTH'):
		data = Journals.objects.filter(Q(year__year=yr) & Q(month__month=mn)).values()
		print(data)
		return JsonResponse(list(data), content_type='application/json', safe=False)


def journal_detailed_view(request, slug_text):
	query = Journals.objects.filter(slug= slug_text)
	if query:
		query = query.first()
	else:
		return HttpResponse("<h1>Page Not Found</h1>")
	context = {
		'post': query
	}
	return render(request, 'museumapp/journals_detail.html', context)


# Objects Views

def objectsMoca(request, slug_text):
    print(slug_text)
    if request.method == 'GET':
        obj_type = slug_text
        obj_material_data = Object.objects.all().values('object_type').distinct()
        data = Object.objects.filter(object_type=obj_type).values()
        provenance_data = Object.objects.filter(object_type=obj_type).values('provenance').distinct()
        time_period_data = Object.objects.filter(object_type=obj_type).values('time_period').distinct()
        print(slug_text)
        heightlight_data = QueryDict

        mat_data_list = []

        for i in data:

            sort_data = i['material'].split('/')

            for j in sort_data:
                if j not in mat_data_list:
                    mat_data_list.append(j.strip())

        mat_data = list(set(mat_data_list))
        print(mat_data)
        
        if slug_text == 'collection-highlights':
        	heightlight_data = Object.objects.filter(collection_highlights= True).values()
        else:
            heightlight_data = Object.objects.filter(object_type= obj_type).values()
        
        return render(request, 'museumapp/objectsMoca1.html', {'data':mat_data, 'obj_material_data': obj_material_data, 'obj_type': obj_type, 'heightlight_data': heightlight_data, 'provenance_data':provenance_data, 'time_period_data':time_period_data})
        
            #return render(request, 'museumapp/objectsMoca1.html',{'data': data, 'obj_material_data': obj_material_data, 'obj_type': obj_type,})
    elif request.method == 'POST':
        search_input = request.POST.get('search_data')
        print(search_input)
        if len(search_input) > 0:
            data = Object.objects.filter(
                Q(object_type__icontains=search_input) | Q(material__icontains=search_input) | Q(
                    provenance__icontains=search_input) | Q(time_period__icontains=search_input) | Q(object_name__icontains = search_input)).values()
            print(data)
            return JsonResponse(list(data), content_type='application/json', safe=False)
        elif len(search_input) <= 0:
            print("SEARCH DATA IS EMPTY")
            all_data = Object.objects.all().values()
            print(all_data)
            return JsonResponse(list(all_data), content_type='application/json', safe=False)


def filter_object_type(request):
	object_type = request.POST.get('object_type')
	print('object_type', object_type)
	if object_type != 'OBJECT TYPE':
		object_filter_data = Object.objects.filter(object_type= object_type).values()
	else:
		object_filter_data = Object.objects.all().values()
	print(object_filter_data)
	#dump = json.dumps(list(object_filter_data))

	mat_data_list = []

	for i in object_filter_data:

		sort_data = i['material'].split('/')

		for j in sort_data:
			if j not in mat_data_list:
				mat_data_list.append(j.strip())
	mat_data = list(set(mat_data_list))
	print(mat_data)
	response = {'result':list(object_filter_data), 'material':mat_data}
	# return JsonResponse(list(object_filter_data), content_type='application/json', safe=False)
	return JsonResponse(response, content_type='application/json', safe=False)


def filter_object_mat_loc_time(request):
	object_type = request.POST.get('object_type')
	material_data = request.POST.get('material')
	location = request.POST.get('location')
	time_period = request.POST.get('time_period')
	print(object_type)
	print(material_data)
	print(location)
	print(time_period)

	if((material_data != 'all') & (location == 'all') & (time_period == 'all')):
		print("Material")
		filter_data = Object.objects.filter(Q(object_type=object_type) & Q(material__icontains= material_data)).values()
		print(filter_data)
		print(len(filter_data))
	elif ((material_data != 'all') & (location != 'all') & (time_period == 'all')):
		print("Location")
		filter_data = Object.objects.filter(Q(object_type=object_type) & Q(material__icontains= material_data) & Q(provenance= location)).values()
		print(filter_data)
		print(len(filter_data))
	elif ((material_data != 'all') & (location != 'all') & (time_period != 'all')):
		print("Period")
		filter_data = Object.objects.filter(Q(object_type=object_type) & Q(material__icontains= material_data) & Q(provenance= location) & Q(time_period= time_period)).values()
		print(filter_data)
		print(len(filter_data))
	elif ((material_data == 'all') & (location != 'all')):
		print("Period")
		filter_data = Object.objects.filter(Q(object_type=object_type) & Q(provenance= location)).values()
		print(filter_data)
		print(len(filter_data))
	elif ((material_data == 'all') & (time_period != 'all')):
		print("Period")
		filter_data = Object.objects.filter(Q(object_type=object_type)  & Q(time_period= time_period)).values()
		print(filter_data)
		print(len(filter_data))
	elif ((material_data == 'all')):
		print("all")
		filter_data = Object.objects.filter(Q(object_type=object_type)).values()
		print(filter_data)
		print(len(filter_data))

	return JsonResponse(list(filter_data), content_type='application/json', safe=False)





def object_detailed_view(request, slug_text):
	query = Object.objects.filter(slug= slug_text)
	print(query)
	if query:
		query = query.first()
	else:
		return HttpResponse("<h1>Page Not Found</h1>")

	get_obj_type = Object.objects.get(slug= slug_text)
	similar_items = Object.objects.filter(object_type = get_obj_type.object_type).exclude(slug = slug_text)
	count = Object.objects.filter(object_type = get_obj_type.object_type).exclude(slug = slug_text).count()
	if count > 3:
			count = 3

	context = {
		'object': query,
		'similarItems': similar_items,
		'count':count
	}

	return render(request, 'museumapp/objectDetailsMoca.html', context)



nav_serach_input = ''


def nav_search(request):
    if request.method == 'GET':
        print("HELLO")
        print(nav_serach_input)

        journals_data = Journals.objects.filter(event_name__icontains=nav_serach_input).values()
        print(journals_data)
        in_the_news_data = InTheNews.objects.filter(event_name__icontains=nav_serach_input).values()
        featured_event_data = Featured_Event.objects.filter(event_name__icontains=nav_serach_input)
        object_data = Object.objects.filter(
            Q(object_name__icontains=nav_serach_input) | Q(collection_name__slug__icontains=nav_serach_input))
        story_data = Story.objects.filter(story_title__icontains=nav_serach_input)

        return render(request, 'museumapp/navigation_search.html',
                      {'journals_data': journals_data, 'in_the_news_data': in_the_news_data,
                       'featured_event_data': featured_event_data, 'object_data': object_data,
                       'story_data': story_data})


def nav_search_ajax(request):
    global nav_serach_input
    nav_serach_input = request.POST.get('search_data')
    print(nav_serach_input)
    return HttpResponse()




#--------------ALL BACKUP PARTS-----------------------

# class StoryPage(ListView):  #Actual Homepage
# 	template_name = "museumapp/story.html"
# 	context_object_name = "story"
	
# 	def get_queryset(self):
# 		return Story.objects.all()

# class StoryDetail(DetailView):
# 	model = Story
# 	template_name = "museumapp/storydetail.html"
# 	context_object_name = "sdetail"
	 
# 	def get_query(self, **kwargs):
# 		demo = self.kwargs['slug']





@csrf_exempt
def buy_tickets(request):
    if request.method == 'GET':
        return render(request, "museumapp/ticketMoca.html", {})
    elif request.method == 'POST':
        date = request.POST.get('date')
        entry_type = request.POST.get('entry_type')
        time = request.POST.get('time')
        total_no = request.POST.get('total_no')
        total_cost = request.POST.get('total_cost')
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        friend_no = request.POST.get('friend_no')
        adult_no = request.POST.get('adult_no')
        child_no = request.POST.get('child_no')


        if entry_type != 'Retracing Monte Santo (the Holy Hill Tour)':
            choosed_datas = Book_ticket(entry_type=entry_type,
										date=str(date),
										time=time,
										no_of_tickets=total_no,
										amount=total_cost,
										full_name=name,
										email=email,
										phone_number=phone,
										adult_no=adult_no,
										child_no=child_no,
										friend_no=friend_no)
            choosed_datas.save()
        else:
            choosed_datas = Book_ticket(entry_type=entry_type,
										date=str(date),
										time='',
										no_of_tickets=total_no,
										amount=total_cost,
										full_name=name,
										email=email,
										phone_number=phone,
										adult_no=adult_no,
										child_no=child_no,
										friend_no=friend_no)
            choosed_datas.save()

        mail = smtplib.SMTP('smtp.gmail.com', 587)
		
        msg_string= ""
        if entry_type == 'Retracing Monte Santo (the Holy Hill Tour)':
            msg_string = "" + str(entry_type) +"\nName : "+ str(name)+"\nEmail : "+ str(email)+"\nPhone Number : "+ str(phone)+ "\nDate : " + str(date) + "\nTickets :\nAdult : " + str(adult_no) + "\nChild : " + str(child_no) + "\nFriends of MoCA : " + str(
            friend_no) + "\nCost : " + str(total_cost) + " Rs. \n\nPLEASE NOTE\n If you are not able to print your ticket, no problem! Just bring your smartphone or tablet with you to the museum. Do ensure that the battery is sufficiently charged. Your ticket is only valid on the selected date and time.\n Smoking is not permitted anywhere on the Museum premises.\n No eatables or beverages are allowed inside the Museum.\n Deposit large bags, backpacks, umbrellas and water bottles at the counter.\n No selfie sticks allowed inside the museum.\n Students Admission with valid Institution Identity cards.\n Camera Pass - Additional Rs. 100. \n Camera with Tripod/Stand- only with Prior Permission from Authority.\n The Museum authorities reserve the right to a admission in Museum." 
        else:
            msg_string = "" + str(entry_type) +"\nName : "+ str(name)+"\nEmail : "+ str(email)+"\nPhone Number : "+ str(phone)+ "\nDate : " + str(date) + "\nTime : " + str(
            time) + "\nTickets:\nAdult: " + str(adult_no) + "\nChild: " + str(child_no) + "\nFriends of MoCA: " + str(
            friend_no) + "\nCost : " + str(total_cost) + " Rs. \n\nPLEASE NOTE\n If you are not able to print your ticket, no problem! Just bring your smartphone or tablet with you to the museum. Do ensure that the battery is sufficiently charged. Your ticket is only valid on the selected date and time.\n Smoking is not permitted anywhere on the Museum premises.\n No eatables or beverages are allowed inside the Museum.\n Deposit large bags, backpacks, umbrellas and water bottles at the counter.\n No selfie sticks allowed inside the museum.\n Students Admission with valid Institution Identity cards.\n Camera Pass - Additional Rs. 100. \n Camera with Tripod/Stand- only with Prior Permission from Authority.\n The Museum authorities reserve the right to a admission in Museum." 
        
        msg = MIMEText(msg_string)

        recipients = ['ekfrazo@gmail.com', 'museumofchristianart@gmail.com', email]

        msg['Subject'] = 'Booked ticketd - MoCA'
        msg['From'] = 'mocagoa@gmail.com'
        msg['To'] = ", ".join(recipients)
        mail.ehlo()
        mail.starttls()
        # mail.login("mocagoa@gmail.com", "Mocaonline@123#")
        mail.login("mocagoa@gmail.com", "Moca123#goa")
        mail.sendmail("ekfrazo@gmail.com", recipients, msg.as_string())
        mail.quit

        return render(request, "museumapp/ticketMoca.html", {})





def membership(request):
    if request.method == 'GET':
        return render(request, 'museumapp/membership.html', {})
    elif request.method == 'POST':
        name = request.POST.get('full_name')
        email = request.POST.get('email')
        ph_no = request.POST.get('ph_no')
        type_of_membership = request.POST.get('type_of_mem')
        amount = request.POST.get('membership_amount')
        print(name)
        print(email)
        print(ph_no)
        print(type_of_membership)
        print(amount)
		
        save_membership = MemberShip(type_of_membership=type_of_membership, amount=amount, full_name=name, email=email,
										phone_number=ph_no)
        save_membership.save()

        mail = smtplib.SMTP('smtp.gmail.com', 587)
        msg_string = "Membership Type : " + str(type_of_membership) + "\nName : " + str(name) + "\nEmail : " + str(
			email) + "\nPhone Number : " + str(ph_no) + "\nAmount : " + str(
			amount) + " Rs.\n\nThanks for joining us. \nKindly transfer the payment to this bank account details or by a cheque to the below address : \nHere are our bank details: \nNEFT details: \nFOR DONATIONS IN INDIAN RUPEES\nAccount Name: MUSEUM OF CHRISTIAN ART GOA\nAccount Type: CURRENT ACCOUNT\nAccount No. 0321201000753\nBank: CANARA BANK\nBranch: OLD GOA BRANCH\nAddress: Near Gandhi Circle, Old Goa, Goa, 403402\nState: GOA\nIFSC Code: CNRB0000321\n\nFOR DONATIONS IN INTERNATIONAL CURRENCY\nAccount Name: MUSEUM OF CHRISTIAN ART GOA\n Account Type: SAVINGS ACCOUNT\n Account No. 40121915242\n Bank: State Bank of India New Delhi, Main Branch\nAddress:  11, Parliament Street, New Delhi, NCT of Delhi, 110001\nState: New Delhi\nIFSC Code: SBIN0000691\nCheque in favour of 'Museum of Christian Art'."
        msg = MIMEText(msg_string)
        recipients = ['ekfrazo@gmail.com', 'museumofchristianart@gmail.com', email]

        msg['Subject'] = 'Membership - MoCA'
        msg['From'] = 'mocagoa@gmail.com'
        msg['To'] = ", ".join(recipients)
        mail.ehlo()
        mail.starttls()
        mail.login("mocagoa@gmail.com", "Moca123#goa")
        mail.sendmail("ekfrazo@gmail.com", recipients, msg.as_string())
        mail.quit

        return render(request, "museumapp/ticketMoca.html", {})



# Shop page alert function
def shopAlert(request):
    return render(request, "museumapp/shopmoca.html",)





def embedding(request):
	return render(request, 'museumapp/embedding.html')


def embeddingOne(request):
	return render(request, 'museumapp/embedding1.html')


def embeddingTwo(request):
	return render(request, 'museumapp/embedding2.html')


def embeddingThree(request):
	return render(request, 'museumapp/embedding3.html')



