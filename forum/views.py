from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views import generic, View
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from .models import Post, Category, Rating
from .forms import CommentForm, PostForm, EditForm


class IndexPostList(generic.ListView):
    model = Post
    queryset = Post.objects.order_by('-created_on')
    template_name = 'index.html'


class AllPostList(generic.ListView):
    model = Post
    queryset = Post.objects.order_by('-created_on')
    template_name = 'posts.html'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class PostDetail(View):
    def get(self, request, slug, *args, **kwargs):
        queryset = Post.objects
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by('created_on')
        user_rating = None
        is_bookmarked = False
        if request.user.is_authenticated:
            user_rating = post.user_rating(request.user)
            is_bookmarked = post.bookmark.filter(id=request.user.id).exists()

        return render(
            request,
            "post_detail.html",
            {
                "user": request.user,
                "user_rating": user_rating,
                "post": post,
                "comments": comments,
                "is_bookmarked": is_bookmarked,
                "commented": False,
                "comment_form": CommentForm(),
                "avg_rating": post.avg_rating(),
            },
        )


class RatingView(View):
    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, slug=kwargs['slug'])
        user = request.user
        value = request.POST.get("value")
        rating, created = Rating.objects.update_or_create(
            user=user, post=post, defaults={'value': value}
            )
        return redirect("post_detail", slug=kwargs['slug'])


class PostBookmark(View):

    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        if post.bookmark.filter(id=self.request.user.id).exists():
            post.bookmark.remove(request.user)
        else:
            post.bookmark.add(request.user)
        return HttpResponseRedirect(reverse('post_detail', args=[slug]))


class FilterCategory(generic.ListView):
    model = Post
    template_name = 'categories.html'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['category'] = self.kwargs['category']
        return context

    def get_queryset(self):
        category = get_object_or_404(Category, name=self.kwargs['category'])
        return Post.objects.filter(category=category)


class FilterBookmark(generic.ListView):
    model = Post
    template_name = 'bookmarked.html'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(bookmark=user)


class CreatePost(generic.CreateView):
    model = Post
    form_class = PostForm
    template_name = 'add_post.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)


class EditPost(generic.UpdateView):
    model = Post
    form_class = EditForm
    template_name = 'edit_post.html'


class DeletePost(generic.DeleteView):
    model = Post
    template_name = 'delete_post.html'
    success_url = reverse_lazy('home')


class Canvas(generic.ListView):
    model = Post
    template_name = 'canvas.html'
