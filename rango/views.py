from django.shortcuts import render

from django.http import HttpResponse

from rango.models import Category

def index(request):
	# Dict is passed to template engine as context
	# Get top 5 most liked categories
	category_list = Category.objects.order_by('-likes')[:5]
	context_dict = {'categories': category_list}
	
	# Returning a rendered response for the client
	return render(request, 'rango/index.html', context_dict)
	
def about(request):

	return render(request, 'rango/about.html')
	#return HttpResponse("Rango says here is the about page. Head back to the main page <a href='/rango/'>here</a>")

