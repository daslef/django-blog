from django import forms

from blog.models import Comment


class EmailPostForm(forms.Form):
    username = forms.CharField(max_length=50)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form__comments"}),
        required=False,
    )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["body"]
