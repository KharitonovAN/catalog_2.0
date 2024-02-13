from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import (
    HomeView,
    ContactsView,
    CategoryListView,
    ProductDetailView,
    CreateProductView,
    ProductListView,
    EditProductView,
    ProductDeleteView,
)


app_name = 'catalog'

urlpatterns = [

    path('', HomeView.as_view(), name='home'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('category/', CategoryListView.as_view(), name='category'),
    path('<int:pk>/products/', ProductListView.as_view(), name='product_list'),
    path('<int:pk>/product_detail/', ProductDetailView.as_view(), name='product_detail'),
    path('save_product/', CreateProductView.as_view(), name='create_product'),
    path('<int:pk>/edit_product/', EditProductView.as_view(), name='edit_product'),
    path('<int:pk>/delete/', ProductDeleteView.as_view(), name='product_confirm_delete'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
