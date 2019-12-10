from django.shortcuts import render
from rest_framework.views import APIView
from bookmarks.serializer import BookmarkSerializer 
from django.views import View as view
from bookmarks.models import Bookmark
from rest_framework import mixins ,permissions,status
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, DestroyModelMixin,CreateModelMixin
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from django.contrib.auth.models import AnonymousUser

# Create your views here.

class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
       
        return obj.owner == request.user
    
class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return 

class BookmarksViewSet(DestroyModelMixin,
                       RetrieveModelMixin,
                       ListModelMixin,
                       GenericViewSet):
    queryset = Bookmark.objects.all()
    authentication_classes = (CsrfExemptSessionAuthentication, SessionAuthentication)
    permission_classes = [IsAuthenticated]
    serializer_class = BookmarkSerializer

    def get_queryset(self):
        
        return Bookmark.objects.filter(user = self.request.user)

    def create(self, request, *args, **kwargs):
         request_copy = request.data.copy()
         print(request_copy)
         request_copy['user'] = str(request.user.id)
         serializer = self.get_serializer(data=request_copy)
         serializer.is_valid(raise_exception=True)
         serializer.save()
         return Response(serializer.data, status=status.HTTP_201_CREATED)
                       
                          

@csrf_exempt
def login(request):
    # CSRF exempt login for REST API client
    
    user = authenticate(username=request.POST['username'],password=request.POST['password'])
    print("found auth match: %s" % user)

    if user is None:
        print('anonimus user returned, no match ....')
        return HttpResponse("No authentication match.",status=403)
    else:
        auth_login(request, user)
        

    return HttpResponse('Success')

@csrf_exempt
def logout(request):
    # CSRF exempt login for REST API client
    auth_logout(request)

    return HttpResponse('Success')
    

    


    
    