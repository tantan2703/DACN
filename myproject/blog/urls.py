from django.urls import path
from .views import blog_detail, like_comment, blog_comment

urlpatterns = [
    # Các URL khác ở đây...

    path('blog/<str:post_title>/', blog_detail, name='blog_detail'),
    path('blog/<str:post_title>/comment/<int:comment_id>/like/', like_comment, name='like_comment'),
    path('blog/<str:post_title>/comment/', blog_comment, name='blog_comment'),
]
