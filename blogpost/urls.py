from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import (
    BlogPostListView,
    BlogPostDetailView,
    BlogPostCreateView,
    BlogPostUpdateView,
    BlogPostDeleteView
)

app_name = 'blogpost'

urlpatterns = [
    path('', BlogPostListView.as_view(), name='blogpost_list'),
    path('create/', BlogPostCreateView.as_view(), name='blogpost_create'),
    path('detail/<int:pk>/', BlogPostDetailView.as_view(), name='blogpost_detail'),
    path('edit/<int:pk>/', BlogPostUpdateView.as_view(), name='blogpost_edit'),
    path('delete/<int:pk>/', BlogPostDeleteView.as_view(), name='blogpost_delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
