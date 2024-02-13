from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from pytils.translit import slugify
from .forms import BlogPostForm
from .models import BlogPost


class BlogPostListView(ListView):
    model = BlogPost
    template_name = 'blogpost/blogpost_list.html'
    context_object_name = 'object_list'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset


class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'blogpost/blogpost_detail.html'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views += 1
        self.object.save()
        return self.object


class BlogPostCreateView(CreateView):
    model = BlogPost
    form_class = BlogPostForm
    success_url = reverse_lazy('blogpost:blogpost_list')

    def form_valid(self, form):
        if form.is_valid():
            new_blogpost = form.save()
            new_blogpost.slug = slugify(new_blogpost.title)
            new_blogpost.save()
        return super().form_valid(form)


class BlogPostUpdateView(UpdateView):
    model = BlogPost
    form_class = BlogPostForm
    success_url = reverse_lazy('blogpost:blogpost_list')

    def form_valid(self, form):
        if form.is_valid():
            new_blogpost = form.save()
            new_blogpost.slug = slugify(new_blogpost.title)
            new_blogpost.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blogpost:blogpost_detail', args=[self.kwargs.get('pk')])


class BlogPostDeleteView(DeleteView):
    model = BlogPost
    success_url = reverse_lazy('blogpost:blogpost_list')
