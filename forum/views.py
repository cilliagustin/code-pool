from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views import generic, View
from django.http import (
    HttpResponseRedirect, HttpResponse, HttpResponseForbidden
    )
from django.urls import reverse_lazy
from django.db.models import Q, Case, When, Value
from .models import Post, Comment, Category, Rating
from .forms import CommentForm, PostForm, EditForm, CategoryForm


class IndexPostList(generic.ListView):
    """
    ListView that displays the six most recently created posts. It queries the
    Post model and orders the posts in descending order by created_on
    attribute. The view uses the index.html template to render the posts.
    """
    model = Post
    queryset = Post.objects.order_by('-created_on')[:6]
    template_name = 'index.html'


class AllPostList(generic.ListView):
    """
     ListView that displays all the posts, ordered in descending order by
     created_on attribute. It queries the Post model and uses the posts.html
     template to render the posts. It also includes pagination to limit the
     number of posts shown per page. Additionally, the context of the view
     includes all categories available for the posts.
    """
    model = Post
    queryset = Post.objects.order_by('-created_on')
    template_name = 'posts.html'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class PostDetail(View):
    """
    Displays a specific post and its comments. It queries the Post
    model to get the specific post instance based on the provided slug. It
    also queries the Comment model to get all comments for the post and orders
    them first by whether they are approved or not and then by their creation
    date. The context of the view includes the post, its comments, and various
    additional details such as the user's rating for the post, whether the post
    is bookmarked by the user, the comment form, and the average rating for 
    the post. The view also handles comment form submissions and the approval
    of comments.
    """
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
            comment_form.instance.author = request.user
            comment = comment_form.save(commit=False)
            comment.post = context["post"]
            comment.save()
            context["commented"] = True
        return render(request, "post_detail.html", context)


class DeleteComment(generic.DeleteView):
    """
    llows users to delete comments. It queries the Comment model to get the
    specific comment instance based on the provided primary key. If the user
    is authorized to delete the comment, it deletes the comment instance and
    redirects to the post_detail view for the post to which the comment
    belonged.
    """
    model = Comment
    template_name = 'delete_comment.html'

    def get_success_url(self):
        post_slug = Comment.objects.get(pk=self.kwargs.get('pk')).post.slug
        return reverse('post_detail', kwargs={'slug': post_slug})

    def get_queryset(self):
        return Comment.objects.filter(pk=self.kwargs.get('pk'))


class ApproveComment(View):
    """
    View that allows superusers to approve comments. It queries the Comment
    model to get the specific comment instance based on the provided primary
    key. If the user is a superuser, it approves the comment and redirects to
    the post_detail view for the post to which the comment belonged.
    """
    def post(self, request, pk):
        if not request.user.is_superuser:
            return HttpResponseForbidden()

        comment = get_object_or_404(Comment, pk=pk)
        comment.approved = True
        comment.save()
        return redirect('post_detail', slug=comment.post.slug)


class RatingView(View):
    """
    View that handles the rating of posts. It queries the Post model to get
    the specific post instance based on the provided slug, gets the user who
    is rating the post, and the rating value from the request. It then updates
    or creates a new Rating instance based on the post, user, and value.
    Afterward, it redirects to the post_detail view for the post that was
    rated.
    """
    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, slug=kwargs['slug'])
        user = request.user
        value = request.POST.get("value")
        rating, created = Rating.objects.update_or_create(
            user=user, post=post, defaults={'value': value}
            )
        return redirect("post_detail", slug=kwargs['slug'])


class PostBookmark(View):
    """
    View that handles bookmarking of posts. It queries the Post model to get
    the specific post instance based on the provided slug. If the user has
    already bookmarked the post, it removes the bookmark, and if the user
    hasn't bookmarked the post, it adds the bookmark. Afterward, it redirects
    to the post_detail view for the post.
    """
    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        if post.bookmark.filter(id=self.request.user.id).exists():
            post.bookmark.remove(request.user)
        else:
            post.bookmark.add(request.user)
        return HttpResponseRedirect(reverse('post_detail', args=[slug]))


class FilterCategory(generic.ListView):
    """
    ListView that displays all the posts that belong to a specific category.
    It queries the Post model to get all posts that belong to the category,
    orders them in descending order by created_on attribute, and uses the
    categories.html template to render the posts. It also includes pagination
    and includes the category as part of the context.
    """
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
    """
    ListView that displays all the posts that the user has bookmarked.
    It queries the Post model to get all posts that the user has bookmarked,
    orders them in descending order by created_on attribute, and uses the
    bookmarked.html template to render the posts. It also includes pagination.
    """
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
    """
    CreateView that allows users to create new posts. It uses the PostForm
    form and the add_post.html template to render the form. After the form
    is submitted and validated, it creates a new Post instance based on the
    form data and the authenticated user, and saves the instance to the
    database.
    """
    model = Post
    form_class = PostForm
    template_name = 'add_post.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)


class EditPost(generic.UpdateView):
    """
    Uses UpdateView to display a form to edit an existing Post object. It uses
    the EditForm form class and the edit_post.html template. Once the form is
    submitted, the view updates the Post object in the database and redirects
    to the detail view for that Post.
    """
    model = Post
    form_class = EditForm
    template_name = 'edit_post.html'


class DeletePost(generic.DeleteView):
    """
    Using DeleteView to display a confirmation page for deleting an existing
    Post object. It uses the delete_post.html template. Once the user confirms
    the deletion, the view deletes the Post object from the database and
    redirects to the home view.
    """
    model = Post
    template_name = 'delete_post.html'
    success_url = reverse_lazy('home')


class EditCategory(generic.UpdateView):
    """
    Using UpdateView to display a form to edit an existing Category object. It
    uses the CategoryForm form class and the edit_category.html template. Once
    the form is submitted, the view updates the Category object in the database
    and redirects to the detail view for that Category.
    """
    model = Category
    form_class = CategoryForm
    template_name = 'edit_category.html'


class CreateCategory(generic.CreateView):
    """
    Displays a form to create a new Category object. It uses the CategoryForm
    form class and the add_category.html template. Once the form is submitted,
    the view creates a new Category object in the database and redirects to
    the detail view for that Category.
    """
    model = Category
    form_class = CategoryForm
    template_name = 'add_category.html'


class CategoryList(generic.ListView):
    """
    Displays a list of Category objects. It uses the category_list.html
    template. It overrides the get_queryset method to filter the list to only
    include Category objects whose name field is not null and is not equal to
    the string 'miscellaneous'. It orders the remaining categories by name,
    with the category named 'miscellaneous' appearing last.
    """
    model = Category
    template_name = 'category_list.html'

    def get_queryset(self):
        return Category.objects.filter(
            Q(name__iexact='miscellaneous') | Q(name__isnull=False)
        ).order_by(
            Case(When(name__iexact='miscellaneous', then=Value(1)), default=Value(0)), 'name'  # noqa
        )


class DeleteCategory(generic.DeleteView):
    """
    Using DeleteView to display a confirmation page for deleting an existing
    Category object. It uses the delete_category.html template. Once the user
    confirms the deletion, the view deletes the Category object from the
    database and redirects to the category_list view.
    """
    model = Category
    template_name = 'delete_category.html'
    success_url = reverse_lazy('category_list')

    def get_queryset(self):
        return Category.objects.filter(pk=self.kwargs.get('pk'))


def canvas_view(request):
    """
    View that returns an HttpResponse object with headers to allow the view to
    be displayed in an iframe on another domain. It's used as a workaround for
    a browser security feature called Same-Origin Policy, which prevents web
    pages from accessing resources on other domains. This view sets the
    X-Frame-Options header to ALLOWALL and the Access-Control-Allow-Origin
    header to a specific domain, which allows the view to be displayed in an
    iframe on that domain.
    """
    response = HttpResponse()
    response['X-Frame-Options'] = 'ALLOWALL'
    response['Access-Control-Allow-Origin'] = 'https://code-pool-agustin-cilli.herokuapp.com'  # noqa
    return response
