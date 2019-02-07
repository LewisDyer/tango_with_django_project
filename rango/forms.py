from django import forms
from rango.models import Page, Category, User, UserProfile

class CategoryForm(forms.ModelForm):
	name = forms.CharField(max_length=Category._meta.get_field('name').max_length, 
						   help_text="Please enter the category name.")
	
	# The user can't see these fields - they're auto-generated values
	views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
	likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
	slug = forms.CharField(widget=forms.HiddenInput(), required=False)
	
	
	class Meta:
		model = Category # what model is this form for?
		fields = ('name',) # what fields are the user entering?
	
class PageForm(forms.ModelForm):
	title = forms.CharField(max_length=Page._meta.get_field('title').max_length, 
	                        help_text="Please enter the title of the page.")
	url = forms.URLField(max_length=Page._meta.get_field('url').max_length,
                       	 help_text="Please enter the URL of the page.")
	views = forms.IntegerField(widget = forms.HiddenInput(), initial=0)
	
	class Meta:
		model = Page # this form is associated with the Page model
		exclude = ('category',) # we're not entering this field on the form
		# alternatively, we could specify the fields we *are* entering
		
	def clean(self):
		cleaned_data = self.cleaned_data
		url = cleaned_data.get('url')
		
		# if url non-empty + not starting with http://, add it
		
		if url and not url.startswith('http://'):
			url = 'http://' + url
			cleaned_data['url'] = url
			
			return cleaned_data

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ('website', 'picture')