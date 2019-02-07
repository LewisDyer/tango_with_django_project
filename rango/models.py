from django.db import models
from django.template.defaultfilters import slugify # replaces whitespace in URLs with hyphens
from django.contrib.auth.models import User

class Category(models.Model): # inherits from models.Model, like all models
	name = models.CharField(max_length=128, unique=True)
	views = models.IntegerField(default=0)
	likes = models.IntegerField(default=0)
	slug = models.SlugField()
	
	def save(self, *args, **kwargs): 
		self.slug = slugify(self.name)
		print("Slugified!")
		print(self.slug)
		super(Category, self).save(*args, **kwargs)

	class Meta:
		verbose_name_plural = 'categories' # don't just stick an 's' at the end!
	
	def __str__(self): # useful to show meaningful info about category during debugging
		return self.name
		
class Page(models.Model):
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	title = models.CharField(max_length=128)
	url = models.URLField()
	views = models.IntegerField(default=0)
	
	def __str__(self):
		return self.title

class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE) 
	# connects this to a User instance

	# extra attributes we want
	website = models.URLField(blank=True)
	picture = models.ImageField(upload_to='profile_images', blank=True)

	def __str__(self):
		return self.user.username