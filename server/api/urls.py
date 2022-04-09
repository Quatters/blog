from django.urls import path
from .views import RegisterView, PostView, CommentView, UserView, LogoutView
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('auth/register/', RegisterView.as_view()),
    path('auth/login/', obtain_auth_token),
    path('auth/user/', UserView.as_view()),
    path('auth/logout/', LogoutView.as_view()),
    path('posts/', PostView.as_view()),
    path('posts/<int:id>/', PostView.as_view()),
    path('comments/<int:post_id>/', CommentView.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)