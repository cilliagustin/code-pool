from .models import Comment, Post
from django import forms


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'slug', 'category', 'html_content', 'css_content','js_content')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'id': 'post-title'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'id': 'post-slug'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'html_content': forms.Textarea(attrs={'class': 'form-control HTML-code', 'placeholder': 'Paste here your HTML code.'}),
            'css_content': forms.Textarea(attrs={'class': 'form-control CSS-code', 'placeholder': 'Paste here your CSS code.'}),
            'js_content': forms.Textarea(attrs={'class': 'form-control JS-code', 'placeholder': 'Paste here your JS code. (Optional)'}),
        }
