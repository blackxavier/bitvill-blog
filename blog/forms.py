from django import forms
from blog.models import Comment


class PostSendMailForm(forms.Form):
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("email", "body")
    def save(self,post,*args, **kwargs):
        
        super(CommentForm, self).save(*args, **kwargs)
        self.post = post
        return self.instance
        
