from django import forms 
from .models import Comment

class EmailPostForm(forms.Form):
    name =  forms.CharField(max_length=25, widget=forms.TextInput(
                attrs={'placeholder': "Name of sender..."}))
    email = forms.EmailField(widget=forms.TextInput(
                attrs={'placeholder': "Sender email..."}))
    to = forms.EmailField(widget=forms.TextInput(
                attrs={'placeholder': "Recepient email..."}))
    comments = forms.CharField(required=False, widget=forms.Textarea)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')