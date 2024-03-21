from rest_framework import *
from museumapp.models import *
from rest_framework import serializers


class StorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Story
		fields = ['story_title', 'story_description', 'story_image', 'slug']

class ChapterSerializer(serializers.ModelSerializer):
	class Meta:
		model = Chapter
		fields = ['story', 'chapter_content', 'left_side_image', 'left_side_caption', 'right_side_caption', 'right_side_image']

class CollectionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Collection
		fields = ['collection_name', 'collection_image']

class ObjectSerializer(serializers.ModelSerializer):
	class Meta:
		model = Object
		fields = ['object_name', 'collection_name', 'object_image', 'time_period', 'material', 'object_description', 'object_details', 'artist', 'date', 'culture', 'medium', 'dimensions', 'accession_number', 'provenance', 'exhibition_history', 'essays_publications', 'keywords', 'location', 'object_type', 'slug']

class EventSerializer(serializers.ModelSerializer):
	class Meta:
		model = Featured_Event
		fields = ['event_name', 'event_image', 'event_short_description', 'event_long_description', 'featured', 'category', 'start_date', 'end_date', 'slug', 'time_duration']
        
        
        
        

# NEWLY ADDED SERIALIZERS

class InTheNewsSerializer(serializers.ModelSerializer):
	class Meta:
		model = InTheNews
		fields = ['event_name', 'event_image', 'event_short_description', 'event_long_description', 'featured',
				  'category', 'year', 'month', 'slug', 'time_duration', 'topic', 'author']



class JournalsSerializer(serializers.ModelSerializer):
	class Meta:
		model = Journals
		fields = ['event_name', 'event_image', 'event_short_description', 'event_long_description', 'featured',
				  'category', 'year', 'month', 'slug', 'time_duration', 'topic', 'author']
