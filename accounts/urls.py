from django.urls import path

from accounts.views import UserRegistration, UserAuthentication, logout_view, EditProfile, ViewProfile


urlpatterns = [
    path('registration/', UserRegistration.as_view(), name='registration'),
    path('login/', UserAuthentication.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),

    path('edit-pofile/<slug:username_slug>', EditProfile.as_view(), name='edit-profile'),
    path('view-pofile/<slug:username_slug>', ViewProfile.as_view(), name='view-profile'),
]
