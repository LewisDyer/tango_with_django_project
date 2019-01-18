from django.db import models

class Category(models.Model): # inherits from models.Model, like all models
	name = models.CharField(max_length=128, unique=True)
	views = models.IntegerField(default=0)
	likes = models.IntegerField(default=0)
	
	class Meta:
		verbose_name_plural = 'Categories' # don't just stick an 's' at the end!
	
	def __str__(self): # useful to show meaningful info about category during debugging
		return self.name
		
class Page(models.Model):
	category = models.ForeignKey(Category)
	title = models.CharField(max_length=128)
	url = models.URLField()
	views = models.IntegerField(default=0)
	
	def __str__(self):
		return self.title