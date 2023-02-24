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
    def setUp(self):
        self.category = Category.objects.create(name='test')
        self.user = User.objects.create_user(
            username='testuser',
            password='12345'
            )
        self.post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            author=self.user,
            category=self.category
            )
        self.comment1 = Comment.objects.create(
            author=self.user,
            post=self.post,
            body='Test comment 1',
            approved=True
            )
        self.comment2 = Comment.objects.create(
            author=self.user,
            post=self.post,
            body='Test comment 2',
            approved=True
            )

    def test_post_detail_response(self):
        response = self.client.get(
            reverse('post_detail', args=[self.post.slug])
            )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'post_detail.html', 'base.html')

    def test_comments_displayed_on_post_detail_page(self):
        response = self.client.get(f'/posts/{self.post.slug}')
        self.assertEqual(
            list(response.context['comments']), [self.comment1, self.comment2]
            )

    def test_invalid_comment_form_submission(self):
        data = {'body': ''}
        response = self.client.post(f'/posts/{self.post.slug}', data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['commented'])
        self.assertEqual(Comment.objects.count(), 2)

    def test_create_comment(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse(
            'post_detail', args=[self.post.slug]
            ), {
            'body': 'Test Comment',
            'approved': True
        })
        self.assertEqual(self.post.comments.count(), 3)


class TestDeleteComment(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='test')
        self.author = User.objects.create_user(
            username='testuser',
            password='12345'
            )
        self.post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            author=self.author,
            category=self.category
            )
        self.comment_author = User.objects.create_user(
            username='commentauthor',
            password='12345'
            )
        self.comment = Comment.objects.create(
            author=self.comment_author,
            body='Test comment',
            post=self.post
            )

    def test_delete_comment_response(self):
        self.client.force_login(self.author)
        response = self.client.get(reverse(
            'delete_comment', args=[self.post.slug, self.comment.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'delete_comment.html', 'base.html')

    def test_delete_comment_by_user(self):
        user = User.objects.create_user(
            username='testuser2',
            password='12345'
            )
        self.client.force_login(user)
        response = self.client.post(reverse(
            'delete_comment', args=[self.post.slug, self.comment.pk]
            ))
        self.assertRedirects(response, reverse(
            'post_detail', args=[self.post.slug]
            ))
        self.assertEqual(Comment.objects.count(), 0)


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
        self.client.login(
            username='testuser',
            password='password')
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
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='secret'
        )
        self.category = Category.objects.create(name='Test Category')

    def test_create_post_response(self):
        response = self.client.get(reverse('add_post'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_post.html', 'base.html')

    def test_create_post(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('add_post'), {
            'title': 'Test Post',
            'slug': 'test-post',
            'html_content': '<p>Test content</p>',
            'css_content': 'body { color: red; }',
            'category': self.category.pk,
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Post.objects.filter(title='Test Post').exists())


class TestEditPostView(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='test')
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
            )
        self.post = Post.objects.create(
            title='test',
            slug='test',
            html_content='<p>Old test content</p>',
            author=self.user,
            category=self.category
        )
        self.client = Client()
        self.client.login(
            username='testuser',
            password='testpassword')

    def test_edit_post_response(self):
        response = self.client.get(reverse('edit_post', args=[self.post.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_post.html', 'base.html')

    def test_edit_post(self):
        response = self.client.post(reverse(
            'edit_post', args=[self.post.slug]
            ), {
            'title': 'New Test Post',
            'slug': 'new-test-post',
            'html_content': '<p>New test content</p>',
            'css_content': 'body { color: blue; }',
            'category': self.category.pk,
        })
        self.assertEqual(response.status_code, 302)
        post = Post.objects.get(slug='new-test-post')
        self.assertEqual(post.title, 'New Test Post')
        self.assertEqual(post.html_content, '<p>New test content</p>')


class TestDeletePostView(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='test')
        self.user = User.objects.create_user(
            username='testuser',
            password='password'
            )
        self.post = Post.objects.create(
            title='test',
            slug='test',
            author=self.user,
            category=self.category
        )

    def test_delete_post_response(self):
        response = self.client.get(reverse(
            'delete_post',
            args=[self.post.slug]
            ))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'delete_post.html', 'base.html')

    def test_delete_post(self):
        self.client.login(
            username='testuser',
            password='password'
            )
        response = self.client.post(reverse(
            'delete_post',
            args=[self.post.slug]
            ))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Post.objects.filter(slug='test').exists())
        self.assertRedirects(response, reverse('home'))


class TestEditCategoryView(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='test')
        self.user = User.objects.create_user(
            username='testuser',
            password='password'
            )

    def test_edit_category_response(self):
        response = self.client.get(
            f'/category/edit_category/{self.category.id}'
            )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_category.html', 'base.html')

    def test_edit_category(self):
        self.client.login(username='testuser', password='password')
        updated_name = 'updated test'
        response = self.client.post(reverse(
            'edit_category',
            args=[self.category.id]), {
            'name': updated_name,
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/category_list/')
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, updated_name)


class TestCreateCategoryView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='password'
            )

    def test_create_category_response(self):
        response = self.client.get('/new_category/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_category.html', 'base.html')

    def test_create_category(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('add_category'), {
            'name': 'Test Category',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Category.objects.filter(name='Test Category').exists())


class TestCategoryListView(TestCase):
    def test_category_list_response(self):
        response = self.client.get('/category_list/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'category_list.html', 'base.html')


class TestDeleteCategoryView(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='test')
        self.user = User.objects.create_user(
            username='testuser',
            password='password'
            )

    def test_delete_category_response(self):
        response = self.client.get(
            f'/category/delete_category/{self.category.id}'
            )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'delete_category.html', 'base.html')

    def test_delete_category(self):
        self.client.login(
            username='testuser',
            password='password'
            )
        response = self.client.post(reverse(
            'delete_category',
            args=[self.category.id]
            ))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Category.objects.filter(name='test').exists())
        self.assertRedirects(response, reverse('category_list'))


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
