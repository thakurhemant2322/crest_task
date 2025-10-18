from rest_framework import generics, permissions
from django.contrib.auth.models import User, Group
from rest_framework.response import Response
from rest_framework import status
from rest_framework.throttling import ScopedRateThrottle

class RegisterView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    throttle_scope = "auth"

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        role = request.data.get('role', 'user')  # 'admin' or 'user'

        if not username or not password:
            return Response({'detail': 'username and password required'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'detail': 'username already taken'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password)
        # ensure groups exist
        admin_g, _ = Group.objects.get_or_create(name='admin')
        user_g, _ = Group.objects.get_or_create(name='user')

        if role == 'admin':
            user.groups.add(admin_g)
        else:
            user.groups.add(user_g)

        return Response({'detail': 'registered successfully', 'username': user.username, 'role': role}, status=status.HTTP_201_CREATED)
