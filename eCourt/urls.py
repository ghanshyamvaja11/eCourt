from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('cases/', include('cases.urls')),
    path('efiling/', include('efiling.urls')),
    path('documents/', include('documents.urls')),
    path('notifications/', include('notifications.urls')),
]