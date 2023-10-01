# urls.py

from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Chrome Extension API",
        default_version='v1',
        description="This API provides access to a video recording and ,transcription service. You can use this API to start and stop video recording sessions, upload video chunks, and generate transcriptions for recorded videos. It's designed to assist in managing video content and transcriptions for various applications.",
        contact=openapi.Contact(email="jthuku490@gmail.com"),
        
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('extension.urls')),  # Include your API URLs here
    path('swagger<str:format>', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
