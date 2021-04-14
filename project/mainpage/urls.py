from django.contrib import admin
from django.urls import path

import mainpage.views

urlpatterns = [
    path('mainpage/', mainpage.views.main_page, name='mainpage'),
    

]
