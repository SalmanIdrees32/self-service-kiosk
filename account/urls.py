from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [  


   #authentication customer
   path('login/', login, name='login'),
   path('sign-up/', sign_up, name='sign_up'),
   path('logout/', logout_view, name='logout'),
   path('forgot-password/', forgot_password, name='forgot_password'),
   path('change-password/<token>/', change_password, name='change-password'),
   path('school-list/', school_list, name='school_list'),

   path('submition-message/<int:ticket_number>/', submition_message, name='submition_message'),
   path('chat_bot/', chat_bot, name='chat_bot'),
]

