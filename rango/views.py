from django.shortcuts import render

from django.http import HttpResponse

def index(request):
	return HttpResponse("Rango says hey there partner! Learn more about Rango <a href='/rango/about/'>here</a>")
	
def about(request):
	return HttpResponse("Rango says here is the about page. Head back to the main page <a href='/rango/'>here</a>")

