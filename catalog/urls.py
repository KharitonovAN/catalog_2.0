from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.views.decorators.cache import never_cache, cache_page
from .views import (
    HomeView,
    ContactsView,
    CategoryListView,
    ProductDetailView,
    CreateProductView,
    ProductListView,
    EditProductView,
    ProductDeleteView,
    PersonalAreaView,
    ModeratorProductsView,
)


app_name = 'catalog'

urlpatterns = [

    path('', HomeView.as_view(), name='home'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('category/', CategoryListView.as_view(), name='category'),
    path('<int:pk>/products/', ProductListView.as_view(), name='product_list'),
    path('<int:pk>/product_detail/', cache_page(60)(ProductDetailView.as_view()), name='product_detail'),
    path('<int:pk>/edit_product/', never_cache(EditProductView.as_view()), name='edit_product'),
    path('<int:pk>/delete/', ProductDeleteView.as_view(), name='product_confirm_delete'),
    path('personal_area/', PersonalAreaView.as_view(), name='personal_area'),
    path('personal_area/all_products', ModeratorProductsView.as_view(), name='moderator_products_list'),
    path('personal_area/save_product/', never_cache(CreateProductView.as_view()), name='create_product'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
