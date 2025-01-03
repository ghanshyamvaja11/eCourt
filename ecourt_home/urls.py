from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('aboutus/', aboutus, name='about'),
    path('contactus/', contactus, name='contact'),
    path('terms-and-condition/', terms_and_conditions, name='t&c'),
    path('privacy-policy/', privacy_policy, name='privacy_policy'),
    # path('faq/', faq, name='faq'),
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
]
