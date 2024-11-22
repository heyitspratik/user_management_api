from django.urls import path
from api.views import UserListCreate, UserDetail

urlpatterns = [
    path('users', UserListCreate.as_view(), name='user-create'),
    path('users/<str:user_id>', UserDetail.as_view(), name='user-detail'),
]
