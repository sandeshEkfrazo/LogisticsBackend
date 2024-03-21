from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin

# Register your models here.
@admin.register(UserRoleRef)
class UserRoleRef(ImportExportModelAdmin):
    list_display = ['id','user_role_name','create_timestamp','last_update_timestamp']

@admin.register(Status)
class Status(ImportExportModelAdmin):
    list_display =['id','status_name']

@admin.register(Filesize)
class Filesize(ImportExportModelAdmin):
    list_display =['id','file_type','size']

@admin.register(Queries)
class Queries(ImportExportModelAdmin):
    def user_role_name(self, obj):
        return obj.isfor.user_role_name

    list_display =['id','questions','answer','user_role_name','status']

@admin.register(Language)
class Language(ImportExportModelAdmin):
    list_dispaly = ['id','name']

@admin.register(Subscriptionplan)
class Subscriptionplan(ImportExportModelAdmin):
    list_dispaly=['id','time_period','validity_days','amount','type_of_service','status']

@admin.register(Aboutus)
class Aboutus(ImportExportModelAdmin):
    list_display = ['id','logo','heading','paragraph','phone_number','email','alternate_phone_number','text']

class TimesearchAdmin(ImportExportModelAdmin):
    list_display = ['time', 'description']

admin.site.register(Timesearch, TimesearchAdmin)