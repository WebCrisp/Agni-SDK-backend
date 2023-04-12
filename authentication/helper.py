from . import models, serializers
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.response import Response

def signInAccount(request):
    email = request.data.get('email', None)
    password = request.data.get('password', None)
    
    if not email or not password:
        return Response({
            'code': 400,
            'msg': 'email and password required'
        }, status=404)

    user = models.UserProfile.objects.filter(email=email).first()

    if not user:
        return {
            'code': 400,
            'msg': 'Invalid username and password'
        }

    refresh = RefreshToken.for_user(user)
    access = AccessToken.for_user(user)

    return Response({
        'success': False,
        'code': 200,
        'refresh': str(refresh),
        'access': str(access),
        'account': serializers.UserSerializer(user).data,
    }, status=200)
