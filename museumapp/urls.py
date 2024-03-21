from django.urls import path
from . import views
from museumapp.views import *
app_name = 'museumapp'
urlpatterns = [
	# path('home/', views.HomePage.as_view(), name='home'),
	
	path('collections', views.CollectionPage.as_view(), name='collection'),
	
	path('listofObjects', views.ObjectViewPage.as_view(), name='listofObjects' ),
	path('colldetails/<str:slug>', views.CollectionObjectDetails.as_view(), name='objectdetails'),
	path('storylist', views.Storylist.as_view()),
	path('stdetailrest/<str:slug>',views.StoryDetailREST.as_view()),
	path('objectlist/<str:slug>', views.Objectlist.as_view()),

	# path('srch/', srch, name = 'srch'),
	path('searchfilter/', views.ProjectListing.as_view(), name = 'listing'),
	path('ajax/getobjtype/', getobj_type, name = 'getobj_type'),
	path('ajax/material/', getmaterial, name = 'getmaterial'), 
	path('ajax/getdate/', getdate, name = 'getdate'),
	path('ajax/getlocation/', getlocation, name = 'getlocation'), 

	path('', views.indexMocaView.as_view(), name='indexMoca'),
	path('about-us', views.aboutMocaView.as_view(), name='aboutUsMoca'),
	path('knowledge-center', views.knowledgeMocaView.as_view(), name='knowledgeCenterMoca'),
	path('plan-a-visit', views.planAVisitMocaView.as_view(), name='planAVisitMoca'),
	path('guided-tours', views.guidedToursMocaView.as_view(), name='guidedToursMoca'),
	path('moca-connections', views.connectionsMocaView.as_view(), name='connectionsMoca'),
	path('moca-cafe', views.cafeMocaView.as_view(), name='cafeMoca'),
	path('moca-learn', views.learnMocaView.as_view(), name='learnMoca'),
	path('moca-support', views.supportMocaView.as_view(), name='supportMoca'),
	path('moca-accessibility', views.accessibilityMocaView.as_view(), name='accessibilityMoca'),
	path('moca-conservation', views.conservationMocaView.as_view(), name='conservationMoca'),
	path('moca-families', views.familiesMocaView.as_view(), name='familiesMoca'),
	path('moca-community-initiatives', views.communityIniMocaView.as_view(), name='communityIniMoca'),
	path('moca-restoration', views.restorationMocaView.as_view(), name='restorationMoca'),
	path('moca-research', views.researchMocaView.as_view(), name='researchMoca'),
	path('moca-library-and-archives', views.libraryArchivesMocaView.as_view(), name='libraryArchivesMoca'),
	path('moca-digital-repository', views.digitalrepMocaView.as_view(), name='digitalrepMoca'),
	path('moca-press', views.mocapressMocaView.as_view(), name='mocapressMoca'),
	path('contact-us', views.contactUsMocaView.as_view(), name='contactUsMoca'),
	path('press', views.pressMocaView.as_view(), name='pressMoca'),
	path('careers', views.careerMocaView.as_view(), name='careerMoca'),
	path('journalold', views.journalMocaView.as_view(), name='journalMoca'),
	path('tickets', views.ticketMocaView.as_view(), name='ticketMoca'),
	path('whats-on1', views.whatsOnMocaView.as_view(), name='whatsOnMoca'),
	path('artculture', views.artCultureMocaView.as_view(), name='artCultureMoca'),
	path('demo', views.demoMocaView.as_view(), name='demoMoca'),
	
	path('moca-stories', views.storiesMocaView.as_view(), name='storiesMoca'),
	path('moca-story/<str:slug>', views.storyDetailsMocaView.as_view(), name='storyDetailsMoca'),
	
	path('moca-collections', views.collectionsMocaView.as_view(), name='collectionsMoca'),
	
	path('moca-object/<str:slug>', views.objectDetailsMocaView.as_view(), name='objectDetailsMoca'),
	

	

	# path('whats-on_old', views.eventsMocaView.as_view(), name='eventsMoca'),
	path('whats-on_old', views.eventsMocaView.as_view(), name='eventsMocaMoca'),
	path('moca-event-listing/', eventListing.as_view(), name = 'eventListing'),
	path('ajax/category/', getcategory, name = 'get_category'),

	path('featured-event/<str:slug>', views.featuredDetailMocaView.as_view(), name='featuredDetailMoca'),


	


	#--------------ALL BACKUP PARTS-----------------------
	#path('story', views.StoryPage.as_view(), name='story'),
	#path('storydetails/<str:slug>', views.StoryDetail.as_view(), name='strydetails'),
	
    
    
    #Newly Added Urls Starts From Here


	# path('whats-on', views.whatsOn_search_data, name='whatsOn_search_data'),
	path('whats-on', views.whatsOn_search_data, name='eventsMoca'),
	path('whatsOn_get_category', views.whatsOn_get_category, name='whatsOn_get_category'),
	path('whatsOn_get_start_end_date', views.whatsOn_get_start_end_date, name='whatsOn_get_start_end_date'),
	path('whatsOn_detailed_view/<slug:slug_text>', views.whatsOn_detailed_view, name='whatsOn_detailed_view'),





	path('in_the_news', views.in_the_news_search_data, name='in_the_news_search_data'),
	path('get_tpoic', views.in_the_news_get_tpoic, name='in_the_news_get_tpoic'),
	path('get_mn_year', views.in_the_news_get_mn_year, name='in_the_news_get_mn_year'),



	path('journal', views.journals_search_data, name='journals_search_data'),
	path('journals_get_tpoic', views.journals_get_tpoic, name='journals_get_tpoic'),
	path('journals_get_mn_year', views.journals_get_mn_year, name='journals_get_mn_year'),
	path('journal_detailed_view/<slug:slug_text>', views.journal_detailed_view, name='journal_detailed_view'),


# Objects URL
	path('moca-objects/<slug:slug_text>', views.objectsMoca, name='objectsMoca'),
	path('filter_object_type/', views.filter_object_type, name='filter_object_type'),
	path('filter_object_mat_loc_time/', views.filter_object_mat_loc_time, name='filter_object_mat_loc_time'),
	path('moca-object-detailed-view/<slug:slug_text>', views.object_detailed_view, name='object_detailed_view'),

	#navigation Search Bar
	path('nav_search/', views.nav_search, name='nav_search'),
	path('nav_search_ajax/', views.nav_search_ajax, name='nav_search_ajax'),


	path('book-tickets/', views.buy_tickets, name='buy_tickets'),
	path('membership/', views.membership, name='membership'),

	#shop alert URL
	path('mocashop/', views.shopAlert, name="shopAlert"),

	path('embedding/', views.embedding, name="embedding"),
	path('The-Life-of-Christ-through-Indo-Portuguese-Art/', views.embeddingOne, name="embeddingOne"),
	path('Goencho-Saib-The-Life-and-Miracles-of-Saint-Francis-Xavier/', views.embeddingTwo, name="embeddingTwo"),
	path('Faith-and-Fabric-Glimpses-of-Sacred-Textiles-from-Goa/', views.embeddingThree, name="embeddingThree"),



]
