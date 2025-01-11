from django.urls import path
from .views import login_view, logout_view, ProtectedView

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('protected/', ProtectedView.as_view(), name='protected'),
]
