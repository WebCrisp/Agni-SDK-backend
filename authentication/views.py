from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import UserSerializer, ProjectSerializer
from .utils import APIKeyAuthentication, ProjectPermission
from .models import Projects, UserProfile
from rest_framework.views import APIView
from . import helper

# auth views
class SignUpView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        user.save()

class GetUserAuthView(APIView):
    def post(self, request):
        print(helper.signInAccount(request))
        return helper.signInAccount(request)

# project views
class ProjectRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    
    authentication_classes = [APIKeyAuthentication]
    permission_classes = [ProjectPermission]

    queryset = Projects.objects.all()
    serializer_class = ProjectSerializer

class ProjectCreateView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Projects.objects.all()
    serializer_class = ProjectSerializer