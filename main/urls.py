from django.urls import path
from .import views

urlpatterns = [
    path('',views.HomePage.as_view(),name='home_page'),
    path('register/',views.RegisterRequest.as_view(),name='register_page'),
    path('login/',views.LoginRequest.as_view(),name='login_page'),
    path('logout/',views.LogoutRequest.as_view(),name='logout_req'),
    path('movies_api,',views.MovieListAPI.as_view(),name='movies_api_page'),
    path('movies_api/creator/<str:pk>',views.MovieCreator.as_view(),name='movie_creator_page')
]