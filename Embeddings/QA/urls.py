from django.urls import path
from QA import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', views.qa_list),
]

urlpatterns = format_suffix_patterns(urlpatterns)