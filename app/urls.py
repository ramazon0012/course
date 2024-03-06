from app.views import *
from django.urls import path
urlpatterns = [
    path('', home, name="home"),
    path('full_search/', full_search, name="full_search"),
    path('account/<str:pk>/', account, name="account"),
    path('account_courses/<str:pk>/', user_courses, name="user_courses"),
    path('add_course/', add_course, name="add_course"),
    path('delete_users/<str:pk>/', delete_users, name='delete_users'),
    path('search/', search, name="search"),
    path('logout/', logoutUser, name='logout'),
    path("login/", loginPage, name="login"),
    path('register/', registerPage, name="register"),
    path('courses/', courses, name="courses"),
    path('courses/<str:name>/', courses_tag, name="courses_tag"),
    path('follow_user/<str:pk>/',follow_user, name="follow_user"),
    path('unfollow_user/<str:pk>/',unfollow_user, name="unfollow_user"),
    path('update_user/<str:pk>/', updateUser, name="updateUser"),
    path('delete_user/<int:user_id>/', delete_user, name='delete_user'),
    path('account/delete_course/<str:pk>/<str:id>', delete_course, name='delete_course'),
    path('<slug:part_slug>/', coursesview,
    name='product_list_by_category'),
    path('detail/<int:pk>/', detail, name="detail"),
    path('detail_video/<int:pk>/<int:id>/', detail_video, name="detail_video"),
    path('like_course/<int:pk>/', like_course, name="like_course"),
    path('deslike_course/<int:pk>/', deslike_course, name="deslike_course"),
]
