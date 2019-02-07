from django.contrib import admin
from rango.models import Category, Page, UserProfile

# adds ability to add pages on creation of a Category
class PageInline(admin.StackedInline):
	model = Page
	extra = 3

class CategoryAdmin(admin.ModelAdmin):
	fieldsets = [(None,      {'fields':['name', 'slug']}),
	             ('Traffic info', {'fields': ['views', 'likes']}),
				 ]
				 
	inlines = [PageInline]
	
	prepopulated_fields = {'slug':('name',)}

admin.site.register(Category, CategoryAdmin)
	
	
class PageAdmin(admin.ModelAdmin):
	list_display = ('title', 'category', 'url')

admin.site.register(Page, PageAdmin)

admin.site.register(UserProfile)