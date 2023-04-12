from django.urls import path
from .views import DocumentAPIView, AddSubCollectionAPIView

urlpatterns = [
    path('add-document/', DocumentAPIView.as_view(), name='add-document'),
    path('query-document/<str:lookup_field>/<str:lookup_value>/', DocumentAPIView.as_view(), name='get-document'),
    path('update-document/', DocumentAPIView.as_view(), name='add-document'),
    path('delete-document/<str:document>', DocumentAPIView.as_view(), name='delete-document'),
    path('create-sub-collection/', AddSubCollectionAPIView.as_view(), name='create-collection'),
]