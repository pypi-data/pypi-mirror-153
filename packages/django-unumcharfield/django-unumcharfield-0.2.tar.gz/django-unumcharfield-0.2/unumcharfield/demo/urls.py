from .                import views
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.UnumCharFieldTestList.as_view(), name='formulas'),
    url(r'^(?P<pk>[A-Z0-9-]+)/$', views.UnumCharFieldTest.as_view(), name='formulas'),
]