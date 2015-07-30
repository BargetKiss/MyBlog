from django.conf.urls import url 
from litdev_comments.views import CommentControl

urlpatterns=[
    url(r'^comment/(?P<slug>\d+)$',CommentControl.as_view()),
]