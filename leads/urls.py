from django.urls import path
from leads.views import (Firstpageview, Homeleadsview, leadview, createleadview,
 updateleadview, deleteleadview, Homeagentsview, CreateAgentView, 
 agentdetailview,UpdateAgentview, DeleteAgentview, AssignAgentView,
  HomeCategoryView, Categorydetailview,updateleadcategoryview, createcategoryview,
   Categoryupdateview, Categorydeleteview, userprofileview, Updateuserprofileview)
from . import views

app_name = "leads"
urlpatterns = [
    path('',Firstpageview.as_view(), name = 'firstpage'),
    path('home/',Homeleadsview.as_view(), name = 'Home'),
    path('homecategory/',HomeCategoryView.as_view(), name = 'Home-category'),
    path('<int:pk>/',leadview.as_view(), name = 'details'),
    path('<int:pk>/category-leads/',Categorydetailview.as_view(), name = 'categorydetails'),
    path('<int:pk>/category-update/',Categoryupdateview.as_view(), name = 'update-category'),
    path('<int:pk>/category-delete/',Categorydeleteview.as_view(), name = 'delete-category'),
    path('category-create/',createcategoryview.as_view(), name = 'create-category'),
    path('create/', createleadview.as_view(), name = 'Createlead'),
    path('<int:pk>/updatelead/',updateleadview.as_view(), name = 'updatelead'),
    path('<int:pk>/updatecategory/',updateleadcategoryview.as_view(), name = 'updatecategory'),
    path('<int:pk>/deletelead/',deleteleadview.as_view(), name = 'deletelead'),
    path('agents/', Homeagentsview.as_view(), name = 'agent-list'),
    path('createagents/', CreateAgentView.as_view(), name = 'createagents'),
    path('<int:pk>/agentdetails/', agentdetailview.as_view(), name = 'agentdetails'),
    path('<int:pk>/agentdetails/updateagent/', UpdateAgentview.as_view(), name = 'updateagent'),
    path('<int:pk>/agentdetails/deleteagent/', DeleteAgentview.as_view(), name = 'deleteagent'),    
    path('<int:pk>/assignagents/', AssignAgentView.as_view(), name = 'assignagent'),
    path('<int:pk>/profile/', userprofileview.as_view(), name = 'userprofile'),
    path('<int:pk>/updateprofile/', Updateuserprofileview.as_view(), name = 'updateprofile'),
    
]
