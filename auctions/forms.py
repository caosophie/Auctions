from django import forms
from .models import User, ActiveListing, ArticleType

class CreateForm(forms.Form):
    title = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'Enter Title'}))
    bid = forms.DecimalField(label='', widget=forms.TextInput(attrs={'placeholder':'Enter Bid'}))
    description=forms.CharField(label='', widget=forms.Textarea(
        attrs={'style': 'height: 125px;width:300px', 'placeholder':'Enter Description'}
        )
    )
    image_url=forms.URLField(label='', widget=forms.URLInput(attrs={'placeholder' : 'Enter Image URL'}))

class CommentForm(forms.Form):
    comm = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Enter your comment'}))

class BidForm(forms.Form):
    bid = forms.DecimalField(label='', widget=forms.TextInput(attrs={'placeholder':'Enter Bid'}))