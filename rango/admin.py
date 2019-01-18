from django.contrib import admin
from rango.models import Category, Page

# adds ability to add pages on creation of a Category
class PageInline(admin.StackedInline):
	model = Page
	extra = 3

class CategoryAdmin(admin.ModelAdmin):
	fieldsets = [(None,      {'fields':['name']}),
	             ('Traffic info', {'fields': ['views', 'likes']}),
				 ]
				 
	inlines = [PageInline]

admin.site.register(Category, CategoryAdmin)
	
	
class PageAdmin(admin.ModelAdmin):
	list_display = ('category', 'title', 'url')

admin.site.register(Page, PageAdmin)