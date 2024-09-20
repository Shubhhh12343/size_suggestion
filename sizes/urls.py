from django.urls import path
from sizes.views import *

urlpatterns = [
        path('', chest_size_view, name='chest_size'),

]
