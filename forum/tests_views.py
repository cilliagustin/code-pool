from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from .models import Post, User, Category, Comment, Rating


class TestIndexView(TestCase):
    def test_index_response(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html', 'base.html')


class TestAllPostListView(TestCase):
    def test_all_post_list_response(self):
        response = self.client.get('/posts')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts.html', 'base.html')


class TestPostDetail(TestCase):
    def test_post_detail_response(self):
        category = Category.objects.create(
            name='test'
            )
        user = User.objects.create(
            username='testuser'
            )
        post = Post.objects.create(
            title='test',
            slug='test',
            author=user,
            category=category
            )
        response = self.client.get(f'/posts/{post.slug}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'post_detail.html', 'base.html')


class TestDeleteComment(TestCase):
    def test_delete_comment_response(self):
        category = Category.objects.create(
            name='test'
            )
        user = User.objects.create(
            username='testuser'
            )
        post = Post.objects.create(
            title='test',
            slug='test',
            author=user,
            category=category
            )
        comment = Comment.objects.create(author=user, body='test', post=post)
        response = self.client.get(f'/category/delete_comment/{comment.id}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'delete_comment.html', 'base.html')


class TestApproveComment(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
            )
        self.category = Category.objects.create(name='test')
        self.post = Post.objects.create(
            title='test',
            slug='test',
            author=self.user,
            category=self.category
            )
        self.comment = Comment.objects.create(
            author=self.user,
            body='test',
            post=self.post
            )


class TestApproveComment(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name="Test Category")
        self.post = Post.objects.create(
            title="Test",
            slug="test",
            author=User.objects.create_user(
                "testuser",
                "testuser@example.com",
                "testpassword"
                ),
            category=self.category,
        )
        self.comment = Comment.objects.create(
            body="Test",
            post=self.post,
            author=User.objects.create_user(
                "testcommentuser",
                "testcommentuser@example.com",
                "testpassword"
                ),
        )
        self.superuser = User.objects.create_superuser(
            "testsuperuser",
            "testsuperuser@example.com",
            "testpassword"
            )
        self.approve_comment_url = reverse(
            'approve_comment',
            args=[self.comment.pk])

    def test_get_approve_comment(self):
        self.client.force_login(self.superuser)
        response = self.client.post(
            '/approve_comment/{}/'.format(self.comment.id)
            )
        self.assertEqual(response.status_code, 302)
        self.comment.refresh_from_db()
        self.assertTrue(self.comment.approved)

    def test_post_approve_comment(self):
        self.client.login(username="testsuperuser", password="testpassword")
        response = self.client.post(self.approve_comment_url)
        self.assertEqual(response.status_code, 302)
        self.comment.refresh_from_db()
        self.assertTrue(self.comment.approved)

    def test_post_approve_comment_not_superuser(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(self.approve_comment_url)
        self.assertEqual(response.status_code, 403)


class TestRatingView(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name="Test Category")
        self.user = User.objects.create_user(
            "testuser",
            "testuser@example.com",
            "testpassword"
        )
        self.post = Post.objects.create(
            title="Test",
            slug="test",
            author=self.user,
            category=self.category,
        )
        self.rating = Rating.objects.create(
            post=self.post,
            user=self.user,
            value=1,
        )
        self.client.login(username='testuser', password='testpassword')

    def test_rate_post(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse(
            'post_rating',
            kwargs={'slug': self.post.slug}
            ), {'value': 4})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Rating.objects.filter(
            user=self.user, post=self.post, value=4
            ).exists())


class TestPostBookmark(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name="Test Category")
        self.user = User.objects.create_user(
            "testuser",
            "testuser@example.com",
            "testpassword"
        )
        self.post = Post.objects.create(
            title="Test",
            slug="test",
            author=self.user,
            category=self.category,
            html_content="Test content"
        )

    def test_bookmark(self):
        self.client.force_login(self.user)

        # Test bookmarking the post
        response = self.client.post(
            reverse('post_bookmark', args=[self.post.slug])
            )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.post.bookmark.count(), 1)
        self.assertIn(self.user, self.post.bookmark.all())

        # Test un-bookmarking the post
        response = self.client.post(
            reverse('post_bookmark', args=[self.post.slug])
            )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.post.bookmark.count(), 0)
        self.assertNotIn(self.user, self.post.bookmark.all())


class TestFilterCategoryView(TestCase):
    def test_filter_category_response(self):
        category = Category.objects.create(
            name='test'
            )
        response = self.client.get(f'/posts/filter/category/{category.name}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'categories.html', 'base.html')


class TestFilterBookmarkView(TestCase):
    def test_filter_bookmark_response(self):
        response = self.client.get('/posts/filter/bookmarked')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookmarked.html', 'base.html')


class TestCreatePostView(TestCase):
    def test_create_post_response(self):
        response = self.client.get('/new_post/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_post.html', 'base.html')


class TestEditPostView(TestCase):
    def test_edit_post_response(self):
        category = Category.objects.create(
            name='test'
            )
        user = User.objects.create(
            username='testuser'
            )
        post = Post.objects.create(
            title='test',
            slug='test',
            author=user,
            category=category
            )
        response = self.client.get(f'/posts/edit_post/{post.slug}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_post.html', 'base.html')


class TestDeletePostView(TestCase):
    def test_delete_post_response(self):
        category = Category.objects.create(
            name='test'
            )
        user = User.objects.create(
            username='testuser'
            )
        post = Post.objects.create(
            title='test',
            slug='test',
            author=user,
            category=category
            )
        response = self.client.get(f'/posts/delete_post/{post.slug}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'delete_post.html', 'base.html')


class TestEditCategoryView(TestCase):
    def test_edit_category_response(self):
        category = Category.objects.create(
            name='test'
            )
        response = self.client.get(f'/category/edit_category/{category.id}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_category.html', 'base.html')


class TestCreateCategoryView(TestCase):
    def test_create_category_response(self):
        response = self.client.get('/new_category/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_category.html', 'base.html')


class TestCategoryListView(TestCase):
    def test_category_list_response(self):
        response = self.client.get('/category_list/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'category_list.html', 'base.html')


class TestDeleteCategoryView(TestCase):
    def test_delete_category_response(self):
        category = Category.objects.create(
            name='test'
            )
        response = self.client.get(f'/category/delete_category/{category.id}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'delete_category.html', 'base.html')


class TestCanvasView(TestCase):
    def test_canvas_view_response(self):
        client = Client()
        response = client.get('/canvas/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['X-Frame-Options'], 'ALLOWALL')
        self.assertEqual(
            response['Access-Control-Allow-Origin'],
            'https://code-pool-agustin-cilli.herokuapp.com'
            )
