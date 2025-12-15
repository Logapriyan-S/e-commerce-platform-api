from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from calcengine.serializers import UserRegisterSerializer, UserProfileSerializer

# ✅ Login View (uses built-in JWT token handling)
class MyLoginView(TokenObtainPairView):
    permission_classes = [AllowAny]

# ✅ Register View
class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            return Response(
                {"message": "Registration successful"},
                status=status.HTTP_201_CREATED
            )
        return response

# ✅ Profile View (requires login + access token)
class ProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
