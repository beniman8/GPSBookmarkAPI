"""drftest1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.models import User,Group,Permission
from rest_framework import routers, serializers, viewsets
from bookmarks.serializer import BookmarkSerializer
from bookmarks.models import Bookmark
import bookmarks.views

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    bookmarks = serializers.PrimaryKeyRelatedField(many = True,queryset= Bookmark.objects.all())
    
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff', 'bookmarks', 'is_superuser']

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class GroupPermissionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'url', 'name', 'codename']

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class BookmarkViewSet(viewsets.ModelViewSet):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer

class GroupPermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = GroupPermissionSerializer



# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'bookmarks', bookmarks.views.BookmarksViewSet)
router.register(r'permissions', GroupPermissionViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('login/',bookmarks.views.login), # for clients no csrf
    path('logout/',bookmarks.views.logout), # for clients no csrf
    path('', include('rest_framework.urls', namespace='rest_framework'))

]
