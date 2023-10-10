from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from . import views
app_name="userprofile"
urlpatterns=[
    path('', views.ProfileListView.as_view(), name="all-profiles-view"),
    path('myprofile/', views.my_profile_view, name="my-profile-view" ),
    path('myinvates/', views.invites_received_view,name="my-invites-view"),
    path('_<str:slug>/', views.ProfileDetailView.as_view(), name="profile-detail-view"),
    path('to_invite/', views.invite_profile_list_view, name="invite-profiles-view"),
    path('send_invite/', views.send_invatations, name="send-invite"),
    path('remove_friend/', views.remove_from_friends, name="remove-friend"),
    path('myinvites/accept/', views.accept_invatation, name="accept-invite"),
    path('myinvites/reject/', views.reject_invatation, name="reject-invite"),
]