from django.shortcuts import render

from django.http import HttpResponse

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm

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

	
def add_category(request):
	form = CategoryForm()
	
	# Received HTTP POST?
	if request.method == 'POST':
		form = CategoryForm(request.POST)
		
		if form.is_valid():
			form.save(commit=True) # save new category to DB
			
			return index(request) # redirect to index page
		else: # supplied form contains errors
			print(form.errors)
	
	return render(request, 'rango/add_category.html', {'form':form})

	
def add_page(request, category_name_slug):
	try:
		category = Category.objects.get(slug=category_name_slug)
	except Category.DoesNotExist:
		category = None
		
	form = PageForm()
	if request.method == 'POST':
		form = PageForm(request.POST)
		if form.is_valid():
			if category:
				page = form.save(commit=False)
				page.category = category
				page.views = 0
				page.save()
				return show_category(request, category_name_slug)
		else:
			print(form.errors)
	
	context_dict = {'form': form, 'category': category}
	return render(request, 'rango/add_page.html', context_dict)

def register(request):
	# A boolean telling template whether registration successful
	registered = False

	if request.method == 'POST':
		user_form = UserForm(data=request.POST)
		profile_form=UserProfileForm(data=request.POST)

		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()

			user.set_password(user.password)
			user.save()

			profile = profile_form.save(commit=False)
			profile.user = user

			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']

			profile.save()

			registered = True
		else:
			print(user_form.errors, profile_form.errors)
	else:
		user_form = UserForm()
		profile_form = UserProfileForm()
	
	return render(request, 'rango/register.html',
				  {'user_form': user_form,
				   'profile_form': profile_form,
				   'registered': registered})

def user_login(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(username=username, password=password)

		if user:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect(reverse('index'))
			else:
				return HttpResponse("Your Rango account is disabled.")
		else:
			print("Invalid login details: {0}, {1}".format(username, password))
			return HttpResponse("Invalid login details supplied.")
	else:
		return render(request, 'rango/login.html', {})

@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('index'))

@login_required
def restricted(request):
	return HttpResponse("Since you're logged in, you can see this text!")