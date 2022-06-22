"""auto_shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from atexit import register
from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from apps.cars.views import *
from apps.profile1.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='home'),
    path('filter_auto', FilterAuto.as_view(), name='filter_auto'),
    path('filter_auto_index', FilterAutoIndex.as_view(), name='filter_auto_index'),
    path('single_page:<int:id>', single, name='single_page'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),


    path('profile:<int:pk>', Ubd_user.as_view(), name='profile'),
    path('favorites', favorites, name='favorites'),
    path('listing', listing, name='listing'),
    path('listings', listings, name='listings'),
    path('addauto', listing, name='addauto'),
    path('messages', messages, name='messages'),
    path('dashboard', dashboard, name='dashboard'),
    path('delete:<int:id>', delete, name='delete'),
    path('delete_like:<int:id>', delete_like, name='delete_like'),
    path('Ubd_post:<int:pk>', Ubd_post.as_view(), name='Ubd_post'),


    path('filter', AutoAll.as_view(), name='filter'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)