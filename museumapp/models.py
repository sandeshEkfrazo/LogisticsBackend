from django.db import models
from tinymce import HTMLField

from django.utils.translation import ugettext_lazy as _

# Create your models here.

class Story(models.Model):
    story_title = models.CharField(max_length=500, blank=True, null=True)
    story_description = models.CharField(max_length=500, blank=True, null=True)
    story_image = models.ImageField(upload_to = 'story_image', blank=True, null=True)
    story_thumbnail = models.ImageField(upload_to = 'story_image', blank=True, null=True)
    slug = models.SlugField(unique=True, null=True)
    hide = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        verbose_name = _("Story")
        verbose_name_plural = _("Stories")
    def __str__(self):
        return '%s' % (self.story_title)

class Chapter(models.Model):
    story = models.ForeignKey(Story, related_name='story_scenes', on_delete=models.CASCADE, blank=True, null=True)
    chapter_content = HTMLField(null=True, blank=True)
    left_side_image =  models.ImageField(upload_to = 'chapter_image', blank=True, null=True)
    left_side_caption = models.ImageField(upload_to = 'chapter_image', blank=True, null=True)
    right_side_image = models.ImageField(upload_to = 'chapter_image', blank=True, null=True)
    right_side_caption = models.ImageField(upload_to = 'chapter_image', blank=True, null=True)

    class Meta:
        verbose_name = _("Chapter")
        verbose_name_plural = _("Chapters")
    

class Collection(models.Model):
    collection_name = models.CharField(max_length=500, blank=True, null=True)
    collection_image = models.ImageField(upload_to = 'collection_image', blank=True, null=True)
    slug = models.SlugField(unique=True, null=True)

    class Meta:
        verbose_name = _("Collection")
        verbose_name_plural = _("Collections")
    def __str__(self):
        return '%s' % (self.collection_name)

class Object(models.Model):
    object_name = models.CharField(max_length=500, null=True, blank=True)
    collection_name = models.ForeignKey(Collection, on_delete=models.CASCADE, blank=True, null=True)
    object_image = models.ImageField(upload_to = 'object_image', blank=True, null=True)
    time_period = models.CharField(max_length=500, blank=True, null=True)
    material = models.CharField(max_length=500, blank=True, null=True)
    object_description = HTMLField(null=True, blank=True)
    object_details = models.BooleanField(default=True, null=True)
    artist = models.CharField(max_length=500, blank=True, null=True)
    date = models.CharField(max_length=500, blank=True, null=True)
    culture = models.CharField(max_length=500, blank=True, null=True)
    medium = models.CharField(max_length=500, blank=True, null=True)
    dimensions = models.CharField(max_length=500, blank=True, null=True)
    accession_number = models.CharField(max_length=500, blank=True, null=True)
    provenance = models.TextField(blank=True, null=True)
    exhibition_history = HTMLField(blank=True, null=True)
    essays_publications = HTMLField(null=True, blank=True)
    keywords = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=500, blank=True, null=True)
    object_type = models.CharField(max_length=500, blank=True, null=True)
    collection_highlights = models.BooleanField(default=False, null=True)
    slug = models.SlugField(unique=True, null=True)

    class Meta:
        verbose_name = _("Object")
        verbose_name_plural = _("Objects")
    def __str__(self):
        return '%s' % (self.object_name)

class Featured_Event(models.Model):
    event_name = models.CharField(max_length=500, blank=True, null=True)
    event_image = models.ImageField(upload_to='', default='', blank=True, null=True)  
    event_cover_image = models.ImageField(upload_to='', default='', blank=True, null=True)    
    event_short_description = models.CharField(max_length=500, blank=True, null=True)
    event_long_description = HTMLField(null=True, blank=True)
    featured = models.BooleanField(default=True, null=True)
    category = models.CharField(max_length=500, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    time_duration = models.CharField(max_length=500, blank=True, null=True, help_text="Please use the following format: hr:min am/pm - hr:min am/pm.")
    slug = models.SlugField(unique=True, null=True)

    class Meta:
        verbose_name = _("Featured Event")
        verbose_name_plural = _("Featured Events")
    def __str__(self):
        return '%s' % (self.event_name)
        
        
        

#NEWLY ADDED MODELS


class InTheNews(models.Model):
    event_name = models.CharField(max_length=500, blank=True, null=True)
    event_image = models.ImageField(upload_to='', default='', blank=True, null=True)
    event_short_description = models.CharField(max_length=500, blank=True, null=True)
    event_long_description = HTMLField(null=True, blank=True)
    featured = models.BooleanField(default=True, null=True)
    category = models.CharField(max_length=500, blank=True, null=True)
    year = models.DateField(blank=True, null=True)
    month = models.DateField(blank=True, null=True)
    time_duration = models.CharField(max_length=500, blank=True, null=True, help_text="Please use the following format: hr:min am/pm - hr:min am/pm.")
    slug = models.SlugField(unique=True, null=True)
    topic = models.CharField(max_length=500, blank=True, null=True)
    author =  models.CharField(max_length=500, blank=True, null=True)
    link =  models.CharField(max_length=500, blank=True, null=True)
    #

    class Meta:
        verbose_name = _("In The News")
        verbose_name_plural = _("In The News")
    def __str__(self):
        return '%s' % (self.event_name)



class Journals(models.Model):
    event_name = models.CharField(max_length=500, blank=True, null=True)
    event_image = models.ImageField(upload_to='', default='', blank=True, null=True)
    event_cover_image = models.ImageField(upload_to='', default='', blank=True, null=True)
    event_short_description = models.CharField(max_length=500, blank=True, null=True)
    event_long_description = HTMLField(null=True, blank=True)
    featured = models.BooleanField(default=True, null=True)
    category = models.CharField(max_length=500, blank=True, null=True)
    year = models.DateField(blank=True, null=True)
    month = models.DateField(blank=True, null=True)
    time_duration = models.CharField(max_length=500, blank=True, null=True, help_text="Please use the following format: hr:min am/pm - hr:min am/pm.")
    slug = models.SlugField(unique=True, null=True)
    topic = models.CharField(max_length=500, blank=True, null=True)
    author =  models.CharField(max_length=500, blank=True, null=True)


    class Meta:
        verbose_name = _("Journals")
        verbose_name_plural = _("Journals")
    def __str__(self):
        return '%s' % (self.event_name)


class Book_ticket(models.Model):
	entry_type = models.CharField(max_length=500, blank=True, null=True)
	date = models.CharField(max_length=100, blank=True, null=True)
	time = models.CharField(max_length=100, blank=True, null=True)
	adult_no = models.CharField(max_length=100, blank=True, null=True)
	child_no = models.CharField(max_length=100, blank=True, null=True)
	friend_no = models.CharField(max_length=100, blank=True, null=True)
	no_of_tickets = models.CharField(max_length=100, null=True, blank=True)
	amount = models.CharField(max_length=100,blank=True, null=True)
	full_name = models.CharField(max_length=200, blank=True, null=True)
	email = models.CharField(max_length=200,blank=True, null=True)
	phone_number = models.CharField(max_length=200,blank=True, null=True)

class MemberShip(models.Model):
	type_of_membership = models.CharField(max_length=500, blank=True, null=True)
	amount = models.CharField(max_length=100, blank=True, null=True)
	full_name = models.CharField(max_length=200, blank=True, null=True)
	email = models.CharField(max_length=200, blank=True, null=True)
	phone_number = models.CharField(max_length=200, blank=True, null=True)