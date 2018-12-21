"""srvup URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from .views import home, HomeView
from videos.views import VideoList, list_view, VideoDetail, detail_view, VideoCreate, create_view, VideoUpdate, \
    VideoDelete
from courses.views import CourseList, CourseDelete, CourseDetail, CourseUpdate, CourseCreate, LectureDetailView, \
    lecturedetailview, CoursePurchaseView
from categories.views import CategoryListView, CategoryDetailView
from django.conf import settings
from django.conf.urls.static import static
from search.views import SearchView

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', home, name='home'),
    path('', HomeView.as_view(), name='home'),
    path('video-list/', VideoList.as_view(), name='video-list'),
    # path('video-list/', list_view, name='video-list'),
    path('video-list/<slug:slug>/', VideoDetail.as_view(), name='video-detail'),
    # path('video-list/<int:pk>/', detail_view, name='video-detail'),
    path('add/', VideoCreate.as_view(), name='video-create'),
    # path('add/', create_view, name='video-create'),
    path('video-list/<slug:slug>/edit/', VideoUpdate.as_view(), name='video-update'),
    path('video-list/<slug:slug>/delete/', VideoDelete.as_view(), name='video-delete'),

    path('course-list/', CourseList.as_view(), name='course-list'),
    # path('video-list/', list_view, name='video-list'),
    path('course-list/<slug:slug>/', CourseDetail.as_view(), name='course-detail'),
    path('course-list/<slug:slug>/purchase/', CoursePurchaseView.as_view(), name='course-purchase'),
    path('course-list/<slug:cslug>/<slug:lslug>/', LectureDetailView.as_view(), name='lecture-detail'),
    # path('course-list/<slug:cslug>/<slug:lslug>/', lecturedetailview, name='lecture-detail'),

    # path('video-list/<int:pk>/', detail_view, name='video-detail'),
    path('course-add/', CourseCreate.as_view(), name='course-create'),
    # path('add/', create_view, name='video-create'),
    path('course-list/<slug:slug>/edit/', CourseUpdate.as_view(), name='course-update'),
    path('course-list/<slug:slug>/delete/', CourseDelete.as_view(), name='course-delete'),

    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<slug:slug>/', CategoryDetailView.as_view(), name='category-detail'),


    path('search/', SearchView.as_view(), name='default'),

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
