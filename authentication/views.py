from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'message': f'Hello, {request.user.username}!'})
    
    
@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)

        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'message': 'Login successful',
            'token': token.key  
        })
    else:
        return Response({'message': 'Invalid credentials'}, status=400)
    

@api_view(['POST'])
def logout_view(request):
    user = request.user
    if user.is_authenticated:
        
        Token.objects.filter(user=user).delete()

        logout(request)

        return Response({'message': 'Logged out successfully'})
    else:
        return Response({'message': 'No user is logged in'}, status=400)
