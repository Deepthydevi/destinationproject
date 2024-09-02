from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('create/', DestinationCreate.as_view(), name='create-destination'),
    path('detail/<int:pk>/', DestinationDetail.as_view(), name='detail'),
    path('update/<int:pk>/', DestinationUpdate.as_view(), name='update'),
    path('delete/<int:pk>/', DestinationDelete.as_view(), name='delete'),
    path('search/<str:Name>/', DestinationSearch.as_view(), name='search'),
    path('', views.index, name='index'),
    path('add/', views.add_destination, name='create-destination'),
    path('update_detail/<int:id>/', views.update_destination, name='update_detail'),
    path('destination_fetch/<int:id>/', views.destination_fetch, name='destination-fetch'),
    path('destination_delete/<int:id>/', views.destination_delete, name='destination_delete'),

]
