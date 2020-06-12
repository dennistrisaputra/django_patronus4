from django.urls import path
from . import views

app_name='reference'
urlpatterns = [
    path('references/', views.ReferenceListView.as_view(), name = 'api_reference_list'),
    path('references/<int:pk>/', views.ReferenceDetailView.as_view(), name= 'api_reference_detail'),

]