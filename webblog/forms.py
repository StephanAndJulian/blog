__author__ = 'stephan'

from django import forms

class LoginForm(forms.Form):
    user_name = forms.CharField(max_length=30, label='Name')
    user_password = forms.CharField(label ='Password', widget=forms.PasswordInput(render_value=False))

class BlogpostCreationForm(forms.Form):
    post_title = forms.CharField(label='Titel', max_length=1000)
    post_content = forms.CharField(label='', max_length=10000, widget=forms.Textarea)
    post_tags = forms.CharField(label='Tags', max_length=500)

    def clean_post_content(self):
        post_content = self.cleaned_data['post_content']
        words = post_content.split()
        for word in words:
            if len(word) > 140:
                raise forms.ValidationError('No words with more than 140 characters.')
        return post_content
