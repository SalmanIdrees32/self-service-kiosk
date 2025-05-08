
from django.contrib import admin
from django.urls import path, include
from konrix.view import index_view
from account.views import home,student_submission
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # path("", view=index_view, name="index"),
    path('management/', home, name='home'),

    #Apps
    path("apps/" , include("apps.urls")),

    #Custom
    path("custom/" , include("custom.urls")),

    # Layouts
    path("layouts/", include("layouts.urls")),

    #Elements
    path("elements/", include("elements.urls")),

    #Docs
    path("docs/", include("documentation.urls")),
    
    # our customer
    path('account/',include('account.urls')),

    path('', student_submission, name='student_submission'),


]
if settings.DEBUG:  # This ensures that static files are served only in development
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)