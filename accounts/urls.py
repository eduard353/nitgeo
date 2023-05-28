from django.urls import path

from accounts import views


app_name = 'accounts'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('activate/<str:username>/<str:token>', views.ActivateAccountView.as_view(), name='activate'),
    path('set-reset-password/<str:username>/<str:token>', views.PasswordSetView.as_view(),
         name='set_reset_password'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('reactivate/', views.ReactivationSentView.as_view(), name='reactivation_sent'),
    path('password-reset/', views.PasswordResetSentView.as_view(), name='password_reset_sent'),
    path('profile/create/', views.ProfileCreateView.as_view(), name='profile_create'),
    path('profile/<str:username>/show', views.ProfileDetailView.as_view(), name='profile_detail'),
    path('profile/<str:username>/follow', views.FollowView.as_view(), name='follow'),
    path('profile/<str:username>/update', views.ProfileUpdateView.as_view(), name='profile_update'),
    path('unfollow/<int:user_id>/', views.UnfollowView.as_view(), name='unfollow'),

]
