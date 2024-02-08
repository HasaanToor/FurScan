"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path
from .views import index, animals, cat_conjunct, Cats,Dogs,Kennel,disclaimer,learnmore,cateyes,CatConjunctForm,bloating

urlpatterns = [
    path("", index, name="index"),
    path('animals/', animals, name='animals'),
    path('Cats/', Cats, name='Cats'),
    path('Dogs/Kennel/', Kennel, name='Kennel'),
    path('Dogs/Bloating/', bloating, name='bloating'),
    path('Dogs/', Dogs, name='Dogs'),
    path('disclaimer/', disclaimer, name='disclaimer'),
    path('learnmore/', learnmore, name='learnmore'),
    path('Cats/cateyes/', cateyes, name='cateyes'),
    path('Cats/cateyes/cat_conjunct/', cat_conjunct, name='cat_conjunct'),
    path('Cats/cateyes/CatConjunctForm/', CatConjunctForm, name='CatConjunctForm'),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)