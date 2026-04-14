from api import views as api_views
from django.urls import path
urlpatterns=[
    path("user/register/",api_views.RegisterView.as_view()),
    path("create-association",api_views.create_association,name='create-association'),
]