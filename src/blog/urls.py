from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('collective_blog.urls')),
]

handler404 = "collective_blog.views.custom_handler404"
handler500 = "collective_blog.views.custom_handler404"
