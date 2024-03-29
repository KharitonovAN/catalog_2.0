from django.forms import inlineformset_factory
from django.urls import reverse, reverse_lazy
from catalog.forms import ProductForm, VersionForm, ModeratorProductForm
from catalog.models import Product, Version, Category
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from catalog.services import get_category_cache
from config import settings
from django.views.generic import (
    CreateView,
    UpdateView,
    ListView,
    TemplateView,
    DetailView,
    DeleteView
)


class HomeView(TemplateView):
    template_name = 'catalog/home.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        product_list = Product.objects.filter(is_published=True).order_by('?')[:2]

        if product_list:
            context_data['object_list'] = product_list
        else:
            context_data['object_list'] = []

        return context_data


class ContactsView(TemplateView):
    template_name = 'catalog/contacts.html'

    def get_context_data(self, **kwargs):
        if self.request.method == 'POST':
            name = self.request.POST. get('name')
            phone = self.request.POST.get('phone')
            email = self.request.POST.get('email')
            message = self.request.POST.get('message')
            print(f'Пришло сообщение:\nИмя: {name}\nТел.: {phone}\nEmail: {email}\nСообщение: {message}')
        return super().get_context_data(**kwargs)


class CategoryListView(ListView):
    model = Category

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        if settings.CASH_ALLOWED:
            context_data['category_list'] = get_category_cache()
        else:
            context_data['category_list'] = Category.objects.all()
        return context_data


class ProductListView(LoginRequiredMixin, ListView):
    model = Product

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(category_id=self.kwargs.get('pk'))
        queryset = queryset.filter(is_published=True)
        return queryset


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        data = context_data['object']
        active_version = data.prod_name.filter(is_active=True)
        if active_version:
            for item in active_version:
                data.version_number = item.version_number
                data.version_name = item.version_name
                context_data['version'] = f'{data.version_number} / {data.version_name}'
        else:
            context_data['version'] = ''
        return context_data


class CreateProductView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Product
    permission_required = 'catalog.add_product'
    permission_denied_message = 'Access is denied!'

    def get_success_url(self):
        return reverse('catalog:product_detail', args=[self.object.pk])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            self.object.creator = self.request.user
            self.object.save()

            formset.instance = self.object
            formset.save()
        return super().form_valid(form)

    def get_form_class(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return ModeratorProductForm
        return ProductForm


class EditProductView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    permission_required = 'catalog.change_product'
    permission_denied_message = 'Access is denied!'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse('catalog:product_detail', kwargs={'pk': pk})

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if self.object.user_create == self.request.user:
            self.object.user_create = self.request.user
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)

    def get_object(self, *args, **kwargs):
        product = super().get_object(*args, **kwargs)
        if product.user_create == self.request.user or self.request.user.is_superuser or self.request.user.is_staff:
            return product
        return reverse('catalog:products')

    def get_form_class(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return ModeratorProductForm
        return ProductForm


class PersonalAreaView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 'catalog/personal_area.html'
    permission_required = [
        'catalog.add_product',
        'catalog.change_product']
    permission_denied_message = 'Доступ запрещен.'


class ModeratorProductsView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Product
    permission_required = [
        'catalog.add_product',
        'catalog.change_product']
    permission_denied_message = 'Доступ запрещен.'

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_staff or self.request.user.is_superuser:
            return queryset.all()

        products = Product.objects.filter(user_create=self.request.user)
        queryset = products
        return queryset


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:home')
