from django.contrib import admin
from .models import Story,Chapter,Collection,Object
from import_export.admin import ImportExportModelAdmin
from .models import *

# Register your models here.

class ChapterInline(admin.TabularInline):
	model = Chapter
	extra = 0

class ObjectInline(admin.TabularInline):
	model = Object
	extra = 0

@admin.register(Chapter)
class ChapterAdmin(ImportExportModelAdmin):
	list_display = ('story', 'chapter_content')

@admin.register(Object)
class ObjectAdmin(ImportExportModelAdmin):
	list_display = ('accession_number', 'object_name', 'collection_name', 'object_type', 'material', 'location', 'date', 'time_period', 'object_description', 'object_details', 'provenance', 'exhibition_history', 'essays_publications')
	prepopulated_fields = {'slug': ('object_name',)}

@admin.register(Story)
class StoryAdmin(ImportExportModelAdmin):
	list_display = ('story_title', 'story_description', 'story_image', 'slug')
	inlines = [ ChapterInline,]
	prepopulated_fields = {'slug': ('story_title',)}

@admin.register(Collection)
class CollectionAdmin(ImportExportModelAdmin):
	list_display = ('collection_name', 'collection_image')
	inlines = [ ObjectInline, ]
	prepopulated_fields = {'slug': ('collection_name',)}

@admin.register(Featured_Event)
class Featured_EventAdmin(ImportExportModelAdmin):
	list_display = ('event_name', 'event_short_description', 'featured')
	prepopulated_fields = {'slug': ('event_name',)}

# @admin.register(Story, Chapter, Collection, Object)
# class ViewAdmin(ImportExportModelAdmin):
# 	pass


# @admin.register(Story)
# 
# admin.site.register(Chapter)
# admin.site.register(Collection)
# @admin.register(Objects)
#


# class ViewAdmin(ImportExportModelAdmin):
# 	pass
# # Register your models here.




#NEWLY ADDED ADMIN

@admin.register(InTheNews)
class InTheNewsAdmin(ImportExportModelAdmin):
	list_display = ('event_name', 'event_short_description', 'featured', 'slug', 'year', 'month')
	prepopulated_fields = {'slug': ('event_name',)}


@admin.register(Journals)
class JournalsAdmin(ImportExportModelAdmin):
	list_display = ('event_name', 'event_short_description', 'featured', 'slug', 'year', 'month')
	prepopulated_fields = {'slug': ('event_name',)}



@admin.register(Book_ticket)
class Book_ticket(admin.ModelAdmin):
	list_display = ('entry_type', 'date', 'time', 'no_of_tickets', 'full_name')


@admin.register(MemberShip)
class MemberShip(admin.ModelAdmin):
	list_display = ('type_of_membership', 'amount', 'full_name', 'email', 'phone_number')


	