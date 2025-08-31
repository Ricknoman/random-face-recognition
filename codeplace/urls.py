from django.urls import path
from codeplace import views

urlpatterns = [
    path('',views.home , name='home'),
    path('upload/',views.upload , name='upload'),
    path('capture/',views.capture , name='capture'),
    path('result/<int:pk>/',views.result , name='result')
]