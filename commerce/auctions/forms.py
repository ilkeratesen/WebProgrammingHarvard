from django.forms import ModelForm, Textarea
from auctions.models import Listings, Bids


class NewListingForm(ModelForm):
    class Meta:
        model = Listings
        fields = ['title', 'description', 'starting_bid','category', 'image']
        widgets = {
            'description': Textarea(attrs={'cols': 40, 'rows': 6})
        }
    def __init__(self, *args, **kwargs):
        super(NewListingForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs\
            .update({
                'class': 'form-control'
            })  
        self.fields['description'].widget.attrs\
            .update({
                'class': 'form-control'
            })  
        self.fields['starting_bid'].widget.attrs\
            .update({
                'class': 'form-control col-lg-6'
            })
        self.fields['category'].widget.attrs\
            .update({
                'class': 'form-control col-lg-6'
            }) 
        self.fields['image'].widget.attrs\
            .update({
                'class': 'form-control'
            })
          
class BidsForm(ModelForm):
    class Meta:
        model = Bids
        fields = ['offer']

    def __init__(self, *args, **kwargs):
        super(BidsForm, self).__init__(*args, **kwargs)
        self.fields['offer'].widget.attrs\
            .update({
                'name': 'Offer',
                'class': 'form-control'
            })    