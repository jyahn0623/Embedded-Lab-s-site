from django.urls import path
from Main.views import *
from Main import views

app_name = 'main'
urlpatterns = [
    path('', Main.as_view(), name="main"),
    path('members/', views.ViewMembers, name="Viewmembers"),
    path('mypage/', views.mypage, name="mypage"),
    path('user/edit/', views.editUser, name="edit-user"),
    path('register/', views.register, name="register"),
    path('ajax/idCheck/', views.isExistsID, name='check-id'),
    path('login/', Login.as_view(), name="login"),
    path('logout/', Logout.as_view(), name="logout"),
    path('board/', ViewBoard.as_view(), name="board"),
    path('board/write/', WriteBoard.as_view(), name="write-board"),
    path('board/<b_id>/', views.readBoard, name='read-board'),
    path('board/<pk>/edit/', EditBoard.as_view(), name="edit-board"),
    path('board/<b_pk>/delete', views.DeleteBoard, name="del-board"),
    path('ajax/file/<pk>/delete', views.delFileWithAjax, name="del-file-ajax"),
    path('board/search', views.searchBoard, name="search-board"),
    path('guestbook/', views.guestbook, name="guestbook"),
    path('ajax/guestbook/', views.ajaxguestbook, name="guestbook-ajax"),
    path('guestbook/write/', views.guestbookWrite, name="guestbook-write")
]


