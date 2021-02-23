from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import get_user_model, authenticate
from rest_framework.settings import api_settings
from rest_framework.authtoken.models import Token
from django.utils.timezone import now
from rest_framework.parsers import MultiPartParser

from django.conf import settings

from django.core.exceptions import ObjectDoesNotExist

from .models import User, Enrollee

from django.db.models import Q

from .serializers import UserSerializer, AuthTokenSerializer, EnrolleeSerializers, UserDetails



from rest_framework.response import Response
from rest_framework import status
from rest_framework import status, viewsets, mixins
# Create your views here.

class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer
    permission_class = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.data
        email = data.get('email')
        phone_no = data.get('phone_no')
        password = data.get('password')
        qs = User.objects.filter(Q(email__iexact=email) | Q(phone_no__iexact=phone_no))
        if qs.exists():
            return Response({"message": "User already exist in our database", "status": 401}, status=401)
        else:
            serializer = UserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            to = authenticate(username=email, password=password);
            token = Token.objects.create(user=to);
            print(token)
            return Response({"message": "your registeration was successful", "status": 200, "data": serializer.data, "token": token.key }, status=200)
        return Response({"message": "Invalid Request", "status": 400}, status=400)


class CreateTokenView(ObtainAuthToken):
    """Create new user in the system"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class CreateUpdateEnrollment(generics.ListAPIView):
    queryset = Enrollee.objects.all()
    serializer_class = EnrolleeSerializers
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        data = request.data
        email = data.get('email')
        phone_no = data.get('phone_no')
        password = data.get('password')
        qs = Enrollee.objects.filter(Q(email__iexact=email) | Q(phone_no__iexact=phone_no))
        if qs.exists():
            return Response({"message": "User already exist in our database", "status": 401}, status=401)
        else:
            serializer = EnrolleeSerializers(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(enrollment_officer=self.request.user)
            return Response({"message": "your registeration was successful", "status": 200, "data": serializer.data}, status=200)
        return Response({"message": "Invalid Request", "status": 400}, status=400)

    def list(self, request):
        """Return Object for the currenc authenticated user"""
        queryset = self.get_queryset().filter(enrollment_officer=self.request.user)
        serializer = EnrolleeSerializers(queryset, many=True)
        return Response(serializer.data)

class UserDataView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def list(self, request):
        data = request.user
        print(request.user)
        queryset = self.get_queryset().filter(email__iexact=data)
        serializer = UserDetails(queryset, many=True)
        return Response(serializer.data[0])
