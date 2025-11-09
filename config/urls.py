from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from todo.views import TodoViewSet
from library.views import BookViewSet

router = DefaultRouter()
router.register('todos', TodoViewSet, basename='todos')
router.register('books', BookViewSet, basename='books')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
