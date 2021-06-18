from django import forms 

class EmailPostForm(forms.Form):
    name =  forms.CharField(max_length=25, widget=forms.TextInput(
                attrs={'placeholder': "Name of sender..."}
    ))
    email = forms.EmailField(widget=forms.TextInput(
                attrs={'placeholder': "Sender email..."}
    ))
    to = forms.EmailField(widget=forms.TextInput(
                attrs={'placeholder': "Recepient email..."}
    ))
    comments = forms.CharField(required=False, widget=forms.Textarea)