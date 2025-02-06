from datetime import datetime

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from .models import Post, Category  # , Location

posts = [
    {}, {}, {}
]


class PostListView(ListView):
    model = Post
    queryset = Post.objects.filter(
        is_published=True,
        category__is_published=True,
        pub_date__lt=datetime.now()
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
            pub_date__lt=datetime.now()
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
            pub_date__lt=datetime.now()
        )


# def index(request):
#     context = {
#         'posts': reversed(posts)
#     }
#     return render(request, "blog/index.html", context)


def post_detail(request, post_id: int):
    context = {
        'post': post for post in posts if post_id == post['id']
    }
    return render(request, "blog/detail.html", context)


# def category_posts(request, category_slug):
#     # context = {
#     #     'category': [post for post in posts if post['category'] ==
#     #  category_slug]
#     # }
#     context = {
#         'category_slug': category_slug
#     }
#     return render(request, "blog/category.html", context)
# Create your views here.
