import django_filters
from museumapp.models import *
class ObjFilter(django_filters.FilterSet):
	class Meta:
		model = Objects
		fields = ['object_type','material','location', 'time_period']