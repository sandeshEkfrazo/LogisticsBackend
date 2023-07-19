from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(UserRoleRef)
class UserRoleRef(admin.ModelAdmin):
    list_display = ['id','user_role_name','create_timestamp','last_update_timestamp']

@admin.register(Status)
class Status(admin.ModelAdmin):
    list_display =['id','status_name']

@admin.register(Filesize)
class Filesize(admin.ModelAdmin):
    list_display =['id','file_type','size']

@admin.register(Queries)
class Queries(admin.ModelAdmin):
    list_display =['id','questions','answer','isfor','status']

@admin.register(Language)
class Language(admin.ModelAdmin):
    list_dispaly = ['id','name']

@admin.register(Subscriptionplan)
class Subscriptionplan(admin.ModelAdmin):
    list_dispaly=['id','time_period','validity_days','amount','type_of_service','status']

@admin.register(Aboutus)
class Aboutus(admin.ModelAdmin):
    list_display = ['id','logo','heading','paragraph','phone_number','email','alternate_phone_number','text']