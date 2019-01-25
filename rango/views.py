from django.shortcuts import render

from django.http import HttpResponse

from rango.models import Category, Page

def index(request):
	# Dict is passed to template engine as context
	# Get top 5 most liked categories
	category_list = Category.objects.order_by('-likes')[:5]
	context_dict = {'categories': category_list}
	
	# Get 5 most viewed pages
	page_list = Page.objects.order_by('-views')[:5]
	context_dict['pages'] = page_list
	
	# Returning a rendered response for the client
	return render(request, 'rango/index.html', context_dict)
	
def about(request):

	return render(request, 'rango/about.html')
	#return HttpResponse("Rango says here is the about page. Head back to the main page <a href='/rango/'>here</a>")

def show_category(request, category_name_slug):

	context_dict = {}
	
	try:
		
		# get category based on URL slug
		category = Category.objects.get(slug=category_name_slug)
		# get all pages for that category
		pages = Page.objects.filter(category=category)
		
		context_dict['pages'] = pages
		context_dict['category'] = category
	except Category.DoesNotExist:
		# when a category isn't a thing
		context_dict['pages'] = None
		context_dict['category'] = None
	
	return render(request, 'rango/category.html', context_dict)
