from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Projects

class APIKeyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        api_key = request.data.get('api_key')
        if api_key:
            try:
                project = Projects.objects.get(api_key=api_key)
            except Projects.DoesNotExist:
                raise AuthenticationFailed('Invalid API key')
            return (project, None)
        raise AuthenticationFailed('API key is required')
    
class ProjectPermission(BasePermission):
    def has_permission(self, request, view):
        jwt_auth = JWTAuthentication()

        print(jwt_auth.authenticate(request))
        try:
            auth_result = jwt_auth.authenticate(request)
        except AuthenticationFailed as e:
            raise AuthenticationFailed("Invalid or expired token")
            
        if auth_result is not None:
            user, token = auth_result
            request.user = user
            request.auth = token
            print(request,'request here')
            return True
        
        return False