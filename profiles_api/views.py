from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from profiles_api import serializers
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from profiles_api import models
from profiles_api import permissions


class HelloApiView(APIView):
    """Test API VIEW"""
    serializer_class = serializers.HelloSerializer

    def get(self, request, format="None"):
        """return a list of APIView features"""
        an_apiview = [
            'Menggunakan HTTP method seperti(get, post, path, put, delete',
            'dan ini sama dengan tradisonal django view',
            'Gives you the most control over you aplication login',
            'Is mapped manually ti URLs',
        ]

        return Response({'message': 'Hello!!', 'an_apiview': an_apiview})

    def post(self, request):
        """Membuat sebuah hello massage dengan nama kita"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({'message': message})
        else:
            return Response(
                serializer.errors,
                status = status.HTTP_400_BAD_REQUEST    
            )

    def put(self, request, pk=None):
        """Handle updating an object"""
        return Response({'method': 'PUT'})
    
    def patch(self, request, pk=None):
        """Handle partial object dari sebuah object"""
        return Response({'method' : 'PATCH'})

    def delete(self, request, pk=None):
        """Menghapus sebuah object"""
        return Response({'method' : 'DELETE'})


class HelloViewSet(viewsets.ViewSet):
    """Mencoba membuat API ViewSet"""
    serializer_class = serializers.HelloSerializer

    def list(self, request):
        """Akan mereturn hello message"""
        a_viewset = [
            'uses action (list, create, retrive, update, partial_update',
            'automatically maps to URLs using Routers',
            'Provides more functionally with less code',
        ]

        return Response({'message': 'hello', 'a_viewset': a_viewset})

    def create(self, request):
        """Membuat hello message"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'hello {name}!'
            return Response({'message': message})
        else:
            return Response(
                serializer.errors,
                status = status.HTTP_400_BAD_REQUEST
            )

    def retrieve(self, request, pk=None):
        """Akan menghandle getting object berdasarkan dari ID"""
        return Response({'http_method' : 'GET'})

    def update(seld, request, pk=None):
        """Akan menghandle updating object"""
        return Response({'http_method' : 'PUT'})

    def partial_update(self, request, pk=None):
        """Akan menghandle updating sebagain dari object"""
        return Response({'http_method':'PATCH'})

    def destroy(self, request, pk=None):
        """Akan menghandle penghapusan object"""
        return Response({'http_method': 'DELETE'})

class UserProfileViewSet(viewsets.ModelViewSet):
    """Menghandle pembuatan dan update profiles"""
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()

    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',)
    
class UserLoginApiView(ObtainAuthToken):
    """Akan menghandle pembuatan user authentication tokens"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """akan menghandle pembuatan, update profile feed item"""
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes = (
        permissions.UpdateOwnStatus,
        IsAuthenticated
    )

    def perform_create(self, serializer):
        """Akan mengatur profile untuk yang sudah login"""
        serializer.save(user_profile=self.request.user)
    
        