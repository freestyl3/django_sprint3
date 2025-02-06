from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from django.utils import timezone

from .models import Post, Category  # , Location


class PostListView(ListView):
    model = Post
    queryset = Post.objects.filter(
        is_published=True,
        category__is_published=True,
        pub_date__lt=timezone.now()
    ).select_related('category').select_related('location')
    ordering = 'id'
    template_name = 'blog/index.html'
    paginate_by = 5


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'blog/category.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_list'] = Post.objects.filter(
            category__id=self.object.id,
            is_published=True,
            pub_date__lt=timezone.now()
        )
        return context

    def get_object(self):
        return get_object_or_404(
            Category,
            slug=self.kwargs['slug'],
            is_published=True
        )


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'

    def get_object(self):
        return get_object_or_404(
            Post,
            pk=self.kwargs['pk'],
            is_published=True,
            category__is_published=True,
            pub_date__lt=timezone.now()
        )
