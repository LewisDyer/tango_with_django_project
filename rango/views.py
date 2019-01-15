from django.shortcuts import render

from django.http import HttpResponse

def index(request):
	# Dict is passed to template engine as context
	context_dict = {'boldmessage': "Crunchy, creamy, cookie, candy, cupcake!"}
	
	# Returning a rendered response for the client
	return render(request, 'rango/index.html', context=context_dict)
	
def about(request):
	return HttpResponse("Rango says here is the about page. Head back to the main page <a href='/rango/'>here</a>")

