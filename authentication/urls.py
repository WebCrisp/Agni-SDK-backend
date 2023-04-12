from django.urls import path
from .views import SignUpView, ProjectRetrieveUpdateDestroyView, ProjectCreateView, GetUserAuthView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signin/', GetUserAuthView.as_view(), name='signin'),
    
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('projects/<str:pk>', ProjectRetrieveUpdateDestroyView.as_view(), name='project-details'),
    path('projects/', ProjectCreateView.as_view(), name='project'),
]