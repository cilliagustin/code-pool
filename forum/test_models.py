from django.test import TestCase
from django.urls import reverse
from django.core.exceptions import ValidationError
from .models import Post, User, Category, Comment, Rating


class TestCategoryModel(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='Test Category'
            )

    def test_name_max_length(self):
        max_length = self.category._meta.get_field('name').max_length
        self.assertEqual(max_length, 255)

    def test_category_str_representation(self):
        self.assertEqual(str(self.category), 'Test Category')

    def test_get_absolute_url(self):
        url = reverse('category_list')
        self.assertEqual(self.category.get_absolute_url(), url)


class TestPostModel(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='Test Category',
        )
        self.user = User.objects.create_user(
            username='testuser',
        )
        self.post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            author=self.user,
            html_content='<p>This is a test post.</p>',
            css_content='body { color: red; }',
            js_content='',
            category=self.category,
        )

    def test_post_str_representation(self):
        expected_str = self.post.title
        self.assertEqual(str(self.post), expected_str)

    def test_post_has_absolute_url(self):
        expected_url = f'/posts/{self.post.slug}'
        self.assertEqual(self.post.get_absolute_url(), expected_url)

    def test_post_avg_rating(self):
        Rating.objects.create(user=self.user, post=self.post, value=4)
        Rating.objects.create(user=self.user, post=self.post, value=2)
        expected_avg = '3.00'
        self.assertEqual(self.post.avg_rating(), expected_avg)

    def test_post_user_rating(self):
        Rating.objects.create(user=self.user, post=self.post, value=4)
        expected_user_rating = 4
        self.assertEqual(
            self.post.user_rating(self.user), expected_user_rating
            )

    def test_post_num_ratings(self):
        Rating.objects.create(user=self.user, post=self.post, value=4)
        Rating.objects.create(user=self.user, post=self.post, value=2)
        expected_num_ratings = 2
        self.assertEqual(self.post.num_ratings(), expected_num_ratings)


class TestRatingModel(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='Test Category'
        )
        self.user = User.objects.create_user(
            username='testuser'
        )
        self.post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            author=self.user,
            html_content='<p>This is a test post.</p>',
            css_content='body { color: red; }',
            js_content='',
            category=self.category,
        )
        self.rating = Rating.objects.create(
            user=self.user,
            post=self.post, value=4)

    def test_rating_value_must_be_between_1_and_5(self):
        with self.assertRaises(ValidationError):
            rating = Rating(user=self.user, post=self.post, value=0)
            rating.full_clean()
            rating.save()
            
        with self.assertRaises(ValidationError):
            rating = Rating(user=self.user, post=self.post, value=6)
            rating.full_clean()
            rating.save()

    def test_rating_can_be_created_with_valid_input(self):
        Rating.objects.create(user=self.user, post=self.post, value=5)
        self.assertEqual(self.post.num_ratings(), 2)

    def test_rating_can_be_updated(self):
        self.rating.value = 3
        self.rating.save()
        self.assertEqual(self.post.avg_rating(), '3.00')


class TestCommentModel(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='Test Category'
            )
        self.user = User.objects.create_user(
            username='testuser'
            )
        self.post = Post.objects.create(
            title='Test Post',
            author=self.user,
            html_content='<p>This is a test post.</p>',
            category=self.category,
        )
        self.comment = Comment.objects.create(
            post=self.post,
            body='Test',
            author=self.user,)

    def test_comment_approved_defaults_to_false(self):
        self.assertFalse(self.comment.approved)

    def test_comment_str_representation(self):
        expected_str = (
            f'Comment {self.comment.body} by {self.comment.author.username}'
            )
        self.assertEqual(str(self.comment), expected_str)

    def test_comment_created_on_is_auto_generated(self):
        comment = Comment.objects.create(
            post=self.post,
            body='Test 2'
            )
        self.assertIsNotNone(comment.created_on)

    def test_comment_ordering_is_by_created_on_oldest_first(self):
        comment2 = Comment.objects.create(
            post=self.post,
            body='Test 2'
            )
        self.assertEqual(
            list(self.post.comments.all()),
            [self.comment, comment2])

    def test_comment_can_be_approved(self):
        self.comment.approved = True
        self.comment.save()
        self.assertTrue(self.comment.approved)
