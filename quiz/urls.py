from django.urls import path # type: ignore
from .views import quiz_view  

urlpatterns = [
    path('', quiz_view, name='quiz'),
]
