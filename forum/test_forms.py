from django.test import TestCase
from .forms import PostForm, EditForm, CommentForm, CategoryForm


class TestPostForm(TestCase):

    def test_title_is_required(self):
        form = PostForm({'title': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors.keys())
        self.assertEqual(
            form.errors['title'][0], 'This field is required.'
            )

    def test_slug_is_required(self):
        form = PostForm({'slug': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('slug', form.errors.keys())
        self.assertEqual(
            form.errors['slug'][0], 'This field is required.'
            )

    def test_category_is_required(self):
        form = PostForm({'category': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('category', form.errors.keys())
        self.assertEqual(
            form.errors['category'][0], 'This field is required.'
            )

    def test_html_content_is_required(self):
        form = PostForm({'html_content': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('html_content', form.errors.keys())
        self.assertEqual(
            form.errors['html_content'][0], 'This field is required.'
            )

    def test_css_content_is_required(self):
        form = PostForm({'css_content': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('css_content', form.errors.keys())
        self.assertEqual(
            form.errors['css_content'][0], 'This field is required.'
            )

    def test_fields_are_explicit_in_form_metaclass(self):
        form = PostForm()
        self.assertEqual(
            form.Meta.fields, [
                'title', 'slug', 'category', 'html_content', 'css_content',
                'js_content'
                ]
        )


class TestEditForm(TestCase):

    def test_title_is_required(self):
        form = EditForm({'title': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors.keys())
        self.assertEqual(
            form.errors['title'][0], 'This field is required.'
            )

    def test_slug_is_required(self):
        form = EditForm({'slug': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('slug', form.errors.keys())
        self.assertEqual(
            form.errors['slug'][0], 'This field is required.'
            )

    def test_category_is_required(self):
        form = EditForm({'category': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('category', form.errors.keys())
        self.assertEqual(
            form.errors['category'][0], 'This field is required.'
            )

    def test_html_content_is_required(self):
        form = EditForm({'html_content': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('html_content', form.errors.keys())
        self.assertEqual(
            form.errors['html_content'][0], 'This field is required.'
            )

    def test_css_content_is_required(self):
        form = EditForm({'css_content': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('css_content', form.errors.keys())
        self.assertEqual(
            form.errors['css_content'][0], 'This field is required.'
            )

    def test_fields_are_explicit_in_form_metaclass(self):
        form = EditForm()
        self.assertEqual(
            form.Meta.fields, [
                'title', 'slug', 'category', 'html_content', 'css_content',
                'js_content'
                ]
        )


class TestCommentForm(TestCase):

    def test_body_is_required(self):
        form = CommentForm({'body': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('body', form.errors.keys())
        self.assertEqual(
            form.errors['body'][0], 'This field is required.'
            )

    def test_fields_are_explicit_in_form_metaclass(self):
        form = CommentForm()
        self.assertEqual(
            form.Meta.fields, ['body']
        )


class TestCategoryForm(TestCase):

    def test_name_is_required(self):
        form = CategoryForm({'name': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors.keys())
        self.assertEqual(
            form.errors['name'][0], 'This field is required.'
            )

    def test_fields_are_explicit_in_form_metaclass(self):
        form = CategoryForm()
        self.assertEqual(
            form.Meta.fields, ['name']
        )
