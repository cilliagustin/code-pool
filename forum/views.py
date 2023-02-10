from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views import generic, View
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.db.models import Q, Case, When, Value
from .models import Post, Comment, Category, Rating
from .forms import CommentForm, PostForm, EditForm, CategoryForm


class IndexPostList(generic.ListView):
    model = Post
    queryset = Post.objects.order_by('-created_on')[:6]
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
    def get_context(self, request, slug):
        queryset = Post.objects
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.order_by('approved', 'created_on')
        user_rating = None
        is_bookmarked = False
        if request.user.is_authenticated:
            user_rating = post.user_rating(request.user)
            is_bookmarked = post.bookmark.filter(id=request.user.id).exists()
        if not request.user.is_superuser:
            comments = comments.filter(approved=True)
        context = {
            "user": request.user,
            "user_rating": user_rating,
            "post": post,
            "comments": comments,
            "is_bookmarked": is_bookmarked,
            "commented": False,
            "comment_form": CommentForm(),
            "avg_rating": post.avg_rating()
        }
        return context

    def get(self, request, slug, *args, **kwargs):
        context = self.get_context(request, slug)
        return render(request, "post_detail.html", context)

    def post(self, request, slug, *args, **kwargs):
        context = self.get_context(request, slug)
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.post = context["post"]
            comment.save()
            context["commented"] = True
        return render(request, "post_detail.html", context)


class DeleteComment(generic.DeleteView):
    model = Comment
    template_name = 'delete_comment.html'

    def get_success_url(self):
        post_slug = Comment.objects.get(pk=self.kwargs.get('pk')).post.slug
        return reverse('post_detail', kwargs={'slug': post_slug})

    def get_queryset(self):
        return Comment.objects.filter(pk=self.kwargs.get('pk'))


class ApproveComment(View):

    def post(self, request, pk):
        if not request.user.is_superuser:
            return HttpResponseForbidden()

        comment = get_object_or_404(Comment, pk=pk)
        comment.approved = True
        comment.save()
        return redirect('post_detail', slug=comment.post.slug)


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
        if self.request.user.is_authenticated:
            return Post.objects.filter(bookmark=self.request.user)
        else:
            return Post.objects.none()


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


class EditCategory(generic.UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'edit_category.html'


class CreateCategory(generic.CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'add_category.html'


class CategoryList(generic.ListView):
    model = Category
    template_name = 'category_list.html'

    def get_queryset(self):
        return Category.objects.filter(
            Q(name__iexact='miscellaneous') | Q(name__isnull=False)
        ).order_by(
            Case(When(name__iexact='miscellaneous', then=Value(1)), default=Value(0)), 'name'  # noqa
        )


class DeleteCategory(generic.DeleteView):
    model = Category
    template_name = 'delete_category.html'
    success_url = reverse_lazy('category_list')

    def get_queryset(self):
        return Category.objects.filter(pk=self.kwargs.get('pk'))


def canvas_view(request):
    response = HttpResponse()
    response['X-Frame-Options'] = 'ALLOWALL'
    response['Access-Control-Allow-Origin'] = 'https://code-pool-agustin-cilli.herokuapp.com'  # noqa
    return response
