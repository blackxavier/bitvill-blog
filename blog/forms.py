from django import forms


class PostSendMailForm(forms.Form):
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)
