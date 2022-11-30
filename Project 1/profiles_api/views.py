from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from profiles_api import serializers
from rest_framework import viewsets
from profiles_api import models
from rest_framework.authentication import TokenAuthentication
from profiles_api import permissions
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated


class HelloApiView(APIView): 
    """Test API View"""
    serializer_class = serializers.HelloSerializer

    def get(self, request, format=None): 
        """Return a list of APIView features"""
    
        an_apiview = ["Testing1", "Testing2", "Testing3"]

        return Response({"message": "Hello APIView", "an_apiview": an_apiview})
    
    def post(self, request):
        """Hello message with name"""

        serializer = self.serializer_class(data=request.data)
        print(request)
        if serializer.is_valid():
            name = serializer.validated_data.get("name")
            message = f"Hello {name}"
            return Response({"message": message})
        else: 
            return Response(
                serializer.errors, 
                status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pK=None): 
        """Handle updating an object"""
        return Response({"method": "put"})
    
    def patch(self, request, pK=None): 
        """Handle a partial update of an object"""
        return Response({"method": "patch"})
    
    def delete(self, request, pK=None): 
        """Delete an object"""
        return Response({"method": "delete"})


class HelloViewSet(viewsets.ViewSet):
    """Test API ViewSet"""

    serializer_class = serializers.HelloSerializer

    def list(self, request): 
        """Return a hello message"""
        a_viewset = ["Testing1", "Testing2", "Testing3"]
        return Response({"message": "Hello ViewSet!", "a_viewset": a_viewset})

    def create(self, request): 
        """Create a new hello message"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(): 
            name = serializer.validated_data.get("name")
            message = f'Hello {name}! From ViewSet'
            return Response({"message": message})
        else: 
            return Response(
                serializer.errors, 
                status=status.HTTP_400_BAD_REQUEST)

    
    def retrieve(self, request, pk=None): 
        """Getting a single object by its ID"""
        return Response({"http_method": "GET"})
    
    def update(self, request, pk=None): 
        """Updating an object"""
        return Response({"http_method": "PUT"})

    def partial_update(self, request, pk=None): 
        """Partial update of an object"""
        return Response({"http_method": "PATCH"})

    def destroy(self, request, pk=None): 
        """Removes an object"""
        return Response({"http_method": "DELETE"})

class UserProfileViewSet(viewsets.ModelViewSet): 
    """Handle creating an account and updating it"""

    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()

    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)

    filter_backends = (filters.SearchFilter,)
    search_fields = ("name", "email")

class UserLoginApiView(ObtainAuthToken): 
    """Create a user auth token"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class UserProfileFeedViewSet(viewsets.ModelViewSet): 
    """Handles creating, reading and updating profile feed items"""
    authentication_classes = (TokenAuthentication, )
    serializer_class = serializers.ProfileFeedItemSerializer

    queryset = models.ProfileFeedItem.objects.all()

    permission_classes = (
        permissions.UpdateOwnStatus,
        IsAuthenticated,
    )

    def perform_create(self, serializer):
        """Sets the user profile to the logged in user"""
        serializer.save(user_profile = self.request.user)
        return super().perform_create(serializer)
    
