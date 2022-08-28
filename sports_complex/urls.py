"""sports_complex URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from django.urls import path
from sports import views as sports_view
from sports.views import (SlotListView,
                          SlotDetailView,
                          SlotCreateView,
                          SlotUpdateView,
                          SlotDeleteView,
                          SportSlotListView,
                          SportListView,
                          SportDetailView,
                          SportCreateView,
                          SportUpdateView,
                          SportDeleteView,
                          MatchCreateView,
                            MatchDeleteView,
                            MatchUpdateView,
                          )
from courts.views import (CourtListView,
                          CourtDetailView,
                          CourtCreateView,
                          CourtUpdateView,
                          CourtDeleteView)
from users import views as user_views
from courts import views as courts_view
from django.conf import settings
from django.conf.urls.static import static
from sports.views import add_slot
from sports.views import remove_slot

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('sports/', SportListView.as_view(), name='sports-home'),
    path('slots/', SlotListView.as_view(), name='slots-home'),
    path('slots/<int:pk>/', SlotDetailView.as_view(), name='slots-detail'),
    path('slots/new/', SlotCreateView.as_view(), name='slots-create'),
    path('slots/<int:pk>/update', SlotUpdateView.as_view(), name='slots-update'),
    path('slots/<int:pk>/delete', SlotDeleteView.as_view(), name='slots-delete'),
    path('sports/new/', SportCreateView.as_view(), name='sports-create'),
    path('sports/<int:pk>/', SportDetailView.as_view(), name='sports-detail'),
    path('sports/<str:name>/', SportSlotListView.as_view(), name='sport-slots'),
    path('sports/<int:pk>/update', SportUpdateView.as_view(), name='sports-update'),
    path('sports/<int:pk>/delete', SportDeleteView.as_view(), name='sports-delete'),
    path('match/new/', MatchCreateView.as_view(), name='match-create'),
    path('match/<int:pk>/update', MatchUpdateView.as_view(), name='match-update'),
    path('match/<int:pk>/delete', MatchDeleteView.as_view(), name='match-delete'),
    path('courts/', CourtListView.as_view(), name='courts-home'),
    path('courts/<int:pk>/', CourtDetailView.as_view(), name='courts-detail'),
    path('courts/new/', CourtCreateView.as_view(), name='courts-create'),
    path('courts/<int:pk>/update', CourtUpdateView.as_view(), name='courts-update'),
    path('courts/<int:pk>/delete', CourtDeleteView.as_view(), name='courts-delete'),
    path('slots/<int:pk>/add', add_slot, name='add_slot'),
    path('slots/<int:pk>/remove', remove_slot, name='remove_slot'),
    path('', sports_view.home, name='main-home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
